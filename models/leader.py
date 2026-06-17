from enum import Enum
from typing import TYPE_CHECKING

from aiogram.types import InputRichMessage

from models.emoji import LeadersEmoji

if TYPE_CHECKING:
    from models.faction import Faction

class LeaderTypes(str, Enum):
    AGENT = "agent"
    COMMANDER = "commander"
    HERO = "hero"

class Leader:
    id: str
    type: LeaderTypes
    name: str
    description: str
    unlocking: str | None = None
    faction: "Faction | None" = None

    def __init__(self, id: str, type: LeaderTypes, name: str, description: str, unlocking: str | None = None, faction: "Faction | None" = None):
        self.id = id
        self.type = type
        self.name = name

        self.description = description
        self.unlocking = unlocking

        self.faction = faction

    @property
    def full(self) -> InputRichMessage:
        buffer = f"""
# {self.faction.emoji.rich if self.faction else ""}{getattr(LeadersEmoji, self.type).rich} {self.name}
{f'*Разблокировка: {self.unlocking}*' if self.unlocking else ""}

{self.description}
"""

        return InputRichMessage(markdown=buffer)