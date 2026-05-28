import json

from models.emoji import CustomEmoji
from models.planet import Planet
from models.technology import Technology


class Faction:
    id: str
    name: str
    emoji: CustomEmoji
    planet: Planet
    starting_technologies: list[Technology]
    starting_units: list
    abilities: list
    faction_specific_units: list
    faction_technologies: list[Technology]
    flagship: dict
    mech: dict
    promissory_note: dict

    agent: dict
    commander: dict
    hero: dict

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id")
        self.name = kwargs.pop("name")

        custom_emoji = kwargs.pop("emoji")
        self.emoji = CustomEmoji(custom_emoji.pop("id"), custom_emoji.pop("base_emoji"))

        self.planet = Planet(**kwargs.pop("planet"))

        self.starting_technologies = kwargs.pop("starting_technologies")

        self.starting_units = kwargs.pop("starting_units")

        self.abilities = kwargs.pop("abilities")

        self.faction_specific_units = kwargs.pop("faction_specific_units")

        self.faction_technologies = kwargs.pop("faction_technologies")

        self.flagship = kwargs.pop("flagship")
        self.mech = kwargs.pop("mech")
        self.promissory_note = kwargs.pop("promissory_note")

        self.agent = kwargs.pop("agent")
        self.commander = kwargs.pop("commander")
        self.hero = kwargs.pop("hero")