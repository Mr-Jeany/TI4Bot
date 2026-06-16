from enum import Enum

from utils import UnitsEmoji


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
    faction: str | None

    upgrade: Unit | None

    def __init__(self, id: str, unit_type: UnitType, name: str, description: str | None, abilities: list, cost: int,
                 combat: int, number_of_attacks: int,
                 move: int | None = None, capacity: int | None = None, prerequisites: dict | None = None,
                 is_faction_specific: bool = False, faction: str | None = None,
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
