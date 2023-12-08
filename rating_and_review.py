from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from States import UserState
from aiogram.types import(ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton)
from call_back import MyCallback
from aiogram.types import CallbackQuery
from review_rating_data import add_rating_and_review,get_all_ratings_and_reviews
from add_users_to_database import get_name
review_rating = Router()

@review_rating.callback_query(MyCallback.filter(F.data.startswith("Review")))
async def review_handler(query : CallbackQuery, callback_data: MyCallback,state : FSMContext):
    userId = callback_data.id
    print(userId,"User Id")
    reviews = await get_all_ratings_and_reviews(userId)
    text = ""
    for review in reviews:
        # review, rating, name
        text += f"🌟 Rating: {review[2]}\n" if review[2] else ""
        text += f"💬 Review: {review[1]}\n" if review[1] else ""
        text += f"👤 Name: {review[3]}\n" if review[3] else ""
        text += "\n"

    if text:
        reply_message = f"📜 **List of Reviews and Ratings** 📜\n\n{text}"
    else:
        reply_message = "No reviews available."

    await query.message.reply(reply_message, parse_mode="Markdown")


@review_rating.callback_query(MyCallback.filter(F.data.startswith("arrive")))
async def review_handler(query : CallbackQuery, callback_data: MyCallback,state : FSMContext):
    _,userId = callback_data.data.split("_")
    data = await state.get_data()
    name = await get_name(data["userId"])
    print(data["userId"])
    print(name,"name review handleer")
    await query.message.answer("Pleas Provide a Review")
    await state.set_state(UserState.review)
    await state.update_data(data = {"userId" : userId})
    await state.update_data(data = {"name" : name[0]})

@review_rating.message(UserState.review)
async def review_handler(message : Message,state : FSMContext):
    await message.answer("Please select Rating")
    await state.update_data(data= {"review" : message.text})
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⭐️",callback_data=MyCallback(data="star_⭐️",id= 1).pack())],
    [InlineKeyboardButton(text="⭐️⭐️",callback_data=MyCallback(data="star_⭐️⭐️",id= 1).pack())],
    [InlineKeyboardButton(text="⭐️⭐️⭐️",callback_data=MyCallback(data="star_⭐️⭐️⭐️",id= 1).pack())],
    [InlineKeyboardButton(text="⭐️⭐️⭐️⭐️",callback_data=MyCallback(data="star_⭐️⭐️⭐️⭐️",id= 1).pack())],
    [InlineKeyboardButton(text="⭐️⭐️⭐️⭐️⭐️",callback_data= MyCallback(data="star_⭐️⭐️⭐️⭐️⭐️",id= 1).pack())],
    ])
    await message.reply("please provide a rating",reply_markup=markup)

@review_rating.callback_query(MyCallback.filter(F.data.startswith("star")))
async def handle_review(query : CallbackQuery , callback_data : MyCallback,state : FSMContext):
    _,stars = callback_data.data.split("_")
    data = await state.get_data()
    review = data["review"]
    userId = data["userId"]
    name = data["name"]
    await add_rating_and_review(userId,review,stars,name)