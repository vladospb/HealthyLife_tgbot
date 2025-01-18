from aiogram.fsm.state import State, StatesGroup 

class Profile(StatesGroup):
    weight = State()
    height = State()
    age = State()
    workout_time = State()
    city = State()

class Food(StatesGroup):
    name = State()
    amount = State()