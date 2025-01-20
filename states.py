from aiogram.fsm.state import State, StatesGroup 

class Profile(StatesGroup):
    weight = State()
    height = State()
    age = State()
    workout_time = State()
    city = State()
    date = State()

class Food(StatesGroup):
    food = State()
    amount = State()
    date = State()

class Water(StatesGroup):
    water_amount = State()
    date = State()

class Workout(StatesGroup):
    workout = State()
    amount = State()
    date = State()