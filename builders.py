from typing import Tuple, List

from utils import get_faction, UnitsEmoji, CardsEmoji, Emoji


async def build_flagship(faction_id):
    faction_dict = await get_faction(faction_id)
    flagship = faction_dict["flagship"]

    name_part = f"<tg-emoji emoji-id='{faction_dict['emoji']['id']}'>{faction_dict['emoji']['base_emoji']}</tg-emoji>{UnitsEmoji.flagship} <b>{flagship['name']}</b>"

    abilities_part = ""
    for ability in flagship["abilities"]:
        abilities_part += f"— {ability}\n"
    abilities_part.rstrip()

    built = f"""
{name_part}
{flagship["description"]}
{abilities_part}
Цена: {flagship["cost"]} | Бой: {flagship["combat"]} | Полёт: {flagship["move"]} | Место: {flagship["capacity"]}
"""

    return built

async def build_mech(faction_id):
    faction_dict = await get_faction(faction_id)
    mech = faction_dict["mech"]

    name_part = f"<tg-emoji emoji-id='{faction_dict['emoji']['id']}'>{faction_dict['emoji']['base_emoji']}</tg-emoji>{UnitsEmoji.mech} <b>{mech['name']}</b>"

    abilities_part = ""
    for ability in mech["abilities"]:
        abilities_part += f"— {ability}\n"
    abilities_part.rstrip()

    built = f"""
{name_part}
{mech["description"]}
{abilities_part}
Цена: {mech["cost"]} | Бой: {mech["combat"]}
"""

    return built

async def build_pn(faction_id):
    faction_dict = await get_faction(faction_id)
    pn = faction_dict["promissory_note"]

    name_part = f"<tg-emoji emoji-id='{faction_dict['emoji']['id']}'>{faction_dict['emoji']['base_emoji']}</tg-emoji>{CardsEmoji.pn} <b>{pn['name']}</b>"

    built = f"""
{name_part}
{pn["description"]}
"""

    return built

async def build_fsu(faction_id: str, unit_type: str):
    faction_dict = await get_faction(faction_id)
    faction_emoji = Emoji(
        faction_dict['emoji']['id'],
        faction_dict['emoji']['base_emoji']
    )
    fsu = faction_dict["faction_specific_units"]

    result = ""
    for unit in fsu:
        if unit["type"] != unit_type:
            continue

        icon = getattr(UnitsEmoji, unit["type"])
        unit["icon_custom_emoji_id"] = icon.id

        abilities_part = ""
        for ability in unit["abilities"]:
            abilities_part += f"— {ability}\n"
        abilities_part.rstrip()

        # TODO: Add auto check for stats
        result += f"""
<b>{faction_emoji}{icon} {unit['name']}</b>
{unit['description']}
{abilities_part}
Цена: {unit["cost"]} | Бой: {unit["combat"]} | Полёт: {unit["move"]} | Место: {unit["capacity"]}

"""


        upgrade = unit["upgrade"]
        abilities_part = ""
        for ability in unit["abilities"]:
            abilities_part += f"— {ability}\n"
        abilities_part.rstrip()
        result += f"""
<b>{faction_emoji}{icon} {upgrade['name']}</b>
{upgrade['description']}
{abilities_part}
Цена: {upgrade["cost"]} | Бой: {upgrade["combat"]} | Полёт: {upgrade["move"]} | Место: {upgrade["capacity"]}

        """

        return result

class MessageParts:
    @staticmethod
    async def faction_specific_units(faction_id):
        """
        Generates a part with units exclusive to a faction
        :param faction_id: ID of a faction to generate units for
        :return: String with text and list with buttons and text
        """
        faction_dict = await get_faction(faction_id)
        faction_emoji = Emoji(
            faction_dict['emoji']['id'],
            faction_dict['emoji']['base_emoji']
        )
        units = faction_dict.get("faction_specific_units", None)

        if not units:
            return None

        result = ""
        buttons = []

        for unit in units:
            icon = getattr(UnitsEmoji, unit["type"])
            result += f"{icon} {unit['name']}\n"

            buttons.append({
                "type": unit["type"],
                "name": unit["name"],
                "icon_custom_emoji_id": icon.id
            })

        result.rstrip()

        return result, buttons