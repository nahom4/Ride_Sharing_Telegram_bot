import asyncio
from datetime import datetime
import logging
from change_profile import profile

import sys
from os import getenv
from dotenv import load_dotenv
from aiohttp import web
from aiogram.fsm.storage import redis
from aiogram import F,Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from User import User
from States import UserState
from book_ride import book_ride
from get_drivers import get_drivers
from ride_booking_data import get_ride_booking,add_booking_data,update_booking_data
from process_user_information import process_user_info
from add_users_to_database import get_name
load_dotenv()
from history import history
from rating_and_review import review_rating
TOKEN = getenv("TOKEN")
WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8080
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_SECRET = "my-secret"
router = Router()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
hashMap = dict()
from call_back import MyCallback

@router.message(CommandStart())
async def handle_initial_contact(message : Message):

    userId = message.from_user.id
    name  = await get_name(userId)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = "🏠 Home",callback_data=MyCallback(data ="Menu",id = userId).pack())]])
    markup = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text="Signup 📝", callback_data =MyCallback(data="signup",id=1).pack())
    ]])

    await message.reply(
        "Welcome",
        reply_markup= keyboard if name else markup
    )
    
@router.callback_query(MyCallback.filter(F.data == "alert driver"))
async def alert_every_driver(query : CallbackQuery,state : FSMContext):
    driver_list = await get_drivers()
    print(driver_list,"hellooooooooooooooooooooooooooooooo")
    data  = await state.get_data()
    passenger_id = data["userId"]
    ride_request_id = f"request_{passenger_id}"
    passenger_name = await get_name(passenger_id)
    passenger_name = passenger_name[0]
    print(passenger_name, "name")
    start = data["start_position"]
    destination = data["destination"]
    await add_booking_data(passenger_id,"pending",datetime.now().strftime("%Y-%m-%d"))
    hashMap[f"{passenger_id}"] = {"passenger_id" : passenger_id,"status" : "pending"}
    for driver in driver_list:
        driver_id = driver[0]
        print(driver_id)
        await bot.send_message(driver_id, f"New ride request from passenger {passenger_name} \n start : {start}  destination : {destination}")
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text="Accept 👍", callback_data =MyCallback(data=f"accept_{passenger_id}",id=driver_id).pack())
    ]])

        await bot.send_message(driver_id, "Do you want to accept this ride request?", reply_markup=inline_keyboard)

@router.callback_query(MyCallback.filter(F.data.startswith('accept')))
async def accept_ride(callback_query:CallbackQuery,callback_data: MyCallback):
    _, ride_request_id = callback_data.data.split("_")
    driver_id = callback_data.id
    _,status,date,_ = await get_ride_booking(ride_request_id)
    name = await get_name(driver_id)
    passenger_inline_keyboard = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text="Arrived at Destination 📍🏁", callback_data =MyCallback(data=f"arrived_{driver_id}",id=driver_id).pack())
    ]])
    
    driver_inline_keyboard = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text="Arrived at Destination 📍🏁", callback_data =MyCallback(data=f"arrived_{ride_request_id}",id=ride_request_id).pack())
    ]])
    if status == "pending":
        await update_booking_data(ride_request_id,"accepted",date,name)
        await bot.send_message(driver_id,"Click this button when you reach your destination", reply_markup=driver_inline_keyboard)
        await bot.send_message(ride_request_id, f"Your ride request has been accepted by driver {name}")
        await bot.send_message(ride_request_id,"Click this button when you reach your destination", reply_markup=passenger_inline_keyboard)


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(book_ride)
    dp.include_router(process_user_info)
    dp.include_router(history)
    dp.include_router(review_rating)
    dp.include_router(profile)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())