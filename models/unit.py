from enum import Enum

from aiogram.types import InputRichMessage
from tabulate import tabulate

from utils import UnitsEmoji

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.faction import Faction

class UnitType(str, Enum):
    CARRIER = "carrier"
    CRUISER = "cruiser"
    DESTROYER = "destroyer"
    DREADNOUGHT = "dreadnaught"
    FIGHTER = "fighter"
    FLAGSHIP = "flagship"
    WARSUN = "warsun"

    INFANTRY = "infantry"
    MECH = "mech"

    SPACE_DOCK = "space_dock"
    PDS = "pds"


class Unit:
    id: str
    unit_type: UnitType

    ### Basic information
    name: str
    description: str | None # Usually has extra ability info like "disables space cannon..."

    abilities: list
    cost: int
    combat: int
    number_of_attacks: int
    move: int | None
    capacity: int | None

    prerequisites: dict | None

    is_faction_specific: bool = False
    faction: "Faction | None" = None

    upgrade: Unit | None

    def __init__(self, id: str, unit_type: UnitType, name: str, description: str | None, abilities: list, cost: int | None = None,
                 combat: int | None = None, number_of_attacks: int | None = None,
                 move: int | None = None, capacity: int | None = None, prerequisites: dict | None = None,
                 is_faction_specific: bool = False, faction: "Faction | None" = None,
                 upgrade: Unit | None = None):
        self.id = id
        self.unit_type = unit_type
        self.name = name
        self.description = description

        self.abilities = abilities
        self.cost = cost
        self.combat = combat
        self.number_of_attacks = number_of_attacks
        self.move = move
        self.capacity = capacity

        self.prerequisites = prerequisites
        self.is_faction_specific = is_faction_specific
        self.faction = faction

        self.upgrade = upgrade

    @property
    def average_hits_per_round(self):
        average_one_dice = 1 - ((self.combat - 1) / 10)
        return average_one_dice*self.number_of_attacks

    @property
    def short(self):
        emoji = getattr(UnitsEmoji, self.unit_type.name.lower(), None)

        return f"{emoji if emoji else ""} {self.name}"

    @property
    def abilities_text(self) -> str:
        buffer = ""
        for ability in self.abilities:
            buffer += f"- {ability}\n"

        buffer = buffer.rstrip()

        return buffer

    @property
    def rich_info(self) -> InputRichMessage:
        headers = []
        data = []

        if self.cost:
            headers.append("Цена")
            data.append(self.cost)

        if self.combat:
            headers.append("Бой")
            if self.number_of_attacks > 1:
                data.append(f"{self.combat}x{self.number_of_attacks}")
            else:
                data.append(self.combat)

        if self.move:
            headers.append("Полёт")
            data.append(self.move)

        if self.capacity:
            headers.append("Место")
            data.append(self.capacity)

        table = tabulate([data], headers=headers, tablefmt="pipe", colglobalalign="left")

        buffer = f"""
# {f'{self.faction.emoji}' if self.faction else ""}{self.short}
{self.description if self.description else ""}
{self.abilities_text}

{table}
"""

        return InputRichMessage(markdown=buffer)

    @property
    def rich_with_upgrade(self) -> InputRichMessage:
        if self.upgrade is None:
            return self.rich_info
        return InputRichMessage(markdown=f"{self.rich_info.markdown}\n\n{self.upgrade.rich_info.markdown}")