from typing import TYPE_CHECKING, List, Dict, Optional
from BaseClasses import LocationProgressType, MultiWorld, Location, Region, Entrance, CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .Options import ZoneUnlockMode, Goal
from .Locations import location_table
from .Regions import single_act_zones

if TYPE_CHECKING:
    from . import Sonic3AIRWorld


def init_rules(world: "Sonic3AIRWorld"):
    i = 1
    for zone in world.zones_available:
        if zone == "Doomsday Zone":
            continue

        entrance = world.multiworld.get_entrance(f"{zone} Entrance", world.player)
        if world.options.ZoneUnlockMode == ZoneUnlockMode.option_linear:
            add_rule(entrance, lambda state, c=i: state.has("Progressive Zone Unlock", world.player, c))
            i += 1
        else:
            if (world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg
             and zone == "Death Egg Zone"):
                pass
            else:
                add_rule(entrance, lambda state, z=zone: state.has(f"Zone Unlock: {z}", world.player))

        if zone not in single_act_zones:
            act_2 = world.multiworld.get_location(f"Act Complete ({zone}: Act 2)", world.player)
            add_rule(act_2, lambda state, z=zone: state.has(f"Act Complete ({z}: Act 1)", world.player))

    for key, data in location_table.items():
        try:
            loc = world.multiworld.get_location(key, world.player)
        except KeyError:
            continue

        if len(data.char_whitelist) > 0:
            add_rule(loc, lambda state, l=data.char_whitelist: state.has_any(l, world.player))
        if len(data.required_items) > 0:
            add_rule(loc, lambda state, l=data.required_items: state.has_all(l, world.player))

    for s in range(world.options.SpecialStageUnlockItemCount):
        entrance = world.multiworld.get_entrance(f"-> Special Stage {s + 1}", world.player)
        add_rule(entrance, lambda state, c=s+1: state.has("Progressive Special Stage Unlock", world.player, c))

    if world.options.Goal == Goal.option_allzones:
        world.multiworld.completion_condition[world.player] = lambda state: all_zones_complete(state, world)
    elif world.is_doomsday_goal():
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Act Complete (Doomsday Zone)", world.player)
        doom_entrance = world.multiworld.get_entrance("Doomsday Zone Entrance", world.player)
        if world.options.Goal == Goal.option_doomsday or world.options.Goal == Goal.option_allzones_doomsday:
            add_rule(doom_entrance, lambda state: state.has("Chaos Emerald", world.player, 7))
        elif world.options.Goal == Goal.option_doomsday_hyper or world.options.Goal == Goal.option_allzones_doomsday_hyper:
            add_rule(doom_entrance, lambda state: state.has("Chaos Emerald", world.player, 14))

        if world.options.Goal == Goal.option_allzones_doomsday or world.options.Goal == Goal.option_allzones_doomsday_hyper:
            add_rule(doom_entrance, lambda state: all_zones_complete(state, world, True))


def all_zones_complete(state: CollectionState, world: "Sonic3AIRWorld", exclude_doomsday=False) -> bool:
    for zone in world.zones_available:
        if exclude_doomsday and zone == "Doomsday Zone":
            continue

        if zone in single_act_zones:
            if not state.has(f"Act Complete ({zone})", world.player):
                return False
        else:
            if not state.has(f"Act Complete ({zone}: Act 2)", world.player):
                return False

    return True
