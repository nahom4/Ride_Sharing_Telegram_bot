from aiogram.filters.callback_data import CallbackData
class MyCallback(CallbackData, prefix="my"):
    data: str
    id: int