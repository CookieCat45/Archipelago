from .Types import LocData, LogicFlags
from typing import Dict, TYPE_CHECKING
from .Options import SpecialStageUnlockItemCount

if TYPE_CHECKING:
    from . import Sonic3AIRWorld

giant_rings = {
    "Angel Island Zone: Act 1 - Giant Ring (First Area, Behind Rock Wall)":
        LocData(466093248, "Angel Island Zone: Act 1", flags=LogicFlags.WALL_SMASH),
    "Angel Island Zone: Act 1 - Giant Ring (Burning Area, Above Red Spring)":
        LocData(37749712, "Angel Island Zone: Act 1", flags=LogicFlags.WALL_SMASH),

    "Angel Island Zone: Act 2 - Giant Ring (Sonic/Tails Route, Near Start, Behind Rock Wall)":
        LocData(431490128, "Angel Island Zone: Act 2", flags=LogicFlags.WALL_SMASH,
                char_whitelist=["Sonic", "Tails", "Knuckles & Tails"]),
    "Angel Island Zone: Act 2 - Giant Ring (Sonic/Tails Route, Upper Path, Right of Waterfall Pond)":
        LocData(918029776, "Angel Island Zone: Act 2", char_whitelist=["Sonic", "Tails", "Knuckles & Tails"]),

    "Hydrocity Zone: Act 1 - Giant Ring (Left of Checkpoint, Below Crumbling Floor)":
        LocData(339740096, "Hydrocity Zone: Act 1"),
    "Hydrocity Zone: Act 1 - Giant Ring (Before Boss, Left of Checkpoint)":
        LocData(826279096, "Hydrocity Zone: Act 1"),

    "Hydrocity Zone: Act 2 - Giant Ring (Left of Snake Blocks, Below Moving Cylinders)":
        LocData(650118720, "Hydrocity Zone: Act 2"),
    "Hydrocity Zone: Act 2 - Giant Ring (Before Boss, Top Right of Twin Moving Cylinders)":
        LocData(935331008, "Hydrocity Zone: Act 2"),

    "Marble Garden Zone: Act 1 - Giant Ring (Top Path, Right of Fake Spikes)":
        LocData(247467196, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Top Path, Left Pointing Sign on Ledge)":
        LocData(113248572, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Top Path, Behind Extra Life, Requires Tails)":
        LocData(222300092, "Marble Garden Zone: Act 1", char_whitelist=["Tails"]),
    "Marble Garden Zone: Act 1 - Giant Ring (Top Path, Behind Breakable Wall)":
        LocData(264243772, "Marble Garden Zone: Act 1", flags=LogicFlags.WALL_SMASH),
    "Marble Garden Zone: Act 1 - Giant Ring (Left of Right Arrow Sign on Ledge)":
        LocData(415238460, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Left of Tar Pit)":
        LocData(356516412, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Left of Spinning Platform Above Steep Slope)":
        LocData(624951868, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Above Red Spring Slope)":
        LocData(448791740, "Marble Garden Zone: Act 1"),

    "Marble Garden Zone: Act 2 - Giant Ring (Top Area, Requires Tails)":
        LocData(138413248, "Marble Garden Zone: Act 2", char_whitelist=["Tails"]),
    "Marble Garden Zone: Act 2 - Giant Ring (Bottom Area, Past Spike Crusher)":
        LocData(356518208, "Marble Garden Zone: Act 2"),
    "Marble Garden Zone: Act 2 - Giant Ring (Left of Crumbling Floor)":
        LocData(641730240, "Marble Garden Zone: Act 2"),

    "Carnival Night Zone: Act 1 - Giant Ring (Knuckles Route, Before Boss)":
        LocData(784337612, "Carnival Night Zone: Act 1", char_whitelist=["Knuckles"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Below Pole Slope)":
        LocData(230688840, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Top Left of Map)":
        LocData(213909836, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Bottom Right of Checkpoint)":
        LocData(457180108, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Right of Double Pillars)":
        LocData(599786056, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Right of Triple Pillars)":
        LocData(767559244, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),

    "Carnival Night Zone: Act 2 - Giant Ring (Near Beginning, Right of Vertical Moving Barrel)":
        LocData(255854668, "Carnival Night Zone: Act 2"),
    "Carnival Night Zone: Act 2 - Giant Ring (Left of Double Monitor Platform)":
        LocData(373294412, "Carnival Night Zone: Act 2"),
    "Carnival Night Zone: Act 2 - Giant Ring (Left of Crusher Barrel Above Tube)":
        LocData(331350604, "Carnival Night Zone: Act 2"),
    "Carnival Night Zone: Act 2 - Giant Ring (Top Right of Intersecting Pole Slopes)":
        LocData(817889996, "Carnival Night Zone: Act 2"),
    "Carnival Night Zone: Act 2 - Giant Ring (Knuckles Route, Near End)":
        LocData(1170213324, "Carnival Night Zone: Act 2", char_whitelist=["Knuckles"]),

    "IceCap Zone: Act 1 - Giant Ring (Right of Breakable Platform Switch)":
        LocData(1119356488, "IceCap Zone: Act 1"),
    "IceCap Zone: Act 1 - Giant Ring (Right of Endless Slide)":
        LocData(1194852808, "IceCap Zone: Act 1"),

    "IceCap Zone: Act 2 - Giant Ring (Knuckles Route, Underwater)":
        LocData(339741512, "IceCap Zone: Act 2", char_whitelist=["Knuckles"]),
    "IceCap Zone: Act 2 - Giant Ring (Underwater, Below Checkpoint)":
        LocData(834669384, "IceCap Zone: Act 2"),
    "IceCap Zone: Act 2 - Giant Ring (Before Boss, Right of Trampoline Rings)":
        LocData(1094714440, "IceCap Zone: Act 2"),

    "Launch Base Zone: Act 1 - Giant Ring (Near Beginning, Below Spinning Cylinder)":
        LocData(46139200, "Launch Base Zone: Act 1"),
    "Launch Base Zone: Act 1 - Giant Ring (Top Left Area)":
        LocData(146800960, "Launch Base Zone: Act 1"),
    "Launch Base Zone: Act 1 - Giant Ring (Below Conveyor Platform Building)":
        LocData(599787585, "Launch Base Zone: Act 1"),

    "Launch Base Zone: Act 2 - Giant Ring (Knuckles Route, Behind Booster)":
        LocData(490736320, "Launch Base Zone: Act 2", char_whitelist=["Knuckles"]),
    "Launch Base Zone: Act 2 - Giant Ring (Sonic/Tails Route, Near Beginning, Underwater)":
        LocData(113247936, "Launch Base Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Launch Base Zone: Act 2 - Giant Ring (Sonic/Tails Route, Left of Spinning Platform Elevator)":
        LocData(163578304, "Launch Base Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Launch Base Zone: Act 2 - Giant Ring (Sonic/Tails Route, Above Booster)":
        LocData(817890496, "Launch Base Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Launch Base Zone: Act 2 - Giant Ring (Sonic/Tails Route, Between Double Spinning Cylinders)":
        LocData(809501248, "Launch Base Zone: Act 2", char_whitelist=["Sonic", "Tails"]),

    "Mushroom Hill Zone: Act 1 - Giant Ring (Knuckles Cave Cutscene)":
        LocData(29361792, "Mushroom Hill Zone: Act 1"),
    "Mushroom Hill Zone: Act 1 - Giant Ring (Knuckles Route, Beginning)":
        LocData(79694336, "Mushroom Hill Zone: Act 1", char_whitelist=["Knuckles"]),
    "Mushroom Hill Zone: Act 1 - Giant Ring (Ledge Right of Swing Rope)":
        LocData(574620736, "Mushroom Hill Zone: Act 1"),
    "Mushroom Hill Zone: Act 1 - Giant Ring (Right of Pulley and Yellow Spring)":
        LocData(759170752, "Mushroom Hill Zone: Act 1"),
    "Mushroom Hill Zone: Act 1 - Giant Ring (Right of Red Spring, Before Boss)":
        LocData(952108864, "Mushroom Hill Zone: Act 1"),

    "Mushroom Hill Zone: Act 2 - Giant Ring (Above Pulley)":
        LocData(272630720, "Mushroom Hill Zone: Act 2"),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Right of Mushroom Weight Trampoline)":
        LocData(482346560, "Mushroom Hill Zone: Act 2"),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Between Brown and Gray Areas)":
        LocData(692060864, "Mushroom Hill Zone: Act 2"),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Behind Rooster, Before Boss)":
        LocData(968885824, "Mushroom Hill Zone: Act 2"),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Knuckles Route, Behind Breakable Blocks)":
        LocData(599787584, "Mushroom Hill Zone: Act 2", flags=LogicFlags.WALL_SMASH, char_whitelist=["Knuckles"]),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Knuckles Route, After Cave Exit)":
        LocData(767560128, "Mushroom Hill Zone: Act 2", flags=LogicFlags.WALL_SMASH, char_whitelist=["Knuckles"]),

    "Flying Battery Zone: Act 1 - Giant Ring (Below Pushable Spikes)":
        LocData(490735040, "Flying Battery Zone: Act 1"),
    "Flying Battery Zone: Act 1 - Giant Ring (Left of 5 Capsules, Before Boss)":
        LocData(616564672, "Flying Battery Zone: Act 1"),

    "Flying Battery Zone: Act 2 - Giant Ring (Left of Rising Pillar Elevator)":
        LocData(406849344, "Flying Battery Zone: Act 2"),
    "Flying Battery Zone: Act 2 - Giant Ring (Top Left of Spinning Cylinder)":
        LocData(633341760, "Flying Battery Zone: Act 2"),

    "Sandopolis Zone: Act 1 - Giant Ring (Right of First Sand Slide)":
        LocData(180357040, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Below Sandfall, After Checkpoint)":
        LocData(423626160, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Below Sand Slide, Above Sand Pit)":
        LocData(473958576, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Upper Area, Requires Tails)":
        LocData(624951600, "Sandopolis Zone: Act 1", char_whitelist=["Tails"]),
    "Sandopolis Zone: Act 1 - Giant Ring (Behind Moving Spike Pillar)":
        LocData(683672880, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Near Protruding Spikes)":
        LocData(931137504, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Near End, Inside Pillar, Knuckles Only)":
        LocData(1042285568, "Sandopolis Zone: Act 1", char_whitelist=["Knuckles"]),

    "Sandopolis Zone: Act 2 - Giant Ring (Knuckles Alternate Route #1)":
        LocData(113247920, "Sandopolis Zone: Act 2", char_whitelist=["Knuckles"]),
    "Sandopolis Zone: Act 2 - Giant Ring (Right of Endless Sand Slide)":
        LocData(356517296, "Sandopolis Zone: Act 2"),
    "Sandopolis Zone: Act 2 - Giant Ring (Knuckles Alternate Route #2)":
        LocData(960497152, "Sandopolis Zone: Act 2", char_whitelist=["Knuckles"]),
    "Sandopolis Zone: Act 2 - Giant Ring (Sonic/Tails Route, Behind Timed Gate)":
        LocData(1346372416, "Sandopolis Zone: Act 2", char_whitelist=["Sonic", "Tails"]),

    "Lava Reef Zone: Act 1 - Giant Ring (Sonic/Tails Route, After Drill Robot, Left of Elevator)":
        LocData(289408700, "Lava Reef Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 1 - Giant Ring (Sonic/Tails Route, Right of Falling Spikes Platform)":
        LocData(381683136, "Lava Reef Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 1 - Giant Ring (Above Checkpoint with Rings, Requires Tails)":
        LocData(440402492, "Lava Reef Zone: Act 1", char_whitelist=["Tails"]),

    "Lava Reef Zone: Act 2 - Giant Ring (Knuckles Route, Left of Spike Platform Conveyor)":
        LocData(339741504, "Lava Reef Zone: Act 2", char_whitelist=["Knuckles"]),
    "Lava Reef Zone: Act 2 - Giant Ring (Sonic/Tails Route, Left of Moving Block, Above Red Spring)":
        LocData(364906176, "Lava Reef Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 2 - Giant Ring (Sonic/Tails Route, Top Left of Spike Platform Conveyor)":
        LocData(465569856, "Lava Reef Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 2 - Giant Ring (Sonic/Tails Route, Right of Twin Moving Blocks, Above Yellow Spring)":
        LocData(557842880, "Lava Reef Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 2 - Giant Ring (Sonic/Tails Route, Right of Spike Pit)":
        LocData(641730112, "Lava Reef Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
}

act_completions = {
    "Angel Island Zone: Act 1 - Complete": LocData(1000, "Angel Island Zone: Act 1"),
    "Angel Island Zone: Act 2 - Complete": LocData(1500, "Angel Island Zone: Act 2"),
    "Hydrocity Zone: Act 1 - Complete": LocData(2000, "Hydrocity Zone: Act 1"),
    "Hydrocity Zone: Act 2 - Complete": LocData(2500, "Hydrocity Zone: Act 2"),
    "Marble Garden Zone: Act 1 - Complete": LocData(3000, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 2 - Complete": LocData(3500, "Marble Garden Zone: Act 2"),
    "Carnival Night Zone: Act 1 - Complete": LocData(4000, "Carnival Night Zone: Act 1"),
    "Carnival Night Zone: Act 2 - Complete": LocData(4500, "Carnival Night Zone: Act 2"),
    "IceCap Zone: Act 1 - Complete": LocData(6000, "IceCap Zone: Act 1"),
    "IceCap Zone: Act 2 - Complete": LocData(6500, "IceCap Zone: Act 2"),
    "Launch Base Zone: Act 1 - Complete": LocData(7000, "Launch Base Zone: Act 1"),
    "Launch Base Zone: Act 2 - Complete": LocData(7500, "Launch Base Zone: Act 2"),
    "Mushroom Hill Zone: Act 1 - Complete": LocData(8000, "Mushroom Hill Zone: Act 1"),
    "Mushroom Hill Zone: Act 2 - Complete": LocData(8500, "Mushroom Hill Zone: Act 2"),
    "Flying Battery Zone: Act 1 - Complete": LocData(5000, "Flying Battery Zone: Act 1"),
    "Flying Battery Zone: Act 2 - Complete": LocData(5500, "Flying Battery Zone: Act 2"),
    "Sandopolis Zone: Act 1 - Complete": LocData(9000, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 2 - Complete": LocData(9500, "Sandopolis Zone: Act 2"),
    "Lava Reef Zone: Act 1 - Complete": LocData(10000, "Lava Reef Zone: Act 1"),
    "Lava Reef Zone: Act 2 - Complete": LocData(10500, "Lava Reef Zone: Act 2"),
    "Hidden Palace Zone: Complete": LocData(22500, "Hidden Palace Zone"),
    "Sky Sanctuary Zone: Complete": LocData(11000, "Sky Sanctuary Zone"),
    "Death Egg Zone: Act 1 - Complete": LocData(12000, "Death Egg Zone: Act 1"),
    "Death Egg Zone: Act 2 - Complete": LocData(12500, "Death Egg Zone: Act 2"),
    "Doomsday Zone: Complete": LocData(13000, "Doomsday Zone"),
}

location_table = {
    **giant_rings,
    **act_completions,
}

def get_total_locations(world: "Sonic3AIRWorld") -> int:
    count = 0
    for reg in world.multiworld.regions:
        if reg.player == world.player:
            for loc in reg.locations:
                if loc.address is not None and not loc.locked:
                    count += 1

    return count


def get_location_names() -> Dict[str, int]:
    names = {name: data.id for name, data in location_table.items()}
    loc_id = 1
    for i in range(SpecialStageUnlockItemCount.range_end):
        for a in range(10):
            blue_name = f"Special Stage {i+1}: {(a+1)*10}% Blue Spheres"
            ring_name = f"Special Stage {i+1}: {(a+1)*10}% Rings"
            names[blue_name] = loc_id
            names[ring_name] = loc_id+1
            loc_id += 2

    return names
