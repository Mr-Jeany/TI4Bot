import asyncio
import itertools
import json
import logging
import os
import random
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputRichMessage

from technologies import get_technology
from utilities.bans.generators import ban_message_generator, ban_buttons_generator, banned_final_message
from utilities.loader import load_all_factions
from utils import AdditionalInfoCallback, BanCallback, ViewFactionsCallback
from models.emoji import UnitsEmoji, CardsEmoji, LeadersEmoji
from uuid import uuid4

FACTIONS: dict | None = None
PROMISSORY_NOTES: dict | None = None
ban_sessions: dict = {}

BOT_TOKEN = os.environ.get("BOT_TOKEN")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Пиши /f и пока вроде ничего больше")

@dp.message(Command("tech"))
async def search_tech_handler(message: Message) -> None:
    message_text = message.text
    arguments = message_text.split(" ", 1)[1].split(" ")
    tech_name = arguments[0]
    tech_object = await get_technology(tech_id_short=tech_name)

    await message.answer(tech_object.full)


@dp.message(Command("faction", "f"))
async def load_faction_handler(message: Message) -> None:
    message_text = message.text
    mt_split = message_text.split(" ", 1)
    if len(mt_split) > 1:
        arguments = mt_split[1].split(" ")
        faction_name = arguments[0]
    else:
        faction_name = ""

    faction_object = FACTIONS.get(faction_name, None)

    if not faction_object:
        buttons_raw = []

        for faction_id, faction_object in FACTIONS.items():
            buttons_raw.append(InlineKeyboardButton(
                text=faction_object.name,
                callback_data=ViewFactionsCallback(faction=faction_id).pack(),
                icon_custom_emoji_id=faction_object.emoji.id
            ))

        buttons_cooked = list(itertools.batched(buttons_raw, 3))

        await message.answer_rich(InputRichMessage(markdown="# Выберите фракцию:"), reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons_cooked))

        return

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
            if unit.unit_type != "flagship":
                button_row.append(
                    InlineKeyboardButton(text=unit.name,
                                         callback_data=AdditionalInfoCallback(type=unit.unit_type, faction=faction_name).pack(),
                                         icon_custom_emoji_id=getattr(UnitsEmoji, unit.unit_type).id)
                )
        if button_row:
            buttons.append(button_row)

    # PN
    button_row = []
    for prom_note_unit in faction_object.promissory_note:
        button_row.append(
            InlineKeyboardButton(text=prom_note_unit.name,
                                 callback_data=AdditionalInfoCallback(type=prom_note_unit.id, faction=faction_name).pack(),
                                 icon_custom_emoji_id=CardsEmoji.prom_note.id)
        )
    buttons.append(button_row)

    # Leaders
    if len(faction_object.agent) == 1:
        button_row = []
        for leader in [faction_object.agent[0], faction_object.commander, faction_object.hero]:
            button_row.append(
                InlineKeyboardButton(text=leader.name,
                                     callback_data=AdditionalInfoCallback(type=leader.type, faction=faction_name).pack(),
                                     icon_custom_emoji_id=getattr(LeadersEmoji, leader.type).id)
            )
        buttons.append(button_row)

    else:
        button_row = []
        for leader in faction_object.agent:
            button_row.append(
                InlineKeyboardButton(text=leader.name,
                                     callback_data=AdditionalInfoCallback(type=leader.id, faction=faction_name).pack(),
                                     icon_custom_emoji_id=getattr(LeadersEmoji, leader.type).id)
            )

        buttons.append(button_row)
        button_row = []
        for leader in [faction_object.commander, faction_object.hero]:
            button_row.append(
                InlineKeyboardButton(text=leader.name,
                                     callback_data=AdditionalInfoCallback(type=leader.type, faction=faction_name).pack(),
                                     icon_custom_emoji_id=getattr(LeadersEmoji, leader.type).id)
            )
        buttons.append(button_row)


    buttons.append(
        [InlineKeyboardButton(text="Назад",
                              callback_data=AdditionalInfoCallback(type="back", faction=faction_name).pack())]
    )
    keyboard_inline = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer_rich(faction_object.full_text, reply_markup=keyboard_inline)

@dp.callback_query(ViewFactionsCallback.filter())
async def view_factions_callback_handler(callback_query: CallbackQuery, callback_data: ViewFactionsCallback) -> None:
    # TODO: Change it and search command to use function to escapre repeating code

    faction_id = callback_data.faction

    message = callback_query.message


    faction_object = FACTIONS[faction_id]
    faction_name = faction_object.id # Who the hell used faction_name instead of faction_id

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
            if unit.unit_type != "flagship":
                button_row.append(
                    InlineKeyboardButton(text=unit.name,
                                         callback_data=AdditionalInfoCallback(type=unit.unit_type,
                                                                              faction=faction_name).pack(),
                                         icon_custom_emoji_id=getattr(UnitsEmoji, unit.unit_type).id)
                )
        if button_row:
            buttons.append(button_row)

    # PN
    button_row = []
    for prom_note_unit in faction_object.promissory_note:
        button_row.append(
            InlineKeyboardButton(text=prom_note_unit.name,
                                 callback_data=AdditionalInfoCallback(type=prom_note_unit.id,
                                                                      faction=faction_name).pack(),
                                 icon_custom_emoji_id=CardsEmoji.prom_note.id)
        )
    buttons.append(button_row)

    # Leaders
    if len(faction_object.agent) == 1:
        button_row = []
        for leader in [faction_object.agent[0], faction_object.commander, faction_object.hero]:
            button_row.append(
                InlineKeyboardButton(text=leader.name,
                                     callback_data=AdditionalInfoCallback(type=leader.type,
                                                                          faction=faction_name).pack(),
                                     icon_custom_emoji_id=getattr(LeadersEmoji, leader.type).id)
            )
        buttons.append(button_row)

    else:
        button_row = []
        for leader in faction_object.agent:
            button_row.append(
                InlineKeyboardButton(text=leader.name,
                                     callback_data=AdditionalInfoCallback(type=leader.type,
                                                                          faction=faction_name).pack(),
                                     icon_custom_emoji_id=getattr(LeadersEmoji, leader.type).id)
            )
        buttons.append(button_row)
        button_row = []
        for leader in [faction_object.commander, faction_object.hero]:
            button_row.append(
                InlineKeyboardButton(text=leader.name,
                                     callback_data=AdditionalInfoCallback(type=leader.type,
                                                                          faction=faction_name).pack(),
                                     icon_custom_emoji_id=getattr(LeadersEmoji, leader.type).id)
            )
        buttons.append(button_row)

    buttons.append(
        [InlineKeyboardButton(text="Назад",
                              callback_data=AdditionalInfoCallback(type="back", faction=faction_name).pack())]
    )

    keyboard_inline = InlineKeyboardMarkup(inline_keyboard=buttons)



    await message.edit_text(rich_message=faction_object.full_text, reply_markup=keyboard_inline)

@dp.callback_query(AdditionalInfoCallback.filter())
async def extra_info_callback_handler(callback_query: CallbackQuery, callback_data: AdditionalInfoCallback) -> None:


    callback_type = callback_data.type
    faction = callback_data.faction

    faction_object = FACTIONS[faction]

    button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                text="Назад",
                callback_data=ViewFactionsCallback(faction=faction_object.id).pack(),
                # icon_custom_emoji_id=faction_object.emoji.id
            )]])

    if callback_type == "flagship" and faction_object.id != "nomad":
        await callback_query.message.edit_text(rich_message=faction_object.flagship.rich_info, reply_markup=button)

    elif callback_type == "mech":
        await callback_query.message.edit_text(rich_message=faction_object.mech.rich_info, reply_markup=button)

    elif callback_type == "promissory_note":
        await callback_query.message.edit_text(rich_message=faction_object.promissory_note.rich_info, reply_markup=button)

    elif callback_type == "agent":
        if len(faction_object.agent) == 1:
            await callback_query.message.edit_text(rich_message=faction_object.agent[0].full, reply_markup=button)

    elif callback_type == "commander":
        await callback_query.message.edit_text(rich_message=faction_object.commander.full, reply_markup=button)

    elif callback_type == "hero":
        await callback_query.message.edit_text(rich_message=faction_object.hero.full, reply_markup=button)

    elif "pn" in callback_type:
        await callback_query.message.edit_text(rich_message=PROMISSORY_NOTES[callback_type].rich_info, reply_markup=button)

    elif "nomad_agent" in callback_type:
        await callback_query.message.edit_text(rich_message=[agent.full for agent in faction_object.agent if agent.id == callback_type][0], reply_markup=button)

    elif callback_type == "back":
        buttons_raw = []

        for faction_id, faction_object in FACTIONS.items():
            buttons_raw.append(InlineKeyboardButton(
                text=faction_object.name,
                callback_data=ViewFactionsCallback(faction=faction_id).pack(),
                icon_custom_emoji_id=faction_object.emoji.id
            ))

        buttons_cooked = list(itertools.batched(buttons_raw, 3))

        await callback_query.message.edit_text(rich_message=InputRichMessage(markdown="# Выберите фракцию:"),
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons_cooked))

        return

    else:
        item = [x for x in faction_object.faction_specific_units if x.unit_type == callback_type][0]

        await callback_query.message.edit_text(rich_message=item.rich_with_upgrade, reply_markup=button)

# Command for getting ban order
@dp.message(Command("ban_order", "bo"))
async def ban_order_handler(message: Message) -> None:
    message_text = message.text
    arguments = message_text.split(" ", 1)[1].split(" ")

    random.shuffle(arguments)
    order = arguments.copy()

    uuid = str(uuid4())
    ban_sessions[uuid] = {
        "order": order,
        "banned_factions": [],
        "immune_factions": ["letnev", "saar", "creuss", "mentak", "naalu", "sardakk", "jolnar", "nomad"],
        "current_person_index": 0
    }

    print(ban_sessions)

    buttons_cooked = await ban_buttons_generator(FACTIONS, uuid, ban_sessions[uuid])

    generated_message = await ban_message_generator(FACTIONS, uuid, ban_sessions[uuid])

    await message.answer_rich(generated_message, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons_cooked))

@dp.callback_query(BanCallback.filter())
async def ban_callback_handler(callback_query: CallbackQuery, callback_data: BanCallback) -> None:
    uuid = callback_data.uuid
    ban = callback_data.ban

    session = ban_sessions[uuid]

    if ban in session["banned_factions"]:
        generated_message = await ban_message_generator(FACTIONS, uuid, ban_sessions[uuid], comment="## Это фракция уже в бане!")
        buttons_cooked = await ban_buttons_generator(FACTIONS, uuid, ban_sessions[uuid])

        try:
            await callback_query.message.edit_text(rich_message=generated_message,
                                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons_cooked))
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise

        return


    session["banned_factions"].append(ban)

    if session["current_person_index"] == len(session["order"]) - 1:
        generated_message = await banned_final_message(FACTIONS, uuid, ban_sessions[uuid])

        try:
            await callback_query.message.edit_text(rich_message=generated_message)
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise

        del ban_sessions[uuid]
        return

    session["current_person_index"] += 1

    generated_message = await ban_message_generator(FACTIONS, uuid, ban_sessions[uuid])
    buttons_cooked = await ban_buttons_generator(FACTIONS, uuid, ban_sessions[uuid])

    try:
        await callback_query.message.edit_text(rich_message=generated_message,
                                             reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons_cooked))
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@dp.message(Command("catch_emoji"))
async def catch_emoji_handler(message: Message) -> None:
    print(message.entities)

    for entity in message.entities:
        if entity.type == "custom_emoji":
            custom_emoji_id = entity.custom_emoji_id
            custom_emoji_symbol = message.text.split(" ")[1]

            await message.answer(f'...<tg-emoji emoji-id="{custom_emoji_id}">{custom_emoji_symbol}</tg-emoji>...\n<code>{custom_emoji_id}</code> - <code>{custom_emoji_symbol}</code>')


async def main() -> None:
    global FACTIONS, PROMISSORY_NOTES
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # TODO: Add loader for all faction and in the future for all techs etc etc

    FACTIONS = await load_all_factions(json.load(open("data/factions.json", encoding="utf-8")))
    FACTIONS = dict(sorted(FACTIONS.items(), key=lambda item: item[1].name))

    PROMISSORY_NOTES = {}
    for faction in FACTIONS.values():
        for promissory_notes in faction.promissory_note:
            PROMISSORY_NOTES[promissory_notes.id] = promissory_notes

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())