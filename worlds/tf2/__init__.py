from copy import deepcopy

import worlds.tf2.Options
from worlds.AutoWorld import World
from typing import List, Mapping, Any, Dict, TextIO
from BaseClasses import Item, MultiWorld, Region
from .Options import TF2Options, MeleeWeaponRules, MvmContractBundleTotal
from .Items import get_item_id, create_item, create_itempool, get_item_ids, init_available_weapons
from .Regions import create_tf2_objectives, get_location_ids, create_mvm_objectives
from .Data import weapon_kill_names, TFClass, weapon_to_class, knives, swords, melee_weapons, class_names
from worlds.LauncherComponents import Component, components, icon_paths, launch_subprocess, Type
from math import floor

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="Client")

components.append(Component("Team Fortress 2 Client", "TF2Client", func=launch_client,
                            component_type=Type.CLIENT, icon='tf2'))

icon_paths['tf2'] = f"ap:{__name__}/icons/tf2.png"

class TF2World(World):
    """
    One of the most popular online action games of all time,
    Team Fortress 2 delivers constant free updates—new game modes, maps, equipment and, most importantly, hats.
    Nine distinct classes provide a broad range of tactical abilities and personalities,
    and lend themselves to a variety of player skills.
    """

    game = "Team Fortress 2"
    options_dataclass = TF2Options
    options: TF2Options
    item_name_to_id = get_item_ids()
    location_name_to_id = get_location_ids()
    item_name_groups = {"Classes": set(class_names)}
    mvm_location_id_counter = 950000

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.available_weapons: List[str] = []
        self.total_locations: int = 0
        self.total_objectives: int = 0
        self.starting_classes: List[str] = []
        self.weapon_kill_counts: Dict[str, int] = {}
        self.class_kill_counts: Dict[str, int] = {}
        self.mvm_kill_counts: Dict[str, int] = {}
        self.mvm_bundles: Dict[str, set] = {}

    def create_item(self, name: str) -> Item:
        return create_item(self, name, get_item_id(name))

    def generate_early(self):
        for weapon in self.options.BannedWeapons.value + self.options.UnbannedWeapons.value:
            valid = False
            for weapon_dict in weapon_kill_names:
                for weapon_name in weapon_dict.values():
                    if weapon == weapon_name:
                        valid = True
                        break

            if not valid:
                raise Exception(f"Invalid weapon name: {weapon}")

        if len(self.options.AllowedClasses.value) > 0:
            class_list = deepcopy(self.options.AllowedClasses.value)
            random_count = self.options.RandomClassPoolCount.value
            if random_count > 0 and random_count < len(class_list):
                # remove random classes until the amount is the same
                while len(class_list) > random_count:
                    class_list.remove(class_list[self.random.randint(0, len(class_list) - 1)])

                self.options.AllowedClasses.value = deepcopy(class_list)

            for i in range(self.options.StartingClassCount):
                if len(class_list) <= 0:
                    break

                starting_class = class_list[self.random.randint(0, len(class_list) - 1)]
                class_list.remove(starting_class)
                self.starting_classes.append(starting_class)
                self.multiworld.push_precollected(self.create_item(starting_class))

            if self.options.WeaponsInPool.value > 0:
                init_available_weapons(self)

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        self.total_locations = create_tf2_objectives(self)
        if self.is_mvm_enabled():
            self.total_locations += create_mvm_objectives(self)
            # force a datapackage update because we create these locations dynamically
            from .. import network_data_package
            network_data_package["games"]["Team Fortress 2"] = self.get_data_package_data()

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Contract Point", self.player, self.get_required_contract_points())

    def get_filler_item_name(self) -> str:
        return "Contract Hint"

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {}
        slot_data["IsCasual"] = bool(len(self.options.AllowedClasses.value) > 0)
        slot_data["IsMvm"] = bool(self.is_mvm_enabled())
        slot_data["WeaponKillCounts"] = self.weapon_kill_counts
        slot_data["ClassKillCounts"] = self.class_kill_counts
        slot_data["RequiredContractPoints"] = self.get_required_contract_points()
        slot_data["DeathLinkAmnesty"] = self.options.DeathLinkAmnesty.value
        slot_data["DeathLink"] = bool(self.options.DeathLink.value)
        if self.is_mvm_enabled():
            slot_data["MvmBundles"] = self.mvm_bundles
            slot_data["MvmKillCounts"] = self.mvm_kill_counts
            slot_data["MvmBossNames"] = deepcopy(self.options.MvmBossWhitelist.value)
            slot_data["MvmContractBossReward"] = self.options.MvmContractBossReward.value
            mvm_location_ids = {}
            for key, val in self.location_name_to_id.items():
                if val >= 950000:
                    mvm_location_ids[key] = val

            slot_data["MvmLocationIds"] = mvm_location_ids

        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"Total Objectives: {self.total_objectives}\n")
        spoiler_handle.write(f"Contract Points Required: {self.get_required_contract_points()}\n")
        spoiler_handle.write(f"Total Weapons: {len(self.available_weapons)}\n")
        if self.is_mvm_enabled():
            spoiler_handle.write(f"MvM Contract Bundles: {self.mvm_bundles}\n")

    def get_required_contract_points(self) -> int:
        return floor(self.total_objectives * (self.options.ContractPointRequirement/100))

    def is_mvm_enabled(self) -> bool:
        return self.options.MvmContractBundleTotal.value > 0

    def is_casual_enabled(self) -> bool:
        return len(self.options.AllowedClasses.value) > 0

    # this needs to be a world-class method
    @staticmethod
    def get_location_id_mvm(name: str) -> int:
        # if it exists in the dict already, use that (another world may have created it already)
        existing_id: int = TF2World.location_name_to_id.get(name, None)
        if existing_id is not None:
            return existing_id

        # add to the dict and increment the counter
        loc_id: int = TF2World.mvm_location_id_counter
        TF2World.location_name_to_id.setdefault(name, loc_id)
        TF2World.mvm_location_id_counter += 1
        return loc_id