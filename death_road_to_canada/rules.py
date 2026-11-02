from BaseClasses import CollectionState
from .locations import MODE_NAMES
from .items import MODE_UNLOCK_ITEMS


BASE_TOILET_MAX = 10
BASE_KILL_MAX = 1000
BASE_CONTAINER_MAX = 80
BASE_WEAPON_MAX = 20
BASE_SIEGE_MAX = 5
BASE_RECRUIT_MAX = 5
BASE_LOCATION_MAX = 20
BASE_STATUP_MAX = 50

TOILET_PER_MODE = 5
KILL_PER_MODE = 500
CONTAINER_PER_MODE = 40
WEAPON_PER_MODE = 10
SIEGE_PER_MODE = 3
RECRUIT_PER_MODE = 3
LOCATION_PER_MODE = 15
STATUP_PER_MODE = 15

MODE_MAX_DAYS = {
    "normal": 15, "familiar": 15, "rare": 15, "short": 9, "long": 25,
    "4jerks": 15, "deadlier": 15, "familiarEX": 15, "rareEX": 15,
    "marathon": 30, "kepa": 15, "4jerksEX": 15, "endless": 999,
    "opp": 15, "quickdeath": 9, "infection": 10, "weather": 15,
    "rpg": 15, "scepter": 15, "mutation": 15, "infectionEX": 7,
    "mutationmodeEX": 15, "horrormode": 15,
}


def get_max_for_modes(base: int, per_mode: int, num_modes: int) -> int:
    return base + (per_mode * (num_modes - 1))


def get_milestone_caps(num_modes: int) -> dict:
    return {
        "toilet":    min(get_max_for_modes(BASE_TOILET_MAX, TOILET_PER_MODE, num_modes), 110),
        "kill":      min(get_max_for_modes(BASE_KILL_MAX, KILL_PER_MODE, num_modes), 11000),
        "container": min(get_max_for_modes(BASE_CONTAINER_MAX, CONTAINER_PER_MODE, num_modes), 880),
        "weapon":    min(get_max_for_modes(BASE_WEAPON_MAX, WEAPON_PER_MODE, num_modes), 220),
        "siege":     min(get_max_for_modes(BASE_SIEGE_MAX, SIEGE_PER_MODE, num_modes), 65),
        "recruit":   min(get_max_for_modes(BASE_RECRUIT_MAX, RECRUIT_PER_MODE, num_modes), 65),
        "location":  min(get_max_for_modes(BASE_LOCATION_MAX, LOCATION_PER_MODE, num_modes), 320),
        "statup":    min(get_max_for_modes(BASE_STATUP_MAX, STATUP_PER_MODE, num_modes), 500),
    }


def set_rules(world) -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    enabled_modes = set(options.enabled_modes.value)
    enabled_modes.update(options.goal_modes.value)

    def get_unlocked_mode_count(state: CollectionState) -> int:
        count = 1
        for mode in enabled_modes:
            if mode == "normal":
                continue
            item = MODE_UNLOCK_ITEMS.get(mode)
            if item and state.has(item, player):
                count += 1
        return count

    if options.mode_unlocks_in_pool:
        for mode in enabled_modes:
            if mode == "normal":
                continue
            unlock_item = MODE_UNLOCK_ITEMS.get(mode)
            if not unlock_item:
                continue
            region_name = f"{MODE_NAMES.get(mode, mode)} Mode"
            for region in multiworld.regions:
                if region.player != player:
                    continue
                for exit in region.exits:
                    if exit.connected_region and exit.connected_region.name == region_name:
                        exit.access_rule = lambda state, item=unlock_item: \
                            state.has(item, player)

    def milestone_rule(threshold_base: int, per_mode: int, target: int):
        def rule(state: CollectionState) -> bool:
            modes = get_unlocked_mode_count(state)
            return target <= threshold_base + per_mode * (modes - 1)
        return rule

    def day_rule(day: int):
        if day > 30:
            return lambda state: state.has("Mode Unlock: Endless", player)
        if day > 25:
            return lambda state: (
                state.has("Mode Unlock: Marathon", player)
                or state.has("Mode Unlock: Endless", player)
            )
        if day > 15:
            return lambda state: (
                state.has("Mode Unlock: Long Road", player)
                or state.has("Mode Unlock: Marathon", player)
                or state.has("Mode Unlock: Endless", player)
            )
        return None

    MILESTONE_RULES = {
        "Toilets Searched:":      (BASE_TOILET_MAX, TOILET_PER_MODE),
        "Zombie Kills:":          (BASE_KILL_MAX, KILL_PER_MODE),
        "Containers Looted:":     (BASE_CONTAINER_MAX, CONTAINER_PER_MODE),
        "Weapons Collected:":     (BASE_WEAPON_MAX, WEAPON_PER_MODE),
        "Sieges Survived:":       (BASE_SIEGE_MAX, SIEGE_PER_MODE),
        "Characters Recruited:":  (BASE_RECRUIT_MAX, RECRUIT_PER_MODE),
        "Locations Visited:":     (BASE_LOCATION_MAX, LOCATION_PER_MODE),
        "Stat Ups Earned:":       (BASE_STATUP_MAX, STATUP_PER_MODE),
    }

    for region in multiworld.regions:
        if region.player != player:
            continue
        for location in region.locations:
            name = location.name

            for prefix, (base, per_mode) in MILESTONE_RULES.items():
                if name.startswith(prefix):
                    count = int(name.split(": ")[1])
                    location.access_rule = milestone_rule(base, per_mode, count)
                    break
            else:
                if name.startswith("Day ") and ("Start" in name or "Clear" in name or "Reached" in name):
                    try:
                        day = int(name.split(" ")[1])
                        rule = day_rule(day)
                        if rule:
                            location.access_rule = rule
                    except (ValueError, IndexError):
                        pass
