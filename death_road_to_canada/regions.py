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
    multiworld = world.multiworld
    player = world.player
    options = world.options

    menu_region = Region("Menu", player, multiworld)
    global_region = Region("Global Milestones", player, multiworld)
    multiworld.regions.append(menu_region)
    multiworld.regions.append(global_region)

    menu_to_global = Entrance(player, "Start Game", menu_region)
    menu_region.exits.append(menu_to_global)
    menu_to_global.connect(global_region)

    enabled_modes = set(options.enabled_modes.value)
    enabled_modes.update(options.goal_modes.value)
    caps = get_milestone_caps(len(enabled_modes))
    max_reachable_day = get_max_reachable_day(enabled_modes)

    def add_location(name: str, region: Region) -> None:
        if name in location_table:
            region.locations.append(
                DRTCLocation(player, name, location_table[name], region)
            )

    def add_milestone_pool(prefix: str, values) -> None:
        for n in values:
            add_location(f"{prefix}{n}", global_region)

    if options.include_global_day_start.value:
        max_days = min(options.max_days_per_mode.value, max_reachable_day, 30)
        for day in range(1, max_days + 1):
            add_location(f"Day {day} Start", global_region)
    if options.include_global_day_clear.value:
        max_days = min(options.max_days_per_mode.value, max_reachable_day, 30)
        for day in range(1, max_days + 1):
            add_location(f"Day {day} Clear", global_region)

    add_milestone_pool(
        "Locations Visited: ",
        get_milestone_values(
            min(options.location_visited_max.value, caps["location"]),
            options.location_visited_interval.value,
        ),
    )
    add_milestone_pool(
        "Zombie Kills: ",
        get_kill_milestone_values(
            min(options.kill_milestone_max.value, caps["kill"]),
        ),
    )
    add_milestone_pool(
        "Containers Looted: ",
        get_milestone_values(
            min(options.container_milestone_max.value, caps["container"]),
            options.container_milestone_interval.value,
        ),
    )
    add_milestone_pool(
        "Toilets Searched: ",
        get_milestone_values(
            min(options.toilet_milestone_max.value, caps["toilet"]),
            options.toilet_milestone_interval.value,
        ),
    )
    add_milestone_pool(
        "Sieges Survived: ",
        get_milestone_values(
            min(options.siege_milestone_max.value, caps["siege"]),
            options.siege_milestone_interval.value, 1,
        ),
    )
    add_milestone_pool(
        "Characters Recruited: ",
        get_milestone_values(
            min(options.recruit_milestone_max.value, caps["recruit"]),
            options.recruit_milestone_interval.value, 1,
        ),
    )
    add_milestone_pool(
        "Weapons Collected: ",
        get_milestone_values(
            min(options.weapon_milestone_max.value, caps["weapon"]),
            options.weapon_milestone_interval.value,
        ),
    )
    add_milestone_pool(
        "Stat Ups Earned: ",
        get_milestone_values(
            min(options.statup_milestone_max.value, caps["statup"]),
            options.statup_milestone_interval.value,
        ),
    )

    if options.include_weapon_categories.value:
        for name in (
            "Found Handgun", "Found Rifle", "Found Shotgun", "Found Blade",
            "Found Explosive", "Found Heavy Weapon", "Found Blunt Weapon",
            "Found Flamethrower", "Found Minigun", "Found AK-47",
            "Found Sledgehammer", "Found Fire Axe", "Found Bow",
        ):
            add_location(name, global_region)

    max_days = options.max_days_per_mode.value
    include_day_start = options.include_day_start.value
    include_day_clear = options.include_day_clear.value

    for mode in enabled_modes:
        mode_display = MODE_NAMES.get(mode, mode)
        mode_region = Region(f"{mode_display} Mode", player, multiworld)
        multiworld.regions.append(mode_region)

        entrance = Entrance(player, f"Enter {mode_display}", global_region)
        global_region.exits.append(entrance)
        entrance.connect(mode_region)

        mode_days = min(MODE_DEFAULT_DAYS.get(mode, 15), max_days)
        if include_day_start:
            for day in range(1, mode_days + 1):
                add_location(f"[{mode_display}] Day {day} Start", mode_region)
        if include_day_clear:
            for day in range(1, mode_days + 1):
                add_location(f"[{mode_display}] Day {day} Clear", mode_region)
        add_location(f"[{mode_display}] Victory", mode_region)

    victory_locations = [
        f"[{MODE_NAMES.get(mode, mode)}] Victory"
        for mode in options.goal_modes.value
    ]
    multiworld.completion_condition[player] = (
        lambda state, locs=victory_locations, p=player:
            all(state.can_reach(loc, "Location", p) for loc in locs)
    )
