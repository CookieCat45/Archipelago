from enum import IntEnum, IntFlag, auto
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification

class Sonic3AIRLocation(Location):
    game = "Sonic 3 A.I.R."

class Sonic3AIRItem(Item):
    game = "Sonic 3 A.I.R."

class LocData(NamedTuple):
    id: int = 0
    region: str = ""
    char_whitelist: List = []
    required_items: List = []
    flags: int = 0

class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification

class LogicFlags(IntFlag):
    NONE = 0
    WALL_SMASH = auto()
    WALL_SMASH_STRIP = auto()
