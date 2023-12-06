from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from States import UserState
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,ReplyKeyboardRemove,InlineKeyboardMarkup,InlineKeyboardButton)
from aiogram.types import CallbackQuery
from User import User
from add_users_to_database import add_user
from call_back import MyCallback
process_user_info = Router()

@process_user_info.callback_query(MyCallback.filter(F.data == "signup"))
async def handle_signUp(query : CallbackQuery, state : FSMContext):
    await query.answer("What is you name")
    await state.set_state(UserState.get_name)

@process_user_info.message(UserState.get_name)
async def process_name(message : Message,state : FSMContext):
    await state.update_data(data= {"name" : message.text})
    await state.set_state(UserState.get_role)
    await state.update_data(data={"userId" : message.from_user.id})
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = "Driver 🚗",callback_data= MyCallback(data="role", id= 1).pack()),InlineKeyboardButton(text = "Passenger 👤",callback_data= MyCallback(data = "role",id = 2).pack())]])
    await message.reply("Please select your role",reply_markup = markup)
    
@process_user_info.callback_query(MyCallback.filter(F.data == "role"))
async def process_role(query : CallbackQuery, callback_data: MyCallback,state : FSMContext):
    role = "Driver" if callback_data.id == 1 else "Passenger"
    await state.update_data(data= {"role" : role})
    await state.set_state(UserState.user_info_collected)
    data = await state.get_data()
    userId = data["userId"]
    user = User(userId=data["userId"],name=data["name"],role=data["role"])
    await add_user(user)
    keyboard = InlineKeyboardMarkup(inline_keyboard=
    [ [InlineKeyboardButton(text = "Book Ride 🚗", callback_data=MyCallback(data = "BookRide",id = userId).pack()), InlineKeyboardButton(text = "Change Profile 🔄", callback_data=MyCallback(data="Change Profile",id= userId).pack())],
       [InlineKeyboardButton(text = "Review ⭐", callback_data= MyCallback(data= "Review",id= userId).pack()), InlineKeyboardButton(text = "History and Receipts 📜", callback_data= MyCallback(data = "History and Receipts",id = userId).pack())]]
    )
    if callback_data.id == 2:
        await query.message.reply("Choose an option:", reply_markup=keyboard)
    else:
        await query.message.reply("You will be notified when a passenger is available")
   


    