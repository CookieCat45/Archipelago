from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType
from typing import TYPE_CHECKING, List, Dict, Optional
from .Locations import location_table, giant_rings, act_completions
from .Items import create_item
from worlds.generic.Rules import add_rule, set_rule
from .Options import ZoneUnlockMode, KnucklesStoryMode, KnucklesGoal
from .Types import Sonic3AIRLocation, Sonic3AIRItem
from copy import deepcopy

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
    create_char_events(world)
    special_stage_region = None
    knuckles_sanctuary: bool = (world.has_knuckles_goal()
                                and world.options.KnucklesGoal == KnucklesGoal.option_allzones_sanctuary)

    if world.options.SpecialStageUnlockItemCount > 0:
        special_stage_region = create_region(world, "Special Stages")
        sphere_loc_id = 1
        ring_loc_id = 2
        for i in range(world.options.SpecialStageUnlockItemCount):
            special_stage = create_region_and_connect(world, f"Special Stage {i+1}",
                                                      f"-> Special Stage {i+1}", special_stage_region)

            if world.options.SpecialStageSphereChecks.value > 0:
                increment = world.options.SpecialStageSphereChecks.value
                for a in range(world.options.SpecialStageSphereChecksLimit.value):
                    if (a+1) % increment != 0:
                        sphere_loc_id += 2
                        continue

                    loc_name = f"Special Stage {i+1}: {a+1}0% Blue Spheres"
                    location = Sonic3AIRLocation(world.player, loc_name, sphere_loc_id, special_stage)
                    special_stage.locations.append(location)
                    sphere_loc_id += 2

            if world.options.SpecialStageRingChecks.value > 0:
                increment = world.options.SpecialStageRingChecks.value
                for a in range(world.options.SpecialStageRingChecksLimit.value):
                    if (a+1) % increment != 0:
                        ring_loc_id += 2
                        continue

                    loc_name = f"Special Stage {i+1}: {a+1}0% Rings"
                    location = Sonic3AIRLocation(world.player, loc_name, ring_loc_id, special_stage)
                    special_stage.locations.append(location)
                    ring_loc_id += 2

    if world.options.ZoneUnlockMode == ZoneUnlockMode.option_linear:
        world.zones_available = deepcopy(zones)
        for zone in world.zones_available:
            # Purge any zones not in the option list
            if zone not in world.options.ZonesAllowed.value:
                world.zones_available.remove(zone)
    else:
        # shuffle mode
        world.zones_available = world.options.ZonesAllowed.value

        # Shuffle and truncate
        world.random.shuffle(world.zones_available)
        del world.zones_available[world.options.ZoneCount:]
        for zone in world.options.ZonesAllowed.value:
            if zone not in world.zones_available:
                world.options.ZonesAllowed.value.remove(zone)

        if world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg:
            if "Death Egg Zone" not in world.zones_available:
                world.zones_available.append("Death Egg Zone")
            if "Death Egg Zone" not in world.options.ZonesAllowed.value:
                world.options.ZonesAllowed.value.append("Death Egg Zone")

    for zone in world.zones_available:
        if zone not in zones:
            raise Exception(f"Invalid zone '{zone}' in ZonesAllowed option for player "
                            f"'{world.multiworld.get_player_name(world.player)}'")

    for zone in world.zones_available:
        # Create zone regions
        zone_region = create_region_and_connect(world, zone, f"{zone} Entrance", menu)
        if special_stage_region is not None and zone not in no_giantring_zones:
            zone_region.connect(special_stage_region, f"{zone} -> Special Stages")

        # Create act regions
        if zone not in single_act_zones:
            act_1 = create_region_and_connect(world, f"{zone}: Act 1", f"{zone}: Act 1 Entrance", zone_region)
            create_region_and_connect(world, f"{zone}: Act 2", f"{zone}: Act 2 Entrance", act_1)

    # Add Sky Sanctuary for Knuckles if relevant
    if knuckles_sanctuary and "Sky Sanctuary Zone" not in world.zones_available:
        create_region_and_connect(world, "Sky Sanctuary Zone", "Sky Sanctuary Zone Entrance", menu)
        world.zones_available.append("Sky Sanctuary Zone")
        if "Sky Sanctuary Zone" not in world.options.ZonesAllowed.value:
            world.options.ZonesAllowed.value.append("Sky Sanctuary Zone")

    # Add Doomsday if it's relevant
    if world.is_doomsday_goal() and not world.is_knuckles_exclusive() or world.is_doomsday_goal_knuckles():
        create_region_and_connect(world, "Doomsday Zone", "Doomsday Zone Entrance", menu)
        if "Doomsday Zone" not in world.options.ZonesAllowed.value:
            world.options.ZonesAllowed.value.append("Doomsday Zone")

    # Determine starting zone with filters for goal related ones
    for zone in world.zones_available:
        if world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg and zone == "Death Egg Zone":
            continue
        if knuckles_sanctuary and zone == "Sky Sanctuary Zone":
            continue

        world.starting_zone = zone
        break

    if world.options.ZoneUnlockMode == ZoneUnlockMode.option_linear:
        world.multiworld.push_precollected(create_item(world, "Progressive Zone Unlock"))
    else:
        world.multiworld.push_precollected(create_item(world, f"Zone Unlock: {world.starting_zone}"))


def create_region(world: "Sonic3AIRWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)
    for (key, data) in location_table.items():
        if not world.options.ShuffleGiantRings and key in giant_rings:
            continue

        if len(data.char_whitelist) > 0:
            exists = False
            for char in data.char_whitelist:
                if world.does_char_exist(char):
                    exists = True
                    break

            # No character for this location exists, skip
            if not exists:
                continue

        if data.region == name:
            if key in act_completions:
                # add event(s) for act completion
                event = None
                if not world.is_knuckles_exclusive() and (world.is_doomsday_goal() or name != "Doomsday Zone"):
                    act_event_name = f"Act Complete ({name})"
                    event = Sonic3AIRLocation(world.player, act_event_name, None, reg)
                    event.place_locked_item(Sonic3AIRItem(act_event_name, ItemClassification.progression, None, world.player))
                    event.show_in_spoiler = False

                if world.has_knuckles_goal():
                    if event is not None:
                        add_rule(event, lambda state: state.has_any(["Sonic", "Tails"], world.player))
                    if world.is_doomsday_goal_knuckles() or name != "Doomsday Zone":
                        act_event_name = f"Knuckles Act Complete ({name})"
                        event2 = Sonic3AIRLocation(world.player, act_event_name, None, reg)
                        event2.place_locked_item(
                            Sonic3AIRItem(act_event_name, ItemClassification.progression, None, world.player))
                        event2.show_in_spoiler = False
                        add_rule(event2, lambda state: state.has("Knuckles", world.player))
                        reg.locations.append(event2)

                if event is not None:
                    reg.locations.append(event)

            location = Sonic3AIRLocation(world.player, key, data.id, reg)
            reg.locations.append(location)
            if len(data.char_whitelist) > 0:
                world.location_char_whitelists[data.id] = [world.char_name_to_id(n) for n in data.char_whitelist]
                if "Sonic & Tails" not in data.char_whitelist and "Sonic" in data.char_whitelist:
                    world.location_char_whitelists[data.id].append(world.char_name_to_id("Sonic & Tails"))
                if "Knuckles & Tails" not in data.char_whitelist and "Knuckles" in data.char_whitelist:
                    world.location_char_whitelists[data.id].append(world.char_name_to_id("Knuckles & Tails"))

            if len(data.required_items) > 0:
                world.location_required_items[data.id] = data.required_items

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


def create_char_events(world: "Sonic3AIRWorld"):
    menu = world.multiworld.get_region("Menu", world.player)
    if world.does_char_exist("Sonic & Tails"):
        event = Sonic3AIRLocation(world.player, "Sonic & Tails", None, menu)
        event.place_locked_item(Sonic3AIRItem("Sonic & Tails", ItemClassification.progression, None, world.player))
        add_rule(event, lambda state: state.has_all(["Sonic", "Tails"], world.player))
        event.show_in_spoiler = False
        menu.locations.append(event)

    if world.does_char_exist("Knuckles & Tails"):
        event = Sonic3AIRLocation(world.player, "Knuckles & Tails", None, menu)
        event.place_locked_item(Sonic3AIRItem("Knuckles & Tails", ItemClassification.progression, None, world.player))
        add_rule(event, lambda state: state.has_all(["Knuckles", "Tails"], world.player))
        event.show_in_spoiler = False
        menu.locations.append(event)
