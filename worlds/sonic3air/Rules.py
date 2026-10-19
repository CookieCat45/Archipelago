from typing import TYPE_CHECKING, List, Dict, Optional
from BaseClasses import LocationProgressType, MultiWorld, Location, Region, Entrance, CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .Options import ZoneUnlockMode, Goal, KnucklesStoryMode, KnucklesGoal
from .Locations import location_table
from .Regions import single_act_zones, zones

if TYPE_CHECKING:
    from . import Sonic3AIRWorld


def init_rules(world: "Sonic3AIRWorld"):
    for key, data in location_table.items():
        try:
            loc = world.multiworld.get_location(key, world.player)
        except KeyError:
            continue

        if len(data.char_whitelist) > 0:
            add_rule(loc, lambda state, l=data.char_whitelist: state.has_any(l, world.player))
        if len(data.required_items) > 0:
            add_rule(loc, lambda state, l=data.required_items: state.has_all(l, world.player))

    i = 1
    prev_zone = ""
    for zone in world.options.ZonesAllowed.value:
        entrance = world.multiworld.get_entrance(f"{zone} Entrance", world.player)
        if world.options.ZoneUnlockMode == ZoneUnlockMode.option_linear:
            add_rule(entrance, lambda state, c=i: state.has("Progressive Zone Unlock", world.player, c))
            if zone != "Doomsday Zone":
                if prev_zone != "":
                    # The previous zone needs to be completed too
                    item_name: str
                    if prev_zone not in single_act_zones:
                        item_name = f"Act Complete ({prev_zone}: Act 2)"
                    else:
                        item_name = f"Act Complete ({prev_zone})"

                    if not world.is_knuckles_exclusive():
                        add_rule(entrance, lambda state, n=item_name: state.has(n, world.player))
                    if world.has_knuckles_goal():
                        if world.options.KnucklesGoal != KnucklesGoal.option_allzones_sanctuary or prev_zone != "Sky Sanctuary Zone":
                            add_rule(entrance, lambda state, n=item_name: state.has(f"Knuckles {n}", world.player))

                prev_zone = zone

            i += 1
        else:
            if world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg and zone == "Death Egg Zone":
                add_rule(entrance, lambda state:
                    all_zones_complete(state, world, True, True) or all_zones_complete(state, world, True, True, True, True))
            elif zone != "Doomsday Zone":
                add_rule(entrance, lambda state, z=zone: state.has(f"Zone Unlock: {z}", world.player))
                if zone == "Sky Sanctuary Zone":
                    if world.has_knuckles_goal() and world.options.KnucklesGoal == KnucklesGoal.option_allzones_sanctuary:
                        add_rule(entrance, lambda state: all_zones_complete(state, world, True, False, True, True), "or")
                        for loc in entrance.connected_region.locations:
                            if loc.address is not None:
                                add_rule(loc, lambda state: state.has_any(["Sonic", "Tails"], world.player))

    for s in range(world.options.SpecialStageUnlockItemCount):
        entrance = world.multiworld.get_entrance(f"-> Special Stage {s + 1}", world.player)
        add_rule(entrance, lambda state, c=s+1: state.has("Progressive Special Stage Unlock", world.player, c))

    doom_entrance = None
    try:
        doom_entrance = world.multiworld.get_entrance("Doomsday Zone Entrance", world.player)
    except KeyError:
        pass

    if not world.is_knuckles_exclusive():
        if world.options.Goal == Goal.option_allzones:
            world.multiworld.completion_condition[world.player] = lambda state: all_zones_complete(state, world, True)
        elif world.is_doomsday_goal():
            world.multiworld.completion_condition[world.player] = lambda state: state.has("Act Complete (Doomsday Zone)", world.player)
            if world.options.Goal == Goal.option_doomsday or world.options.Goal == Goal.option_allzones_doomsday:
                add_rule(doom_entrance, lambda state: state.has("Chaos Emerald", world.player, 7))
            elif world.options.Goal == Goal.option_doomsday_hyper or world.options.Goal == Goal.option_allzones_doomsday_hyper:
                add_rule(doom_entrance, lambda state: state.has("Chaos Emerald", world.player, 14))

            if world.options.Goal == Goal.option_allzones_doomsday or world.options.Goal == Goal.option_allzones_doomsday_hyper:
                add_rule(doom_entrance, lambda state: all_zones_complete(state, world, True))

    if world.has_knuckles_goal():
        old_rule = world.multiworld.completion_condition[world.player]
        if world.options.KnucklesGoal == KnucklesGoal.option_allzones:
            world.multiworld.completion_condition[world.player] = \
                lambda state: old_rule(state) and all_zones_complete(state, world, True, False, True, False)
        elif world.is_doomsday_goal_knuckles():
            world.multiworld.completion_condition[world.player] = \
                lambda state: old_rule(state) and state.has("Knuckles Act Complete (Doomsday Zone)", world.player)

            if (world.options.KnucklesGoal == KnucklesGoal.option_doomsday
             or world.options.KnucklesGoal == KnucklesGoal.option_allzones_doomsday):
                add_rule(doom_entrance, lambda state: state.has("Chaos Emerald", world.player, 7))
            elif (world.options.KnucklesGoal == KnucklesGoal.option_doomsday_hyper
             or world.options.KnucklesGoal == KnucklesGoal.option_allzones_doomsday_hyper):
                add_rule(doom_entrance, lambda state: state.has("Chaos Emerald", world.player, 14))

            if (world.options.KnucklesGoal == KnucklesGoal.option_allzones_doomsday
             or world.options.KnucklesGoal == KnucklesGoal.option_allzones_doomsday_hyper):
                add_rule(doom_entrance, lambda state: all_zones_complete(state, world, True, False, True, True))
        elif world.options.KnucklesGoal == KnucklesGoal.option_allzones_sanctuary:
            world.multiworld.completion_condition[world.player] = \
                lambda state: old_rule(state) and state.has("Knuckles Act Complete (Sky Sanctuary Zone)", world.player)
            loc = world.multiworld.get_location("Knuckles Act Complete (Sky Sanctuary Zone)", world.player)
            add_rule(loc, lambda state: all_zones_complete(state, world, True, False, True, True))

    set_specific_rules(world)

    for zone in world.options.ZonesAllowed.value:
        if zone not in single_act_zones:
            entrance = world.multiworld.get_entrance(f"{zone}: Act 2 Entrance", world.player)
            loc = world.multiworld.get_location(f"{zone}: Act 1 - Complete", world.player)  # also copy the rules from the location
            has_rule = False
            if not world.is_knuckles_exclusive():
                add_rule(entrance, lambda state, z=zone: loc.access_rule(state) and state.has(f"Act Complete ({z}: Act 1)", world.player))
                has_rule = True
            if world.has_knuckles_goal():
                add_rule(entrance, lambda state, z=zone: loc.access_rule(state) and state.has(f"Knuckles Act Complete ({z}: Act 1)", world.player), "or" if has_rule else "and")


def all_zones_complete(state: CollectionState, world: "Sonic3AIRWorld",
                       exclude_doomsday=False, exclude_deathegg=False,
                       knuckles=False, exclude_sanctuary=False) -> bool:
    knuckles_str = "Knuckles "
    if not knuckles:
        knuckles_str = ""

    for zone in world.options.ZonesAllowed.value:
        if exclude_deathegg and zone == "Death Egg Zone":
            continue

        if exclude_doomsday and zone == "Doomsday Zone":
            continue

        if exclude_sanctuary and zone == "Sky Sanctuary Zone":
            continue

        if zone in single_act_zones:
            if not state.has(f"{knuckles_str}Act Complete ({zone})", world.player):
                return False
        else:
            if not state.has(f"{knuckles_str}Act Complete ({zone}: Act 2)", world.player):
                return False

    return True


def set_specific_rules(world: "Sonic3AIRWorld"):
    pass
