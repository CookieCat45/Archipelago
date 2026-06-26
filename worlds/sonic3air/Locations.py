from .Types import LocData
from typing import Dict
from .Options import SpecialStageSphereChecks, SpecialStageRingChecks

location_table = {
    "Angel Island Zone: Act 1 - Giant Ring (First Area, Behind Rock Wall)":
        LocData(4723946, "Angel Island Zone: Act 1"),
    "Angel Island Zone: Act 1 - Giant Ring (Burning Area, Above Red Spring)":
        LocData(440513, "Angel Island Zone: Act 1"),

    "Angel Island Zone: Act 2 - Giant Ring (Near Start, Behind Rock Wall)":
        LocData(7785820, "Angel Island Zone: Act 2"),
    "Angel Island Zone: Act 2 - Giant Ring (Upper Path, Right of Waterfall Pond)":
        LocData(12651212, "Angel Island Zone: Act 2")
}


def get_location_names() -> Dict[str, int]:
    names = {name: data.id for name, data in location_table.items()}
    loc_id = 1
    for i in range(14):
        for a in range(10):
            blue_name = f"Special Stage {i+1}: {(a+1)*10}% Blue Spheres"
            ring_name = f"Special Stage {i+1}: {(a+1)*10}% Rings"
            names[blue_name] = loc_id
            names[ring_name] = loc_id+1
            loc_id += 2

    return names
