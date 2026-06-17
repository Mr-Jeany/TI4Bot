from typing import TYPE_CHECKING

from aiogram.types import InputRichMessage

from models.emoji import CardsEmoji

if TYPE_CHECKING:
    from models.faction import Faction

class PromissoryNote:
    id: str
    name: str
    description: str
    is_faction_specific: bool = False
    faction: "Faction | None" = None

    def __init__(self, id: str, name: str, description: str, is_faction_specific: bool = False, faction: "Faction | None" = None):
        self.id = id
        self.name = name
        self.description = description

        self.is_faction_specific = is_faction_specific
        self.faction = faction

    @property
    def full(self) -> str:
        buffer = f"""
{self.faction.emoji if self.faction else ""} {self.name}

{self.description}
"""

        return buffer

    @property
    def rich_info(self) -> InputRichMessage:
        buffer = f"""
# {self.faction.emoji if self.faction else ""}{CardsEmoji.prom_note} {self.name}

{self.description}
        """

        return InputRichMessage(markdown=buffer)