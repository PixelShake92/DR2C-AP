"""
Death Road to Canada Access Rules
"""

from BaseClasses import CollectionState
from .locations import MODE_NAMES
from .items import MODE_UNLOCK_ITEMS


# Base thresholds with 1 mode unlocked
BASE_TOILET_MAX = 10
BASE_KILL_MAX = 1000
BASE_CONTAINER_MAX = 80
BASE_WEAPON_MAX = 20
BASE_SIEGE_MAX = 5
BASE_RECRUIT_MAX = 5
BASE_LOCATION_MAX = 20

# Per additional mode bonus
TOILET_PER_MODE = 5
KILL_PER_MODE = 500
CONTAINER_PER_MODE = 40
WEAPON_PER_MODE = 10
SIEGE_PER_MODE = 3
RECRUIT_PER_MODE = 3
LOCATION_PER_MODE = 15

# Day limits by mode
MODE_MAX_DAYS = {
    "normal": 15,
    "familiar": 15,
    "rare": 15,
    "short": 9,
    "long": 25,
    "4jerks": 15,
    "deadlier": 15,
    "familiarEX": 15,
    "rareEX": 15,
    "marathon": 30,
    "kepa": 15,
    "4jerksEX": 15,
    "endless": 999,
    "opp": 15,
    "quickdeath": 9,
    "infection": 10,
    "weather": 15,
    "rpg": 15,
    "scepter": 15,
    "mutation": 15,
    "infectionEX": 7,
}


def get_max_for_modes(base: int, per_mode: int, num_modes: int) -> int:
    """Calculate the maximum milestone value achievable with a given number of modes."""
    return base + (per_mode * (num_modes - 1))


def get_milestone_caps(num_modes: int) -> dict:
    """Get all milestone caps for a given number of modes."""
    return {
        "toilet": get_max_for_modes(BASE_TOILET_MAX, TOILET_PER_MODE, num_modes),
        "kill": get_max_for_modes(BASE_KILL_MAX, KILL_PER_MODE, num_modes),
        "container": get_max_for_modes(BASE_CONTAINER_MAX, CONTAINER_PER_MODE, num_modes),
        "weapon": get_max_for_modes(BASE_WEAPON_MAX, WEAPON_PER_MODE, num_modes),
        "siege": get_max_for_modes(BASE_SIEGE_MAX, SIEGE_PER_MODE, num_modes),
        "recruit": get_max_for_modes(BASE_RECRUIT_MAX, RECRUIT_PER_MODE, num_modes),
        "location": get_max_for_modes(BASE_LOCATION_MAX, LOCATION_PER_MODE, num_modes),
    }


def set_rules(world) -> None:
    """Set access rules for locations."""
    multiworld = world.multiworld
    player = world.player
    options = world.options
    
    # Get the set of modes that are actually enabled for this world
    enabled_modes = set(options.enabled_modes.value)
    enabled_modes.update(options.goal_modes.value)
    
    # Calculate max possible modes for this world
    max_possible_modes = len(enabled_modes)
    
    def get_unlocked_mode_count(state: CollectionState) -> int:
        """Count how many enabled modes the player has access to."""
        count = 1  # Normal is always available
        for mode in enabled_modes:
            if mode == "normal":
                continue
            item_name = MODE_UNLOCK_ITEMS.get(mode)
            if item_name and state.has(item_name, player):
                count += 1
        return count
    
    # === MODE ACCESS RULES ===
    if options.mode_unlocks_in_pool:
        for mode in enabled_modes:
            if mode == "normal":
                continue
            
            mode_display = MODE_NAMES.get(mode, mode)
            unlock_item = MODE_UNLOCK_ITEMS.get(mode)
            
            if unlock_item:
                region_name = f"{mode_display} Mode"
                
                for region in multiworld.regions:
                    if region.player == player:
                        for exit in region.exits:
                            if exit.connected_region and exit.connected_region.name == region_name:
                                exit.access_rule = lambda state, item=unlock_item: \
                                    state.has(item, player)
    
    # === MILESTONE LOGIC RULES ===
    # Get caps for this world
    caps = get_milestone_caps(max_possible_modes)
    
    # Helper to check if milestone is accessible based on mode count
    def create_milestone_rule(threshold_base: int, per_mode: int, target: int):
        """Returns a rule function that checks if target milestone is reachable."""
        def rule(state: CollectionState) -> bool:
            modes = get_unlocked_mode_count(state)
            max_accessible = threshold_base + (per_mode * (modes - 1))
            return target <= max_accessible
        return rule
    
    # Helper for day milestone rules
    def create_day_rule(day: int):
        """Returns a rule function for global day milestones."""
        if day > 30:
            # Day 31+ requires Endless
            def rule(state: CollectionState) -> bool:
                return state.has("Mode Unlock: Endless", player)
            return rule
        elif day > 25:
            # Day 26-30 requires Marathon or Endless
            def rule(state: CollectionState) -> bool:
                return (
                    state.has("Mode Unlock: Marathon", player) or
                    state.has("Mode Unlock: Endless", player)
                )
            return rule
        elif day > 15:
            # Day 16-25 requires Long Road, Marathon, or Endless
            def rule(state: CollectionState) -> bool:
                return (
                    state.has("Mode Unlock: Long Road", player) or
                    state.has("Mode Unlock: Marathon", player) or
                    state.has("Mode Unlock: Endless", player)
                )
            return rule
        else:
            # Days 1-15: Always accessible (Normal mode)
            return None
    
    # Apply rules to milestone locations
    for region in multiworld.regions:
        if region.player != player:
            continue
        
        for location in region.locations:
            loc_name = location.name
            
            # Toilet milestones
            if loc_name.startswith("Toilets Searched:"):
                count = int(loc_name.split(": ")[1])
                location.access_rule = create_milestone_rule(
                    BASE_TOILET_MAX, TOILET_PER_MODE, count
                )
            
            # Kill milestones
            elif loc_name.startswith("Zombie Kills:"):
                count = int(loc_name.split(": ")[1])
                location.access_rule = create_milestone_rule(
                    BASE_KILL_MAX, KILL_PER_MODE, count
                )
            
            # Container milestones
            elif loc_name.startswith("Containers Looted:"):
                count = int(loc_name.split(": ")[1])
                location.access_rule = create_milestone_rule(
                    BASE_CONTAINER_MAX, CONTAINER_PER_MODE, count
                )
            
            # Weapon milestones
            elif loc_name.startswith("Weapons Collected:"):
                count = int(loc_name.split(": ")[1])
                location.access_rule = create_milestone_rule(
                    BASE_WEAPON_MAX, WEAPON_PER_MODE, count
                )
            
            # Siege milestones
            elif loc_name.startswith("Sieges Survived:"):
                count = int(loc_name.split(": ")[1])
                location.access_rule = create_milestone_rule(
                    BASE_SIEGE_MAX, SIEGE_PER_MODE, count
                )
            
            # Recruit milestones
            elif loc_name.startswith("Characters Recruited:"):
                count = int(loc_name.split(": ")[1])
                location.access_rule = create_milestone_rule(
                    BASE_RECRUIT_MAX, RECRUIT_PER_MODE, count
                )
            
            # Location visited milestones
            elif loc_name.startswith("Locations Visited:"):
                count = int(loc_name.split(": ")[1])
                location.access_rule = create_milestone_rule(
                    BASE_LOCATION_MAX, LOCATION_PER_MODE, count
                )
            
            # Global day milestones (e.g., "Day 15 Reached", "Day 16 Start")
            elif loc_name.startswith("Day ") and ("Reached" in loc_name or "Start" in loc_name or "Clear" in loc_name):
                # Extract day number from "Day X ..." format
                parts = loc_name.split(" ")
                try:
                    day = int(parts[1])
                    rule = create_day_rule(day)
                    if rule:
                        location.access_rule = rule
                except (ValueError, IndexError):
                    pass  # Skip if day number can't be parsed
