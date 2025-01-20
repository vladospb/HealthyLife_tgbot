import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_API_TOKEN
from handlers import router


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(filename='bot.log', level=logging.INFO)
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