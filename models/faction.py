import json

from models.ability import Ability
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
    abilities: list[Ability] | None
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
                 abilities: list[Ability] | None,
                 faction_technologies: list[Technology] | None,
                 faction_specific_units: list[Unit] | None,

                 flagship: Unit,

                 **kwargs):
        # Correct way to create
        self.id = id
        self.name = name
        self.emoji = emoji

        self.planets = planets
        self.starting_units = starting_units

        self.abilities = abilities
        self.faction_technologies = faction_technologies

        self.faction_specific_units = faction_specific_units

        self.flagship = flagship

        # Raw
        self.starting_technologies = kwargs.pop("starting_technologies")



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
            planets += f"{planet}; "

        planets = planets[:-2]

        units = "<b>Начальные отряды: </b>"

        for unit_id, unit_count in self.starting_units:
            units += f"{str(getattr(UnitsEmoji, unit_id))*unit_count}"

        buffer = f"{planets}\n{units}"

        return f"{buffer}"

    @property
    def abilities_text(self) -> str | None:
        if not self.abilities:
            return None

        buffer = "<b>— Способности —</b>\n"
        for ability in self.abilities:
            buffer += f"{ability}\n\n"

        buffer = buffer.rstrip()

        return buffer

    @property
    def faction_technologies_text(self) -> str | None:
        if not self.faction_technologies:
            return None

        buffer = "<b>— Фракционные технологии —</b>"

        for tech in self.faction_technologies:
            buffer += f"\n{tech.faction_info}\n"

        buffer  = buffer.rstrip()

        return buffer

    @property
    def faction_specific_units_text(self) -> str | None:
        if not self.faction_specific_units:
            return None

        buffer = "<b>— Особые отряды —</b>"

        for unit in self.faction_specific_units:
            buffer += f"\n{unit.short}\n"

        buffer = buffer.rstrip()

        return buffer

    @property
    def full_text(self) -> str:
        buffer = f"""
{self.header}

{self.subheader}

{self.abilities_text}
"""
        if self.faction_technologies_text:
            buffer += f"\n{self.faction_technologies_text}\n"

        if self.faction_specific_units_text:
            buffer += f"\n{self.faction_specific_units_text}"

        return buffer