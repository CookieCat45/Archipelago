from typing import List, TYPE_CHECKING, Dict, Any
from schema import Schema, Optional
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Range, Toggle, DeathLink, Choice, OptionList, DefaultOnToggle, OptionGroup, StartInventoryPool, \
OptionDict

if TYPE_CHECKING:
    from . import Sonic3AIRWorld

def adjust_options(world: "Sonic3AIRWorld"):
    if world.ut_regen:
        return

    if world.is_knuckles_exclusive():
        world.options.StartingCharacter.value = StartingCharacter.option_knuckles
    elif world.options.KnucklesStoryMode == KnucklesStoryMode.option_removed and world.options.StartingCharacter == StartingCharacter.option_knuckles:
        world.options.StartingCharacter.value = StartingCharacter.option_sonic

    if world.is_knuckles_exclusive() and world.options.KnucklesGoal == KnucklesGoal.option_allzones_sanctuary:
        if world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg:
            # This makes no sense, so change it
            world.options.ZoneUnlockMode.value = ZoneUnlockMode.option_shuffled

    if world.options.DisableSuperEmeralds:
        if world.options.Goal == Goal.option_doomsday_hyper:
            world.options.Goal.value = Goal.option_doomsday
        if world.options.KnucklesGoal == KnucklesGoal.option_doomsday_hyper:
            world.options.KnucklesGoal = KnucklesGoal.option_doomsday

    if "Doomsday Zone" in world.options.ZonesAllowed.value:
        world.options.ZonesAllowed.value.remove("Doomsday Zone")
    if "Doomsday Zone" in world.options.RandomZoneList.value:
        world.options.RandomZoneList.value.remove("Doomsday Zone")


class StartingCharacter(Choice):
    """The character that you will start the game with."""
    option_sonic = 0
    option_tails = 1
    option_knuckles = 2


class ZoneUnlockMode(Choice):
    """Determines how zone unlocking works.
    linear: Zones are unlocked via progressive items, with the unlock order determined by the ZonesAllowed option list.
        You start with the first zone in the list. To progress, the zones must be completed in order.
    shuffled: Individual zone unlocks are shuffled into the item pool. You start with a random zone.
    shuffled_deathegg: Same as shuffled, but locks Death Egg Zone until all other zones are completed.
    """
    option_linear = 0
    option_shuffled = 1
    option_shuffled_deathegg = 2


class ZonesAllowed(OptionList):
    """List of zone names to allow in the game (excluding Doomsday Zone which is conditional)
    Note that some other options may force certain zones to exist anyway regardless of this list (Death Egg, Sky Sanctuary)"""
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


class RandomZoneCount(Range):
    """Determines the number of random zones to add from the RandomZoneList option."""
    range_start = 0
    range_end = 13
    default = 0


class RandomZoneList(OptionList):
    """When RandomZoneCount is greater than 0, a pool from this list will be selected and added to the list of allowed zones.
    The zones will be inserted into the list at random locations."""
    default = ()


class Goal(Choice):
    """Determines what the goal of the game is
    allzones: Complete all available zones as Sonic and/or Tails
    doomsday: Collect all Chaos Emeralds and finish Doomsday Zone
    doomsday_hyper: Collect all Chaos + Super Emeralds and finish Doomsday Zone
    allzones_doomsday: Complete all zones, collect 7 Emeralds and finish Doomsday Zone
    allzones_doomsday_hyper: Complete all zones, collect 14 Emeralds and finish Doomsday Zone
    """
    option_allzones = 0
    option_doomsday = 1
    option_doomsday_hyper = 2
    option_allzones_doomsday = 3
    option_allzones_doomsday_hyper = 4


class KnucklesStoryMode(Choice):
    """Determines how the Knuckles storyline should be factored in
    normal: Completing acts as Knuckles will count towards completing a zone globally
    goal: Adds another goal requirement based on the KnucklesGoal option in addition to the standard goal requirements
    removed: Knuckles is not playable and all of his levels are inaccessible
    exclusive: Sonic and Tails are removed, only Knuckles and his levels are playable
    exclusive_tails: Same as Exclusive, but Tails is re-added and Knuckles+Tails are playable together (not Tails alone)"""
    option_normal = 0
    option_goal = 1
    option_removed = 2
    option_exclusive = 3
    option_exclusive_tails = 4


class KnucklesGoal(Choice):
    """If KnucklesStoryMode is set to 'goal' or 'exclusive' this option determines the goal requirement for Knuckles
    allzones: Complete all available zones as Knuckles
    doomsday: Collect all Chaos Emeralds and finish Doomsday Zone
    doomsday_hyper: Collect all Chaos + Super Emeralds and finish Doomsday Zone
    allzones_doomsday: Complete all zones, collect 7 Emeralds and finish Doomsday Zone
    allzones_doomsday_hyper: Complete all zones, collect 14 Emeralds and finish Doomsday Zone
    allzones_sanctuary: Same as 'allzones', but Sky Sanctuary will always be the last completable zone for Knuckles,
        and will be the Mecha Sonic boss for him"""
    option_allzones = 0
    option_doomsday = 1
    option_doomsday_hyper = 2
    option_allzones_doomsday = 3
    option_allzones_doomsday_hyper = 4
    option_allzones_sanctuary = 5


class ShuffleGiantRings(DefaultOnToggle):
    """Turns the Giant Rings found in most levels into location checks."""


class ChaosEmeraldFragments(Range):
    """If this option's value is greater than 1, all Chaos Emeralds in the pool will be removed
    and split into Chaos Emerald Fragments. This option's value determines the number
    of fragments required to obtain one Emerald."""
    range_start = 0
    range_end = 5
    default = 0


class ExtraChaosEmeraldFragments(Range):
    """Extra emerald fragments to put in the item pool, if fragments are enabled."""
    range_start = 0
    range_end = 25
    default = 8


class DisableSuperEmeralds(Toggle):
    """If enabled, only 7 total Chaos Emeralds will be added to the item pool, removing the 7 additional Super Emeralds.
    This will adjust your goal options if necessary."""


class SpecialStageUnlockItemCount(Range):
    """Shuffles a specified number of items into the pool that unlock access to Special Stages.
    A value of 0 will prevent Special Stages from being accessible at all."""
    range_start = 0
    range_end = 14


class SpecialStageSphereChecks(Range):
    """Adds checks to Special Stages that are cleared by collecting certain amounts of blue spheres.
    The value of this option determines every X0% of spheres collected that will become a check.
    For example, a value of 2 would result in every 20% of spheres becoming a check."""
    range_start = 0
    range_end = 10
    default = 2


class SpecialStageRingChecks(Range):
    """Adds checks to Special Stages that are cleared by collecting certain amounts of rings.
    The value of this option determines every X0% of rings collected that will become a check.
    For example, a value of 2 would result in every 20% of rings becoming a check."""
    range_start = 0
    range_end = 10


class SpecialStageSphereChecksLimit(Range):
    """Limit for the threshold of sphere checks available (X0%)."""
    range_start = 0
    range_end = 10
    default = 10


class SpecialStageRingChecksLimit(Range):
    """Limit for the threshold of ring checks available (X0%)."""
    range_start = 0
    range_end = 10
    default = 10


class JunkItemWeights(OptionDict):
    """Weights for junk items to be added to the pool.
    This can include the following items:
    - 10 Rings
    - Extra Life
    - Fire Shield
    - Bubble Shield
    - Electric Shield
    - Speed Shoes
    - Invincibility
    - Spring Trap (Spawns a spring in front of the direction that the player is moving)
    - Missile Trap (Spawns multiple homing missiles that chase the player throughout the level)"""
    default = {
        "10 Rings": 50,
        "Extra Life": 10,
        "Fire Shield": 10,
        "Bubble Shield": 10,
        "Electric Shield": 10,
        "Speed Shoes": 5,
        "Invincibility": 5,
        "Spring Trap": 0,
        "Missile Trap": 0,
    }


class GiantRingRewardCount(Range):
    """The amount of rings that should be received when collecting a giant ring."""
    range_start = 0
    range_end = 100
    default = 50


@dataclass
class Sonic3AIROptions(PerGameCommonOptions):
    StartingCharacter: StartingCharacter
    ZoneUnlockMode: ZoneUnlockMode
    ZonesAllowed: ZonesAllowed
    RandomZoneList: RandomZoneList
    RandomZoneCount: RandomZoneCount
    Goal: Goal
    KnucklesStoryMode: KnucklesStoryMode
    KnucklesGoal: KnucklesGoal
    ShuffleGiantRings: ShuffleGiantRings
    ChaosEmeraldFragments: ChaosEmeraldFragments
    ExtraChaosEmeraldFragments: ExtraChaosEmeraldFragments
    DisableSuperEmeralds: DisableSuperEmeralds
    SpecialStageUnlockItemCount: SpecialStageUnlockItemCount
    SpecialStageSphereChecks: SpecialStageSphereChecks
    SpecialStageRingChecks: SpecialStageRingChecks
    SpecialStageSphereChecksLimit: SpecialStageSphereChecksLimit
    SpecialStageRingChecksLimit: SpecialStageRingChecksLimit
    JunkItemWeights: JunkItemWeights
    GiantRingRewardCount: GiantRingRewardCount
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
