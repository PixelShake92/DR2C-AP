"""
Death Road to Canada Options
"""

from dataclasses import dataclass
from typing import Dict, Any
from Options import (
    Toggle, DefaultOnToggle, Choice, Range, OptionSet,
    PerGameCommonOptions, DeathLink
)

# 23 modes total. Day lengths in parens; unmarked = 15.
MODE_LIST = """
  normal          Normal (starts unlocked)
  familiar        Familiar Characters
  rare            Rare Characters
  short           Short Trip (9)
  long            Long Road (25)
  4jerks          Four Jerks
  deadlier        Deadlier Road
  familiarEX      Familiar EXTREME
  rareEX          Rare EXTREME
  marathon        Marathon (30)
  kepa            K*E*P*A
  4jerksEX        Four Jerks EXTREME
  endless         Endless (30+)
  opp             O*P*P
  quickdeath      Quick Death (9)
  infection       Infection (10)
  weather         Severe Weather
  rpg             RPG Mode
  scepter         Scepter Mode (12)
  mutation        Mutation
  infectionEX     Infection EXTREME (7)
  mutationmodeEX  Mutation EXTREME
  horrormode      The Horrors
"""


class GoalModes(OptionSet):
    """
    Modes you need to beat to win. ALL listed modes must be cleared.
    At least one required.

    Valid keys (23):
      normal, familiar, rare, short, long, 4jerks, deadlier, familiarEX,
      rareEX, marathon, kepa, 4jerksEX, endless, opp, quickdeath,
      infection, weather, rpg, scepter, mutation, infectionEX,
      mutationmodeEX, horrormode

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
        "mutation", "infectionEX", "mutationmodeEX", "horrormode"
    })
    default = frozenset({"normal"})


class EnabledModes(OptionSet):
    """
    Modes that get per-mode locations (day start, day clear, victory).
    Goal modes are always enabled regardless. More modes raises most
    milestone caps.

    Valid keys (23):
      normal, familiar, rare, short, long, 4jerks, deadlier, familiarEX,
      rareEX, marathon, kepa, 4jerksEX, endless, opp, quickdeath,
      infection, weather, rpg, scepter, mutation, infectionEX,
      mutationmodeEX, horrormode

    Day lengths:
      7:  infectionEX
      9:  short, quickdeath
      10: infection
      12: scepter
      15: normal, familiar, rare, 4jerks, deadlier, familiarEX, rareEX,
          kepa, 4jerksEX, opp, weather, rpg, mutation, mutationmodeEX,
          horrormode
      25: long
      30: marathon, endless

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
        "mutation", "infectionEX", "mutationmodeEX", "horrormode"
    })
    default = frozenset({"normal"})


class MaxDaysPerMode(Range):
    """
    Day locations generated per enabled mode. Clamped to the mode's own
    length (short/quickdeath=9, infection=10, scepter=12, most=15,
    long=25, marathon/endless=30, infectionEX=7).
    """
    display_name = "Max Days Per Mode"
    range_start = 1
    range_end = 30
    default = 15


class KillMilestoneMax(Range):
    """
    Kill milestone cap. 0 disables.
    Steps: every 50 up to 1000, every 100 past that.

    Scales base 1000 + 500 per extra enabled mode. Hard cap 11000 at 21+ modes:
      1 mode = 1000  |  5 = 3000  |  10 = 5500  |  21-23 = 11000
    """
    display_name = "Kill Milestone Max"
    range_start = 0
    range_end = 11000
    default = 1000


class KillMilestoneInterval(Choice):
    """
    Spacing between kill checks.
    e.g. max 500 at every_50 = 10 checks, every_250 = 2 checks.
    """
    display_name = "Kill Milestone Interval"
    option_every_50 = 50
    option_every_100 = 100
    option_every_250 = 250
    default = 50


class ContainerMilestoneMax(Range):
    """
    Container loot cap. 0 disables.

    Scales base 80 + 40 per extra enabled mode. Hard cap 880 at 21+ modes:
      1 mode = 80  |  5 = 240  |  10 = 440  |  21-23 = 880
    """
    display_name = "Container Milestone Max"
    range_start = 0
    range_end = 880
    default = 300


class ContainerMilestoneInterval(Choice):
    """
    Spacing between container checks.
    e.g. max 100 at every_10 = 10 checks, every_25 = 4 checks.
    """
    display_name = "Container Milestone Interval"
    option_every_1 = 1
    option_every_5 = 5
    option_every_10 = 10
    option_every_25 = 25
    default = 10


class ToiletMilestoneMax(Range):
    """
    Toilet search cap. 0 disables.

    Scales base 10 + 5 per extra enabled mode. Hard cap 110 at 21+ modes:
      1 mode = 10  |  5 = 30  |  10 = 55  |  21-23 = 110
    """
    display_name = "Toilet Milestone Max"
    range_start = 0
    range_end = 110
    default = 25


class ToiletMilestoneInterval(Choice):
    """Spacing between toilet checks."""
    display_name = "Toilet Milestone Interval"
    option_every_1 = 1
    option_every_5 = 5
    default = 5


class SiegeMilestoneMax(Range):
    """
    Siege survival cap. 0 disables.
    Sieges = night zombie waves at your camp.

    Scales base 5 + 3 per extra enabled mode. Hard cap 65 at 21+ modes:
      1 mode = 5  |  5 = 17  |  10 = 32  |  21-23 = 65
    """
    display_name = "Siege Milestone Max"
    range_start = 0
    range_end = 65
    default = 10


class SiegeMilestoneInterval(Choice):
    """Spacing between siege checks."""
    display_name = "Siege Milestone Interval"
    option_every_1 = 1
    option_every_2 = 2
    option_every_5 = 5
    default = 1


class RecruitMilestoneMax(Range):
    """
    Total characters recruited across runs. 0 disables.

    Scales base 5 + 3 per extra enabled mode. Hard cap 65 at 21+ modes:
      1 mode = 5  |  5 = 17  |  10 = 32  |  21-23 = 65
    """
    display_name = "Recruit Milestone Max"
    range_start = 0
    range_end = 65
    default = 10


class RecruitMilestoneInterval(Choice):
    """Spacing between recruit checks."""
    display_name = "Recruit Milestone Interval"
    option_every_1 = 1
    option_every_2 = 2
    option_every_5 = 5
    default = 1


class WeaponMilestoneMax(Range):
    """
    Total weapons picked up across runs. 0 disables.

    Scales base 20 + 10 per extra enabled mode. Hard cap 220 at 21+ modes:
      1 mode = 20  |  5 = 60  |  10 = 110  |  21-23 = 220
    """
    display_name = "Weapon Milestone Max"
    range_start = 0
    range_end = 220
    default = 50


class WeaponMilestoneInterval(Choice):
    """Spacing between weapon checks."""
    display_name = "Weapon Milestone Interval"
    option_every_1 = 1
    option_every_5 = 5
    option_every_10 = 10
    default = 5


class StatUpMilestoneMax(Range):
    """
    Total stat raises across runs from any source: CYOA events, siege
    rewards, RPG orbs, and every dotted stat method including AP stat
    items. 0 disables.

    Team-wide events fire PER CHARACTER - a party of 4 getting +1 FIT
    counts as 4 stat-ups. Lower the max or widen the interval if that's
    too fast.

    Scales base 50 + 15 per extra enabled mode. Hard cap 500 at 31+ modes:
      1 mode = 50  |  5 = 110  |  10 = 185  |  23 = 380  |  max = 500
    """
    display_name = "Stat Up Milestone Max"
    range_start = 0
    range_end = 500
    default = 50


class StatUpMilestoneInterval(Choice):
    """
    Spacing between stat-up checks. Wider intervals keep this check pool
    from completing too fast given team-wide events multiply the count.
    """
    display_name = "Stat Up Milestone Interval"
    option_every_1 = 1
    option_every_2 = 2
    option_every_5 = 5
    option_every_10 = 10
    option_every_25 = 25
    default = 5


class IncludeWeaponCategories(Toggle):
    """
    Add 13 locations that fire on first find of each weapon type:
    Handgun, Rifle, Shotgun, Blade, Explosive, Heavy, Blunt, Flamethrower,
    Minigun, AK-47, Sledgehammer, Fire Axe, Bow.
    """
    display_name = "Include Weapon Categories"


class LocationVisitedMax(Range):
    """
    Map locations explored, cumulative across runs. 0 disables.

    Scales base 20 + 15 per extra enabled mode. Hard cap 320 at 21+ modes:
      1 mode = 20  |  5 = 80  |  10 = 155  |  21-23 = 320
    """
    display_name = "Locations Visited Max"
    range_start = 0
    range_end = 320
    default = 50


class LocationVisitedInterval(Choice):
    """Spacing between locations-visited checks."""
    display_name = "Locations Visited Interval"
    option_every_1 = 1
    option_every_5 = 5
    option_every_10 = 10
    default = 5


class IncludeDayStartLocations(Toggle):
    """
    Per-mode day-start locations: [Normal] Day 1 Start, [Long Road] Day 1 Start etc.
    One per day per enabled mode.
    """
    display_name = "Include Day Start Locations"


class IncludeDayClearLocations(Toggle):
    """
    Per-mode day-clear locations: [Normal] Day 1 Clear, etc.
    Fires when you survive to the next day.
    """
    display_name = "Include Day Clear Locations"


class IncludeGlobalDayStart(Toggle):
    """
    Shared day-start checks across all modes: Day 1 Start, Day 2 Start...
    One check per day number regardless of which mode reached it.
    """
    display_name = "Include Global Day Start"


class IncludeGlobalDayClear(Toggle):
    """
    Shared day-clear checks across all modes. One per day number.
    """
    display_name = "Include Global Day Clear"


class ModeUnlocksInPool(DefaultOnToggle):
    """
    ON (default): all modes except Normal start locked; unlocks drop as
    progression items in the pool.
    OFF: every enabled mode is unlocked at start, no unlock items in pool.
    """
    display_name = "Mode Unlocks in Pool"


class TrapPercentage(Range):
    """
    Share of filler slots replaced with traps (0-100). Traps:
    Food Spoiled, Morale Crisis, Ambush, Gas Leak, Weapon Jam, Thief,
    Injury, Car Damage, Argument, Bandits, Bad Omen, Bad Weather,
    Gear Lost, Food Poison, False Hope, Pandora's Box.
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
    statup_milestone_max: StatUpMilestoneMax
    statup_milestone_interval: StatUpMilestoneInterval
    include_weapon_categories: IncludeWeaponCategories
    mode_unlocks_in_pool: ModeUnlocksInPool
    trap_percentage: TrapPercentage
    death_link: DeathLink