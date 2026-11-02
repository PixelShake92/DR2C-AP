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
    "mutationmodeEX": 21, "horrormode": 22,
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
    "mutationmodeEX": "Mutation EXTREME", "horrormode": "The Horrors",
}

MODE_DEFAULT_DAYS = {
    "normal": 15, "familiar": 15, "rare": 15, "short": 9, "long": 25,
    "4jerks": 15, "deadlier": 15, "familiarEX": 15, "rareEX": 15,
    "marathon": 30, "kepa": 15, "4jerksEX": 15, "endless": 30,
    "opp": 15, "quickdeath": 9, "infection": 10, "weather": 15,
    "rpg": 15, "scepter": 12, "mutation": 15, "infectionEX": 7,
    "mutationmodeEX": 15, "horrormode": 15,
}


def get_max_reachable_day(enabled_modes: Set[str]) -> int:
    if not enabled_modes:
        return 15
    return max((MODE_DEFAULT_DAYS.get(m, 15) for m in enabled_modes), default=15)


def create_all_location_names() -> Dict[str, int]:
    locations = {}

    for day in range(1, 31):
        locations[f"Day {day} Start"] = BASE_ID + 1000 + day
        locations[f"Day {day} Clear"] = BASE_ID + 1100 + day

    for count in range(1, 321):
        locations[f"Locations Visited: {count}"] = BASE_ID + 2000 + count
    for sieges in range(1, 66):
        locations[f"Sieges Survived: {sieges}"] = BASE_ID + 3000 + sieges
    for weapons in range(1, 221):
        locations[f"Weapons Collected: {weapons}"] = BASE_ID + 4200 + weapons
    for toilets in range(1, 111):
        locations[f"Toilets Searched: {toilets}"] = BASE_ID + 7000 + toilets
    for recruits in range(1, 66):
        locations[f"Characters Recruited: {recruits}"] = BASE_ID + 8000 + recruits
    for containers in range(1, 881):
        locations[f"Containers Looted: {containers}"] = BASE_ID + 9000 + containers
    for statups in range(1, 501):
        locations[f"Stat Ups Earned: {statups}"] = BASE_ID + 13000 + statups

    weapon_categories = {
        4001: "Found Handgun", 4002: "Found Rifle", 4003: "Found Shotgun",
        4004: "Found Blade", 4005: "Found Explosive", 4006: "Found Heavy Weapon",
        4007: "Found Blunt Weapon",
        4102: "Found Flamethrower", 4103: "Found Minigun", 4105: "Found AK-47",
        4106: "Found Sledgehammer", 4107: "Found Fire Axe", 4109: "Found Bow",
    }
    for offset, name in weapon_categories.items():
        locations[name] = BASE_ID + offset

    for kills in range(50, 1001, 50):
        loc_id = BASE_ID + 6999 if kills == 1000 else BASE_ID + 6000 + kills
        locations[f"Zombie Kills: {kills}"] = loc_id
    for kills in range(1100, 11001, 100):
        locations[f"Zombie Kills: {kills}"] = BASE_ID + 5000 + (kills // 100)

    for mode_key, mode_id in MODE_IDS.items():
        mode_display = MODE_NAMES[mode_key]
        max_days = MODE_DEFAULT_DAYS[mode_key]
        base = BASE_ID + 10000 + (mode_id * 100)
        for day in range(1, max_days + 1):
            locations[f"[{mode_display}] Day {day} Start"] = base + day
            locations[f"[{mode_display}] Day {day} Clear"] = base + 30 + day
        locations[f"[{mode_display}] Victory"] = base + 99

    return locations


location_table: Dict[str, int] = create_all_location_names()


def get_milestone_values(max_val: int, interval: int, start: int = None) -> List[int]:
    if max_val <= 0:
        return []
    if start is None:
        start = interval
    return list(range(start, max_val + 1, interval))


def get_kill_milestone_values(max_val: int) -> List[int]:
    milestones = list(range(50, min(max_val, 1000) + 1, 50))
    if max_val > 1000:
        milestones += list(range(1100, max_val + 1, 100))
    return milestones


def get_location_count(world) -> int:
    from .rules import get_milestone_caps

    options = world.options
    enabled_modes = set(options.enabled_modes.value)
    enabled_modes.update(options.goal_modes.value)
    caps = get_milestone_caps(len(enabled_modes))
    max_reachable_day = get_max_reachable_day(enabled_modes)

    count = 0

    if options.include_global_day_start.value:
        count += min(options.max_days_per_mode.value, max_reachable_day, 30)
    if options.include_global_day_clear.value:
        count += min(options.max_days_per_mode.value, max_reachable_day, 30)

    count += len(get_milestone_values(
        min(options.location_visited_max.value, caps["location"]),
        options.location_visited_interval.value))
    count += len(get_kill_milestone_values(
        min(options.kill_milestone_max.value, caps["kill"])))
    count += len(get_milestone_values(
        min(options.container_milestone_max.value, caps["container"]),
        options.container_milestone_interval.value))
    count += len(get_milestone_values(
        min(options.toilet_milestone_max.value, caps["toilet"]),
        options.toilet_milestone_interval.value))
    count += len(get_milestone_values(
        min(options.siege_milestone_max.value, caps["siege"]),
        options.siege_milestone_interval.value, 1))
    count += len(get_milestone_values(
        min(options.recruit_milestone_max.value, caps["recruit"]),
        options.recruit_milestone_interval.value, 1))
    count += len(get_milestone_values(
        min(options.weapon_milestone_max.value, caps["weapon"]),
        options.weapon_milestone_interval.value))
    count += len(get_milestone_values(
        min(options.statup_milestone_max.value, caps["statup"]),
        options.statup_milestone_interval.value))

    if options.include_weapon_categories.value:
        count += 13

    max_days = options.max_days_per_mode.value
    for mode in enabled_modes:
        mode_days = min(MODE_DEFAULT_DAYS.get(mode, 15), max_days)
        if options.include_day_start.value:
            count += mode_days
        if options.include_day_clear.value:
            count += mode_days
        count += 1  # victory

    return count
