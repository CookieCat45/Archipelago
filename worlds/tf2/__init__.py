import worlds.tf2.Options
from worlds.AutoWorld import World
from typing import List, Mapping, Any, Dict, TextIO
from BaseClasses import Item, MultiWorld
from .Options import TF2Options, ol_to_list, MeleeWeaponRules
from .Items import get_item_id, create_item, create_itempool, get_item_ids, init_available_weapons
from .Regions import create_tf2_objectives, get_location_ids
from .Data import weapon_kill_names, TFClass, weapon_to_class, knives, swords, melee_weapons
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

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.available_weapons: List[str] = []
        self.total_locations: int = 0
        self.total_objectives: int = 0
        self.starting_class = TFClass.UNKNOWN
        self.weapon_kill_counts: Dict[str, int] = {}
        self.class_kill_counts: Dict[str, int] = {}

    def create_item(self, name: str) -> Item:
        return create_item(self, name, get_item_id(name))

    def generate_early(self):
        for weapon in self.options.BannedWeapons:
            valid = False
            for weapon_dict in weapon_kill_names:
                for weapon_name in weapon_dict.values():
                    if weapon == weapon_name:
                        valid = True
                        break

            if not valid:
                raise Exception(f"Invalid weapon name: {weapon}")

        starting_class: TFClass
        try:
            starting_class = TFClass(self.options.StartingClass)
        except ValueError:
            class_list = ol_to_list(self.options.AllowedClasses)
            starting_class = TFClass[class_list[self.random.randint(0, len(class_list) - 1)].upper()]

        self.starting_class = starting_class
        self.multiworld.push_precollected(self.create_item(starting_class.tostr()))
        init_available_weapons(self)

    def create_regions(self):
        self.total_locations = create_tf2_objectives(self)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Contract Point", self.player, self.get_required_contract_points())

    def get_filler_item_name(self) -> str:
        return "Contract Hint"

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {}
        slot_data["WeaponKillCounts"] = self.weapon_kill_counts
        slot_data["ClassKillCounts"] = self.class_kill_counts
        slot_data["RequiredContractPoints"] = self.get_required_contract_points()
        slot_data["DeathLinkAmnesty"] = self.options.DeathLinkAmnesty.value
        slot_data["DeathLink"] = bool(self.options.DeathLink.value)
        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"Total Weapons: {len(self.available_weapons)}\n")
        spoiler_handle.write(f"Total Objectives: {self.total_objectives}\n")
        spoiler_handle.write(f"Contract Points Required: {self.get_required_contract_points()}")

    def get_required_contract_points(self) -> int:
        return floor(self.total_objectives * (self.options.ContractPointRequirement/100))
