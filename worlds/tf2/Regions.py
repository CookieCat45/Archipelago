from copy import deepcopy

from BaseClasses import Region, ItemClassification
from typing import TYPE_CHECKING, Dict
from .Data import (TF2Location, TF2Item, weapon_to_class, TFClass, multiclass_weapons, weapon_kill_names, weapon_list,
                   class_names)
from .Options import WeaponKillObjectiveCount, GeneralKillObjectiveCount
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import TF2World

def create_tf2_objectives(world: "TF2World") -> int:
    location_count = 0
    added_weapons = []
    menu = world.multiworld.get_region("Menu", world.player)
    for class_name in world.options.AllowedClasses:
        class_name = class_name.lower().capitalize()
        class_region = Region(f"{class_name} Objectives", world.player, world.multiworld)
        menu.connect(class_region, f"-> {class_name} Objectives",
                     lambda state, c=class_name: state.has(c, world.player))

        # create general kill objectives (per class)
        contract_point_loc = TF2Location(world.player, f"Contract Point - {class_name} Kills", None)
        contract_point_loc.place_locked_item(
            TF2Item("Contract Point", ItemClassification.progression, None, world.player))
        contract_point_loc.show_in_spoiler = False
        contract_point_loc.parent_region = class_region
        class_region.locations.append(contract_point_loc)
        world.total_objectives += 1

        count = world.options.GeneralKillObjectiveCount.value
        world.class_kill_counts.setdefault(class_name, count)
        for i in range(count):
            loc_name = f"{class_name} General Kill #{i + 1}"
            loc = TF2Location(world.player, loc_name, get_location_id(class_name) + i)
            loc.parent_region = class_region
            class_region.locations.append(loc)
            location_count += 1

        # create weapon objectives
        for weapon in world.available_weapons:
            class_type = TFClass[class_name.upper()]
            weapon_dict = weapon_kill_names[class_type]
            if weapon not in weapon_dict.values() or weapon in added_weapons:
                continue

            added_weapons.append(weapon)
            count = world.options.WeaponKillObjectiveCount.value
            plando_val = world.options.WeaponKillCountPlando.value.get(weapon, 0)
            plando_val = min(plando_val, world.options.WeaponKillObjectiveCount.range_end)
            if plando_val > 0:
                count = plando_val

            world.weapon_kill_counts.setdefault(weapon, count)
            for i in range(count):
                loc_name = f"{weapon} Kill #{i+1}"
                loc = TF2Location(world.player, loc_name, get_location_id(weapon)+i)
                loc.parent_region = class_region
                set_rule(loc, lambda state, w=weapon: state.has(w, world.player))
                class_region.locations.append(loc)
                location_count += 1

            contract_point_loc = TF2Location(world.player, f"Contract Point - {weapon} Kills", None)
            contract_point_loc.place_locked_item(
                TF2Item("Contract Point", ItemClassification.progression, None, world.player))
            contract_point_loc.show_in_spoiler = False
            contract_point_loc.parent_region = class_region
            set_rule(contract_point_loc, lambda state, w=weapon: state.has(w, world.player))
            class_region.locations.append(contract_point_loc)
            world.total_objectives += 1

        world.multiworld.regions.append(class_region)

    return location_count


def create_mvm_objectives(world: "TF2World") -> int:
    menu = world.multiworld.get_region("Menu", world.player)
    available_bots = deepcopy(world.options.MvmCommonBotWhitelist.value | world.options.MvmGiantWhitelist.value)
    available_bosses = deepcopy(world.options.MvmBossWhitelist.value)  # bosses are a separate thing
    location_count = 0
    bundle_counter = 0
    current_bundle = 1
    bundle_contract_list = []
    bundle_name = "MvM Contract Bundle #1"
    boss_contract_total = world.options.MvmBossContractAmount.value
    bundle_ids = []
    boss_bundle_ids = []
    for i in range(world.options.MvmContractBundleTotal.value):
        bundle_ids.append(i+1)

    if boss_contract_total > 0:
        while len(boss_bundle_ids) < boss_contract_total:
            world.random.shuffle(bundle_ids)
            for i in bundle_ids:
                boss_bundle_ids.append(i)
                if len(boss_bundle_ids) >= boss_contract_total:
                    break

    boss_count = 0
    for i in range(world.options.MvmContractBundleTotal.value * world.options.MvmContractBundleContractCount):
        if len(available_bots) <= 0:
            break

        bot: str
        if (boss_contract_total > 0 and current_bundle in boss_bundle_ids and len(available_bosses) > 0
        and boss_count < boss_contract_total):
            bot = world.random.choices(list(available_bosses.keys()), weights=list(available_bosses.values()), k=1)[0]
            del available_bosses[bot]
        else:
            bot = world.random.choices(list(available_bots.keys()), weights=list(available_bots.values()), k=1)[0]
            del available_bots[bot]

        count: int
        if bot in world.options.MvmCommonBotWhitelist:
            count = world.options.MvmContractCommonKillCount.value
        elif bot in world.options.MvmGiantWhitelist:
            count = world.options.MvmContractGiantKillCount.value
        elif bot in world.options.MvmBossWhitelist:
            count = world.options.MvmContractBossReward.value
            boss_count += 1
        else:
            continue

        bundle_contract_list.append(bot)
        mvm_region = Region(f"MvM Contract - {bot} Kills", world.player, world.multiworld)
        menu.connect(mvm_region, f"Menu -> MvM Contract - {bot} Kills",
                     lambda state, b=bundle_name: state.has(b, world.player))
        contract_point_loc = TF2Location(world.player, f"MvM Contract Point - {bot} Kills", None)
        contract_point_loc.place_locked_item(
            TF2Item("Contract Point", ItemClassification.progression, None, world.player))
        contract_point_loc.show_in_spoiler = False
        contract_point_loc.parent_region = mvm_region
        mvm_region.locations.append(contract_point_loc)
        world.total_objectives += 1
        plando_val = world.options.MvmKillCountPlando.value.get(bot, 0)
        plando_val = min(plando_val, world.options.MvmContractCommonKillCount.range_end)
        if plando_val > 0:
            world.mvm_kill_counts[bot] = plando_val
            if bot not in world.options.MvmBossWhitelist:
                count = plando_val
        elif bot in world.options.MvmBossWhitelist:
            world.mvm_kill_counts[bot] = 1
        else:
            world.mvm_kill_counts[bot] = count

        for n in range(count):
            loc_name: str
            if bot in world.options.MvmBossWhitelist:
                loc_name = f"{bot} Reward #{n + 1}"
            else:
                loc_name = f"{bot} Kill #{n+1}"

            loc = TF2Location(world.player, loc_name, world.get_location_id_mvm(loc_name))
            loc.parent_region = mvm_region
            mvm_region.locations.append(loc)
            location_count += 1

        bundle_counter += 1
        if bundle_counter >= world.options.MvmContractBundleContractCount or len(available_bots) <= 0:
            world.mvm_bundles[bundle_name] = set(bundle_contract_list)
            bundle_contract_list = []
            bundle_counter = 0
            current_bundle += 1
            bundle_name = f"MvM Contract Bundle #{current_bundle}"

    return location_count


def get_location_id(name: str) -> int:
    # fix conflicts
    if name == "Hot Hand":
        return 30725
    elif name == "Manmelter":
        return 30960
    elif name == "Equalizer":
        return 20900
    elif name == "Gunslinger":
        return 61000
    elif name == "Direct Hit":
        return 62000

    try:
        class_type: TFClass = TFClass[name.upper()]
        if class_type != TFClass.UNKNOWN:
            return int(class_type) * 100
    except KeyError:
        pass

    class_type = TFClass.UNKNOWN
    try:
        class_type = TFClass[weapon_to_class.get(name).upper()]
    except AttributeError:
        pass

    weapon_id: int
    if name in multiclass_weapons:
        weapon_id = 20000
    elif class_type != TFClass.UNKNOWN:
        weapon_id = int(class_type) * 10000
    else:
        raise Exception(f"Can't generate location ID for '{name}'")

    ascii_values = list(name.encode('ascii'))
    for val in ascii_values:
        weapon_id += val

    return weapon_id


def get_location_ids() -> Dict[str, int]:
    location_ids = {}
    for class_name in class_names:
        for i in range(GeneralKillObjectiveCount.range_end):
            loc_name = f"{class_name} - General Kill #{i+1}"
            location_ids.setdefault(loc_name, get_location_id(class_name)+i)

    for weapon in weapon_list:
        for i in range(WeaponKillObjectiveCount.range_end):
            loc_name = f"{weapon} - Kill #{i+1}"
            location_ids.setdefault(loc_name, get_location_id(weapon)+i)

    return location_ids
