from typing import NamedTuple, Union
from BaseClasses import Item, Tutorial, ItemClassification, MultiWorld
from .Options import Sonic3AIROptions
from .Regions import init_regions
from .Locations import get_location_names
from .Items import fill_itempool, create_item, item_table
from .Rules import init_rules
from ..AutoWorld import World, WebWorld


class Sonic3AIRWorld(World):
    game = "Sonic 3 A.I.R."
    topology_present = False
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = Sonic3AIROptions
    options: Sonic3AIROptions

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.total_locations = 0
        self.zones_available = []
        self.starting_zone = ""

    def create_regions(self):
        init_regions(self)

    def create_items(self):
        fill_itempool(self)

    def set_rules(self):
        init_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def is_doomsday_goal(self) -> bool:
        return self.options.Goal.value > 0