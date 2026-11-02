from typing import Dict, Any, ClassVar
from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
from .items import DRTCItem, item_table, create_item_pool, FILLER_ITEMS
from .locations import DRTCLocation, location_table
from .options import DRTCOptions
from .regions import create_regions


class DRTCWebWorld(WebWorld):
    theme = "dirt"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="How to set up DR2C for Archipelago.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["PixelShake92"]
        )
    ]


class DRTCWorld(World):
    """Roguelike road trip to Canada. Zombies, bandits, dumb team choices."""

    game = "Death Road to Canada"
    web = DRTCWebWorld()
    options_dataclass = DRTCOptions
    options: DRTCOptions

    topology_present = False

    item_name_to_id: ClassVar[Dict[str, int]] = {
        name: data["id"] for name, data in item_table.items()
    }
    location_name_to_id: ClassVar[Dict[str, int]] = location_table

    required_client_version = (0, 5, 0)

    MODE_TO_UNLOCK: ClassVar[Dict[str, str]] = {
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
        "mutationmodeEX": "Mode Unlock: Mutation EXTREME",
        "horrormode": "Mode Unlock: The Horrors",
    }

    def create_item(self, name: str) -> DRTCItem:
        data = item_table[name]
        return DRTCItem(name, data["classification"], data["id"], self.player)

    def create_items(self) -> None:
        self.multiworld.itempool += create_item_pool(self)

        if not self.options.mode_unlocks_in_pool.value:
            needed = set(self.options.enabled_modes.value)
            needed.update(self.options.goal_modes.value)
            needed.discard("normal")  # always unlocked
            for mode in needed:
                item_name = self.MODE_TO_UNLOCK.get(mode)
                if item_name and item_name in item_table:
                    self.multiworld.push_precollected(self.create_item(item_name))

    def create_regions(self) -> None:
        create_regions(self)

    def set_rules(self) -> None:
        from .rules import set_rules
        set_rules(self)

    def generate_basic(self) -> None:
        pass

    def generate_output(self, output_directory: str) -> None:
        pass

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal_modes": list(self.options.goal_modes.value),
            "enabled_modes": list(self.options.enabled_modes.value),
            "death_link": self.options.death_link.value,
        }

    def get_filler_item_name(self) -> str:
        return self.random.choice(FILLER_ITEMS)
