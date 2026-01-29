"""
Death Road to Canada Archipelago World
"""

from typing import Dict, List, Any, ClassVar
from BaseClasses import Item, ItemClassification, Region, Location, Tutorial
from worlds.AutoWorld import World, WebWorld
from .items import DRTCItem, item_table, create_item_pool
from .locations import DRTCLocation, location_table, create_all_location_names
from .options import DRTCOptions
from .regions import create_regions


class DRTCWebWorld(WebWorld):
    theme = "dirt"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to setting up Death Road to Canada for Archipelago multiworld.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["PixelShake92"]
        )
    ]


class DRTCWorld(World):
    """
    Death Road to Canada is a randomly generated road trip action-roguelike. 
    You manage a group of survivors as they travel across the USA to reach the 
    safety of Canada, facing zombies, bandits, and difficult choices along the way.
    """
    
    game = "Death Road to Canada"
    web = DRTCWebWorld()
    options_dataclass = DRTCOptions
    options: DRTCOptions
    
    topology_present = False  # No logical requirements between locations
    
    item_name_to_id: ClassVar[Dict[str, int]] = {name: data["id"] for name, data in item_table.items()}
    location_name_to_id: ClassVar[Dict[str, int]] = location_table
    
    required_client_version = (0, 5, 0)
    
    def create_item(self, name: str) -> DRTCItem:
        """Create an item for this world."""
        item_data = item_table[name]
        return DRTCItem(name, item_data["classification"], item_data["id"], self.player)
    
    def create_items(self) -> None:
        """Create and add items to the multiworld pool."""
        item_pool = create_item_pool(self)
        self.multiworld.itempool += item_pool
        
        # If mode unlocks are NOT in the pool, give unlocks for enabled/goal modes as starting items
        if not self.options.mode_unlocks_in_pool.value:
            # Get all modes that need to be unlocked
            needed_modes = set(self.options.enabled_modes.value)
            needed_modes.update(self.options.goal_modes.value)
            
            # Map mode keys to unlock item names (must match item_table exactly)
            mode_to_unlock = {
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
            
            for mode in needed_modes:
                # Normal mode doesn't need an unlock
                if mode == "normal":
                    continue
                item_name = mode_to_unlock.get(mode)
                if item_name and item_name in item_table:
                    self.multiworld.push_precollected(self.create_item(item_name))
    
    def create_regions(self) -> None:
        """Create regions and locations."""
        create_regions(self)
    
    def set_rules(self) -> None:
        """Set access rules for locations."""
        from .rules import set_rules
        set_rules(self)
    
    def generate_basic(self) -> None:
        """Generate basic structures."""
        pass
    
    def generate_output(self, output_directory: str) -> None:
        """Generate output files if needed."""
        pass
    
    def fill_slot_data(self) -> Dict[str, Any]:
        """Return data to be sent to the client."""
        return {
            "goal_modes": list(self.options.goal_modes.value),
            "enabled_modes": list(self.options.enabled_modes.value),
            "death_link": self.options.death_link.value,
        }
    
    def get_filler_item_name(self) -> str:
        """Return the name of a filler item."""
        return "Food Pack (+5)"
