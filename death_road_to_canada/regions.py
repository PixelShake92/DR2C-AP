"""
Death Road to Canada Regions
"""

from BaseClasses import Region, Entrance
from .locations import (
    DRTCLocation, 
    location_table,
    MODE_NAMES,
    MODE_DEFAULT_DAYS,
    get_milestone_values,
    get_kill_milestone_values,
    get_max_reachable_day,
)
from .rules import get_milestone_caps


def create_regions(world) -> None:
    """Create regions and locations for the world."""
    multiworld = world.multiworld
    player = world.player
    options = world.options
    
    # Create Menu region
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)
    
    # Create Global Milestones region
    global_region = Region("Global Milestones", player, multiworld)
    multiworld.regions.append(global_region)
    
    # Connect Menu to Global
    menu_to_global = Entrance(player, "Start Game", menu_region)
    menu_region.exits.append(menu_to_global)
    menu_to_global.connect(global_region)
    
    # === CALCULATE MILESTONE CAPS BASED ON ENABLED MODES ===
    enabled_modes = set(options.enabled_modes.value)
    enabled_modes.update(options.goal_modes.value)
    num_modes = len(enabled_modes)
    caps = get_milestone_caps(num_modes)
    
    # Get max reachable day based on enabled modes
    max_reachable_day = get_max_reachable_day(enabled_modes)
    
    # === GLOBAL DAY START ===
    if options.include_global_day_start.value:
        # Cap at BOTH the option AND the max reachable by enabled modes
        max_days = min(options.max_days_per_mode.value, max_reachable_day, 30)
        for day in range(1, max_days + 1):
            loc_name = f"Day {day} Start"
            if loc_name in location_table:
                loc_id = location_table[loc_name]
                location = DRTCLocation(player, loc_name, loc_id, global_region)
                global_region.locations.append(location)
    
    # === GLOBAL DAY CLEAR ===
    if options.include_global_day_clear.value:
        # Cap at BOTH the option AND the max reachable by enabled modes
        max_days = min(options.max_days_per_mode.value, max_reachable_day, 30)
        for day in range(1, max_days + 1):
            loc_name = f"Day {day} Clear"
            if loc_name in location_table:
                loc_id = location_table[loc_name]
                location = DRTCLocation(player, loc_name, loc_id, global_region)
                global_region.locations.append(location)
    
    # === LOCATIONS VISITED MILESTONES ===
    loc_max = min(options.location_visited_max.value, caps["location"])
    loc_interval = options.location_visited_interval.value
    for count in get_milestone_values(loc_max, loc_interval):
        loc_name = f"Locations Visited: {count}"
        if loc_name in location_table:
            loc_id = location_table[loc_name]
            location = DRTCLocation(player, loc_name, loc_id, global_region)
            global_region.locations.append(location)
    
    # === KILL MILESTONES ===
    kill_max = min(options.kill_milestone_max.value, caps["kill"])
    for kills in get_kill_milestone_values(kill_max):
        loc_name = f"Zombie Kills: {kills}"
        if loc_name in location_table:
            loc_id = location_table[loc_name]
            location = DRTCLocation(player, loc_name, loc_id, global_region)
            global_region.locations.append(location)
    
    # === CONTAINER MILESTONES ===
    container_max = min(options.container_milestone_max.value, caps["container"])
    container_interval = options.container_milestone_interval.value
    for containers in get_milestone_values(container_max, container_interval):
        loc_name = f"Containers Looted: {containers}"
        if loc_name in location_table:
            loc_id = location_table[loc_name]
            location = DRTCLocation(player, loc_name, loc_id, global_region)
            global_region.locations.append(location)
    
    # === TOILET MILESTONES ===
    toilet_max = min(options.toilet_milestone_max.value, caps["toilet"])
    toilet_interval = options.toilet_milestone_interval.value
    for toilets in get_milestone_values(toilet_max, toilet_interval):
        loc_name = f"Toilets Searched: {toilets}"
        if loc_name in location_table:
            loc_id = location_table[loc_name]
            location = DRTCLocation(player, loc_name, loc_id, global_region)
            global_region.locations.append(location)
    
    # === SIEGE MILESTONES (start at 1) ===
    siege_max = min(options.siege_milestone_max.value, caps["siege"])
    siege_interval = options.siege_milestone_interval.value
    for sieges in get_milestone_values(siege_max, siege_interval, 1):
        loc_name = f"Sieges Survived: {sieges}"
        if loc_name in location_table:
            loc_id = location_table[loc_name]
            location = DRTCLocation(player, loc_name, loc_id, global_region)
            global_region.locations.append(location)
    
    # === RECRUIT MILESTONES (start at 1) ===
    recruit_max = min(options.recruit_milestone_max.value, caps["recruit"])
    recruit_interval = options.recruit_milestone_interval.value
    for recruits in get_milestone_values(recruit_max, recruit_interval, 1):
        loc_name = f"Characters Recruited: {recruits}"
        if loc_name in location_table:
            loc_id = location_table[loc_name]
            location = DRTCLocation(player, loc_name, loc_id, global_region)
            global_region.locations.append(location)
    
    # === WEAPON MILESTONES ===
    weapon_max = min(options.weapon_milestone_max.value, caps["weapon"])
    weapon_interval = options.weapon_milestone_interval.value
    for weapons in get_milestone_values(weapon_max, weapon_interval):
        loc_name = f"Weapons Collected: {weapons}"
        if loc_name in location_table:
            loc_id = location_table[loc_name]
            location = DRTCLocation(player, loc_name, loc_id, global_region)
            global_region.locations.append(location)
    
    # === WEAPON CATEGORIES ===
    if options.include_weapon_categories.value:
        weapon_categories = [
            "Found Handgun", "Found Rifle", "Found Shotgun", "Found Blade",
            "Found Explosive", "Found Heavy Weapon", "Found Blunt Weapon",
            "Found Flamethrower", "Found Minigun", "Found AK-47",
            "Found Sledgehammer", "Found Fire Axe", "Found Bow",
        ]
        for loc_name in weapon_categories:
            if loc_name in location_table:
                loc_id = location_table[loc_name]
                location = DRTCLocation(player, loc_name, loc_id, global_region)
                global_region.locations.append(location)
    
    # === PER-MODE REGIONS ===
    max_days = options.max_days_per_mode.value
    include_day_start = options.include_day_start.value
    include_day_clear = options.include_day_clear.value
    
    for mode in enabled_modes:
        mode_display = MODE_NAMES.get(mode, mode)
        region_name = f"{mode_display} Mode"
        
        mode_region = Region(region_name, player, multiworld)
        multiworld.regions.append(mode_region)
        
        entrance = Entrance(player, f"Enter {mode_display}", global_region)
        global_region.exits.append(entrance)
        entrance.connect(mode_region)
        
        mode_days = min(MODE_DEFAULT_DAYS.get(mode, 15), max_days)
        
        # Day Start locations (per-mode)
        if include_day_start:
            for day in range(1, mode_days + 1):
                loc_name = f"[{mode_display}] Day {day} Start"
                if loc_name in location_table:
                    loc_id = location_table[loc_name]
                    location = DRTCLocation(player, loc_name, loc_id, mode_region)
                    mode_region.locations.append(location)
        
        # Day Clear locations (per-mode)
        if include_day_clear:
            for day in range(1, mode_days + 1):
                loc_name = f"[{mode_display}] Day {day} Clear"
                if loc_name in location_table:
                    loc_id = location_table[loc_name]
                    location = DRTCLocation(player, loc_name, loc_id, mode_region)
                    mode_region.locations.append(location)
        
        # Victory location
        loc_name = f"[{mode_display}] Victory"
        if loc_name in location_table:
            loc_id = location_table[loc_name]
            location = DRTCLocation(player, loc_name, loc_id, mode_region)
            mode_region.locations.append(location)
    
    # Set completion condition - ALL of the goal modes' victories required
    goal_modes = options.goal_modes.value
    victory_locations = []
    for mode in goal_modes:
        mode_display = MODE_NAMES.get(mode, mode)
        victory_locations.append(f"[{mode_display}] Victory")
    
    # Player wins if they can reach ALL of the goal victory locations
    multiworld.completion_condition[player] = lambda state, locs=victory_locations, p=player: \
        all(state.can_reach(loc, "Location", p) for loc in locs)
