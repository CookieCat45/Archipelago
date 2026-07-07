from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType
from typing import TYPE_CHECKING, List, Dict, Optional
from .Locations import location_table, giant_rings, act_completions
from .Items import create_item
from .Options import ZoneUnlockMode
from .Types import Sonic3AIRLocation, Sonic3AIRItem

if TYPE_CHECKING:
    from . import Sonic3AIRWorld


zones = [
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
    # "Doomsday Zone"
]

single_act_zones = [
    "Sky Sanctuary Zone",
    "Hidden Palace Zone",
    "Doomsday Zone"
]

no_giantring_zones = [
    "Sky Sanctuary Zone",
    "Hidden Palace Zone",
    "Death Egg Zone",
    "Doomsday Zone"
]

def init_regions(world: "Sonic3AIRWorld"):
    menu = create_region(world, "Menu")
    special_stage_region = None
    if world.options.SpecialStageUnlockItemCount > 0:
        special_stage_region = create_region(world, "Special Stages")
        sphere_loc_id = 1
        ring_loc_id = 2
        sphere_count = 10 // world.options.SpecialStageSphereChecks
        ring_count = 10 // world.options.SpecialStageRingChecks
        for i in range(world.options.SpecialStageUnlockItemCount):
            special_stage = create_region_and_connect(world, f"Special Stage {i+1}",
                                                      f"-> Special Stage {i+1}", special_stage_region)
            if sphere_count > 0:
                increment = 10 // sphere_count
                for a in range(sphere_count):
                    loc_name = f"Special Stage {i+1}: {(a+1)*increment}0% Blue Spheres"
                    location = Sonic3AIRLocation(world.player, loc_name, sphere_loc_id, special_stage)
                    special_stage.locations.append(location)
                    world.total_locations += 1
                    sphere_loc_id += 2

            if ring_count > 0:
                increment = 10 // ring_count
                for a in range(ring_count):
                    loc_name = f"Special Stage {i+1}: {(a+1)*increment}0% Rings"
                    location = Sonic3AIRLocation(world.player, loc_name, ring_loc_id, special_stage)
                    special_stage.locations.append(location)
                    world.total_locations += 1
                    ring_loc_id += 2

    if world.options.ZoneUnlockMode == ZoneUnlockMode.option_linear:
        world.zones_available = zones
        for zone in world.zones_available:
            # Purge any zones not in the option list
            if zone not in world.options.ZonesAllowed.value:
                world.zones_available.remove(zone)

        # Truncate
        del world.zones_available[world.options.ZoneCount:]
    else:
        # shuffle mode
        world.zones_available = world.options.ZonesAllowed.value

        # Always put Death Egg at the end if we're doing shuffled_deathegg
        if (world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg
         and "Death Egg Zone" in world.zones_available):
            world.zones_available.remove("Death Egg Zone")

        # Shuffle and truncate
        world.random.shuffle(world.zones_available)
        del world.zones_available[world.options.ZoneCount:]

        if world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg:
            world.zones_available.append("Death Egg Zone")
            if "Death Egg Zone" not in world.options.ZonesAllowed.value:
                world.options.ZonesAllowed.value.append("Death Egg Zone")

    for zone in world.zones_available:
        if zone not in zones:
            raise Exception(f"Invalid zone '{zone}' in ZonesAllowed option for player "
                            f"'{world.multiworld.get_player_name(world.player)}'")

    world.random.shuffle(world.zones_available)
    for zone in world.zones_available:
        # Create zone regions
        zone_region = create_region_and_connect(world, zone, f"{zone} Entrance", menu)
        if special_stage_region is not None and zone not in no_giantring_zones:
            zone_region.connect(special_stage_region, f"{zone} -> Special Stages")

        # Create act regions
        if zone not in single_act_zones:
            act_1 = create_region_and_connect(world, f"{zone}: Act 1", f"{zone}: Act 1 Entrance", zone_region)
            create_region_and_connect(world, f"{zone}: Act 2", f"{zone}: Act 2 Entrance", act_1)

    # Add Doomsday if it's relevant
    if world.is_doomsday_goal():
        create_region_and_connect(world, "Doomsday Zone", "Doomsday Zone Entrance", menu)
        world.options.ZonesAllowed.value.append("Doomsday Zone")

    world.starting_zone = world.zones_available[0]
    if world.options.ZoneUnlockMode == ZoneUnlockMode.option_linear:
        world.multiworld.push_precollected(create_item(world, "Progressive Zone Unlock"))
    else:
        world.multiworld.push_precollected(create_item(world, f"Zone Unlock: {world.starting_zone}"))


def create_region(world: "Sonic3AIRWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)
    for (key, data) in location_table.items():
        if not world.options.ShuffleGiantRings and key in giant_rings:
            continue

        if data.region == name:
            if key in act_completions:
                # add an event for act completion
                act_event_name = f"Act Complete ({name})"
                event = Sonic3AIRLocation(world.player, act_event_name, None, reg)
                event.place_locked_item(Sonic3AIRItem(act_event_name, ItemClassification.progression, None, world.player))
                event.show_in_spoiler = False
                reg.locations.append(event)

            location = Sonic3AIRLocation(world.player, key, data.id, reg)
            reg.locations.append(location)
            world.total_locations += 1

    world.multiworld.regions.append(reg)
    return reg


def create_region_and_connect(world: "Sonic3AIRWorld",
                              name: str, entrancename: str, connected_region: Region, is_exit: bool = True) -> Region:

    reg: Region = create_region(world, name)
    entrance_region: Region
    exit_region: Region

    if is_exit:
        entrance_region = connected_region
        exit_region = reg
    else:
        entrance_region = reg
        exit_region = connected_region

    entrance_region.connect(exit_region, entrancename)
    return reg
