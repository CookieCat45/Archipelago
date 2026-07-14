from .Types import LocData
from typing import Dict
from .Options import SpecialStageSphereChecks, SpecialStageRingChecks, SpecialStageUnlockItemCount

giant_rings = {
    "Angel Island Zone: Act 1 - Giant Ring (First Area, Behind Rock Wall)":
        LocData(4661152, "Angel Island Zone: Act 1", wall_smash=True),
    "Angel Island Zone: Act 1 - Giant Ring (Burning Area, Above Red Spring)":
        LocData(377719, "Angel Island Zone: Act 1", wall_smash=True),

    "Angel Island Zone: Act 2 - Giant Ring (Sonic/Tails Route, Near Start, Behind Rock Wall)":
        LocData(4315110, "Angel Island Zone: Act 2", wall_smash=True, char_whitelist=["Sonic", "Tails"]),
    "Angel Island Zone: Act 2 - Giant Ring (Sonic/Tails Route, Upper Path, Right of Waterfall Pond)":
        LocData(9180502, "Angel Island Zone: Act 2", char_whitelist=["Sonic", "Tails"]),

    "Hydrocity Zone: Act 1 - Giant Ring (Left of Checkpoint, Below Crumbling Floor)":
        LocData(3397594, "Hydrocity Zone: Act 1"),
    "Hydrocity Zone: Act 1 - Giant Ring (Before Boss, Left of Checkpoint)":
        LocData(8262986, "Hydrocity Zone: Act 1"),

    "Hydrocity Zone: Act 2 - Giant Ring (Left of Snake Blocks, Below Moving Cylinders)":
        LocData(6501367, "Hydrocity Zone: Act 2"),
    "Hydrocity Zone: Act 2 - Giant Ring (Before Boss, Top Right of Twin Moving Cylinders)":
        LocData(9353493, "Hydrocity Zone: Act 2"),

    "Marble Garden Zone: Act 1 - Giant Ring (Top Path, Right of Fake Spikes)":
        LocData(2474823, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Top Path, Left Pointing Sign on Ledge)":
        LocData(1132646, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Top Path, Behind Extra Life, Requires Tails)":
        LocData(2223165, "Marble Garden Zone: Act 1", char_whitelist=["Tails"]),
    "Marble Garden Zone: Act 1 - Giant Ring (Top Path, Behind Breakable Wall)":
        LocData(2642595, "Marble Garden Zone: Act 1", wall_smash=True),
    "Marble Garden Zone: Act 1 - Giant Ring (Left of Right Arrow Sign on Ledge)":
        LocData(4152544, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Left of Tar Pit)":
        LocData(3565342, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Left of Spinning Platform Above Steep Slope)":
        LocData(6249696, "Marble Garden Zone: Act 1"),
    "Marble Garden Zone: Act 1 - Giant Ring (Above Red Spring Slope)":
        LocData(4488089, "Marble Garden Zone: Act 1"),

    "Marble Garden Zone: Act 2 - Giant Ring (Top Area, Requires Tails)":
        LocData(1384292, "Marble Garden Zone: Act 2", char_whitelist=["Tails"]),
    "Marble Garden Zone: Act 2 - Giant Ring (Bottom Area, Past Spike Crusher)":
        LocData(3565330, "Marble Garden Zone: Act 2"),
    "Marble Garden Zone: Act 2 - Giant Ring (Left of Crumbling Floor)":
        LocData(6417457, "Marble Garden Zone: Act 2"),

    "Carnival Night Zone: Act 1 - Giant Ring (Knuckles Route, Before Boss)":
        LocData(7843508, "Carnival Night Zone: Act 1", char_whitelist=["Knuckles"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Below Pole Slope)":
        LocData(2307027, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Top Left of Map)":
        LocData(2139255, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Bottom Right of Checkpoint)":
        LocData(4571951, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Right of Double Pillars)":
        LocData(5998014, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Carnival Night Zone: Act 1 - Giant Ring (Sonic/Tails Route, Right of Triple Pillars)":
        LocData(7675736, "Carnival Night Zone: Act 1", char_whitelist=["Sonic", "Tails"]),

    "Carnival Night Zone: Act 2 - Giant Ring (Near Beginning, Right of Vertical Moving Barrel)":
        LocData(2558673, "Carnival Night Zone: Act 2"),
    "Carnival Night Zone: Act 2 - Giant Ring (Left of Double Monitor Platform)":
        LocData(3733078, "Carnival Night Zone: Act 2"),
    "Carnival Night Zone: Act 2 - Giant Ring (Left of Crusher Barrel Above Tube)":
        LocData(3313648, "Carnival Night Zone: Act 2"),
    "Carnival Night Zone: Act 2 - Giant Ring (Top Right of Intersecting Pole Slopes)":
        LocData(8179040, "Carnival Night Zone: Act 2"),
    "Carnival Night Zone: Act 2 - Giant Ring (Knuckles Route, Near End)":
        LocData(11702256, "Carnival Night Zone: Act 2", char_whitelist=["Knuckles"]),

    "IceCap Zone: Act 1 - Giant Ring (Right of Breakable Platform Switch)":
        LocData(11193660, "IceCap Zone: Act 1"),
    "IceCap Zone: Act 1 - Giant Ring (Right of Endless Slide)":
        LocData(11948635, "IceCap Zone: Act 1"),

    "IceCap Zone: Act 2 - Giant Ring (Knuckles Route, Underwater)":
        LocData(3397486, "IceCap Zone: Act 2", char_whitelist=["Knuckles"]),
    "IceCap Zone: Act 2 - Giant Ring (Underwater, Below Checkpoint)":
        LocData(8346764, "IceCap Zone: Act 2"),
    "IceCap Zone: Act 2 - Giant Ring (Before Boss, Right of Trampoline Rings)":
        LocData(10947233, "IceCap Zone: Act 2"),

    "Launch Base Zone: Act 1 - Giant Ring (Near Beginning, Below Spinning Cylinder)":
        LocData(461461, "Launch Base Zone: Act 1"),
    "Launch Base Zone: Act 1 - Giant Ring (Top Left Area)":
        LocData(1468094, "Launch Base Zone: Act 1"),
    "Launch Base Zone: Act 1 - Giant Ring (Below Conveyor Platform Building)":
        LocData(5997942, "Launch Base Zone: Act 1"),

    "Launch Base Zone: Act 2 - Giant Ring (Knuckles Route, Behind Booster)":
        LocData(4907411, "Launch Base Zone: Act 2", char_whitelist=["Knuckles"]),
    "Launch Base Zone: Act 2 - Giant Ring (Sonic/Tails Route, Near Beginning, Underwater)":
        LocData(1132538, "Launch Base Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Launch Base Zone: Act 2 - Giant Ring (Sonic/Tails Route, Left of Spinning Platform Elevator)":
        LocData(1635854, "Launch Base Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Launch Base Zone: Act 2 - Giant Ring (Sonic/Tails Route, Above Booster)":
        LocData(8178968, "Launch Base Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Launch Base Zone: Act 2 - Giant Ring (Sonic/Tails Route, Between Double Spinning Cylinders)":
        LocData(8095082, "Launch Base Zone: Act 2", char_whitelist=["Sonic", "Tails"]),

    "Mushroom Hill Zone: Act 1 - Giant Ring (Knuckles Cave Cutscene)":
        LocData(293665, "Mushroom Hill Zone - Act 1"),
    "Mushroom Hill Zone: Act 1 - Giant Ring (Knuckles Route, Beginning)":
        LocData(796981, "Mushroom Hill Zone - Act 1", char_whitelist=["Knuckles"]),
    "Mushroom Hill Zone: Act 1 - Giant Ring (Ledge Right of Swing Rope)":
        LocData(5746260, "Mushroom Hill Zone - Act 1"),
    "Mushroom Hill Zone: Act 1 - Giant Ring (Right of Pulley and Yellow Spring)":
        LocData(7591754, "Mushroom Hill Zone - Act 1"),
    "Mushroom Hill Zone: Act 1 - Giant Ring (Right of Red Spring, Before Boss)":
        LocData(9521134, "Mushroom Hill Zone - Act 1"),

    "Mushroom Hill Zone: Act 2 - Giant Ring (Above Pulley)":
        LocData(2726349, "Mushroom Hill Zone - Act 2"),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Right of Mushroom Weight Trampoline)":
        LocData(4823501, "Mushroom Hill Zone - Act 2"),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Between Brown and Gray Areas)":
        LocData(6920653, "Mushroom Hill Zone - Act 2"),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Behind Rooster, Before Boss)":
        LocData(9688894, "Mushroom Hill Zone - Act 2"),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Knuckles Route, Behind Breakable Blocks)":
        LocData(5997906, "Mushroom Hill Zone - Act 2", wall_smash=True, char_whitelist=["Knuckles"]),
    "Mushroom Hill Zone: Act 2 - Giant Ring (Knuckles Route, After Cave Exit)":
        LocData(7675628, "Mushroom Hill Zone - Act 2", wall_smash=True, char_whitelist=["Knuckles"]),

    "Flying Battery Zone: Act 1 - Giant Ring (Below Pushable Spikes)":
        LocData(4907471, "Flying Battery Zone: Act 1"),
    "Flying Battery Zone: Act 1 - Giant Ring (Left of 5 Capsules, Before Boss)":
        LocData(6165762, "Flying Battery Zone: Act 1"),

    "Flying Battery Zone: Act 2 - Giant Ring (Left of Rising Pillar Elevator)":
        LocData(4068598, "Flying Battery Zone: Act 2"),
    "Flying Battery Zone: Act 2 - Giant Ring (Top Left of Spinning Cylinder)":
        LocData(6333523, "Flying Battery Zone: Act 2"),

    "Sandopolis Zone: Act 1 - Giant Ring (Right of First Sand Slide)":
        LocData(1803590, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Below Sandfall)":
        LocData(4236287, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Below Sand Slide, Above Sand Pit)":
        LocData(4739603, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Upper Area, Requires Tails)":
        LocData(6249552, "Sandopolis Zone: Act 1", char_whitelist=["Tails"]),
    "Sandopolis Zone: Act 1 - Giant Ring (Behind Moving Spike Pillar)":
        LocData(6836755, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Near Protruding Spikes)":
        LocData(9311394, "Sandopolis Zone: Act 1"),
    "Sandopolis Zone: Act 1 - Giant Ring (Near End, Inside Pillar, Knuckles Only)":
        LocData(10422885, "Sandopolis Zone: Act 1", char_whitelist=["Knuckles"]),

    "Sandopolis Zone: Act 2 - Giant Ring (Knuckles Alternate Route #1)":
        LocData(1132490, "Sandopolis Zone: Act 2", char_whitelist=["Knuckles"]),
    "Sandopolis Zone: Act 2 - Giant Ring (Right of Endless Sand Slide)":
        LocData(3565186, "Sandopolis Zone: Act 2"),
    "Sandopolis Zone: Act 2 - Giant Ring (Knuckles Alternate Route #2)":
        LocData(9604984, "Sandopolis Zone: Act 2", char_whitelist=["Knuckles"]),
    "Sandopolis Zone: Act 2 - Giant Ring (Sonic/Tails Route, Behind Timed Gate)":
        LocData(13463743, "Sandopolis Zone: Act 2", char_whitelist=["Sonic", "Tails"]),

    "Lava Reef Zone: Act 1 - Giant Ring (Sonic/Tails Route, After Drill Robot, Left of Elevator)":
        LocData(2894085, "Lava Reef Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 1 - Giant Ring (Sonic/Tails Route, Right of Falling Spikes Platform)":
        LocData(3816832, "Lava Reef Zone: Act 1", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 1 - Giant Ring (Above Checkpoint with Rings, Requires Tails)":
        LocData(4404035, "Lava Reef Zone: Act 1", char_whitelist=["Tails"]),

    "Lava Reef Zone: Act 2 - Giant Ring (Knuckles Route, Left of Spike Platform Conveyor)":
        LocData(3397390, "Lava Reef Zone: Act 2", char_whitelist=["Knuckles"]),
    "Lava Reef Zone: Act 2 - Giant Ring (Sonic/Tails Route, Left of Moving Block, Above Red Spring)":
        LocData(3649048, "Lava Reef Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 2 - Giant Ring (Sonic/Tails Route, Top Left of Spike Platform Conveyor)":
        LocData(4655681, "Lava Reef Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 2 - Giant Ring (Sonic/Tails Route, Right of Twin Moving Blocks, Above Yellow Spring)":
        LocData(5578428, "Lava Reef Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
    "Lava Reef Zone: Act 2 - Giant Ring (Sonic/Tails Route, Right of Spike Pit)":
        LocData(6417289, "Lava Reef Zone: Act 2", char_whitelist=["Sonic", "Tails"]),
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
