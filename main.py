import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from builders import build_flagship, build_mech, build_pn, MessageParts, build_fsu
from utils import AdditionalInfoCallback, Leaders, get_faction, UnitsEmoji, CardsEmoji, LeadersEmoji

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

dp = Dispatcher()

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

    faction_specific_units, fsu_buttons = await MessageParts.faction_specific_units(faction_name)

    built = f"""
{name_part}

<b>Домашние планеты</b>: {planet_part}
<b>Начальные технологии</b>: {starting_tech_part}
<b>Начальные отряды:</b>
{starting_units_part}

<b>— Способности —</b>
{abilities_part}
{f"\n<b>— Особые отряды —</b>\n{faction_specific_units}\n" if faction_specific_units else ""}
<b>— Фракционные технологии —</b>
{faction_technologies_part}"""

    ### Extra Info / Buttons
    extra_info_values = {
        UnitsEmoji: {
            "flagship": "Флагман",
            "mech": "Мех"
        },

        CardsEmoji: {
            "prom_note": "Фракционное обещание"
        },

        LeadersEmoji: {
            "agent": "Агент",
            "commander": "Командир",
            "hero": "Герой"
        }
    }

    buttons = []
    for extra_info_emoji, extra_info in extra_info_values.items():
        button_row = []
        for extra_info_id, extra_info_name in extra_info.items():
            button_row.append(
                InlineKeyboardButton(text=extra_info_name,
                                     callback_data=AdditionalInfoCallback(type=extra_info_id, faction=faction_name).pack(),
                                     icon_custom_emoji_id=getattr(extra_info_emoji, extra_info_id).id)
            )

        buttons.append(button_row)

    if faction_specific_units:
        custom_units = []

        for unit in fsu_buttons:
            custom_units.append(
                InlineKeyboardButton(text=unit["name"],
                                     callback_data=AdditionalInfoCallback(type=unit["type"], faction=faction_name).pack(),
                                     icon_custom_emoji_id=unit["icon_custom_emoji_id"])
            )

        buttons.insert(1, custom_units)
        keyboard_inline = InlineKeyboardMarkup(inline_keyboard=buttons)
    else:
        keyboard_inline = InlineKeyboardMarkup(inline_keyboard=buttons)
    ### Extra Info / Buttons End

    # Length test, if needed:
    # await message.answer(str(len(built)))
    await message.answer(built, reply_markup=keyboard_inline)

@dp.callback_query(AdditionalInfoCallback.filter())
async def extra_info_callback_handler(callback_query: CallbackQuery, callback_data: AdditionalInfoCallback) -> None:
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

    elif callback_type in ["warsun"]:
        unit = await build_fsu(faction, callback_type)
        await callback_query.message.edit_text(
            unit
        )

    else:
        await callback_query.message.edit_text(f"ошибочка где-то")

@dp.message(Command("catch_emoji"))
async def catch_emoji_handler(message: Message) -> None:
    print(message.entities)

    for entity in message.entities:
        if entity.type == "custom_emoji":
            custom_emoji_id = entity.custom_emoji_id
            custom_emoji_symbol = message.text.split(" ")[1]

            await message.answer(f'...<tg-emoji emoji-id="{custom_emoji_id}">{custom_emoji_symbol}</tg-emoji>...\n<code>{custom_emoji_id}</code> - <code>{custom_emoji_symbol}</code>')

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())