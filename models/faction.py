import json

from aiogram.types import InputRichMessage

from models.ability import Ability
from models.emoji import CustomEmoji, UnitsEmoji, TechnologySpecialityEmoji, OtherEmoji
from models.leader import Leader
from models.planet import Planet
from models.promissory_note import PromissoryNote
from models.technology import Technology
from models.unit import Unit


class Faction:
    id: str
    name: str

    commodities: int
    complexity: int

    emoji: CustomEmoji
    planets: list[Planet]
    starting_technologies: list[Technology]
    starting_units: list
    abilities: list[Ability] | None
    faction_specific_units: list | None
    faction_technologies: list[Technology]

    flagship: Unit
    mech: Unit
    promissory_note: PromissoryNote

    agent: Leader
    commander: Leader
    hero: Leader

    def __init__(self,
                 id: str,
                 name: str,

                 commodities: int,
                 complexity: int,

                 emoji: CustomEmoji,
                 planets: list[Planet],
                 starting_units: list,
                 abilities: list[Ability] | None,
                 faction_technologies: list[Technology] | None,
                 faction_specific_units: list[Unit] | None,
                 starting_technologies: list,

                 flagship: Unit,
                 mech: Unit,

                 agent: Leader,
                 commander: Leader,
                 hero: Leader,

                 promissory_note: PromissoryNote):
        # Correct way to create
        self.id = id
        self.name = name

        self.commodities = commodities
        self.complexity = complexity

        self.emoji = emoji
        self.type = type

        self.planets = planets
        self.starting_units = starting_units

        self.abilities = abilities
        self.faction_technologies = faction_technologies

        self.faction_specific_units = faction_specific_units
        if faction_specific_units:
            for unit in faction_specific_units:
                unit.faction = self

        self.flagship = flagship
        self.flagship.faction = self

        self.mech = mech
        self.mech.faction = self

        self.promissory_note = promissory_note
        self.promissory_note.faction = self

        self.agent = agent
        self.agent.faction = self

        self.commander = commander
        self.commander.faction = self

        self.hero = hero
        self.hero.faction = self

        self.starting_technologies = starting_technologies

    @property
    def header(self) -> str:
        return f"# {self.emoji} {self.name}"

    @property
    def subheader(self) -> str:
        # PLANETS
        planets = "## Начальные планеты"

        for planet in self.planets:
            planets += f"\n- {planet}"


        # STARTING UNITS
        units = "## Начальные отряды\n"

        for unit_id, unit_count in self.starting_units:
            units += f"{(str(getattr(UnitsEmoji, unit_id).rich) + " ") *unit_count}"


        # STARTING TECHNOLOGIES
        st = "## Начальные технологии\n"

        for tech_name, tech_color in self.starting_technologies:
            st += f"- {(str(getattr(TechnologySpecialityEmoji, tech_color).rich) + " ")} {tech_name}\n"

        buffer = f"""
{planets}

---

{units}

---

{st}
"""

        return f"{buffer}"

    @property
    def abilities_text(self) -> str | None:
        if not self.abilities:
            return None

        buffer = "## Способности\n"
        for ability in self.abilities:
            buffer += f"#### {ability.name}\n{ability.description}\n"

        buffer = buffer.rstrip()

        return buffer

    @property
    def faction_technologies_text(self) -> str | None:
        if not self.faction_technologies:
            return None

        buffer = "## Фракционные технологии"

        for tech in self.faction_technologies:
            buffer += f"""
#### {(str(tech.color_icon.rich) + " ")*tech.prerequisites[tech.color] if tech.color_icon != TechnologySpecialityEmoji.choose else tech.color_icon.rich} {tech.name}\n{tech.description}\n
"""

        buffer  = buffer.rstrip()

        return buffer

    @property
    def faction_specific_units_text(self) -> str | None:
        if not self.faction_specific_units:
            return None

        buffer = "## Особые отряды"

        for unit in self.faction_specific_units:
            buffer += f"\n{unit.short}\n"

        buffer = buffer.rstrip()

        return buffer

    @property
    def full_text(self) -> InputRichMessage:
        buffer = f"""
{self.header}

{OtherEmoji.commodity.rich} {self.commodities}

---

{self.subheader}

---

{self.abilities_text}
"""
        if self.faction_technologies_text:
            buffer += f"\n---\n{self.faction_technologies_text}\n"

        if self.faction_specific_units_text:
            buffer += f"\n---\n{self.faction_specific_units_text}"

        # print(buffer)
        return InputRichMessage(markdown=buffer)