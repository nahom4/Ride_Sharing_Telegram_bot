from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from States import UserState
from aiogram.types import(ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton)
from call_back import MyCallback
from aiogram.types import CallbackQuery
book_ride = Router()
@book_ride.callback_query(MyCallback.filter(F.data == "BookRide"))
async def book_ride_handler(query : CallbackQuery, callback_data: MyCallback,state : FSMContext):
    await query.message.answer("Enter starting position")
    await state.set_state(UserState.start_position)

@book_ride.message(UserState.start_position)  
async def handle_initial_location(message : Message,state : FSMContext):
    await state.update_data(data={"start_position" : message.text})
    await state.set_state(UserState.destination)
    await message.answer("Enter destination")

@book_ride.message(UserState.destination)
async def handle_destination(message : Message, state : FSMContext):
    await state.update_data(data={"destination" : message.text})
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = "Yes",callback_data=MyCallback(data="alert driver",id=1).pack()),InlineKeyboardButton(text = "No",callback_data = MyCallback(data="don't alert",id= 2).pack())]
    ],resize_keyboard=True) 
    await message.reply("Should I notify drivers",reply_markup=reply_markup)
    await state.set_state(UserState.notify_driver)
    await state.update_data(data= {"userId" : f"{message.from_user.id}"})





    