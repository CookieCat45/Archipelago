from worlds.AutoWorld import PerGameCommonOptions
from dataclasses import dataclass
from Options import (Range, Toggle, DeathLink, Choice, OptionDict, DefaultOnToggle, OptionGroup,
                     OptionList, StartInventoryPool)

class AllowedClasses(OptionList):
    """The classes that will have their relevant items and locations added to the multiworld.
    If you don't want to be forced to play a certain class, you can remove them from this list.
    Removing every class will prevent any class or weapon related locations from being created."""
    default = (
        "Scout",
        "Soldier",
        "Pyro",
        "Demoman",
        "Heavy",
        "Engineer",
        "Medic",
        "Sniper",
        "Spy",
    )

class StartingClassCount(Range):
    """How many class unlocks you will start with."""
    range_start = 1
    range_end = 9
    default = 2

class RandomClassPoolCount(Range):
    """If this option is greater than 0, a random selection of classes from the AllowedClasses option will be added
    to the pool, instead of every class in the list. This option's value determines the amount that are selected."""
    range_start = 0
    range_end = 9
    default = 0

class BannedWeapons(OptionList):
    """List of weapons that will never be added to the item pool or have kill checks requiring them."""
    default = (
        "Flying Guillotine",
        "Bat",
        "Wrap Assassin",
        "Fan O'War",
        "Atomizer",
        "Sun-on-a-Stick",
        "Candy Cane",
        "Boston Basher",
        "Sandman",

        "Mantreads",
        "Righteous Bison",
        "Market Gardener",
        "Escape Plan",
        "Pain Train",

        "Thermal Thruster",
        "Detonator",
        "Homewrecker",
        "Sharpened Volcano Fragment",
        "Reflect",
        "Hot Hand",

        "Chargin' Targe",
        "Splendid Screen",
        "Tide Turner",

        "Gloves of Running Urgently",
        "Eviction Notice",

        "Pomson 6000",
        "Rescue Ranger",
        "Short Circuit",
        "Wrench",
        "Jag",
        "Eureka Effect",
        "Southern Hospitality",

        "Overdose",
        "Amputator",

        "Classic",
        "Cleaner's Carbine",
        "Kukri",
        "Tribalman's Shiv",
        "Shahanshah",

        "L'Etranger",
    )

class ContractPointRequirement(Range):
    """How many objectives, as a percentage of the total, need to be completed to finish your goal"""
    range_start = 10
    range_end = 90
    default = 75

class WeaponsInPool(Range):
    """The number of weapon items that get shuffled into the pool."""
    range_start = 0
    range_end = 100
    default = 25

class EvenWeaponCounts(DefaultOnToggle):
    """Split the amount of weapon unlocks per class in the item pool as evenly as possible."""

class MeleeWeaponRules(Choice):
    """The rules that dictate how melee weapon unlocks should be added to the item pool."""
    option_allow_all = 0
    option_disallow_all = 1
    option_allow_knives_only = 2
    option_allow_swords_only = 3
    option_allow_knives_and_swords_only = 4
    default = 4

class IncludeStockWeapons(Choice):
    """Whether to include Stock weapons in the pool."""
    option_false = 0
    option_true = 1
    option_no_melee = 2
    default = 0

class UnbannedWeapons(OptionList):
    """Weapons in this list will always be allowed in the pool and will take priority over other options that ban
    weapons such as BannedWeapons and MeleeWeaponRules."""
    default = (

    )

class TrapChance(Range):
    """The chance for a junk item in the pool to be replaced by a trap."""
    range_start = 0
    range_end = 100
    default = 0

class ParanoiaTrapWeight(Range):
    """The weight of Paranoia Traps in the trap pool.
    Paranoia Traps will play the Spy's decloaking sound."""
    range_start = 0
    range_end = 100
    default = 40

class KillbindTrapWeight(Range):
    """The weight of Killbind Traps in the trap pool.
    Killbind Traps cause you to die (or explode) immediately."""
    range_start = 0
    range_end = 100
    default = 0

class DisconnectTrapWeight(Range):
    """The weight of Disconnect Traps in the trap pool.
    Disconnect Traps immediately disconnect you from the game server (NOT the Archipelago server)."""
    range_start = 0
    range_end = 100
    default = 0

class SndRestartTrapWeight(Range):
    """The weight of snd_restart traps in the trap pool.
    snd_restart traps force the game to run the snd_restart command, which causes a lag spike."""
    range_start = 0
    range_end = 100
    default = 0

class TauntTrapWeight(Range):
    """The weight of Taunt Traps in the trap pool.
    Taunt traps force you to taunt constantly for 15 seconds."""
    range_start = 0
    range_end = 100
    default = 20

class MeleeOnlyTrapWeight(Range):
    """The weight of Melee-Only Traps in the trap pool.
    Melee-Only Traps force you to use your melee weapon for 30 seconds."""
    range_start = 0
    range_end = 100
    default = 20

class GeneralKillObjectiveCount(Range):
    """The number of general kills performed as each class that will be location checks.
    For example, 5 kills as Scout would be 5 checks at one per kill."""
    range_start = 5
    range_end = 15
    default = 5

class WeaponKillObjectiveCount(Range):
    """The number of kills performed with each unique weapon in the multiworld that will be location checks.
    For example, 3 kills with the Direct Hit would be 3 checks at one per kill.
    Weapons and their respective classes need to be unlocked before being able to send out checks with them,
    but you are still allowed to use any weapon at any time."""
    range_start = 2
    range_end = 10
    default = 3

class WeaponKillCountPlando(OptionDict):
    """Use this to set a specific required kill count for weapons. This cannot be higher than 10."""
    default = {}

class MvmContractBundleTotal(Range):
    """The total number of MvM contract bundle items in the pool. MvM contract bundles will give you
    multiple contracts to complete based on the MvmContractBundleObjectiveCount option value.
    Contract objectives are related to killing robots. If this option's value is 0, MvM will be disabled.

    NOTE: There are certain quirks with how MvM handles console killfeed messages, resulting in the following caveats:
    - Common robot kills will only count if they are killed by you OR if you assist in killing them.
    - Giant kills will count if they are killed by any member of your team."""
    range_start = 0
    range_end = 8
    default = 0

class MvmContractBundleContractAmount(Range):
    """The amount of contracts that an MvM contract bundle will give to you.
    Note that the total available contracts may be capped by the bots available in the whitelists below."""
    range_start = 1
    range_end = 5
    default = 2

class MvmContractCommonKillCount(Range):
    """The kill requirement each common robot contract will have.
    Setting this value high may force you to repeat missions."""
    range_start = 1
    range_end = 20
    default = 4

class MvmContractGiantKillCount(Range):
    """The kill requirement each giant robot contract will have.
    Setting this value high may force you to repeat missions."""
    range_start = 1
    range_end = 10
    default = 2

class MvmBossContractAmount(Range):
    """Adds X Boss contracts to the contract pool. Boss contracts will only have 1 kill requirement.
    Note that this is independent of other contracts.
    Boss contracts will always be added to the contract pool if this option is turned on."""
    range_start = 0
    range_end = 10
    default = 0

class MvmContractBossReward(Range):
    """How many checks are rewarded upon completion of a boss contract."""
    range_start = 1
    range_end = 20
    default = 10

class MvmCommonBotWhitelist(OptionDict):
    """Whitelist of robots permitted to be contract objectives.
    The value next to the name indicates the weight (how likely it is to be chosen when adding contracts).
    Technically, this can work with any robot type as long as its name matches an existing one.
    However, some names are fixed up automatically:

    - All types of banner soldier bots (extended or not) are merged into their respective names
    - Minor League Scout and Hyper League Scout are merged into 'Sandman Scout'
    - Some heavy bots are named 'Heavyweapons' which gets merged into 'Heavy'
    - Scorch Shot and Flare pyros are merged into 'Flare Pyro'
    - Steel Gauntlet Pushers are merged into Steel Gauntlet
    - Razorback Snipers and Sydney Snipers are merged into Sniper"""
    default = {
        "Scout": 50,
        "Soldier": 50,
        "Pyro": 50,
        "Demoman": 50,
        "Heavy": 50,
        "Uber Medic": 50,
        "Quick-Fix Medic": 50,
        "Sandman Scout": 50,
        "Buff Soldier": 50,
        "Concheror Soldier": 50,
        "Flare Pyro": 50,
        "Demoknight": 50,
        "Steel Gauntlet": 50,
        "Heavyweight Champ": 50,
        "Bowman": 50,
    }

class MvmGiantWhitelist(OptionDict):
    """Same as above, but for giants."""
    default = {
        "Super Scout": 50,
        "Giant Soldier": 50,
        "Giant Charged Soldier": 50,
        "Giant Rapid Fire Soldier": 50,
        "Giant Pyro": 50,
        "Giant Demoman": 50,
        "Giant Heavy": 50,
        "Giant Deflector Heavy": 50,
        "Giant Medic": 50,
        "Giant Demoknight": 50,
    }

class MvmBossWhitelist(OptionDict):
    """Same as above, but for bosses."""
    default = {
        "Sergeant Crits": 50,
        "Chief Blast Soldier": 50,
        "Sir Nukesalot": 50,
        "Major Bomber": 50,
        "Captain Punch": 50,
        "Chief Heal-on-Kill Heavy": 50,
    }

class MvmKillCountPlando(OptionDict):
    """Use this to set a specific required kill count for bot types. This cannot be higher than 20."""
    default = {}

class DeathLinkAmnesty(Range):
    """How many deaths that are required to send out a DeathLink."""
    range_start = 1
    range_end = 15
    default = 5

@dataclass
class TF2Options(PerGameCommonOptions):
    AllowedClasses: AllowedClasses
    StartingClassCount: StartingClassCount
    RandomClassPoolCount: RandomClassPoolCount
    BannedWeapons: BannedWeapons
    ContractPointRequirement: ContractPointRequirement
    WeaponsInPool: WeaponsInPool
    GeneralKillObjectiveCount: GeneralKillObjectiveCount
    WeaponKillObjectiveCount: WeaponKillObjectiveCount
    EvenWeaponCounts: EvenWeaponCounts
    MeleeWeaponRules: MeleeWeaponRules
    IncludeStockWeapons: IncludeStockWeapons
    UnbannedWeapons: UnbannedWeapons
    WeaponKillCountPlando: WeaponKillCountPlando
    MvmContractBundleTotal: MvmContractBundleTotal
    MvmContractBundleContractCount: MvmContractBundleContractAmount
    MvmContractCommonKillCount: MvmContractCommonKillCount
    MvmContractGiantKillCount: MvmContractGiantKillCount
    MvmContractBossReward: MvmContractBossReward
    MvmBossContractAmount: MvmBossContractAmount
    MvmCommonBotWhitelist: MvmCommonBotWhitelist
    MvmGiantWhitelist: MvmGiantWhitelist
    MvmBossWhitelist: MvmBossWhitelist
    MvmKillCountPlando: MvmKillCountPlando
    TrapChance: TrapChance
    TauntTrapWeight: TauntTrapWeight
    MeleeOnlyTrapWeight: MeleeOnlyTrapWeight
    SndRestartTrapWeight: SndRestartTrapWeight
    ParanoiaTrapWeight: ParanoiaTrapWeight
    KillbindTrapWeight: KillbindTrapWeight
    DisconnectTrapWeight: DisconnectTrapWeight
    DeathLink: DeathLink
    DeathLinkAmnesty: DeathLinkAmnesty
    start_inventory_from_pool: StartInventoryPool
