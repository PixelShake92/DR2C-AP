"""
Death Road to Canada Options
"""

from dataclasses import dataclass
from typing import Dict, Any
from Options import (
    Toggle, DefaultOnToggle, Choice, Range, OptionSet,
    PerGameCommonOptions, DeathLink
)

# Mode list for documentation (shown in descriptions)
MODE_LIST = """
Available modes:
  - normal: Normal Mode (default, always unlocked)
  - familiar: Familiar Characters
  - rare: Rare Characters
  - short: Short Trip (9 days)
  - long: Long Road (25 days)
  - 4jerks: Four Jerks
  - deadlier: Deadlier Road
  - familiarEX: Familiar EXTREME
  - rareEX: Rare EXTREME
  - marathon: Marathon (30 days)
  - kepa: K*E*P*A
  - 4jerksEX: Four Jerks EXTREME
  - endless: Endless (unlimited days)
  - opp: O*P*P
  - quickdeath: Quick Death (9 days)
  - infection: Infection (10 days)
  - weather: Severe Weather
  - rpg: RPG Mode
  - scepter: Scepter Mode
  - mutation: Mutation
  - infectionEX: Infection EXTREME (7 days)
"""


class GoalModes(OptionSet):
    """
    Which game mode victories count as completing the game.
    You must reach Canada in ALL of the selected modes to complete your goal.
    At least one mode must be selected.
    
    Available modes:
      normal, familiar, rare, short, long, 4jerks, deadlier,
      familiarEX, rareEX, marathon, kepa, 4jerksEX, endless,
      opp, quickdeath, infection, weather, rpg, scepter,
      mutation, infectionEX
    
    Example:
      goal_modes:
        - normal
        - deadlier
    """
    display_name = "Goal Modes"
    valid_keys = frozenset({
        "normal", "familiar", "rare", "short", "long", "4jerks", "deadlier",
        "familiarEX", "rareEX", "marathon", "kepa", "4jerksEX", "endless",
        "opp", "quickdeath", "infection", "weather", "rpg", "scepter",
        "mutation", "infectionEX"
    })
    default = frozenset({"normal", "deadlier"})


class EnabledModes(OptionSet):
    """
    Which game modes generate per-mode locations (days reached, victory).
    Only modes in this list will have their progression tracked as locations.
    Goal modes are always enabled regardless of this setting.
    More enabled modes = higher milestone caps become accessible.
    
    Available modes:
      normal, familiar, rare, short, long, 4jerks, deadlier,
      familiarEX, rareEX, marathon, kepa, 4jerksEX, endless,
      opp, quickdeath, infection, weather, rpg, scepter,
      mutation, infectionEX
    
    Mode day lengths:
      - 7 days: infectionEX
      - 9 days: short, quickdeath
      - 10 days: infection
      - 12 days: scepter
      - 15 days: normal, familiar, rare, 4jerks, deadlier, familiarEX,
                 rareEX, kepa, 4jerksEX, opp, weather, rpg, mutation
      - 25 days: long
      - 30 days: marathon, endless
    
    Example:
      enabled_modes:
        - normal
        - familiar
        - deadlier
    """
    display_name = "Enabled Modes"
    valid_keys = frozenset({
        "normal", "familiar", "rare", "short", "long", "4jerks", "deadlier",
        "familiarEX", "rareEX", "marathon", "kepa", "4jerksEX", "endless",
        "opp", "quickdeath", "infection", "weather", "rpg", "scepter",
        "mutation", "infectionEX"
    })
    default = frozenset({"normal", "deadlier"})


class MaxDaysPerMode(Range):
    """
    Maximum number of day locations to generate per enabled mode.
    Higher values = more locations but longer games.
    
    Note: This is capped by each mode's actual day length:
      - Short/Quick Death: 9 days max
      - Infection: 10 days max
      - Scepter: 12 days max
      - Most modes: 15 days max
      - Long Road: 25 days max
      - Marathon/Endless: 30 days max
    """
    display_name = "Max Days Per Mode"
    range_start = 1
    range_end = 30
    default = 15


class KillMilestoneMax(Range):
    """
    Maximum kill milestone. Locations are generated at intervals up to this value.
    Set to 0 to disable kill milestones.
    
    Intervals: 50-1000 uses 50-kill steps, 1100+ uses 100-kill steps.
    
    Scaling: Base 1000 + 500 per additional enabled mode.
      1 mode  = 1,000 max    |  5 modes  = 3,000 max
      10 modes = 5,500 max   |  21 modes = 11,000 max
    """
    display_name = "Kill Milestone Max"
    range_start = 0
    range_end = 11000
    default = 1000


class KillMilestoneInterval(Choice):
    """
    Interval between kill milestone locations.
    
    Example with max 500:
      every_50  = 10 locations (50, 100, 150... 500)
      every_100 = 5 locations (100, 200, 300, 400, 500)
      every_250 = 2 locations (250, 500)
    """
    display_name = "Kill Milestone Interval"
    option_every_50 = 50
    option_every_100 = 100
    option_every_250 = 250
    default = 50


class ContainerMilestoneMax(Range):
    """
    Maximum container milestone. Set to 0 to disable.
    
    Scaling: Base 80 + 40 per additional enabled mode.
      1 mode  = 80 max     |  5 modes  = 240 max
      10 modes = 440 max   |  21 modes = 880 max
    """
    display_name = "Container Milestone Max"
    range_start = 0
    range_end = 880
    default = 300


class ContainerMilestoneInterval(Choice):
    """
    Interval between container milestone locations.
    
    Example with max 100:
      every_1  = 100 locations
      every_5  = 20 locations
      every_10 = 10 locations
      every_25 = 4 locations
    """
    display_name = "Container Milestone Interval"
    option_every_1 = 1
    option_every_5 = 5
    option_every_10 = 10
    option_every_25 = 25
    default = 10


class ToiletMilestoneMax(Range):
    """
    Maximum toilet milestone. Set to 0 to disable.
    
    Scaling: Base 10 + 5 per additional enabled mode.
      1 mode  = 10 max    |  5 modes  = 30 max
      10 modes = 55 max   |  21 modes = 110 max
    """
    display_name = "Toilet Milestone Max"
    range_start = 0
    range_end = 110
    default = 25


class ToiletMilestoneInterval(Choice):
    """
    Interval between toilet milestone locations.
    """
    display_name = "Toilet Milestone Interval"
    option_every_1 = 1
    option_every_5 = 5
    default = 5


class SiegeMilestoneMax(Range):
    """
    Maximum siege survival milestone. Set to 0 to disable.
    Sieges are random events where zombies attack your camp at night.
    
    Scaling: Base 5 + 3 per additional enabled mode.
      1 mode  = 5 max     |  5 modes  = 17 max
      10 modes = 32 max   |  21 modes = 65 max
    """
    display_name = "Siege Milestone Max"
    range_start = 0
    range_end = 65
    default = 10


class SiegeMilestoneInterval(Choice):
    """
    Interval between siege milestone locations.
    """
    display_name = "Siege Milestone Interval"
    option_every_1 = 1
    option_every_2 = 2
    option_every_5 = 5
    default = 1


class RecruitMilestoneMax(Range):
    """
    Maximum recruit milestone. Set to 0 to disable.
    Tracks how many characters you've recruited to your party.
    
    Scaling: Base 5 + 3 per additional enabled mode.
      1 mode  = 5 max     |  5 modes  = 17 max
      10 modes = 32 max   |  21 modes = 65 max
    """
    display_name = "Recruit Milestone Max"
    range_start = 0
    range_end = 65
    default = 10


class RecruitMilestoneInterval(Choice):
    """
    Interval between recruit milestone locations.
    """
    display_name = "Recruit Milestone Interval"
    option_every_1 = 1
    option_every_2 = 2
    option_every_5 = 5
    default = 1


class WeaponMilestoneMax(Range):
    """
    Maximum weapon collection milestone. Set to 0 to disable.
    Tracks total weapons picked up (cumulative across runs).
    
    Scaling: Base 20 + 10 per additional enabled mode.
      1 mode  = 20 max    |  5 modes  = 60 max
      10 modes = 110 max  |  21 modes = 220 max
    """
    display_name = "Weapon Milestone Max"
    range_start = 0
    range_end = 220
    default = 50


class WeaponMilestoneInterval(Choice):
    """
    Interval between weapon milestone locations.
    """
    display_name = "Weapon Milestone Interval"
    option_every_1 = 1
    option_every_5 = 5
    option_every_10 = 10
    default = 5


class IncludeWeaponCategories(Toggle):
    """
    Include weapon category discovery locations.
    These trigger when you find your first weapon of each type.
    
    Categories (13 total):
      Found Handgun, Found Rifle, Found Shotgun, Found Blade,
      Found Explosive, Found Heavy Weapon, Found Blunt Weapon,
      Found Flamethrower, Found Minigun, Found AK-47,
      Found Sledgehammer, Found Fire Axe, Found Bow
    """
    display_name = "Include Weapon Categories"


class LocationVisitedMax(Range):
    """
    Maximum locations visited milestone. Set to 0 to disable.
    Tracks how many map locations you've explored.
    
    Scaling: Base 20 + 15 per additional enabled mode.
      1 mode  = 20 max    |  5 modes  = 80 max
      10 modes = 155 max  |  21 modes = 320 max
    """
    display_name = "Locations Visited Max"
    range_start = 0
    range_end = 320
    default = 50


class LocationVisitedInterval(Choice):
    """
    Interval between locations visited milestone locations.
    """
    display_name = "Locations Visited Interval"
    option_every_1 = 1
    option_every_5 = 5
    option_every_10 = 10
    default = 5


class IncludeDayStartLocations(Toggle):
    """
    Include per-mode Day Start locations.
    Creates a location for starting each day in each enabled mode.
    
    Example with normal and deadlier enabled:
      [Normal] Day 1 Start, [Normal] Day 2 Start, ...
      [Deadlier Road] Day 1 Start, [Deadlier Road] Day 2 Start, ...
    """
    display_name = "Include Day Start Locations"


class IncludeDayClearLocations(Toggle):
    """
    Include per-mode Day Clear locations.
    Creates a location for completing/surviving each day in each enabled mode.
    
    Example with normal and deadlier enabled:
      [Normal] Day 1 Clear, [Normal] Day 2 Clear, ...
      [Deadlier Road] Day 1 Clear, [Deadlier Road] Day 2 Clear, ...
    """
    display_name = "Include Day Clear Locations"


class IncludeGlobalDayStart(Toggle):
    """
    Include global Day Start locations (shared across all modes).
    These trigger when you start a new day in ANY mode.
    
    Example: Day 1 Start, Day 2 Start, etc.
    
    Note: Only one check per day number, regardless of mode.
    """
    display_name = "Include Global Day Start"


class IncludeGlobalDayClear(Toggle):
    """
    Include global Day Clear locations (shared across all modes).
    These trigger when you complete a day in ANY mode.
    
    Example: Day 1 Clear, Day 2 Clear, etc.
    
    Note: Only one check per day number, regardless of mode.
    """
    display_name = "Include Global Day Clear"


class ModeUnlocksInPool(DefaultOnToggle):
    """
    Include game mode unlocks as items in the randomizer pool.
    
    When ON (default):
      - All modes except Normal start LOCKED
      - You must receive mode unlock items to play other modes
      - Adds progression items to the pool
    
    When OFF:
      - All enabled modes are available from the start
      - No mode unlock items in the pool
    """
    display_name = "Mode Unlocks in Pool"


class TrapPercentage(Range):
    """
    Percentage of filler items that become traps.
    
    Traps include:
      Food Spoiled, Morale Crisis, Ambush, Gas Leak, Weapon Jam,
      Thief, Injury, Car Damage, Argument, Bandits, Bad Omen,
      Bad Weather, Gear Lost, Food Poison, False Hope, Pandora's Box
    
    0 = No traps, 100 = All filler becomes traps
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


@dataclass
class DRTCOptions(PerGameCommonOptions):
    goal_modes: GoalModes
    enabled_modes: EnabledModes
    max_days_per_mode: MaxDaysPerMode
    include_day_start: IncludeDayStartLocations
    include_day_clear: IncludeDayClearLocations
    include_global_day_start: IncludeGlobalDayStart
    include_global_day_clear: IncludeGlobalDayClear
    location_visited_max: LocationVisitedMax
    location_visited_interval: LocationVisitedInterval
    kill_milestone_max: KillMilestoneMax
    kill_milestone_interval: KillMilestoneInterval
    container_milestone_max: ContainerMilestoneMax
    container_milestone_interval: ContainerMilestoneInterval
    toilet_milestone_max: ToiletMilestoneMax
    toilet_milestone_interval: ToiletMilestoneInterval
    siege_milestone_max: SiegeMilestoneMax
    siege_milestone_interval: SiegeMilestoneInterval
    recruit_milestone_max: RecruitMilestoneMax
    recruit_milestone_interval: RecruitMilestoneInterval
    weapon_milestone_max: WeaponMilestoneMax
    weapon_milestone_interval: WeaponMilestoneInterval
    include_weapon_categories: IncludeWeaponCategories
    mode_unlocks_in_pool: ModeUnlocksInPool
    trap_percentage: TrapPercentage
    death_link: DeathLink