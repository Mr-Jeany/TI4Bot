import asyncio
import json
from typing import Dict, Any

from aiogram.filters.callback_data import CallbackData

class Emoji:
    def __init__(self, emoji_id: str, symbol: str):
        self.id = emoji_id
        self.symbol = symbol

    def __str__(self):
        return f"<tg-emoji emoji-id='{self.id}'>{self.symbol}</tg-emoji>"

class TechnologySpeciality:
    green = "<tg-emoji emoji-id='5224642078507572156'>🌟</tg-emoji>"
    yellow = "<tg-emoji emoji-id='5224586883882848672'>🌟</tg-emoji>"
    blue = "<tg-emoji emoji-id='5226561134319933905'>🌟</tg-emoji>"
    red = "<tg-emoji emoji-id='5224243557082112236'>🌟</tg-emoji>"

class UnitsEmoji:
    flagship = Emoji(
        "5229066702276304464",
        "🚀"
    )

    mech = Emoji(
        "5230997083917423709",
        "🤖"
    )

    warsun = Emoji(
        "5229040764968805275",
        "🌞"
    )


class CardsEmoji:
    pn = Emoji(
        "5229063115978612584",
        "🎫"
    )

class LeadersEmoji:
    agent = Emoji(
        "5228730127164155764",
        "1️⃣"
    )

    commander = Emoji(
        "5228927841688660110",
        "2️⃣"
    )

    hero = Emoji(
        "5228749536121365977",
        "3️⃣"
    )

class AdditionalInfoCallback(CallbackData, prefix="addinfo"):
    type: str
    faction: str


class CustomEmoji:
    def __init__(self, custom_emoji_id, base_emoji):
        self.custom_emoji_id = custom_emoji_id
        self.base_emoji = base_emoji

    def __str__(self):
        return f"<tg-emoji emoji-id='{self.custom_emoji_id}'>{self.base_emoji}</tg-emoji>"

async def get_faction(faction_id) -> Dict[Any, Any] | None:
    factions = json.load(open("factions.json", encoding="utf-8"))

    for faction in factions["items"]:
        if faction["id"] == faction_id:
            return faction

    return None


### Leaders
class Leaders:
    @staticmethod
    async def build_agent(faction_id):
        faction_dict = await get_faction(faction_id)
        agent = faction_dict["agent"]

        emoji = CustomEmoji(custom_emoji_id=faction_dict["emoji"]["id"], base_emoji=faction_dict["emoji"]["base_emoji"])

        built = f"""
{emoji} <b>{agent['name']}</b> (Агент)

{agent['description']}
"""
        return built

    @staticmethod
    async def build_commander(faction_id):
        faction_dict = await get_faction(faction_id)
        commander = faction_dict["commander"]

        emoji = CustomEmoji(custom_emoji_id=faction_dict["emoji"]["id"], base_emoji=faction_dict["emoji"]["base_emoji"])

        built = f"""
{emoji} <b>{commander['name']}</b> (Командир)

<i><b>Разблокировка:</b> {commander['condition']}</i>

{commander['description']}
"""
        return built

    @staticmethod
    async def build_hero(faction_id):
        faction_dict = await get_faction(faction_id)
        hero = faction_dict["hero"]

        emoji = CustomEmoji(custom_emoji_id=faction_dict["emoji"]["id"], base_emoji=faction_dict["emoji"]["base_emoji"])

        built = f"""
{emoji} <b>{hero['name']}</b> (Герой)

<i><b>Разблокировка:</b> {hero['condition']}</i>

{hero['description']}
"""
        return built