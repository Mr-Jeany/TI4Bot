import json

from models.emoji import CustomEmoji, UnitsEmoji
from models.planet import Planet
from models.technology import Technology
from models.unit import Unit


class Faction:
    id: str
    name: str
    emoji: CustomEmoji
    planets: list[Planet]
    starting_technologies: list[Technology]
    starting_units: list
    abilities: list
    faction_specific_units: list | None
    faction_technologies: list[Technology]
    flagship: Unit
    mech: dict
    promissory_note: dict

    agent: dict
    commander: dict
    hero: dict

    def __init__(self,
                 id: str,
                 name: str,

                 emoji: CustomEmoji,
                 planets: list[Planet],
                 starting_units: list,

                 flagship: Unit,

                 **kwargs):
        # Correct way to create
        self.id = id
        self.name = name
        self.emoji = emoji

        self.planets = planets
        self.starting_units = starting_units

        # Raw
        self.starting_technologies = kwargs.pop("starting_technologies")

        self.abilities = kwargs.pop("abilities")

        self.faction_specific_units = kwargs.pop("faction_specific_units", None)

        self.faction_technologies = kwargs.pop("faction_technologies")

        self.flagship = flagship
        self.mech = kwargs.pop("mech")
        self.promissory_note = kwargs.pop("promissory_note")

        self.agent = kwargs.pop("agent")
        self.commander = kwargs.pop("commander")
        self.hero = kwargs.pop("hero")

    @property
    def header(self) -> str:
        return f"<b>{self.emoji} {self.name}</b>"

    @property
    def subheader(self) -> str:
        """
        Returns faction starting planets and units
        """
        planets = "<b>Начальные планеты:</b> "

        for planet in self.planets:
            planets += f"{planet};"

        planets = planets[:-1]

        units = "<b>Начальные отряды: </b>"

        for unit_id, unit_count in self.starting_units:
            units += f"{str(getattr(UnitsEmoji, unit_id))*unit_count}"

        buffer = f"{planets}\n{units}"

        return f"{buffer}"

    @property
    def full_text(self) -> str:
        return f"{self.header}\n\n{self.subheader}"