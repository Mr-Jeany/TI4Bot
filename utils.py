from aiogram.filters.callback_data import CallbackData


class AdditionalInfoCallback(CallbackData, prefix="addinfo"):
    type: str
    faction: str

class BanCallback(CallbackData, prefix="ban"):
    banned_factions: list
    immune_factions: list
    ban_order: list
    current_person_index: int