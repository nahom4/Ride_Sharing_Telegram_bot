from aiogram.fsm.state import State, StatesGroup
class UserState(StatesGroup):
    get_name = State()
    get_role = State()
    start_position = State()
    user_info_collected = State()
    destination = State()
    complete = State()
    notify_driver = State()
    book_ride = State()
    change_profile = State()
    history_and_receipts = State()
    review = State()
    new_name = State()