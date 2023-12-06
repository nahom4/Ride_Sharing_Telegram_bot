from aiogram import Router,F
from aiogram.types import CallbackQuery
from call_back import MyCallback
from ride_booking_data import get_all_booking
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

history = Router()
@history.callback_query(MyCallback.filter(F.data == "History and Receipts"))
async def handle_history(query : CallbackQuery,callback_data: MyCallback):
    requests  = await get_all_booking(userId=callback_data.id)
    text = "History:\n"
    text += "Status - Date - Driver"
    for request in requests:
        text += f"{request[1]} - {request[2]} - {request[3]}\n"

    await query.message.reply(text)
