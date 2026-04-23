from enum import IntEnum, IntFlag
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification

class Sonic3AIRLocation(Location):
    game = "Sonic 3 A.I.R."

class Sonic3AIRItem(Item):
    game = "Sonic 3 A.I.R."

class LocData(NamedTuple):
    id: int = 0
    region: str = ""

class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
