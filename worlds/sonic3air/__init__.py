from typing import NamedTuple, Union, Mapping, Any, Optional
from BaseClasses import Item, Tutorial, ItemClassification, MultiWorld
from Options import Option
from .Options import Sonic3AIROptions, KnucklesStoryMode, KnucklesGoal, ZoneUnlockMode, Goal, adjust_options
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
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.starting_zone = ""
        self.location_char_whitelists = {}
        self.location_required_items = {}
        self.ut_regen = False

    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            self.ut_regen = True
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            self.starting_zone = slot_data["starting_zone"]
            for key, value in slot_data.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    setattr(self.options, key, opt.from_any(value))

        adjust_options(self)
        self.multiworld.push_precollected(self.create_item(self.get_starting_char()))

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
            "ChaosEmeraldFragments": self.options.ChaosEmeraldFragments.value,
            "DisableSuperEmeralds": self.options.DisableSuperEmeralds.value,
            "GiantRingRewardCount": self.options.GiantRingRewardCount.value,
            "DeathLink": self.options.death_link.value,
            "SpecialSeed": self.random.randint(1, 900000000),
            "LocationRequiredItems": self.location_required_items,
            "LocationCharWhitelists": self.location_char_whitelists,
            "StartingCharacter": self.options.StartingCharacter.value,
            "ExtraChaosEmeraldFragments": self.options.ExtraChaosEmeraldFragments.value,
            "SpecialStageSphereChecks": self.options.SpecialStageSphereChecks.value,
            "SpecialStageRingChecks": self.options.SpecialStageRingChecks.value,
            "SpecialStageSphereChecksLimit": self.options.SpecialStageSphereChecksLimit.value,
            "SpecialStageRingChecksLimit": self.options.SpecialStageRingChecksLimit.value,
            "starting_zone": self.starting_zone,
        }

        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data

    def get_starting_char(self) -> str:
        starting_chars = {0: "Sonic", 1: "Tails", 2: "Knuckles"}
        return starting_chars[self.options.StartingCharacter.value]

    def get_emerald_count(self) -> int:
        if self.options.DisableSuperEmeralds:
            return 7
        return 14

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
