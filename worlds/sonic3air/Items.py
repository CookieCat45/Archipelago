from .Types import ItemData, Sonic3AIRItem
from BaseClasses import Location, Item, ItemClassification
from typing import TYPE_CHECKING, List, Dict, Optional

if TYPE_CHECKING:
    from . import Sonic3AIRWorld

items_junk = {
    "10 Rings": ItemData(2020300001, ItemClassification.filler),
    "Extra Life": ItemData(2020300002, ItemClassification.filler),
    "Fire Shield": ItemData(2020300003, ItemClassification.filler),
    "Bubble Shield": ItemData(2020300004, ItemClassification.filler),
    "Electric Shield": ItemData(2020300005, ItemClassification.filler),
    "Invincibility": ItemData(2020300006, ItemClassification.filler),
    "Speed Shoes": ItemData(2020300007, ItemClassification.filler),
}

items_characters = {
    "Sonic": ItemData(2020300008, ItemClassification.progression),
    "Tails": ItemData(2020300009, ItemClassification.progression),
    "Knuckles": ItemData(2020300010, ItemClassification.progression),
}

items_zones = {
    "Zone Unlock: Angel Island Zone": ItemData(2020300011, ItemClassification.progression),
    "Zone Unlock: Hydrocity Zone": ItemData(2020300012, ItemClassification.progression),
    "Zone Unlock: Marble Garden Zone": ItemData(2020300013, ItemClassification.progression),
    "Zone Unlock: Carnival Night Zone": ItemData(2020300014, ItemClassification.progression),
    "Zone Unlock: IceCap Zone": ItemData(2020300015, ItemClassification.progression),
    "Zone Unlock: Launch Base Zone": ItemData(2020300016, ItemClassification.progression),
    "Zone Unlock: Mushroom Hill Zone": ItemData(2020300017, ItemClassification.progression),
    "Zone Unlock: Flying Battery Zone": ItemData(2020300018, ItemClassification.progression),
    "Zone Unlock: Sandopolis Zone": ItemData(2020300019, ItemClassification.progression),
    "Zone Unlock: Lava Reef Zone": ItemData(2020300020, ItemClassification.progression),
    "Zone Unlock: Hidden Palace Zone": ItemData(2020300021, ItemClassification.progression),
    "Zone Unlock: Sky Sanctuary Zone": ItemData(2020300022, ItemClassification.progression),
    "Zone Unlock: Death Egg Zone": ItemData(2020300023, ItemClassification.progression),
    "Progressive Zone Unlock": ItemData(2020300024, ItemClassification.progression),
    "Progressive Special Stage Unlock": ItemData(2020300025, ItemClassification.progression),
}

item_table = {
    **items_junk,
    **items_characters,
    **items_zones,
}

def fill_itempool(world: "Sonic3AIRWorld"):
    item_count = 0
    zone_unlock_mode = world.options.ZoneUnlockMode
    for item, data in item_table.items():
        if data.classification == ItemClassification.filler:
            continue

        if item.startswith("Zone Unlock: "):
            if zone_unlock_mode == zone_unlock_mode.option_linear:
                continue

            zone: str = item[len("Zone Unlock: ")-1:]
            if zone == world.starting_zone:
                continue

            if zone_unlock_mode != zone_unlock_mode.option_shuffled_deathegg and zone == "Death Egg Zone":
                continue

            if zone not in world.zones_available:
                continue

        if zone_unlock_mode != zone_unlock_mode.option_linear and item == "Progressive Zone Unlock":
            continue

        count = get_item_count(world, item)
        item_count += count
        for i in range(count):
            world.multiworld.itempool.append(create_item(world, item))

    for i in range(world.total_locations - item_count):
        # TODO: junk item weights
        world.multiworld.itempool.append(create_item(world, "10 Rings"))


def get_item_count(world: "Sonic3AIRWorld", item: str) -> int:
    if item == "Progressive Zone Unlock":
        return len(world.zones_available)-1
    elif item == "Progressive Special Stage Unlock":
        return world.options.SpecialStageUnlockItemCount.value

    return 1


def create_item(world: "Sonic3AIRWorld", name: str) -> Item:
    data = item_table[name]
    return Sonic3AIRItem(name, data.classification, data.code, world.player)