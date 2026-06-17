from aiogram.filters.callback_data import CallbackData


class AdditionalInfoCallback(CallbackData, prefix="addinfo"):
    type: str
    faction: str
