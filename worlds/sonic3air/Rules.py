from typing import TYPE_CHECKING, List, Dict, Optional
from BaseClasses import LocationProgressType, MultiWorld, Location, Region, Entrance
from worlds.generic.Rules import add_rule, set_rule
from .Options import ZoneUnlockMode
from .Locations import location_table

if TYPE_CHECKING:
    from . import Sonic3AIRWorld


def init_rules(world: "Sonic3AIRWorld"):
    return

    i = 1
    for zone in world.zones_available:
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
