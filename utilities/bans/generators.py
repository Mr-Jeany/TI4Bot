import itertools

from aiogram.types import InputRichMessage, InlineKeyboardButton
from tabulate import tabulate

from models.faction import Faction
from utils import BanCallback


async def ban_message_generator(factions: dict[str, Faction],
                                uuid: str,
                                ban_data: dict,
                                comment: str = None):
    ban_order = ban_data["order"]
    headers = [str(x) for x in range(1, len(ban_order) + 1)]

    banned_factions = ban_data["banned_factions"]

    banned_line = None
    if banned_factions:
        banned_line = " ".join([factions[faction].emoji.rich for faction in banned_factions])

    table = tabulate(
        [ban_order],
        headers=headers,
        tablefmt="pipe",
        colalign=["left"] * len(headers),
    )

    buffer = f"""
# 🚫 Баны

### Очередь: {ban_order[ban_data["current_person_index"]]}

{"Забанены: " + banned_line if banned_line else ""}

{table}

{'\n---\n' + comment if comment else ''}
"""

    return InputRichMessage(markdown=buffer)

async def ban_buttons_generator(factions: dict[str, Faction],
                                uuid: str,
                                ban_data: dict):
    buttons_raw = []
    for faction_name, faction_object in factions.items():
        if faction_object.id in ban_data["banned_factions"]:
            buttons_style = "danger"
        elif faction_object.id in ban_data["immune_factions"]:
            buttons_style = "success"
        else:
            buttons_style = None

        buttons_raw.append(InlineKeyboardButton(
            text=faction_object.name,
            callback_data=BanCallback(uuid=uuid, ban=faction_object.id).pack(),
            icon_custom_emoji_id=faction_object.emoji.id,
            style=buttons_style
        ))

    buttons_cooked = list(itertools.batched(buttons_raw, 5))

    return buttons_cooked

async def banned_final_message(factions: dict[str, Faction],
                               uuid: str,
                               ban_data: dict,
                               comment: str = None):
    ban_order = ban_data["order"]

    banned_factions = ban_data["banned_factions"]

    banned_line = None
    if banned_factions:
        banned_line = " ".join([factions[faction].emoji.rich for faction in banned_factions])

    allowed_line = " ".join([faction_object.emoji.rich for faction_id, faction_object in factions.items() if faction_object.id not in ban_data["banned_factions"]])

    buffer = f"""
# 🚫 Баны

{"**Забанены: **" + banned_line if banned_line else ""}

{"**Разрешены:**\n" + allowed_line}

{'\n---\n' + comment if comment else ''}

---

*Игроки: {', '.join(ban_order)}*
"""

    return InputRichMessage(markdown=buffer)