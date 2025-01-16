import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup 
from bot_utils import logging_start, parse_response_for_bot
import requests
from config import BOT_API_TOKEN


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(BOT_API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Влад Дубровин тебя любит<3")

class Profile(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity_time = State()
    city = State()

# Хендлер на команду /set_profile
@dp.message(Command("set_profile"))
async def start_form(message: Message, state: FSMContext):
    await message.reply("Введи свой вес (в кг)")
    await state.set_state(Profile.weight)

@dp.message(Profile.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.reply("Введи свой рост (в см)")
    await state.set_state(Profile.height)

@dp.message(Profile.height)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.reply("Введи свой возраст")
    await state.set_state(Profile.age)

@dp.message(Profile.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply("Сколько минут активности у тебя в день?")
    await state.set_state(Profile.activity_time)

@dp.message(Profile.activity_time)
async def process_activity_time(message: Message, state: FSMContext):
    await state.update_data(activity_time=message.text)
    await message.reply("В каком городе ты находишься?")
    await state.set_state(Profile.city)

@dp.message(Profile.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

# Хендлер на команду /weight_input

# Хендлер на команду /height_input

# Хендлер на команду /a_input

# Хендлер на команду /weight_input

# Хендлер на команду /weight_input

# Хендлер на сообщение без команды
@dp.message(F.text)
async def msg_without_com(message: Message):
    text = message.text
    print(type(text))
    check = 'тоже' in text.lower() or 'и я' in text.lower()
    # Отправляем новое сообщение с добавленным текстом
    await message.reply(
        '<3' if check else '=('
        )

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())