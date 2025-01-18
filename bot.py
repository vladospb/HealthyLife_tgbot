import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from bot_utils import logging_start, parse_response_for_bot
import requests
from config import BOT_API_TOKEN
from handlers import router


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(BOT_API_TOKEN)
# Диспетчер
dp = Dispatcher()
dp.include_router(router)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())