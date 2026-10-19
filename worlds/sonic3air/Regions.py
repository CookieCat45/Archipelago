from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType
from typing import TYPE_CHECKING, List, Dict, Optional
from .Locations import location_table, giant_rings, act_completions
from .Items import create_item
from worlds.generic.Rules import add_rule, set_rule
from .Options import ZoneUnlockMode, KnucklesStoryMode, KnucklesGoal
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
    "Doomsday Zone"
]

single_act_zones = [
    "Sky Sanctuary Zone",
    "Hidden Palace Zone",
    "Doomsday Zone"
]

def init_regions(world: "Sonic3AIRWorld"):
    menu = create_region(world, "Menu")
    create_char_events(world)
    knuckles_sanctuary: bool = (world.has_knuckles_goal() and world.options.KnucklesGoal == KnucklesGoal.option_allzones_sanctuary)
    if world.options.SpecialStageUnlockItemCount > 0:
        special_stage_region = create_region_and_connect(world, "Special Stages", " -> Special Stages", menu)
        sphere_loc_id = 1
        ring_loc_id = 2
        for i in range(world.options.SpecialStageUnlockItemCount):
            special_stage = create_region_and_connect(world, f"Special Stage {i+1}", f"-> Special Stage {i+1}", special_stage_region)
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

    random_count = world.options.RandomZoneCount.value
    random_list = world.options.RandomZoneList.value
    while random_count > 0 and len(random_list) > 0 and len(world.options.ZonesAllowed.value) < 13:
        random_zone = random_list[world.random.randint(0, len(random_list) - 1)]
        random_list.remove(random_zone)
        if random_zone not in world.options.ZonesAllowed.value:
            if len(world.options.ZonesAllowed.value) == 0:
                world.options.ZonesAllowed.value.append(random_zone)
            else:
                world.options.ZonesAllowed.value.insert(world.random.randint(0, len(world.options.ZonesAllowed.value)-1), random_zone)
            random_count -= 1

    # Add Sky Sanctuary for Knuckles if relevant
    if knuckles_sanctuary and "Sky Sanctuary Zone" not in world.options.ZonesAllowed.value:
        world.options.ZonesAllowed.value.append("Sky Sanctuary Zone")

    if world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg:
        if "Death Egg Zone" in world.options.ZonesAllowed.value:
            world.options.ZonesAllowed.value.remove("Death Egg Zone")
        world.options.ZonesAllowed.value.append("Death Egg Zone")

    # Add Doomsday if it's relevant
    if world.is_doomsday_goal() and not world.is_knuckles_exclusive() or world.is_doomsday_goal_knuckles():
        world.options.ZonesAllowed.value.append("Doomsday Zone")

    for zone in world.options.ZonesAllowed.value:
        if zone not in zones:
            raise Exception(f"Invalid zone '{zone}' in ZonesAllowed option for player '{world.multiworld.get_player_name(world.player)}'")

        zone_region = create_region_and_connect(world, zone, f"{zone} Entrance", menu)
        if zone not in single_act_zones:
            act_1 = create_region_and_connect(world, f"{zone}: Act 1", f"{zone}: Act 1 Entrance", zone_region)
            create_region_and_connect(world, f"{zone}: Act 2", f"{zone}: Act 2 Entrance", act_1)

    # Determine starting zone with filters for goal related ones
    if world.options.ZoneUnlockMode == ZoneUnlockMode.option_linear:
        world.multiworld.push_precollected(create_item(world, "Progressive Zone Unlock"))
    else:
        starting_zone_pool = []
        for zone in world.options.ZonesAllowed.value:
            if zone == "Doomsday Zone":
                continue
            if world.options.ZoneUnlockMode == ZoneUnlockMode.option_shuffled_deathegg and zone == "Death Egg Zone":
                continue
            if knuckles_sanctuary and zone == "Sky Sanctuary Zone":
                continue

            starting_zone_pool.append(zone)

        world.starting_zone = starting_zone_pool[world.random.randint(0, len(starting_zone_pool)-1)]
        world.multiworld.push_precollected(create_item(world, f"Zone Unlock: {world.starting_zone}"))


def create_region(world: "Sonic3AIRWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    # Gather matching locations for this region
    for (key, data) in location_table.items():
        if data.region != name:
            continue

        if not world.options.ShuffleGiantRings and key in giant_rings:
            continue

        if len(data.char_whitelist) > 0:
            exists = False
            for char in data.char_whitelist:
                if world.does_char_exist(char):
                    exists = True
                    break

            # No character that can reach this location exists, skip
            if not exists:
                continue

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
                    # we need Sonic/Tails to complete their version of the act since it's separate now
                    add_rule(event, lambda state: state.has_any(["Sonic", "Tails"], world.player))
                if world.is_doomsday_goal_knuckles() or name != "Doomsday Zone":
                    act_event_name = f"Knuckles Act Complete ({name})"
                    event2 = Sonic3AIRLocation(world.player, act_event_name, None, reg)
                    event2.place_locked_item(Sonic3AIRItem(act_event_name, ItemClassification.progression, None, world.player))
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
