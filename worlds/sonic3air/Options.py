from typing import List, TYPE_CHECKING, Dict, Any
from schema import Schema, Optional
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Range, Toggle, DeathLink, Choice, OptionList, DefaultOnToggle, OptionGroup, StartInventoryPool


class StartingCharacter(Choice):
    """The character that you will start the game with."""
    option_sonic = 0
    option_tails = 1
    option_knuckles = 2


class ZoneUnlockMode(Choice):
    """Determines how zone unlocking works.
    linear: Zones are unlocked in the vanilla order through a progressive item. You start with Angel Island Zone.
    shuffled: Individual zone unlocks are shuffled into the item pool. You start with a random zone.
    shuffled_deathegg: Same as shuffled, but locks Death Egg Zone until all other zones are completed,
        and removes Death Egg Zone from the item pool.
    """
    option_linear = 0
    option_shuffled = 1
    option_shuffled_deathegg = 2


class ZoneCount(Range):
    """Determines the total number of zones available."""
    range_start = 1
    range_end = 13
    default = 13


class ZonesAllowed(OptionList):
    """List of zone names to allow in the game (excluding Doomsday Zone which is conditional)
    If playing in linear mode, missing zones will be skipped.
    If playing in shuffled mode, missing zones will not be added to the item pool."""
    default = (
        "Angel Island Zone",
        "Hydrocity Zone",
        "Marble Garden Zone",
        "Carnival Night Zone",
        "IceCap Zone",
        "Launch Base Zone",
        "Mushroom Hill Zone",
        "Flying Battery Zone",
        "Sandopolis Zone",
        "Lava Reef Zone",
        "Hidden Palace Zone",
        "Sky Sanctuary Zone",
        "Death Egg Zone",
    )


class Goal(Choice):
    """Determines what the goal of the game is.
    allzones: Complete all available zones.
    doomsday: Collect all Chaos Emeralds and finish Doomsday Zone.
    doomsday_hyper: Collect all Chaos + Super Emeralds and finish Doomsday Zone.
    allzones_doomsday: Complete all zones, collect all Chaos Emeralds and finish Doomsday Zone.
    allzones_doomsday_hyper: Complete all zones, collect all Chaos + Super Emeralds and finish Doomsday Zone.
    """
    option_allzones = 0
    option_doomsday = 1
    option_doomsday_hyper = 2
    option_allzones_doomsday = 3
    option_allzones_doomsday_hyper = 4


class ShuffleGiantRings(DefaultOnToggle):
    """Turns the Giant Rings found in most levels into location checks."""


class SpecialStageUnlockItemCount(Range):
    """Shuffles a specified number of items into the pool that unlock access to Special Stages.
    A value of 0 will prevent Special Stages from being accessible at all."""
    range_start = 0
    range_end = 14


class SpecialStageSphereChecks(Range):
    """Adds checks to Special Stages that are cleared by collecting certain amounts of blue spheres.
    The value of this option determines the percentage of spheres that are necessary to complete a check.
    For example, if the value is 2:
    2 / 10 = 0.2 (every 20% of spheres collected in a stage)."""
    range_start = 0
    range_end = 10


class SpecialStageRingChecks(Range):
    """Adds checks to Special Stages that are cleared by collecting certain amounts of rings.
    The value of this option determines the percentage of rings that are necessary to complete a check.
    For example, if the value is 2:
    2 / 10 = 0.2 (every 20% of rings collected in a stage)."""
    range_start = 0
    range_end = 10


@dataclass
class Sonic3AIROptions(PerGameCommonOptions):
    StartingCharacter: StartingCharacter
    ZoneUnlockMode: ZoneUnlockMode
    ZoneCount: ZoneCount
    ZonesAllowed: ZonesAllowed
    Goal: Goal
    ShuffleGiantRings: ShuffleGiantRings
    SpecialStageUnlockItemCount: SpecialStageUnlockItemCount
    SpecialStageSphereChecks: SpecialStageSphereChecks
    SpecialStageRingChecks: SpecialStageRingChecks
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
