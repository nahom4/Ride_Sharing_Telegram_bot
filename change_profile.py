from aiogram import Router,F
from aiogram.types import CallbackQuery
from States import UserState
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
from aiogram.fsm.context import FSMContext
from add_users_to_database import update_user_name
profile = Router()
@profile.callback_query(MyCallback.filter(F.data == "Change Profile"))
async def handle_change_profile(query : CallbackQuery,callback_data: MyCallback):
    userId = callback_data.id
    markUp = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Change Name",callback_data= MyCallback(data = "change name",id = userId).pack())]])
    await query.message.answer("Change You Name",reply_markup=markUp)

@profile.callback_query(MyCallback.filter(F.data == "change name"))
async def handle_change_profile(query : CallbackQuery,callback_data: MyCallback,state : FSMContext):
    userId = callback_data.id
    await query.message.answer("Enter new Name")
    await state.set_state(UserState.new_name)
    await state.update_data(data= {"id" : userId})

@profile.message(UserState.new_name)
async def handle_change_profile(message : Message,state : FSMContext):
    data = await state.get_data()
    await update_user_name(data["id"],message.text)

    
