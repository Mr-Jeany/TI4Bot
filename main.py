import asyncio
import logging
import os
import random
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputRichMessage

from builders import build_flagship, build_mech, build_pn, MessageParts, build_fsu
from models.planet import Planet
from models.unit import Unit, UnitType
from technologies import get_technology
from utilities.loader import load_faction
from utils import AdditionalInfoCallback, Leaders, get_faction, UnitsEmoji, CardsEmoji, LeadersEmoji
from tabulate import tabulate

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command("tech"))
async def search_tech_handler(message: Message) -> None:
    message_text = message.text
    arguments = message_text.split(" ", 1)[1].split(" ")
    tech_name = arguments[0]
    tech_object = await get_technology(tech_id_short=tech_name)

    await message.answer(tech_object.full)

@dp.message(Command("unit"))
async def search_unit_handler(message: Message) -> None:
    message_text = message.text
    arguments = message_text.split(" ", 1)[1].split(" ")
    unit_name = arguments[0]

    unit = Unit(
        id=unit_name,
        unit_type=UnitType.WARSUN,
        name="Unit Name",
        description="Description",
        abilities=[],
        cost=1,
        combat=2,
        number_of_attacks=1
    )

    await message.answer(unit.short)


@dp.message(Command("flagship"))
async def flagship_handler(message: Message) -> None:
    message_text = message.text
    arguments = message_text.split(" ", 1)[1].split(" ")
    faction_name = arguments[0]

    faction_dict = await get_faction(faction_name)

    flagship = Unit(f"{faction_name}_{UnitType.FLAGSHIP.lower()}", UnitType.FLAGSHIP, **faction_dict["flagship"])

    await message.answer(f"{flagship.short}")


@dp.message(Command("faction"))
async def load_faction_handler(message: Message) -> None:
    message_text = message.text
    arguments = message_text.split(" ", 1)[1].split(" ")
    faction_name = arguments[0]

    faction_dict = await get_faction(faction_name)

    faction_object = await load_faction(faction_name, faction_dict)

    buttons = []

    # TODO: Change buttons below to a data-driven system

    # Flagship and mech
    button_row = []
    button_row.append(
        InlineKeyboardButton(text=faction_object.flagship.name,
                             callback_data=AdditionalInfoCallback(type="flagship", faction=faction_name).pack(),
                             icon_custom_emoji_id=UnitsEmoji.flagship.id)
    )

    button_row.append(
        InlineKeyboardButton(text=faction_object.mech.name,
                             callback_data=AdditionalInfoCallback(type="mech", faction=faction_name).pack(),
                             icon_custom_emoji_id=UnitsEmoji.mech.id)
    )
    buttons.append(button_row)

    # FSU
    if faction_object.faction_specific_units:
        button_row = []
        for unit in faction_object.faction_specific_units:
            button_row.append(
                InlineKeyboardButton(text=unit.name,
                                     callback_data=AdditionalInfoCallback(type=unit.unit_type, faction=faction_name).pack(),
                                     icon_custom_emoji_id=getattr(UnitsEmoji, unit.unit_type).id)
            )
    buttons.append(button_row)

    # PN
    button_row = []
    button_row.append(
        InlineKeyboardButton(text=faction_object.promissory_note.name,
                             callback_data=AdditionalInfoCallback(type="promissory_note", faction=faction_name).pack(),
                             icon_custom_emoji_id=CardsEmoji.prom_note.id)
    )
    buttons.append(button_row)

    # Leaders
    button_row = []
    for leader in [faction_object.agent, faction_object.commander, faction_object.hero]:
        button_row.append(
            InlineKeyboardButton(text=leader.name,
                                 callback_data=AdditionalInfoCallback(type=leader.type, faction=faction_name).pack(),
                                 icon_custom_emoji_id=getattr(LeadersEmoji, leader.type).id)
        )
    buttons.append(button_row)


    keyboard_inline = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer_rich(faction_object.full_text, reply_markup=keyboard_inline)


# Command for getting ban order
@dp.message(Command("shuffle"))
async def shuffle_things_handler(message: Message) -> None:
    message_text = message.text
    arguments = message_text.split(" ", 1)[1].split(";")

    random.shuffle(arguments)

    await message.answer(f"Случайный порядок:\n- {'\n- '.join(arguments)}")


@dp.callback_query(AdditionalInfoCallback.filter())
async def extra_info_callback_handler(callback_query: CallbackQuery, callback_data: AdditionalInfoCallback) -> None:
    await callback_query.answer()

    callback_type = callback_data.type
    faction = callback_data.faction

    faction_dict = await get_faction(faction)

    faction_object = await load_faction(faction, faction_dict)

    if callback_type == "flagship":
        await callback_query.message.delete()
        await callback_query.message.answer_rich(faction_object.flagship.rich_info)

    elif callback_type == "mech":
        await callback_query.message.delete()
        await callback_query.message.answer_rich(faction_object.mech.rich_info)

    elif callback_type == "promissory_note":
        await callback_query.message.delete()
        await callback_query.message.answer_rich(faction_object.promissory_note.rich_info)

    elif callback_type == "agent":
        await callback_query.message.delete()
        await callback_query.message.answer_rich(faction_object.agent.full)

    elif callback_type == "commander":
        await callback_query.message.delete()
        await callback_query.message.answer_rich(faction_object.commander.full)

    elif callback_type == "hero":
        await callback_query.message.delete()
        await callback_query.message.answer_rich(faction_object.hero.full)

    else:
        await callback_query.message.delete()

        item = [x for x in faction_object.faction_specific_units if x.unit_type == callback_type][0]

        await callback_query.message.answer_rich(item.rich_with_upgrade)



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

    # TODO: Add loader for all faction and in the future for all techs etc etc

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())