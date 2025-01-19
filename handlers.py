from aiogram import Router
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from states import Profile, Food
from aiogram import F
import aiohttp
from database import save_profile
from log_food_database import log_food
from get_food_info import get_food_info
from openwheather_api import get_temperature

router = Router()

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    username = message.from_user.username
    id = message.from_user.id
    await message.answer(f'{username}, {id}')

# Обработчик команды /help
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply(
        """Доступные команды:
        /start - Начало работы
        /set_profile - Настройка профиля
        /keyboard - Пример кнопок
        /log_water - Отчет о выпитом
        /log_food - Отчет о съеденном
        /log_workout - Отчет о тренировке"""
        )

# Обработчик команды /set_profile
@router.message(Command("set_profile"))
async def start_profile(message: Message, state: FSMContext):
    await message.reply("Введи свой вес (в кг)")
    await state.set_state(Profile.weight)

@router.message(Profile.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.reply("Введи свой рост (в см)")
    await state.set_state(Profile.height)

@router.message(Profile.height)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.reply("Введи свой возраст")
    await state.set_state(Profile.age)

@router.message(Profile.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply("Сколько минут активности у тебя в день?")
    await state.set_state(Profile.workout_time)

@router.message(Profile.workout_time)
async def process_workout_time(message: Message, state: FSMContext):
    await state.update_data(workout_time=message.text)
    await message.reply("В каком городе ты находишься?")
    await state.set_state(Profile.city)

@router.message(Profile.city)
async def process_city(message: Message, state: FSMContext):
    data = await state.get_data()
    weight = data.get('weight')
    height = data.get('height')
    age = data.get('age')
    workout_time = data.get('workout_time')
    city = message.text
    save_profile(f"'{message.from_user.id}'", f"'{message.from_user.username}'", f"'{weight}'", f"'{height}'", f"'{age}'", f"'{workout_time}'", f"'{city}'")
    await message.reply(f'Норма воды - {round(float(weight) * 0.03, 1)} л/день\nНорма калорий - {round(10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 5 * float(workout_time), -2)} ККалл/день')
    await state.clear()

# Обработчик команды /log_food
@router.message(Command("log_food"))
async def start_log_food(message: Message, state: FSMContext):
    await state.update_data(food=message.text)
    kall_per_100 = get_food_info(message.text)
    await state.update_data(kall_per_100=kall_per_100)
    await message.reply(f"{message.text} — {kall_per_100} ккал на 100 г. Сколько грамм вы съели?")
    await state.set_state(Food.amount)

@router.message(Food.amount)
async def process_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    food = data.get('food').replace('/log_food ', '')
    kall_per_100 = data.get('kall_per_100')
    amount = message.text
    calories = round((int(kall_per_100) if kall_per_100 != None else 0) * float(float(amount) / 100), 1)
    log_food(message.from_user.id, food, amount, calories)
    await message.reply(f'Записано: {calories} ккал.')
    await state.clear()

# Хендлер на команду /weight_input

# Хендлер на команду /height_input

# Хендлер на команду /a_input

# Хендлер на команду /weight_input

# Хендлер на команду /weight_input

# Хендлер на сообщение без команды
@router.message(F.text)
async def msg_without_com(message: Message):
    text = message.text
    print(type(text))
    check = 'тоже' in text.lower() or 'и я' in text.lower()
    # Отправляем новое сообщение с добавленным текстом
    await message.reply(
        '<3' if check else '=('
        )