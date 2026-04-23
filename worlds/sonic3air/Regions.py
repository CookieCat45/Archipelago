from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType
from typing import TYPE_CHECKING, List, Dict, Optional
from .Locations import location_table
from .Items import create_item
from .Types import Sonic3AIRLocation

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

def init_regions(world: "Sonic3AIRWorld"):
    menu = create_region(world, "Menu")
    if world.options.ZoneUnlockMode.value == 0:
        # linear mode
        world.zones_available = zones
        for zone in world.zones_available:
            if zone not in world.options.ZonesAllowed.value:
                world.zones_available.remove(zone)

        del world.zones_available[world.options.ZoneCount:]
    else:
        # shuffle mode
        world.zones_available = world.options.ZonesAllowed.value
        if world.options.ZoneUnlockMode.value == 2 and "Death Egg Zone" in world.zones_available:
            world.zones_available.remove("Death Egg Zone")

        world.random.shuffle(world.zones_available)
        del world.zones_available[world.options.ZoneCount:]
        if world.options.ZoneUnlockMode.value == 2:
            world.zones_available.append("Death Egg Zone")

    for zone in world.zones_available:
        if zone not in zones:
            raise Exception(f"Invalid zone '{zone}' in ZonesAllowed option for player "
                            f"'{world.multiworld.get_player_name(world.player)}'")

    world.random.shuffle(world.zones_available)
    for zone in world.zones_available:
        zone_region = create_region_and_connect(world, zone, f"{zone} Entrance", menu)
        if zone not in single_act_zones:
            create_region_and_connect(world, f"{zone}: Act 1", f"{zone}: Act 1 Entrance", zone_region)
            create_region_and_connect(world, f"{zone}: Act 2", f"{zone}: Act 2 Entrance", zone_region)

    if world.is_doomsday_goal():
        create_region_and_connect(world, "Doomsday Zone", "Doomsday Zone Entrance", menu)

    world.starting_zone = world.zones_available[0]
    if world.options.ZoneUnlockMode.value == 0:
        world.multiworld.push_precollected(create_item(world, "Progressive Zone Unlock"))
    else:
        world.multiworld.push_precollected(create_item(world, f"Zone Unlock: {world.starting_zone}"))


def create_region(world: "Sonic3AIRWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    for (key, data) in location_table.items():
        if data.region == name:
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