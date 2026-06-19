from aiogram.filters.callback_data import CallbackData


class AdditionalInfoCallback(CallbackData, prefix="addinfo"):
    type: str
    faction: str

class BanCallback(CallbackData, prefix="ban"):
    uuid: str
    ban: str

class ViewFactionsCallback(CallbackData, prefix="viewfactions"):
    faction: str