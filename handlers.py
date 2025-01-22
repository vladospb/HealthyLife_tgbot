from aiogram import Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import sklearn
import joblib
from states import Profile, Food, Water, Workout
from databases.profile_database import save_profile, get_profile_info
from databases.log_food_database import log_food, get_food_calories
from databases.log_water_database import log_water, get_water_amount
from databases.log_workout_database import log_workout, get_workout_calories
from api.gpt_api import get_food_info, get_workout_info
from api.openwheather_api import get_temperature

router = Router()
BASE_PROFILE = [80, 170, 40, 'Saint-Petersurg']
calories_calc_model = joblib.load('LinearRegr/calories_calc.pkl')

# Обработчик нажатий на кнопки
@router.message(Command("keyboard"))
async def show_keyboard(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Создать профиль', callback_data='btn1')],
            [InlineKeyboardButton(text='Список команд', callback_data='btn2')],
            [InlineKeyboardButton(text='Съел', callback_data='btn3')],
            [InlineKeyboardButton(text='Выпил', callback_data='btn4')],
            [InlineKeyboardButton(text='Потренировался', callback_data='btn5')],
            [InlineKeyboardButton(text='Прогресс', callback_data='btn6')]
        ]
    )
    await message.reply('Выберите опцию:', reply_markup=keyboard)



# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    username = message.from_user.username
    await message.answer(f"Добро пожаловать, {username}!\nВведи /help для списка команд:")



# Обработчик команды /help
@router.callback_query(lambda call: call.data == 'btn2')
async def handle_help_button(call: types.CallbackQuery):
    await call.answer()
    await cmd_help(call.message)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply(
        """Доступные команды:
        /start - Начало работы
        /help - Список команд
        /set_profile - Создание профиля
        /keyboard - Кнопки
        /log_water - Добавление выпитой воды
        /log_food - Добавление съеденной еды
        /log_workout - Добавление выполненной тренировки
        /check_progress - Проверить свой прогресс за сегодня"""
        )



# Обработчик команды /set_profile
@router.callback_query(lambda call: call.data == 'btn1')
async def handle_profile_button(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await start_profile(call.message, state)

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
    save_profile(message.from_user.id, message.date.strftime("%Y-%m-%d"), message.from_user.username, weight, height, age, workout_time, city)
    city_temperature = get_temperature(city)
    water_norm = round(float(weight) * 0.03 + max(0, (city_temperature - 20) / 5) * 0.25 + float(workout_time) / 60 * 0.5, 1)
    food_norm = round(calories_calc_model.predict([[float(weight), float(height), float(age)]])[0] + 5 * float(workout_time), -2)
    await message.reply(f'Норма воды - {water_norm} л/день\nНорма калорий - {food_norm} ККалл/день\n/keyboard')
    await state.clear()



# Обработчик команды /log_food
@router.callback_query(lambda call: call.data == 'btn3')
async def handle_log_food_button(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await start_log_food(call.message, state)

@router.message(Command("log_food"))
async def start_log_food(message: Message, state: FSMContext):
    await message.reply('Напиши название продукта, который съел')
    await state.set_state(Food.food)

@router.message(Food.food)
async def process_workout_time(message: Message, state: FSMContext):
    await state.update_data(food=message.text)
    kall_per_100 = get_food_info(message.text)
    await state.update_data(kall_per_100=kall_per_100)
    await state.update_data(workout_time=message.text)
    await message.reply(f"{message.text} — {kall_per_100} ккал на 100 г. Сколько грамм съел?")
    await state.set_state(Food.amount)

@router.message(Food.amount)
async def process_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    food = data.get('food')
    kall_per_100 = data.get('kall_per_100')
    amount = message.text
    calories = round((int(kall_per_100) if kall_per_100 != None else 0) * float(float(amount) / 100), 1)
    log_food(message.from_user.id, message.date.strftime("%Y-%m-%d"), food, amount, calories)
    await message.reply(f'Записано: {calories} ккал.\n/keyboard')
    await state.clear()



# Обработчик команды /log_water
@router.callback_query(lambda call: call.data == 'btn4')
async def handle_log_water_button(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await start_log_water(call.message, state)

@router.message(Command("log_water"))
async def start_log_water(message: Message, state: FSMContext):
    await message.reply('Сколько выпил воды в миллилитрах?')
    await state.set_state(Water.water_amount)

@router.message(Water.water_amount)
async def process_water(message: Message, state: FSMContext):
    water_amount = message.text
    log_water(message.from_user.id, message.date.strftime("%Y-%m-%d"), water_amount)
    await message.reply(f'Записано: {water_amount} мл.\n/keyboard')
    await state.clear()



# Обработчик команды /log_workout
@router.callback_query(lambda call: call.data == 'btn5')
async def handle_log_workout_button(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await start_log_workout(call.message, state)

@router.message(Command("log_workout"))
async def start_log_workout(message: Message, state: FSMContext):
    await message.reply('Напиши название активности, которую выполнил')
    await state.set_state(Workout.workout)

@router.message(Workout.workout)
async def process_workout_time(message: Message, state: FSMContext):
    await state.update_data(workout=message.text)
    kall_per_min = get_workout_info(message.text)
    await state.update_data(kall_per_min=kall_per_min)
    await state.update_data(workout_time=message.text)
    await message.reply(f"{message.text} — {kall_per_min} ккал на 1 мин. Сколько минут выполнял?")
    await state.set_state(Workout.amount)

@router.message(Workout.amount)
async def process_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    workout = data.get('workout')
    kall_per_min = data.get('kall_per_min')
    amount = message.text
    calories = round((int(kall_per_min) if kall_per_min != None else 0) * float(amount), 1)
    log_workout(message.from_user.id, message.date.strftime("%Y-%m-%d"), workout, amount, calories)
    await message.reply(f'Записано: -{calories} ккал.\n/keyboard')
    await state.clear()



# Обработчик команды /check_progress
@router.callback_query(lambda call: call.data == 'btn6')
async def handle_check_progress_button(call: types.CallbackQuery):
    await call.answer()
    id = call.from_user.id
    await cmd_check_progress(call.message, id)

@router.message(Command("check_progress"))
async def cmd_check_progress(message: types.Message, id: int = None):
    if id is None:
        id = message.from_user.id
    date = message.date.strftime("%Y-%m-%d")
    try:
        weight, height, age, city = get_profile_info(id)
    except:
        weight, height, age, city = BASE_PROFILE
    city_temperature = get_temperature(city)
    water_amount = get_water_amount(id, date)
    workout_cal = get_workout_calories(id, date)
    food_cal = get_food_calories(id, date)

    print(round(float(weight) * 0.03 * max(1, 1 + (city_temperature - 20) / 20), 1))

    water_norm = round(float(weight) * 0.03 + max(0, (city_temperature - 20) / 5) * 0.25 + workout_cal / 600 * 0.5, 1)
    food_norm = round(calories_calc_model.predict([[weight, height, age]])[0], 0)

    water_left = round(water_norm - water_amount / 1000, 1)
    water_left = str(water_left) + ' л' if water_left >= 1 else str(round(water_left * 1000, 0)) + ' мл'
    water_amount = str(round(water_amount  / 1000, 1)) + ' л' if water_amount >= 980 else str(round(water_amount, 0)) + ' мл'

    food_left = round(food_norm - (food_cal - workout_cal), 0)

    await message.reply(
        f"""Прогресс:
Вода:
- Выпито: {water_amount} из {water_norm} л.
- Осталось: {water_left}.
Калории:
- Потреблено: {food_cal} ккал из {food_norm} ккал.
(без учета активности)
- Сожжено: {workout_cal} ккал.
- Ещё нужно съесть для поддержания веса: {food_left} ккал.\n/keyboard"""
        )



"""# Команда для генерации и отправки графика
@router.message_handler(commands=['graph_water'])
async def cmd_graph_water(message: types.Message):
    # Генерируем график
    days = list(water_consumption.keys())
    amounts = list(water_consumption.values())

    plt.figure(figsize=(10, 5))
    plt.plot(days, amounts, marker='o')
    plt.title("Потребление воды (л)")
    plt.xlabel('Дни')
    plt.ylabel('Количество воды (л)')
    plt.xticks(rotation=45)
    plt.grid()

    # Сохраняем график в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Отправляем график пользователю
    await message.answer_photo(photo=buf)
    plt.close()"""



# Хендлер на сообщение без команды
@router.message(F.text)
async def cmd_help(message: types.Message):
    await message.reply(
        """Доступные команды:
        /start - Начало работы
        /set_profile - Настройка профиля
        /keyboard - Пример кнопок
        /log_water - Отчет о выпитом
        /log_food - Отчет о съеденном
        /log_workout - Отчет о тренировке
        /check_progress - Проверить свой прогресс за сегодня"""
        )