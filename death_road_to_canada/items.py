"""
Death Road to Canada Items

All items that can be sent to players in the Death Road to Canada APWorld.
Item IDs match the ap-item-XXX handlers in archipelago.df
"""

from typing import Dict, List
from BaseClasses import Item, ItemClassification
import random


class DRTCItem(Item):
    game = "Death Road to Canada"


BASE_ID = 847000

# =============================================================================
# ITEM DEFINITIONS
# =============================================================================
# Item codes correspond to ap-item-XXX in archipelago.df
# Format: {"id": BASE_ID + code, "classification": ItemClassification.X}

item_table: Dict[str, Dict] = {
    # =========================================================================
    # RESOURCES (100s)
    # =========================================================================
    "Food Pack (+5)": {"id": BASE_ID + 100, "classification": ItemClassification.filler},
    "Food Crate (+15)": {"id": BASE_ID + 101, "classification": ItemClassification.useful},
    "Gas Can (+50)": {"id": BASE_ID + 102, "classification": ItemClassification.useful},
    "Ammo Box (+20)": {"id": BASE_ID + 103, "classification": ItemClassification.useful},
    "Medical Kit (+5)": {"id": BASE_ID + 104, "classification": ItemClassification.useful},
    
    # =========================================================================
    # STAT TRAINING (110s)
    # =========================================================================
    "Shooting Training": {"id": BASE_ID + 110, "classification": ItemClassification.useful},
    "Strength Training": {"id": BASE_ID + 111, "classification": ItemClassification.useful},
    "Fitness Training": {"id": BASE_ID + 112, "classification": ItemClassification.useful},
    "Medical Training": {"id": BASE_ID + 113, "classification": ItemClassification.useful},
    "Mechanical Training": {"id": BASE_ID + 114, "classification": ItemClassification.useful},
    "Morale Boost": {"id": BASE_ID + 115, "classification": ItemClassification.filler},
    
    # =========================================================================
    # SPECIFIC WEAPONS (120s)
    # =========================================================================
    "Pistol": {"id": BASE_ID + 120, "classification": ItemClassification.useful},
    "Shotgun": {"id": BASE_ID + 121, "classification": ItemClassification.useful},
    "Uzi": {"id": BASE_ID + 122, "classification": ItemClassification.useful},
    "Rifle": {"id": BASE_ID + 123, "classification": ItemClassification.useful},
    "Grenades x3": {"id": BASE_ID + 124, "classification": ItemClassification.useful},
    "Chainsaw": {"id": BASE_ID + 125, "classification": ItemClassification.useful},
    "AK-47": {"id": BASE_ID + 126, "classification": ItemClassification.useful},
    "Flamethrower": {"id": BASE_ID + 127, "classification": ItemClassification.useful},
    
    # =========================================================================
    # SPECIAL (130s)
    # =========================================================================
    "Zombo Point": {"id": BASE_ID + 130, "classification": ItemClassification.useful},
    "Engine Repair (+2)": {"id": BASE_ID + 131, "classification": ItemClassification.useful},
    "Survivor Cache": {"id": BASE_ID + 132, "classification": ItemClassification.useful},
    
    # =========================================================================
    # PROGRESSIVE RESOURCES (200s)
    # =========================================================================
    "Food Scraps (+3)": {"id": BASE_ID + 200, "classification": ItemClassification.filler},
    "Food Supplies (+8)": {"id": BASE_ID + 201, "classification": ItemClassification.filler},
    "Food Stockpile (+12)": {"id": BASE_ID + 202, "classification": ItemClassification.useful},
    "Food Feast (+20)": {"id": BASE_ID + 203, "classification": ItemClassification.useful},
    "Gas Reserve (+25)": {"id": BASE_ID + 210, "classification": ItemClassification.filler},
    "Gas Tank (+75)": {"id": BASE_ID + 211, "classification": ItemClassification.useful},
    "Gas Barrel (+100)": {"id": BASE_ID + 212, "classification": ItemClassification.useful},
    "Gas Depot (+150)": {"id": BASE_ID + 213, "classification": ItemClassification.useful},
    "Ammo Clip (+10)": {"id": BASE_ID + 220, "classification": ItemClassification.filler},
    "Ammo Cache (+30)": {"id": BASE_ID + 221, "classification": ItemClassification.useful},
    "Ammo Crate (+50)": {"id": BASE_ID + 222, "classification": ItemClassification.useful},
    "Ammo Stockpile (+75)": {"id": BASE_ID + 223, "classification": ItemClassification.useful},
    "Bandages (+3)": {"id": BASE_ID + 230, "classification": ItemClassification.filler},
    "First Aid (+8)": {"id": BASE_ID + 231, "classification": ItemClassification.useful},
    "Medical Supplies (+15)": {"id": BASE_ID + 232, "classification": ItemClassification.useful},
    
    # =========================================================================
    # CHARACTER UPGRADES (300s)
    # =========================================================================
    "STR Manual": {"id": BASE_ID + 300, "classification": ItemClassification.useful},
    "FIT Guide": {"id": BASE_ID + 301, "classification": ItemClassification.useful},
    "SHT Voucher": {"id": BASE_ID + 302, "classification": ItemClassification.useful},
    "MED Textbook": {"id": BASE_ID + 303, "classification": ItemClassification.useful},
    "MCH Handbook": {"id": BASE_ID + 304, "classification": ItemClassification.useful},
    "Strength +2": {"id": BASE_ID + 310, "classification": ItemClassification.useful},
    "Fitness +2": {"id": BASE_ID + 311, "classification": ItemClassification.useful},
    "Shooting +2": {"id": BASE_ID + 312, "classification": ItemClassification.useful},
    "Medical +2": {"id": BASE_ID + 313, "classification": ItemClassification.useful},
    "Mechanical +2": {"id": BASE_ID + 314, "classification": ItemClassification.useful},
    "Vitality Boost": {"id": BASE_ID + 321, "classification": ItemClassification.useful},
    "Speed Boost": {"id": BASE_ID + 322, "classification": ItemClassification.useful},
    
    # =========================================================================
    # MORALE (400s)
    # =========================================================================
    "Morale +1": {"id": BASE_ID + 400, "classification": ItemClassification.filler},
    "Morale +2": {"id": BASE_ID + 401, "classification": ItemClassification.filler},
    "Morale +3": {"id": BASE_ID + 402, "classification": ItemClassification.useful},
    "Morale +8": {"id": BASE_ID + 403, "classification": ItemClassification.useful},
    "Calming Tea": {"id": BASE_ID + 410, "classification": ItemClassification.useful},
    "Friendship": {"id": BASE_ID + 411, "classification": ItemClassification.useful},
    "Therapy Session": {"id": BASE_ID + 412, "classification": ItemClassification.useful},
    
    # =========================================================================
    # RANDOM WEAPONS (500s) - The main weapon variety!
    # =========================================================================
    "Random Common Melee": {"id": BASE_ID + 500, "classification": ItemClassification.filler},
    "Random Common Gun": {"id": BASE_ID + 501, "classification": ItemClassification.useful},
    "Random Uncommon Melee": {"id": BASE_ID + 502, "classification": ItemClassification.useful},
    "Random Uncommon Gun": {"id": BASE_ID + 503, "classification": ItemClassification.useful},
    "Random Rare Melee": {"id": BASE_ID + 504, "classification": ItemClassification.useful},
    "Random Rare Gun": {"id": BASE_ID + 505, "classification": ItemClassification.useful},
    "Random Weapons x3": {"id": BASE_ID + 510, "classification": ItemClassification.useful},
    "Random Armory x5": {"id": BASE_ID + 511, "classification": ItemClassification.useful},
    "Molotov x3": {"id": BASE_ID + 520, "classification": ItemClassification.useful},
    "Bombs x3": {"id": BASE_ID + 521, "classification": ItemClassification.useful},
    "Grenades x5": {"id": BASE_ID + 522, "classification": ItemClassification.useful},
    "Legendary Weapon": {"id": BASE_ID + 530, "classification": ItemClassification.progression},
    
    # =========================================================================
    # UTILITY (600s)
    # =========================================================================
    "Car Parts (+3 Engine)": {"id": BASE_ID + 600, "classification": ItemClassification.useful},
    "Mechanic Kit (+6 Eng, +2 Body)": {"id": BASE_ID + 601, "classification": ItemClassification.useful},
    "Full Heal": {"id": BASE_ID + 622, "classification": ItemClassification.useful},
    
    # =========================================================================
    # SPECIAL ITEMS (700s)
    # =========================================================================
    "Zombo Point +1": {"id": BASE_ID + 700, "classification": ItemClassification.useful},
    "Zombo Point +2": {"id": BASE_ID + 701, "classification": ItemClassification.useful},
    "Zombo Point +5": {"id": BASE_ID + 702, "classification": ItemClassification.useful},
    "Mystery Box": {"id": BASE_ID + 710, "classification": ItemClassification.useful},
    "Pandora's Box": {"id": BASE_ID + 711, "classification": ItemClassification.trap},
    "Supply Drop": {"id": BASE_ID + 730, "classification": ItemClassification.useful},
    
    # =========================================================================
    # MODE UNLOCKS (800s) - PROGRESSION items!
    # These names MUST match what __init__.py uses in mode_to_unlock mapping
    # =========================================================================
    "Mode Unlock: Familiar Characters": {"id": BASE_ID + 800, "classification": ItemClassification.progression},
    "Mode Unlock: Rare Characters": {"id": BASE_ID + 801, "classification": ItemClassification.progression},
    "Mode Unlock: Short Trip": {"id": BASE_ID + 802, "classification": ItemClassification.progression},
    "Mode Unlock: Long Road": {"id": BASE_ID + 803, "classification": ItemClassification.progression},
    "Mode Unlock: Four Jerks": {"id": BASE_ID + 804, "classification": ItemClassification.progression},
    "Mode Unlock: Deadlier Road": {"id": BASE_ID + 805, "classification": ItemClassification.progression},
    "Mode Unlock: Familiar EXTREME": {"id": BASE_ID + 806, "classification": ItemClassification.progression},
    "Mode Unlock: Rare EXTREME": {"id": BASE_ID + 807, "classification": ItemClassification.progression},
    "Mode Unlock: Marathon": {"id": BASE_ID + 808, "classification": ItemClassification.progression},
    "Mode Unlock: K*E*P*A": {"id": BASE_ID + 809, "classification": ItemClassification.progression},
    "Mode Unlock: Four Jerks EXTREME": {"id": BASE_ID + 810, "classification": ItemClassification.progression},
    "Mode Unlock: Endless": {"id": BASE_ID + 811, "classification": ItemClassification.progression},
    "Mode Unlock: O*P*P": {"id": BASE_ID + 812, "classification": ItemClassification.progression},
    "Mode Unlock: Quick Death": {"id": BASE_ID + 813, "classification": ItemClassification.progression},
    "Mode Unlock: Infection": {"id": BASE_ID + 814, "classification": ItemClassification.progression},
    "Mode Unlock: Severe Weather": {"id": BASE_ID + 815, "classification": ItemClassification.progression},
    "Mode Unlock: RPG Mode": {"id": BASE_ID + 816, "classification": ItemClassification.progression},
    "Mode Unlock: Scepter Mode": {"id": BASE_ID + 817, "classification": ItemClassification.progression},
    "Mode Unlock: Mutation": {"id": BASE_ID + 818, "classification": ItemClassification.progression},
    "Mode Unlock: Infection EXTREME": {"id": BASE_ID + 819, "classification": ItemClassification.progression},
    
    # =========================================================================
    # TRAPS (900s)
    # =========================================================================
    "Food Spoiled": {"id": BASE_ID + 900, "classification": ItemClassification.trap},
    "Morale Crisis": {"id": BASE_ID + 901, "classification": ItemClassification.trap},
    "Ambush": {"id": BASE_ID + 902, "classification": ItemClassification.trap},
    "Gas Leak": {"id": BASE_ID + 903, "classification": ItemClassification.trap},
    "Weapon Jam": {"id": BASE_ID + 904, "classification": ItemClassification.trap},
    "Thief": {"id": BASE_ID + 905, "classification": ItemClassification.trap},
    "Injury": {"id": BASE_ID + 906, "classification": ItemClassification.trap},
    "Car Damage": {"id": BASE_ID + 907, "classification": ItemClassification.trap},
    "Argument": {"id": BASE_ID + 908, "classification": ItemClassification.trap},
    "Bandits": {"id": BASE_ID + 909, "classification": ItemClassification.trap},
    "Bad Omen": {"id": BASE_ID + 910, "classification": ItemClassification.trap},
    "Bad Weather": {"id": BASE_ID + 911, "classification": ItemClassification.trap},
    "Gear Lost": {"id": BASE_ID + 912, "classification": ItemClassification.trap},
    "Food Poison": {"id": BASE_ID + 913, "classification": ItemClassification.trap},
    "False Hope": {"id": BASE_ID + 914, "classification": ItemClassification.trap},
}

# =============================================================================
# MODE UNLOCK ITEM MAPPING
# =============================================================================
# Maps mode internal names to their unlock item names (must match item_table keys)
MODE_UNLOCK_ITEMS: Dict[str, str] = {
    "familiar": "Mode Unlock: Familiar Characters",
    "rare": "Mode Unlock: Rare Characters",
    "short": "Mode Unlock: Short Trip",
    "long": "Mode Unlock: Long Road",
    "4jerks": "Mode Unlock: Four Jerks",
    "deadlier": "Mode Unlock: Deadlier Road",
    "familiarEX": "Mode Unlock: Familiar EXTREME",
    "rareEX": "Mode Unlock: Rare EXTREME",
    "marathon": "Mode Unlock: Marathon",
    "kepa": "Mode Unlock: K*E*P*A",
    "4jerksEX": "Mode Unlock: Four Jerks EXTREME",
    "endless": "Mode Unlock: Endless",
    "opp": "Mode Unlock: O*P*P",
    "quickdeath": "Mode Unlock: Quick Death",
    "infection": "Mode Unlock: Infection",
    "weather": "Mode Unlock: Severe Weather",
    "rpg": "Mode Unlock: RPG Mode",
    "scepter": "Mode Unlock: Scepter Mode",
    "mutation": "Mode Unlock: Mutation",
    "infectionEX": "Mode Unlock: Infection EXTREME",
}

# =============================================================================
# ITEM POOL CONFIGURATION
# =============================================================================

FILLER_ITEMS = [
    "Food Pack (+5)",
    "Food Scraps (+3)",
    "Gas Reserve (+25)",
    "Ammo Clip (+10)",
    "Bandages (+3)",
    "Morale +1",
    "Morale +2",
    "Morale Boost",
    "Random Common Melee",
]

USEFUL_ITEMS = [
    "Food Crate (+15)",
    "Gas Can (+50)",
    "Ammo Box (+20)",
    "Medical Kit (+5)",
    "Shooting Training",
    "Strength Training",
    "Fitness Training",
    "Medical Training",
    "Mechanical Training",
    "Pistol",
    "Shotgun",
    "Uzi",
    "Rifle",
    "Grenades x3",
    "Chainsaw",
    "AK-47",
    "Flamethrower",
    "Zombo Point",
    "Engine Repair (+2)",
    "Survivor Cache",
    "Food Supplies (+8)",
    "Food Stockpile (+12)",
    "Food Feast (+20)",
    "Gas Tank (+75)",
    "Gas Barrel (+100)",
    "Gas Depot (+150)",
    "Ammo Cache (+30)",
    "Ammo Crate (+50)",
    "Ammo Stockpile (+75)",
    "First Aid (+8)",
    "Medical Supplies (+15)",
    "STR Manual",
    "FIT Guide",
    "SHT Voucher",
    "MED Textbook",
    "MCH Handbook",
    "Strength +2",
    "Fitness +2",
    "Shooting +2",
    "Medical +2",
    "Mechanical +2",
    "Vitality Boost",
    "Speed Boost",
    "Morale +3",
    "Morale +8",
    "Calming Tea",
    "Friendship",
    "Therapy Session",
    "Random Common Gun",
    "Random Uncommon Melee",
    "Random Uncommon Gun",
    "Random Rare Melee",
    "Random Rare Gun",
    "Random Weapons x3",
    "Random Armory x5",
    "Molotov x3",
    "Bombs x3",
    "Grenades x5",
    "Car Parts (+3 Engine)",
    "Mechanic Kit (+6 Eng, +2 Body)",
    "Full Heal",
    "Zombo Point +1",
    "Zombo Point +2",
    "Zombo Point +5",
    "Mystery Box",
    "Supply Drop",
    "Legendary Weapon",
]

TRAP_ITEMS = [
    "Food Spoiled",
    "Morale Crisis",
    "Ambush",
    "Gas Leak",
    "Weapon Jam",
    "Thief",
    "Injury",
    "Car Damage",
    "Argument",
    "Bandits",
    "Bad Omen",
    "Bad Weather",
    "Gear Lost",
    "Food Poison",
    "False Hope",
    "Pandora's Box",
]


def create_item_pool(world) -> List[DRTCItem]:
    """
    Create the item pool for a Death Road to Canada world.
    
    This function builds the item pool based on the world's options,
    balancing filler, useful items, traps, and progression items.
    """
    from .locations import get_location_count
    
    player = world.player
    options = world.options
    item_pool = []
    
    # Get total location count to match
    total_locations = get_location_count(world)
    
    # === MODE UNLOCK ITEMS (PROGRESSION) ===
    # Add mode unlocks for enabled modes (except normal which is always available)
    if options.mode_unlocks_in_pool.value:
        enabled_modes = set(options.enabled_modes.value)
        enabled_modes.update(options.goal_modes.value)
        
        for mode, item_name in MODE_UNLOCK_ITEMS.items():
            if mode in enabled_modes and mode != "normal":
                if item_name in item_table:
                    item_data = item_table[item_name]
                    item = DRTCItem(item_name, item_data["classification"], item_data["id"], player)
                    item_pool.append(item)
    
    # === CALCULATE REMAINING SLOTS ===
    remaining = total_locations - len(item_pool)
    if remaining <= 0:
        return item_pool
    
    # === TRAP PERCENTAGE ===
    trap_percent = options.trap_percentage.value if hasattr(options, 'trap_percentage') else 20
    trap_count = int(remaining * trap_percent / 100)
    
    # === USEFUL vs FILLER split (remaining after traps) ===
    # 60% useful, 40% filler
    non_trap_count = remaining - trap_count
    useful_count = int(non_trap_count * 0.6)
    filler_count = non_trap_count - useful_count
    
    # Add traps
    for _ in range(trap_count):
        trap_name = random.choice(TRAP_ITEMS)
        item_data = item_table[trap_name]
        item = DRTCItem(trap_name, item_data["classification"], item_data["id"], player)
        item_pool.append(item)
    
    # Add useful items
    for _ in range(useful_count):
        useful_name = random.choice(USEFUL_ITEMS)
        item_data = item_table[useful_name]
        item = DRTCItem(useful_name, item_data["classification"], item_data["id"], player)
        item_pool.append(item)
    
    # Add filler
    for _ in range(filler_count):
        filler_name = random.choice(FILLER_ITEMS)
        item_data = item_table[filler_name]
        item = DRTCItem(filler_name, item_data["classification"], item_data["id"], player)
        item_pool.append(item)
    
    return item_pool