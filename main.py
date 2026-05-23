import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from utils import AdditionalInfoCallback, Leaders

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

dp = Dispatcher()

async def build_flagship(faction_id):
    faction_dict = await get_faction(faction_id)
    flagship = faction_dict["flagship"]

    name_part = f"<tg-emoji emoji-id='{faction_dict['emoji']['id']}'>{faction_dict['emoji']['base_emoji']}</tg-emoji> <b>{flagship['name']}</b> (Флагман)"

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

    name_part = f"<tg-emoji emoji-id='{faction_dict['emoji']['id']}'>{faction_dict['emoji']['base_emoji']}</tg-emoji> <b>{mech['name']}</b> (Мех)"

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

    name_part = f"<tg-emoji emoji-id='{faction_dict['emoji']['id']}'>{faction_dict['emoji']['base_emoji']}</tg-emoji> <b>{pn['name']}</b> (Фракционное обещание)"

    built = f"""
{name_part}
{pn["description"]}
"""

    return built

async def get_faction(faction_id) -> Dict[Any, Any] | None:
    factions = json.load(open("factions.json", encoding="utf-8"))

    for faction in factions["items"]:
        if faction["id"] == faction_id:
            return faction

    return None


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("faction"))
async def search_faction_handler(message: Message) -> None:
    message_text = message.text
    arguments = message_text.split(" ", 1)[1].split(" ")
    faction_name = arguments[0]

    faction_dict = await get_faction(faction_name)

    name_part = f"<tg-emoji emoji-id='{faction_dict['emoji']['id']}'>{faction_dict['emoji']['base_emoji']}</tg-emoji> <b>{faction_dict['name']}</b>"
    planet_part = f"{faction_dict['planet']['name']} ({faction_dict['planet']['value']})"

    ### Starting Tech Part
    starting_technologies = faction_dict['starting_technologies']
    starting_tech_part = ""

    from utils import TechnologySpeciality
    for tech in starting_technologies:
        speciality = getattr(TechnologySpeciality, tech["color"])
        starting_tech_part += f"{speciality} {tech['name']}"
    ### End of Starting Tech Part


    ### Starting Units Part
    starting_units = faction_dict['starting_units']
    starting_units_part = ""

    for unit in starting_units:
        starting_units_part += f"- {unit['type']} ({unit['count']})\n"

    starting_units_part.rstrip()
    ### End of Starting Units Part


    ### Abilities Part
    abilities = faction_dict['abilities']
    abilities_part = ""

    for ability in abilities:
        abilities_part += f"<b>{ability['name']}</b>: {ability['description']}\n\n"

    abilities_part.rstrip()
    ### End of Abilities Part


    ### Faction Technologies Part
    faction_technologies = faction_dict['faction_technologies']
    faction_technologies_part = ""

    for faction_tech in faction_technologies:
        speciality = getattr(TechnologySpeciality, faction_tech["color"])
        faction_technologies_part += f"{speciality} <b>{faction_tech['name']}</b>: {faction_tech['description']}"

        for prerequisite_color, number in faction_tech["prerequisites"].items():
            speciality = getattr(TechnologySpeciality, prerequisite_color)
            faction_technologies_part += f"\n— Требование: {speciality*number}"

        faction_technologies_part += "\n\n"

    faction_technologies_part.rstrip()
    ### End of Faction Technologies Part

    built = f"""
{name_part}

<b>Домашние планеты</b>: {planet_part}
<b>Начальные технологии</b>: {starting_tech_part}
<b>Начальные отряды:</b>
{starting_units_part}

<b>— Способности —</b>
{abilities_part}

<b>— Фракционные технологии —</b>
{faction_technologies_part}"""

    ### Extra Info / Buttons
    flagship = InlineKeyboardButton(text="Флагман", callback_data=AdditionalInfoCallback(type="flagship", faction="creuss").pack())
    mech = InlineKeyboardButton(text="Мех", callback_data=AdditionalInfoCallback(type="mech", faction="creuss").pack())
    pn = InlineKeyboardButton(text="Фракционное обещание", callback_data=AdditionalInfoCallback(type="prom_note", faction="creuss").pack())

    agent = InlineKeyboardButton(text="Агент", callback_data=AdditionalInfoCallback(type="agent", faction="creuss").pack())
    commander = InlineKeyboardButton(text="Командир", callback_data=AdditionalInfoCallback(type="commander", faction="creuss").pack())
    hero = InlineKeyboardButton(text="Герой", callback_data=AdditionalInfoCallback(type="hero", faction="creuss").pack())

    keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[[flagship, mech], [pn], [agent, commander, hero]])
    ### Extra Info / Buttons End

    # Length test, if needed:
    # await message.answer(str(len(built)))
    await message.answer(built, reply_markup=keyboard_inline)

@dp.callback_query(AdditionalInfoCallback.filter())
async def unit_callback_handler(callback_query: CallbackQuery, callback_data: AdditionalInfoCallback) -> None:
    await callback_query.answer()

    callback_type = callback_data.type
    faction = callback_data.faction

    if callback_type == "flagship":
        flagship = await build_flagship(faction)
        await callback_query.message.edit_text(flagship)

    elif callback_type == "mech":
        mech = await build_mech(faction)
        await callback_query.message.edit_text(mech)

    elif callback_type == "prom_note":
        pn = await build_pn(faction)
        await callback_query.message.edit_text(pn)

    elif callback_type == "agent":
        agent = await Leaders.build_agent(faction)
        await callback_query.message.edit_text(agent)

    elif callback_type == "commander":
        commander = await Leaders.build_commander(faction)
        await callback_query.message.edit_text(commander)

    elif callback_type == "hero":
        hero = await Leaders.build_hero(faction)
        await callback_query.message.edit_text(hero)

    else:
        await callback_query.message.edit_text(f"ошибочка где-то")

@dp.message(Command("catch_emoji"))
async def catch_emoji_handler(message: Message) -> None:
    print(message.entities)

    for entity in message.entities:
        if entity.type == "custom_emoji":
            custom_emoji_id = entity.custom_emoji_id
            custom_emoji_symbol = message.text.split(" ")[1]

            await message.answer(f'...<tg-emoji emoji-id="{custom_emoji_id}">{custom_emoji_symbol}</tg-emoji>...\n{custom_emoji_id} - {custom_emoji_symbol}')

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())