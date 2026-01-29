"""
Death Road to Canada Locations
"""

from typing import Dict, List, Set
from BaseClasses import Location


class DRTCLocation(Location):
    game = "Death Road to Canada"


BASE_ID = 847000

MODE_IDS = {
    "normal": 0, "familiar": 1, "rare": 2, "short": 3, "long": 4,
    "4jerks": 5, "deadlier": 6, "familiarEX": 7, "rareEX": 8,
    "marathon": 9, "kepa": 10, "4jerksEX": 11, "endless": 12,
    "opp": 13, "quickdeath": 14, "infection": 15, "weather": 16,
    "rpg": 17, "scepter": 18, "mutation": 19, "infectionEX": 20,
}

MODE_NAMES = {
    "normal": "Normal", "familiar": "Familiar", "rare": "Rare Characters",
    "short": "Short Trip", "long": "Long Road", "4jerks": "Four Jerks",
    "deadlier": "Deadlier Road", "familiarEX": "Familiar EXTREME",
    "rareEX": "Rare EXTREME", "marathon": "Marathon", "kepa": "K*E*P*A",
    "4jerksEX": "Four Jerks EXTREME", "endless": "Endless", "opp": "O*P*P",
    "quickdeath": "Quick Death", "infection": "Infection",
    "weather": "Severe Weather", "rpg": "RPG Mode", "scepter": "Scepter Mode",
    "mutation": "Mutation", "infectionEX": "Infection EXTREME",
}

MODE_DEFAULT_DAYS = {
    "normal": 15, "familiar": 15, "rare": 15, "short": 9, "long": 25,
    "4jerks": 15, "deadlier": 15, "familiarEX": 15, "rareEX": 15,
    "marathon": 30, "kepa": 15, "4jerksEX": 15, "endless": 30,
    "opp": 15, "quickdeath": 9, "infection": 10, "weather": 15,
    "rpg": 15, "scepter": 12, "mutation": 15, "infectionEX": 7,
}


def get_max_reachable_day(enabled_modes: Set[str]) -> int:
    """Get the maximum day reachable by any enabled mode.
    
    This is used to cap global day locations - we shouldn't create
    Day 16+ locations if no enabled mode can reach them.
    """
    if not enabled_modes:
        return 15  # Default to Normal mode's max
    
    max_day = 0
    for mode in enabled_modes:
        mode_max = MODE_DEFAULT_DAYS.get(mode, 15)
        if mode_max > max_day:
            max_day = mode_max
    
    return max_day


def create_all_location_names() -> Dict[str, int]:
    """Generate all possible location names and IDs."""
    locations = {}
    
    # === GLOBAL DAY START LOCATIONS (legacy) ===
    # Day Start: 1000 + day (1001-1030) - shared across all modes
    for day in range(1, 31):
        loc_id = BASE_ID + 1000 + day
        locations[f"Day {day} Start"] = loc_id
    
    # === GLOBAL DAY CLEAR LOCATIONS ===
    # Day Clear: 1100 + day (1101-1130) - shared across all modes
    for day in range(1, 31):
        loc_id = BASE_ID + 1100 + day
        locations[f"Day {day} Clear"] = loc_id
    
    # === LOCATIONS VISITED MILESTONES ===
    # ID: BASE + 2000 + count (2001-2320) - expanded to 320
    for count in range(1, 321):
        loc_id = BASE_ID + 2000 + count
        locations[f"Locations Visited: {count}"] = loc_id
    
    # === SIEGE MILESTONES ===
    # ID: BASE + 3000 + count (3001-3065) - expanded to 65
    for sieges in range(1, 66):
        loc_id = BASE_ID + 3000 + sieges
        locations[f"Sieges Survived: {sieges}"] = loc_id
    
    # === WEAPON CATEGORY LOCATIONS ===
    # ID: BASE + 4001-4007 (common categories) and 4102-4109 (rare weapons)
    weapon_categories = {
        4001: "Found Handgun",
        4002: "Found Rifle", 
        4003: "Found Shotgun",
        4004: "Found Blade",
        4005: "Found Explosive",
        4006: "Found Heavy Weapon",
        4007: "Found Blunt Weapon",
        4102: "Found Flamethrower",
        4103: "Found Minigun",
        4105: "Found AK-47",
        4106: "Found Sledgehammer",
        4107: "Found Fire Axe",
        4109: "Found Bow",
    }
    for offset, name in weapon_categories.items():
        locations[name] = BASE_ID + offset
    
    # === WEAPON COUNT MILESTONES ===
    # ID: BASE + 4200 + count (4201-4420) - expanded to 220
    for weapons in range(1, 221):
        loc_id = BASE_ID + 4200 + weapons
        locations[f"Weapons Collected: {weapons}"] = loc_id
    
    # === KILL MILESTONES ===
    # 50-1000: ID = BASE + 6000 + kills (6050-6950, 6999 for 1000) - every 50
    for kills in range(50, 1001, 50):
        if kills == 1000:
            loc_id = BASE_ID + 6999
        else:
            loc_id = BASE_ID + 6000 + kills
        locations[f"Zombie Kills: {kills}"] = loc_id
    
    # 1100-11000: ID = BASE + 5000 + (kills/100) (5011-5110) - every 100, expanded to 11000
    for kills in range(1100, 11001, 100):
        loc_id = BASE_ID + 5000 + (kills // 100)
        locations[f"Zombie Kills: {kills}"] = loc_id
    
    # === TOILET MILESTONES ===
    # ID: BASE + 7000 + count (7001-7110) - expanded to 110
    for toilets in range(1, 111):
        loc_id = BASE_ID + 7000 + toilets
        locations[f"Toilets Searched: {toilets}"] = loc_id
    
    # === RECRUIT MILESTONES ===
    # ID: BASE + 8000 + count (8001-8065) - expanded to 65
    for recruits in range(1, 66):
        loc_id = BASE_ID + 8000 + recruits
        locations[f"Characters Recruited: {recruits}"] = loc_id
    
    # === CONTAINER MILESTONES ===
    # ID: BASE + 9000 + count (9001-9880) - expanded to 880
    for containers in range(1, 881):
        loc_id = BASE_ID + 9000 + containers
        locations[f"Containers Looted: {containers}"] = loc_id
    
    # === PER-MODE LOCATIONS ===
    # ID: BASE + 10000 + (mode_id * 100) + offset
    # offset 1-30 = day start, 31-60 = day clear, 99 = victory
    for mode_key, mode_id in MODE_IDS.items():
        mode_display = MODE_NAMES[mode_key]
        max_days = MODE_DEFAULT_DAYS[mode_key]
        
        # Day Start locations (offset 1-30)
        for day in range(1, max_days + 1):
            loc_id = BASE_ID + 10000 + (mode_id * 100) + day
            locations[f"[{mode_display}] Day {day} Start"] = loc_id
        
        # Day Clear locations (offset 31-60, so day 1 clear = 31)
        for day in range(1, max_days + 1):
            loc_id = BASE_ID + 10000 + (mode_id * 100) + 30 + day
            locations[f"[{mode_display}] Day {day} Clear"] = loc_id
        
        # Victory location (offset 99)
        loc_id = BASE_ID + 10000 + (mode_id * 100) + 99
        locations[f"[{mode_display}] Victory"] = loc_id
    
    return locations


location_table: Dict[str, int] = create_all_location_names()


def get_milestone_values(max_val: int, interval: int, start: int = None) -> List[int]:
    """Generate list of milestone values based on max and interval."""
    if max_val <= 0:
        return []
    if start is None:
        start = interval
    return list(range(start, max_val + 1, interval))


def get_kill_milestone_values(max_val: int) -> List[int]:
    """Generate list of kill milestone values with tiered intervals.
    50-1000: every 50 kills
    1100-11000: every 100 kills
    """
    milestones = []
    # 50-1000 at 50 intervals
    for kills in range(50, min(max_val, 1000) + 1, 50):
        milestones.append(kills)
    # 1100-11000 at 100 intervals
    if max_val > 1000:
        for kills in range(1100, max_val + 1, 100):
            milestones.append(kills)
    return milestones


def get_location_count(world) -> int:
    """Get total number of locations for this world based on options."""
    from .rules import get_milestone_caps
    
    count = 0
    options = world.options
    
    # Calculate caps based on enabled modes
    enabled_modes = set(options.enabled_modes.value)
    enabled_modes.update(options.goal_modes.value)
    num_modes = len(enabled_modes)
    caps = get_milestone_caps(num_modes)
    
    # Get the maximum day reachable by any enabled mode
    max_reachable_day = get_max_reachable_day(enabled_modes)
    
    # Global Day Start - capped at max reachable day
    if options.include_global_day_start.value:
        max_days = min(options.max_days_per_mode.value, max_reachable_day)
        count += min(max_days, 30)  # Also cap at 30 days absolute max
    
    # Global Day Clear - capped at max reachable day
    if options.include_global_day_clear.value:
        max_days = min(options.max_days_per_mode.value, max_reachable_day)
        count += min(max_days, 30)  # Also cap at 30 days absolute max
    
    # Locations Visited (capped by mode count)
    loc_max = min(options.location_visited_max.value, caps["location"])
    loc_interval = options.location_visited_interval.value
    count += len(get_milestone_values(loc_max, loc_interval))
    
    # Kills (tiered intervals: 50 for 50-1000, 100 for 1100+) (capped by mode count)
    kill_max = min(options.kill_milestone_max.value, caps["kill"])
    count += len(get_kill_milestone_values(kill_max))
    
    # Containers (capped by mode count)
    container_max = min(options.container_milestone_max.value, caps["container"])
    container_interval = options.container_milestone_interval.value
    count += len(get_milestone_values(container_max, container_interval))
    
    # Toilets (capped by mode count)
    toilet_max = min(options.toilet_milestone_max.value, caps["toilet"])
    toilet_interval = options.toilet_milestone_interval.value
    count += len(get_milestone_values(toilet_max, toilet_interval))
    
    # Sieges (start at 1) (capped by mode count)
    siege_max = min(options.siege_milestone_max.value, caps["siege"])
    siege_interval = options.siege_milestone_interval.value
    count += len(get_milestone_values(siege_max, siege_interval, 1))
    
    # Recruits (start at 1) (capped by mode count)
    recruit_max = min(options.recruit_milestone_max.value, caps["recruit"])
    recruit_interval = options.recruit_milestone_interval.value
    count += len(get_milestone_values(recruit_max, recruit_interval, 1))
    
    # Weapons (capped by mode count)
    weapon_max = min(options.weapon_milestone_max.value, caps["weapon"])
    weapon_interval = options.weapon_milestone_interval.value
    count += len(get_milestone_values(weapon_max, weapon_interval))
    
    # Weapon categories (13 total)
    if options.include_weapon_categories.value:
        count += 13
    
    # Per-mode locations
    max_days = options.max_days_per_mode.value
    include_day_start = options.include_day_start.value
    include_day_clear = options.include_day_clear.value
    
    for mode in enabled_modes:
        mode_days = min(MODE_DEFAULT_DAYS.get(mode, 15), max_days)
        if include_day_start:
            count += mode_days  # Day Start locations
        if include_day_clear:
            count += mode_days  # Day Clear locations
        count += 1  # Victory location
    
    return count
