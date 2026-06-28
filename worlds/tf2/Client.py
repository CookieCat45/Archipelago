import asyncio
from enum import IntEnum
import Utils
import os
from typing import Dict, Any
from .Rcon import RCONClient, BadRCONPassword
import socket
from random import randint
from copy import deepcopy
from NetUtils import JSONtoTextParser, JSONMessagePart, ClientStatus
from .Data import (class_uses_weapon, TFClass, TFKillInfo, get_kill_info, stock_melee,
                   allclass_melee_internal, weapon_to_class, get_multiclass_weapon_classes)
from .Items import get_item_id
from .Regions import get_location_id
from CommonClient import CommonContext, gui_enabled, ClientCommandProcessor, logger, get_base_parser
from kvui import GameManager
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

DEBUG = False

class TF2GameMode(IntEnum):
    UNKNOWN = 0,
    CASUAL = 1,
    MVM = 2

class TF2UIMode(IntEnum):
    UNKNOWN = 0,
    VIEWING_CLASS = 1,
    MVM_GRID = 2,
    MVM_BUNDLE = 3,

class TF2JSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text

class TF2Cmd:
    def __init__(self, cmd, args="", is_confilter=False):
        self.cmd = cmd
        self.args = args
        self.is_confilter = is_confilter

class TF2CommandProcessor(ClientCommandProcessor):
    def _cmd_tf2_connect(self, password: str):
        """Connect to TF2 RCON"""
        if isinstance(self.ctx, TF2Context):
            if self.ctx.game_folder_path == "":
                self.ctx.find_tf2_folder()

            if self.ctx.rcon is not None and self.ctx.rcon_password != "":
                logger.info("You're already connected!")
                return

            self.ctx.rcon_password = password

    def _cmd_tf2_contracthints(self):
        """Show any obtained contract hints"""
        if isinstance(self.ctx, TF2Context):
            if len(self.ctx.contract_hints) <= 0:
                logger.info("You have no contract hints.")
                return

            showed_hint = False
            for hint in self.ctx.contract_hints:
                if self.ctx.is_mvm:
                    bundle_name = self.ctx.get_bot_bundle_name(hint)
                    if bundle_name != "UNKNOWN" and not self.ctx.has_item(bundle_name):
                        hint += f" ({bundle_name})"
                        logger.info(hint)
                        showed_hint = True
                        continue

                if self.ctx.is_casual and hint not in self.ctx.mvm_kill_reqs.keys() and not self.ctx.has_item(hint):
                    logger.info(hint)
                    showed_hint = True

            if not showed_hint:
                logger.info("You don't have any contract hints (for unobtained contracts).")

    def _cmd_deathlink(self):
        """Toggle DeathLink"""
        if isinstance(self.ctx, TF2Context):
            Utils.async_start(self.ctx.update_death_link(False if "DeathLink" in self.ctx.tags else True))

    if DEBUG:
        def _cmd_tf2_sendcmd(self, text: str):
            if isinstance(self.ctx, TF2Context):
                if self.ctx.rcon is not None:
                    self.ctx.rcon.command(text)


class TF2Context(CommonContext):
    game = "Team Fortress 2"
    command_processor = TF2CommandProcessor

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gamejsontotext = TF2JSONToTextParser(self)
        self.autoreconnect_task = None
        self.endpoint = None
        self.rcon = None
        self.rcon_task = None
        self.steam_name = ""
        self.items_handling = 0b111
        self.cmd_queue = []
        self.slot_data = None
        self.game_mode = TF2GameMode.UNKNOWN
        self.is_casual = False
        self.is_mvm = False
        self.ui_mode = TF2UIMode.UNKNOWN
        self.death_count = 0
        self.death_req = 3
        self.taunt_trap_duration = 0
        self.melee_only_duration = 0
        self.weapon_kill_reqs = {}
        self.class_kill_reqs = {}
        self.weapon_kill_counts = {}
        self.class_kill_counts = {}
        self.mvm_kill_reqs = {}
        self.mvm_kill_counts = {}
        self.mvm_bundles = {}
        self.mvm_location_ids = {}
        self.mvm_boss_names = []
        self.mvm_boss_reward = 0
        self.contract_hints = []
        self.current_mvm_bundle = ""
        self.points = 0
        self.required_points = 0
        self.game_folder_path = ""
        self.condump_io = None
        self.rcon_password = ""
        self.current_class = TFClass.UNKNOWN
        self.class_check_time = 0
        self.mode_check_time = 0

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TF2Context, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    def on_deathlink(self, data: Dict[str, Any]) -> None:
        self.killbind()
        super().on_deathlink(data)

    def find_tf2_folder(self):
        saved_path = Utils.local_path('data', 'tf2_dir.txt')
        if os.path.isfile(saved_path):
            with open(saved_path) as file:
                self.game_folder_path = file.read()
                print(f"Found saved path: {self.game_folder_path}")

        if self.game_folder_path == "" or not os.path.isdir(self.game_folder_path):
            # try some common paths
            common_paths = [
                "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2",
                "D:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2",
                "/home/user/.steam/steam/steamapps/common/Team Fortress 2",
                "/home/deck/.steam/steam/steamapps/common/Team Fortress 2",
            ]

            for p in common_paths:
                if os.path.isdir(p):
                    self.game_folder_path = p
                    break

            while not self.game_folder_path.endswith("common/Team Fortress 2") or not os.path.isdir(self.game_folder_path):
                self.game_folder_path = Utils.open_directory("Where is your Team Fortress 2 game directory?")

            if not os.path.isfile(saved_path):
                with open(saved_path, mode='x') as file:
                    file.write(self.game_folder_path)
                    print(f"Saving path: {self.game_folder_path}")

    def is_connected(self) -> bool:
        return self.server and self.server.socket.open

    def get_condump_file(self) -> str:
        return self.game_folder_path + "/tf/ap_dump.txt"

    def has_item(self, item_name: str) -> bool:
        item_id = get_item_id(item_name)
        for i in self.items_received:
            if i.item == item_id:
                return True

        return False

    def on_console_line(self, line: str):
        # if DEBUG:
            # logger.info(f"Console output: {line}")

        start = line.find("map     : ")
        if start != -1:
            start += 10
        end = line.find(" at: ")
        if start != -1 and end != -1:
            map_name = line[start:end]
            old_mode = self.game_mode
            if map_name.find("mvm_") == 0:
                self.game_mode = TF2GameMode.MVM
            else:
                self.game_mode = TF2GameMode.CASUAL

            if self.game_mode != old_mode:
                if self.game_mode == TF2GameMode.MVM:
                    logger.info(f"Game Mode changed to: Mann vs. Machine")
                elif self.game_mode == TF2GameMode.CASUAL:
                    logger.info(f"Game Mode changed to: Casual")
                else:
                    logger.info(f"Game Mode changed to: Unknown")
        elif line.find("ap_say ") == 0:
            index = line.find("ap_say ")+7
            message: str = line[index:]
            message = message.strip("\n")
            Utils.async_start(self.send_msgs([{"cmd": "Say", "text": message}]))
        elif line.find("ap_classmissing") == 0:
            if self.current_class == TFClass.UNKNOWN:
                self.show_unknown_class_warning()
                return

            message = ""
            class_name = self.current_class.tostr()
            class_count = self.class_kill_counts.get(class_name, 0)
            class_req = self.class_kill_reqs.get(class_name, 0)
            if class_count < class_req:
                message += f"{class_name} Kills: {class_count}/{class_req}\necho "

            for weapon in self.weapon_kill_reqs.keys():
                if not self.has_item(weapon) or not class_uses_weapon(class_name, weapon):
                    continue

                count = self.weapon_kill_counts.get(weapon, 0)
                req = self.weapon_kill_reqs.get(weapon, 0)
                if count >= req:
                    continue

                message += f"{weapon}: {count}/{req}\necho "

            if message == "":
                self.echo(f"You have no pending objectives for the {class_name} class.")
            else:
                self.echo(message)

        elif line.find("not executing.") != -1 or line.find("execing") != -1:
            # Class change
            old_class = self.current_class
            if line.find("scout.cfg") != -1:
                self.current_class = TFClass.SCOUT
            elif line.find("soldier.cfg") != -1:
                self.current_class = TFClass.SOLDIER
            elif line.find("pyro.cfg") != -1:
                self.current_class = TFClass.PYRO
            elif line.find("demoman.cfg") != -1:
                self.current_class = TFClass.DEMOMAN
            elif line.find("heavyweapons.cfg") != -1 or line.find("heavy.cfg") != -1:
                self.current_class = TFClass.HEAVY
            elif line.find("engineer.cfg") != -1:
                self.current_class = TFClass.ENGINEER
            elif line.find("medic.cfg") != -1:
                self.current_class = TFClass.MEDIC
            elif line.find("sniper.cfg") != -1:
                self.current_class = TFClass.SNIPER
            elif line.find("spy.cfg") != -1:
                self.current_class = TFClass.SPY

            if self.current_class != TFClass.UNKNOWN and self.current_class != old_class:
                self.echo(f"Your class is: {self.current_class.tostr()}")
        elif line.find(self.steam_name) != -1 and line.find(self.steam_name) != 0:
            if not self.is_connected():
                return

            # death link
            if line.find("killed") != -1 and line.find("with") != -1:
                if "DeathLink" in self.tags:
                    info: TFKillInfo = get_kill_info(line)
                    if info.victim == self.steam_name:
                        self.death_count += 1
                        if self.death_count >= self.death_req:
                            self.death_count = 0
                            if info.weapon != "":
                                line = line.replace(info.weapon_internal, info.weapon)
                            Utils.async_start(self.send_death(line))
        elif ((line.find(self.steam_name) == 0 or self.game_mode == TF2GameMode.MVM)
         and self.game_mode != TF2GameMode.UNKNOWN):
            if not self.is_connected():
                return

            if line.find("killed") == -1 or line.find("with") == -1:
                return

            is_casual = bool(
                self.is_casual and self.game_mode == TF2GameMode.CASUAL and self.current_class != TFClass.UNKNOWN)
            sound_played_novice = False
            sound_played_expert = False
            info: TFKillInfo = get_kill_info(line)
            if self.is_mvm and self.game_mode == TF2GameMode.MVM:
                bot = info.victim
                # do a quick name fixup
                if bot == "Heavyweapons":
                    bot = "Heavy"
                elif bot == "Heavy Shotgun":
                    bot = "Shotgun Heavy"
                elif bot == "Extended Battalion Soldier":
                    bot = "Battalion Soldier"
                elif bot == "Extended Buff Soldier":
                    bot = "Buff Soldier"
                elif bot == "Extended Concheror Soldier":
                    bot = "Concheror Soldier"
                elif bot == "Fast Scorch Shot" or bot == "Pyro Pusher":
                    bot = "Flare Pyro"
                elif bot == "Minor League Scout" or bot == "Hyper League Scout":
                    bot = "Sandman Scout"
                elif bot == "Steel Gauntlet Pusher":
                    bot = "Steel Gauntlet"
                elif bot == "Razorback Sniper" or bot == "Sydney Sniper":
                    bot = "Sniper"
                elif bot == "Giant Rapid Fire Demoman":
                    bot = "Giant Demoman"

                req = self.mvm_kill_reqs.get(bot, 0)
                val = self.mvm_kill_counts.get(bot, 0)
                if req > 0 and val < req and self.has_bot_contract(bot):
                    location_ids = []
                    if bot not in self.mvm_boss_names:
                        location_ids.append(self.mvm_location_ids[f"{bot} Kill #{val+1}"])
                    else:
                        for i in range(self.mvm_boss_reward):
                            location_ids.append(self.mvm_location_ids[f"{bot} Reward #{i+1}"])

                    Utils.async_start(self.send_msgs([{"cmd": "LocationChecks", "locations": location_ids}]))
                    val += 1
                    self.mvm_kill_counts[bot] = val
                    key = format(f"MvmKillCount_{self.team}_{self.slot}_{bot}")
                    Utils.async_start(self.send_msgs([{"cmd": "Set", "key": key,
                                                       "operations": [
                                                           {"operation": "replace", "value": val}]}]))
                    if val >= req:
                        self.echo(f"COMPLETED CONTRACT: {bot} Kills ({val}/{req})")
                        self.play_gamesound("Quest.StatusTickExpert")
                        self.add_contract_points(1)
                    else:
                        self.play_gamesound("Quest.StatusTickNovice")

                    self.update_ui()

            elif is_casual:
                if line.find(self.steam_name) == 0:
                    class_name = self.current_class.tostr()
                    if not self.has_item(class_name):
                        # player does not have this class, don't send any checks
                        return

                    if class_name in self.class_kill_reqs.keys():
                        # Class general kill
                        val = self.class_kill_counts.get(class_name, 0)
                        req = self.class_kill_reqs.get(class_name, 0)
                        if val < req:
                            location_id = get_location_id(class_name) + val
                            Utils.async_start(self.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}]))
                            val += 1
                            self.class_kill_counts[class_name] = val
                            key = format(f"ClassCount_{self.team}_{self.slot}_{class_name}")
                            Utils.async_start(self.send_msgs([{"cmd": "Set", "key": key,
                                                               "operations": [
                                                                   {"operation": "replace", "value": val}]}]))

                            if val >= req:
                                self.echo(f"COMPLETED CONTRACT: Kills as {class_name} ({val}/{req})")
                                self.play_gamesound("Quest.StatusTickExpert")
                                self.add_contract_points(1)
                                sound_played_expert = True
                            else:
                                self.play_gamesound("Quest.StatusTickNovice")
                                sound_played_novice = True

                            self.update_ui()
                else:
                    for i in range(6):
                        self.show_unknown_class_warning()
                    return

                if info.weapon_internal == "bleed_kill":
                    if self.current_class == TFClass.ENGINEER:
                        info.weapon = "Southern Hospitality"
                        info.weapon_internal = "southern_hospitality"
                    elif self.current_class == TFClass.SNIPER:
                        info.weapon = "Tribalman's Shiv"
                        info.weapon_internal = "tribalkukri"
                    elif self.current_class == TFClass.SCOUT:
                        # Scout has two different weapons that cause bleeding, so just pick one
                        guillotine_kills = self.weapon_kill_counts.get("Flying Guillotine", 0)
                        guillotine_req = self.weapon_kill_reqs.get("Flying Guillotine", 0)
                        basher_kills = self.weapon_kill_counts.get("Boston Basher", 0)
                        basher_req = self.weapon_kill_reqs.get("Boston Basher", 0)
                        if self.has_item("Flying Guillotine") and guillotine_kills < guillotine_req:
                            info.weapon = "Flying Guillotine"
                            info.weapon_internal = "guillotine"
                        elif self.has_item("Boston Basher") and basher_kills < basher_req:
                            info.weapon = "Boston Basher"
                            info.weapon_internal = "boston_basher"
                elif info.weapon_internal in allclass_melee_internal:
                    # convert allclass melee to stock weapon name
                    info.weapon = stock_melee[int(self.current_class)-1]

                weapon = info.weapon
                if weapon in self.weapon_kill_reqs.keys() and self.has_item(weapon):
                    # Weapon kill
                    val = self.weapon_kill_counts.get(weapon, 0)
                    req = self.weapon_kill_reqs.get(weapon, 0)
                    if val < req:
                        location_id = get_location_id(weapon) + val
                        Utils.async_start(self.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}]))
                        val += 1
                        self.weapon_kill_counts[weapon] = val
                        key = format(f"WeaponCount_{self.team}_{self.slot}_{weapon}")
                        Utils.async_start(self.send_msgs([{"cmd": "Set", "key": key,
                                                           "operations":[{"operation": "replace", "value": val}]}]))

                        if val >= req:
                            self.echo(f"COMPLETED CONTRACT: Kills with {weapon} ({val}/{req})")
                            self.add_contract_points(1)
                            if not sound_played_expert:
                                self.play_gamesound("Quest.StatusTickExpert")
                        else:
                            if not sound_played_novice and not sound_played_expert:
                                self.play_gamesound("Quest.StatusTickNovice")

                        self.update_ui()

    def show_unknown_class_warning(self):
        if self.game_mode == TF2GameMode.MVM:
            return

        self.echo("!!! Your current player class is unknown by the Archipelago client. "
                  "If you are in-game, swap to a different class to fix this issue.!!!")

    def play_sound(self, sound: str):
        self.cmd_queue.append(TF2Cmd(cmd='play', args=sound))

    def play_gamesound(self, sound: str):
        self.cmd_queue.append(TF2Cmd(cmd='playgamesound', args=sound))

    def update_ui(self):
        if self.game_mode == TF2GameMode.MVM and self.is_mvm:
            self.ui.show_bundle(self.current_mvm_bundle)
        elif self.current_class != TFClass.UNKNOWN and self.is_casual:
            self.ui.show_weapon_grid(self.current_class.tostr())
        else:
            self.ui.update_tf2_tab()

    def add_contract_points(self, amount: int):
        if self.points >= self.required_points:
            return

        self.points += amount
        self.echo(f"Contract Points: {self.points}/{self.required_points}")
        Utils.async_start(self.send_msgs([{"cmd": "Set", "key": f"ContractPoints_{self.team}_{self.slot}",
                                           "operations": [{"operation": "replace", "value": self.points}]}]))

        if self.points >= self.required_points:
            Utils.async_start(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
            self.echo("********* CONGRATULATIONS! You're finished! ********")
            self.play_gamesound("Game.HappyBirthday")

    def cleanup(self):
        self.rcon_password = ""
        self.rcon = None
        self.current_class = TFClass.UNKNOWN
        self.game_mode = TF2GameMode.UNKNOWN

    def has_bot_contract(self, bot: str) -> bool:
        for key, val in self.mvm_bundles.items():
            if not self.has_item(key):
                continue

            for b in val:
                if bot == b:
                    return True

        return False

    def get_bot_bundle_name(self, bot: str) -> str:
        for key, val in self.mvm_bundles.items():
            for b in val:
                if bot == b:
                    return key

        return "UNKNOWN"

    def mvm_has_any_pending_objectives(self) -> bool:
        for key, val in self.mvm_bundles.items():
            if not self.has_item(key):
                continue

            for bot in val:
                count = self.mvm_kill_counts.get(bot, 0)
                req = self.mvm_kill_reqs[bot]
                if count < req:
                    return True

        return False

    def mvm_bundle_has_pending_objectives(self, bundle: str) -> bool:
        if not self.has_item(bundle):
            return False

        for bot in self.mvm_bundles[bundle]:
            count = self.mvm_kill_counts.get(bot, 0)
            req = self.mvm_kill_reqs[bot]
            if count < req:
                return True

        return False

    def class_has_pending_objectives(self, class_name: str) -> bool:
        class_kills = self.class_kill_counts.get(class_name, 0)
        class_count = self.class_kill_reqs.get(class_name)
        if class_kills < class_count:
            return True

        for weapon, count in self.weapon_kill_reqs.items():
            if class_uses_weapon(class_name, weapon) and self.has_item(weapon):
                weapon_kills = self.weapon_kill_counts.get(weapon, 0)
                if weapon_kills < count:
                    return True

        return False

    def on_print_json(self, args: dict):
        text = self.gamejsontotext(deepcopy(args["data"]))
        self.echo(text)

        if self.ui:
            self.ui.print_json(args["data"])
        else:
            text = self.jsontotextparser(args["data"])
            logger.info(text)

    def echo(self, text: str):
        for cmd in self.cmd_queue:
            if cmd.is_confilter:
                self.cmd_queue.remove(cmd)

        self.cmd_queue.append(TF2Cmd(f"con_filter_text \"\""))
        self.cmd_queue.append(TF2Cmd(f"wait 5; echo", f"\"[ARCHIPELAGO] {text}\""))
        self.cmd_queue.append(TF2Cmd(f"wait 6; con_filter_text brwetghrweuifwiuffew", is_confilter=True))

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.is_casual = self.slot_data["IsCasual"]
            self.is_mvm = self.slot_data["IsMvm"]
            if self.is_casual:
                self.weapon_kill_reqs = self.slot_data["WeaponKillCounts"]
                self.class_kill_reqs = self.slot_data["ClassKillCounts"]

            if self.is_mvm:
                self.mvm_bundles = self.slot_data["MvmBundles"]
                self.mvm_kill_reqs = self.slot_data["MvmKillCounts"]
                self.mvm_location_ids = self.slot_data["MvmLocationIds"]
                self.mvm_boss_names = self.slot_data["MvmBossNames"]
                self.mvm_boss_reward = self.slot_data["MvmContractBossReward"]

            self.required_points = self.slot_data["RequiredContractPoints"]
            self.death_req = self.slot_data["DeathLinkAmnesty"]
            if self.slot_data["DeathLink"] is True and "DeathLink" not in self.tags:
                Utils.async_start(self.update_death_link(True))

            get_list = []
            notify_list = []
            if self.is_casual:
                for key in self.class_kill_reqs.keys():
                    get_list.append(f"ClassCount_{self.team}_{self.slot}_{key}")
                    notify_list.append(f"ClassCount_{self.team}_{self.slot}_{key}")

                for key in self.weapon_kill_reqs.keys():
                    get_list.append(f"WeaponCount_{self.team}_{self.slot}_{key}")
                    notify_list.append(f"WeaponCount_{self.team}_{self.slot}_{key}")

            if self.is_mvm:
                for key in self.mvm_kill_reqs.keys():
                    get_list.append(f"MvmKillCount_{self.team}_{self.slot}_{key}")
                    notify_list.append(f"MvmKillCount_{self.team}_{self.slot}_{key}")

            get_list.append(f"ContractPoints_{self.team}_{self.slot}")
            notify_list.append(f"ContractPoints_{self.team}_{self.slot}")
            get_list.append(f"ContractHints_{self.team}_{self.slot}")
            if DEBUG:
                logger.info(f"Get: {get_list}")
                logger.info(f"SetNotify: {notify_list}")

            Utils.async_start(self.send_msgs([{"cmd": "Get","keys": get_list}]))
            Utils.async_start(self.send_msgs([{"cmd": "SetNotify","keys": notify_list}]))
            self.update_ui()
            logger.info("\n********************************************************************"
                        "\nTo connect to TF2 RCON: "
                        "\n\n1. In the in-game console, enter the command: exec archipelago/start"
                        "\n2. In-game, make sure that the rcon_password convar in the console is set to something"
                        "\n3. Enter /tf2_connect <password> in this client. The password should be whatever rcon_password is."
                        "\n\nIf connecting to the RCON fails, you may not be running the game with the -usercon launch option."
                        "\n\nOnce you are connected to TF2, the RCON connection may time out while on the loading screen. THIS IS NORMAL!"
                        "\nIt should reconnect automatically once you're finished loading in."
                        "\n********************************************************************\n")
        elif cmd == "ReceivedItems":
            start_index = args["index"]
            if start_index == 0:
                return

            progression = False
            new_class = False
            paranoia = False
            mvm_bundle = False
            if start_index <= len(self.items_received):
                for i in args['items']:
                    if i.item == 50: # Contract Hint
                        self.give_contract_hint()
                    elif i.item == 51: # Killbind Trap
                        self.killbind()
                    elif i.item == 52: # Disconnect Trap
                        self.cmd_queue.append(TF2Cmd(cmd='disconnect'))
                    elif i.item == 53: # Paranoia Trap
                        paranoia = True
                    elif i.item == 54: # snd_restart Trap
                        self.cmd_queue.append(TF2Cmd(cmd='snd_restart'))
                    elif i.item == 55: # Taunt Trap
                        self.taunt_trap_duration = 15
                    elif i.item == 56: # Melee Only Trap
                        self.melee_only_duration = 30
                    elif i.item <= 9:
                        new_class = True
                    elif i.item >= 950000:
                        mvm_bundle = True
                    else:
                        # assume progression, probably a weapon
                        progression = True

            if paranoia:
                self.cmd_queue.append(TF2Cmd("wait", "20"))
                self.play_gamesound("Player.Spy_UnCloak")
            elif new_class:
                self.cmd_queue.append(TF2Cmd("wait", "8"))
                self.play_sound("ui/duel_challenge_accepted.wav")
            elif mvm_bundle:
                self.cmd_queue.append(TF2Cmd("wait", "8"))
                self.play_gamesound("MVM.Warning")
            elif progression:
                self.cmd_queue.append(TF2Cmd("wait", "4"))
                self.play_gamesound("BaseCombatWeapon.WeaponMaterialize")

            self.update_ui()
        elif cmd == "Retrieved" or cmd == "SetReply":
            if cmd == "SetReply":
                key = args["key"]
                if "_read_client" in key or "_read_hints" in key:
                    return

                val = args["value"]
                old_val = args["original_value"]
                slot = args["slot"]
                if DEBUG:
                    logger.info(f"SetReply: {key} = {val} (old value: {old_val}, slot: {slot})")

                if val <= old_val or slot == self.slot:
                    return

                self.update_retrieved_data(key, val, True)
            else:
                for key, val in args["keys"].items():
                    if DEBUG:
                        logger.info(f"Retrieved: {key} = {val}")

                    self.update_retrieved_data(key, val)

            self.update_ui()

    def update_retrieved_data(self, key: str, val: Any, play_sound: bool=False):
        if val is None:
            return

        if key.startswith("WeaponCount_"):
            key = key.replace(f"WeaponCount_{self.team}_{self.slot}_", "")
            self.weapon_kill_counts[key] = val
            if play_sound:
                # someone in the same slot got a kill - play sounds to others
                req = self.weapon_kill_reqs.get(key, 0)
                if val >= req:
                    self.echo(f"COMPLETED CONTRACT: Kills with {key} ({val}/{req})")
                    self.play_gamesound("Quest.StatusTickExpert")
                else:
                    self.play_gamesound("Quest.StatusTickNovice")
        elif key.startswith("ClassCount_"):
            key = key.replace(f"ClassCount_{self.team}_{self.slot}_", "")
            self.class_kill_counts[key] = val
            if play_sound:
                # someone in the same slot got a kill - play sounds to others
                req = self.class_kill_reqs.get(key, 0)
                if val >= req:
                    self.echo(f"COMPLETED CONTRACT: Kills as {key} ({val}/{req})")
                    self.play_gamesound("Quest.StatusTickExpert")
                else:
                    self.play_gamesound("Quest.StatusTickNovice")
        elif key.startswith("MvmKillCount_"):
            key = key.replace(f"MvmKillCount_{self.team}_{self.slot}_", "")
            self.mvm_kill_counts[key] = val
            if play_sound:
                # someone in the same slot got a kill - play sounds to others
                req = self.mvm_kill_reqs.get(key, 0)
                if val >= req:
                    self.echo(f"COMPLETED CONTRACT: {key} Kills ({val}/{req})")
                    self.play_gamesound("Quest.StatusTickExpert")
                else:
                    self.play_gamesound("Quest.StatusTickNovice")
        elif key.startswith("ContractPoints") and val > self.points:
            self.points = val
        elif key.startswith("ContractHints"):
            self.contract_hints = val

    def give_contract_hint(self):
        possible_hints = []
        if self.is_casual:
            for weapon in self.weapon_kill_reqs.keys():
                if weapon in self.contract_hints or self.has_item(weapon):
                    continue

                possible_hints.append(weapon)

        if self.is_mvm:
            for bot in self.mvm_kill_reqs.keys():
                if bot in self.contract_hints or self.has_bot_contract(bot):
                    continue

                possible_hints.append(bot)

        if len(possible_hints) <= 0:
            return

        hint = possible_hints[randint(0, len(possible_hints)-1)]
        self.contract_hints.append(hint)
        Utils.async_start(self.send_msgs([{"cmd": "Set", "key": f"ContractHints_{self.team}_{self.slot}", "default": [],
                                           "operations": [{"operation": "add", "value": [hint]}]}]))

        bundle_name = self.get_bot_bundle_name(hint)
        if bundle_name != "UNKNOWN":
            hint += f" ({bundle_name})"

        logger.info(f"Contract revealed: {hint}")
        self.echo(f"Contract revealed: {hint}")

    def killbind(self):
        cmd: str
        if randint(1, 2) == 1:
            cmd = "kill"
        else:
            cmd = "explode"
        self.cmd_queue.append(TF2Cmd(cmd=cmd))

    def run_gui(self):
        self.ui = TF2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def rcon_loop(ctx: TF2Context):
    while not ctx.exit_event.is_set():
        if ctx.rcon_password != "":
            try:
                with RCONClient(socket.gethostbyname(socket.gethostname()), 27015, password=ctx.rcon_password) as ctx.rcon:
                    logger.info("Connected to TF2 RCON!")
                    # clean up the old file if it exists
                    condump = ctx.get_condump_file()
                    if os.path.isfile(condump):
                        with open(condump, 'r+', encoding='utf-8', errors='ignore') as file:
                            file.truncate(0)

                    while True:
                        if ctx.exit_event.is_set():
                            break

                        if ctx.steam_name == "":
                            name = ctx.rcon.command("name")
                            name = name.replace("\"name\" = ", "")
                            index = name.find(" ( def. \"unnamed\" )")
                            name = name[1:index-1]
                            ctx.steam_name = name
                            ctx.class_check_time = 0
                            logger.info(f"Your name is: {ctx.steam_name}")

                        if ctx.current_class == TFClass.UNKNOWN:
                            ctx.class_check_time -= 0.1
                            if ctx.class_check_time <= 0:
                                ctx.show_unknown_class_warning()
                                ctx.class_check_time = 30.0

                        ctx.mode_check_time -= 0.1
                        if ctx.mode_check_time <= 0:
                            ctx.rcon.command("wait 1; status")
                            ctx.mode_check_time = 5.0

                        if len(ctx.cmd_queue) > 0:
                            for c in ctx.cmd_queue:
                                ctx.rcon.command(c.cmd, c.args)
                                await asyncio.sleep(0.06) # don't send commands too fast or some may get dropped
                            ctx.cmd_queue.clear()

                        if ctx.taunt_trap_duration > 0:
                            ctx.rcon.command("taunt")
                            ctx.taunt_trap_duration -= 0.1

                        if ctx.melee_only_duration > 0:
                            ctx.rcon.command("slot3")
                            ctx.melee_only_duration -= 0.1

                        condump = ctx.get_condump_file()
                        if ctx.condump_io is not None or os.path.isfile(condump):
                            if ctx.condump_io is None:
                                ctx.condump_io = open(condump, 'r', encoding='utf-8', errors='ignore')

                            for line in ctx.condump_io:
                                ctx.on_console_line(line)

                        await asyncio.sleep(0.1)
            except ConnectionRefusedError:
                logger.info("TF2 RCON connection was refused."
                            "Make sure that the game is running with the -usercon launch option.")
                ctx.cleanup()
            except Exception as e:
                logger.info(f"TF2 RCON Connection failed or aborted ({e})")
                ctx.rcon = None
                ctx.condump_io = None
                if not isinstance(e, BadRCONPassword):
                    logger.info("Attempting to connect again in 10 seconds...")
                    await asyncio.sleep(10)
                else:
                    ctx.rcon_password = ""

        await asyncio.sleep(0.1)


class TF2Manager(GameManager):
    ctx: TF2Context
    def __init__(self, ctx):
        super().__init__(ctx)
        self.tf2_tab = None

    logging_pairs = [
        ("Client", "Archipelago")
    ]
    base_title = "Archipelago Team Fortress 2 Client"

    def build(self) -> Layout:
        super().build()
        self.tf2_tab = self.add_client_tab(title="TF2 Contracts", content=GridLayout(cols=3))
        self.update_tf2_tab()
        return self.container

    def update_tf2_tab(self, hide_buttons=False):
        self.tf2_tab.content.clear_widgets()
        self.tf2_tab.content.cols = 0
        if hide_buttons:
            return

        if self.ctx.is_casual:
            self.tf2_tab.content.cols += len(self.ctx.class_kill_reqs)

        if self.ctx.is_mvm:
            self.tf2_tab.content.cols += 1

        if not self.ctx.is_connected():
            return

        if self.ctx.is_casual:
            for class_name in self.ctx.class_kill_reqs.keys():
                has_class = self.ctx.has_item(class_name)
                clr = (1, 1, 1, 1)
                if not has_class:
                    clr = (1, 1, 1, 0.4)
                elif self.ctx.class_has_pending_objectives(class_name):
                    clr = (0.3, 1, 1, 1)

                display = class_name
                button = Button(text=display, size_hint_y=None, height=50, width=100, color=clr)
                if has_class:
                    button.bind(on_release=lambda press, cls=class_name: self.show_weapon_grid(cls))

                self.tf2_tab.content.add_widget(button)

        if self.ctx.is_mvm:
            clr = (1, 1, 1, 1)
            if self.ctx.mvm_has_any_pending_objectives():
                clr = (0.3, 1, 1, 1)

            button = Button(text="MvM", size_hint_y=None, height=50, width=100, color=clr)
            button.bind(on_release=lambda press: self.show_mvm_grid())
            self.tf2_tab.content.add_widget(button)

    def show_mvm_grid(self):
        self.update_tf2_tab()
        if not self.ctx.is_mvm:
            self.ctx.ui_mode = TF2UIMode.UNKNOWN
            return

        self.ctx.ui_mode = TF2UIMode.MVM_GRID
        grid = GridLayout(cols=5, size_hint_y=None, col_default_width=150,
                          row_default_height=60)

        grid.add_widget(Label(text=f"Contract Points: {self.ctx.points}/{self.ctx.required_points}", size_hint_y=None,
                              color=(0.5, 0.5, 1, 1)))

        btn = Button(text='Show All Contracts', size_hint_y=None, height=40)
        btn.bind(on_release=lambda press: self.show_bundle(""))
        grid.add_widget(btn)
        for bundle in self.ctx.mvm_bundles.keys():
            number = int(bundle[-1])
            clr: tuple
            if not self.ctx.has_item(bundle):
                clr = (1, 1, 1, 0.4)
            elif self.ctx.mvm_bundle_has_pending_objectives(bundle):
                clr = (0.3, 1, 1, 1)
            else:
                clr = (0.2, 1, 0.2, 1)

            btn = Button(text=f'Bundle #{number}', size_hint_y=None, height=40, color=clr)
            if self.ctx.has_item(bundle):
                btn.bind(on_release=lambda press, b=bundle: self.show_bundle(b))

            grid.add_widget(btn)

        self.tf2_tab.content.add_widget(grid)

    def show_bundle(self, bundle: str):
        self.update_tf2_tab()

        if not self.ctx.is_mvm or (bundle != "" and bundle not in self.ctx.mvm_bundles):
            self.ctx.ui_mode = TF2UIMode.UNKNOWN
            return

        self.ctx.current_mvm_bundle = bundle
        self.ctx.ui_mode = TF2UIMode.MVM_BUNDLE
        grid = GridLayout(cols=4, size_hint_y=None, col_default_width=200,row_default_height=60)
        grid.add_widget(Label(text=f"Contract Points: {self.ctx.points}/{self.ctx.required_points}", size_hint_y=None,
                              color=(0.5, 0.5, 1, 1)))

        grid.bind(minimum_height=grid.setter('height'))
        grid.bind(minimum_width=grid.setter('width'))
        scroll = ScrollView(size_hint=(None, None), size=(Window.width, Window.height))
        if bundle == "":
            btn = Button(text=f'Showing All\nGo Back', size_hint=(-0.25, -0.25))
        else:
            number = int(bundle[-1])
            btn = Button(text=f'Bundle #{number}\nGo Back', size_hint=(-0.25, -0.25))

        btn.bind(on_release=lambda press: self.show_mvm_grid())
        grid.add_widget(btn)
        bot_list = []
        if bundle != "":
            bot_list = list(self.ctx.mvm_bundles[bundle])
        else:
            for key, val in self.ctx.mvm_bundles.items():
                if self.ctx.has_item(key):
                    for bot in val:
                        bot_list.append(bot)

        for bot in bot_list:
            count = self.ctx.mvm_kill_counts.get(bot, 0)
            req = self.ctx.mvm_kill_reqs[bot]
            clr = (1, 1, 1, 1)
            if count > 0 and count < req:
                clr = (1, 1, 0.5, 1)
            elif count >= req:
                clr = (0.2, 1, 0.2, 1)

            text = f"{bot}\n{count}/{req}"
            grid.add_widget(Label(text=text, size_hint_y=None, color=clr))

        scroll.add_widget(grid)

        # FIXME: Somehow the scrollview stretches the first button widget?????? Kivy sucks ass.
        self.tf2_tab.content.add_widget(scroll, True)

    def show_weapon_grid(self, class_name: str):
        if not self.ctx.has_item(class_name):
            return

        self.update_tf2_tab()
        if not self.ctx.is_casual or class_name not in self.ctx.class_kill_reqs.keys():
            self.ctx.ui_mode = TF2UIMode.UNKNOWN
            return

        self.ctx.ui_mode = TF2UIMode.VIEWING_CLASS
        grid = GridLayout(cols=5, size_hint_y=None, col_default_width=150, col_force_default=True,
                          row_default_height=80, row_force_default=True)

        grid.add_widget(Label(text=f"Contract Points: {self.ctx.points}/{self.ctx.required_points}", size_hint_y=None,
                              color=(0.5, 0.5, 1, 1)))

        class_type = TFClass[class_name.upper()]
        class_kills = self.ctx.class_kill_counts.get(class_name, 0)
        class_count = self.ctx.class_kill_reqs.get(class_name)
        if class_count > 0:
            text = format(f"  Kills as {class_name}\n  {class_kills}/{class_count}")
            clr = (0.2, 1, 0.2, 1) if class_kills >= class_count else (1, 1, 0, 1) if class_kills > 0 else (1, 1, 1, 1)
            grid.add_widget(Label(text=text, size_hint_y=None, color=clr))

        for weapon, count in self.ctx.weapon_kill_reqs.items():
            if class_uses_weapon(class_type.tostr(), weapon):
                if self.ctx.has_item(weapon) or weapon in self.ctx.contract_hints:
                    weapon_kills = self.ctx.weapon_kill_counts.get(weapon, 0)
                    text = format(f"  {weapon}\n  {weapon_kills}/{count}")
                    clr = (0.2, 1, 0.2, 1) if weapon_kills >= count else (1, 1, 0.5, 1) if weapon_kills > 0 else (
                    1, 1, 1, 0.4) if not self.ctx.has_item(weapon) else (1, 1, 1, 1)
                    grid.add_widget(Label(text=text, size_hint_y=None, color=clr))
                else:
                    grid.add_widget(Label(text="?????", size_hint_y=None, color=(1, 1, 1, 0.4)))

        self.tf2_tab.content.add_widget(grid)

def launch():
    async def main():
        parser = get_base_parser()
        args = parser.parse_args()
        ctx = TF2Context(args.connect, args.password)
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        logger.info("Starting Team Fortress 2 RCON")
        ctx.rcon_task = asyncio.create_task(rcon_loop(ctx), name="RCONLoop")
        await ctx.rcon_task
        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("TF2Client")
    # options = Utils.get_options()

    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
