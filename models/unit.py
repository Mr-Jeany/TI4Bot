from enum import Enum


class UnitType(Enum, str):
    CARRIER = "carrier"
    CRUISER = "cruiser"
    DESTROYER = "destroyer"
    DREADNOUGHT = "dreadnaught"
    FIGHTER = "fighter"
    FLAGSHIP = "flagship"
    WAR_SUN = "war_sun"

    INFANTRY = "infantry"
    MECH = "mech"

    SPACE_DOCK = "space_dock"
    PDS = "pds"


class Unit:
    id: str
    unit_type: UnitType

    ### Basic information
    name: str
    description: str # Usually has extra ability info like "disables space cannon..."

    abilities: list
    cost: int
    combat: int
    number_of_attacks: int
    move: int | None
    capacity: int | None

    prerequisites: dict | None

    is_faction_specific: bool = False
    faction: str | None

    def __init__(self, id: str, unit_type: UnitType, name: str, description: str, abilities: list, cost: int,
                 combat: int, number_of_attacks: int,
                 move: int | None = None, capacity: int | None = None, prerequisites: int | None = None,
                 is_faction_specific: bool = False, faction: str | None = None):
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

    @property
    def average_hits_per_round(self):
        average_one_dice = 1 - ((self.combat - 1) / 10)
        return average_one_dice*self.number_of_attacks
