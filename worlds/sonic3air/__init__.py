from typing import NamedTuple, Union, Mapping, Any
from BaseClasses import Item, Tutorial, ItemClassification, MultiWorld
from .Options import Sonic3AIROptions, KnucklesStoryMode, KnucklesGoal, ZoneUnlockMode
from .Regions import init_regions
from .Locations import get_location_names
from .Items import fill_itempool, create_item, item_table, get_random_junk
from .Rules import init_rules
from ..AutoWorld import World, WebWorld


class Sonic3AIRWorld(World):
    game = "Sonic 3 A.I.R."
    topology_present = False
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = Sonic3AIROptions
    options: Sonic3AIROptions

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.zones_available = []
        self.starting_zone = ""
        self.starting_character = "Sonic"
        self.location_char_whitelists = {}
        self.location_required_items = {}

    def generate_early(self) -> None:
        if self.options.KnucklesStoryMode.value >= 3:
            self.starting_character = "Knuckles"
        elif self.options.StartingCharacter == self.options.StartingCharacter.option_sonic:
            self.starting_character = "Sonic"
        elif self.options.StartingCharacter == self.options.StartingCharacter.option_tails:
            self.starting_character = "Tails"
        elif self.options.StartingCharacter == self.options.StartingCharacter.option_knuckles:
            self.starting_character = "Knuckles"

        if self.options.KnucklesStoryMode == KnucklesStoryMode.option_removed and self.starting_character == "Knuckles":
            self.starting_character = "Sonic"

        self.multiworld.push_precollected(self.create_item(self.starting_character))
        if self.is_knuckles_exclusive() and self.options.KnucklesGoal == KnucklesGoal.option_allzones_sanctuary:
            if self.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg:
                # This makes no sense, so change it
                self.options.ZoneUnlockMode.value = ZoneUnlockMode.option_shuffled

    def create_regions(self):
        init_regions(self)

    def create_items(self):
        fill_itempool(self)

    def set_rules(self):
        init_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def get_filler_item_name(self) -> str:
        return get_random_junk(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {
            "ZoneUnlockMode": self.options.ZoneUnlockMode.value,
            "ZonesAllowed": self.options.ZonesAllowed.value,
            "ZoneCount": len(self.options.ZonesAllowed.value),
            "Goal": self.options.Goal.value,
            "SpecialStageUnlockItemCount": self.options.SpecialStageUnlockItemCount.value,
            "KnucklesStoryMode": self.options.KnucklesStoryMode.value,
            "KnucklesGoal": self.options.KnucklesGoal.value,
            "ShuffleGiantRings": self.options.ShuffleGiantRings.value,
            "DeathLink": self.options.death_link.value,
            "SpecialSeed": self.random.randint(1, 500000000),
            "LocationRequiredItems": self.location_required_items,
            "LocationCharWhitelists": self.location_char_whitelists
        }

        return slot_data

    def is_doomsday_goal(self) -> bool:
        return self.options.Goal.value > 0

    def is_doomsday_goal_knuckles(self) -> bool:
        return self.has_knuckles_goal() and self.options.KnucklesGoal.value >= 1 and self.options.KnucklesGoal.value <= 4

    def has_knuckles_goal(self) -> bool:
        return (self.options.KnucklesStoryMode != KnucklesStoryMode.option_normal
                and self.options.KnucklesStoryMode != KnucklesStoryMode.option_removed)

    def is_knuckles_exclusive(self) -> bool:
        return self.options.KnucklesStoryMode == KnucklesStoryMode.option_exclusive \
            or self.options.KnucklesStoryMode == KnucklesStoryMode.option_exclusive_tails

    def does_char_exist(self, char: str) -> bool:
        if char == "Knuckles":
            return self.options.KnucklesStoryMode != KnucklesStoryMode.option_removed
        elif char == "Sonic" or char == "Sonic & Tails":
            return not self.is_knuckles_exclusive()
        elif char == "Tails":
            if self.is_knuckles_exclusive():
                return self.options.KnucklesStoryMode == KnucklesStoryMode.option_exclusive_tails
        elif char == "Knuckles & Tails":
            return self.options.KnucklesStoryMode != KnucklesStoryMode.option_exclusive \
             and self.options.KnucklesStoryMode != KnucklesStoryMode.option_removed

        return True

    @staticmethod
    def char_name_to_id(name: str) -> int:
        if name == "Sonic":
            return 1
        elif name == "Tails":
            return 2
        elif name == "Knuckles":
            return 3
        elif name == "Sonic & Tails":
            return 0
        elif name == "Knuckles & Tails":
            return 4

        return -1
