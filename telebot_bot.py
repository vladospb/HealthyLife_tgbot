import telebot
from bot_utils import logging_start, parse_response_for_bot
from dotenv import load_dotenv
from os import getenv
import requests

WELCOME_MESSAGE = """Привет! Я могу помочь тебе рассчитать дневные нормы воды и калорий, а также отслеживать тренировки и питание."""
WAIT_MESSAGE = """Думаю..."""
ERROR_MESSAGE = """Ой, что-то пошло не так. Попробуй позже"""

load_dotenv()
BOT_API_TOKEN = getenv("BOT_API_TOKEN")
LOG_FILE = getenv("LOG_FILE")

logger = logging_start(LOG_FILE)

# создаем бота
bot = telebot.TeleBot(BOT_API_TOKEN)
# уьираем вебхук, чтобы пользоваться polling
bot.remove_webhook()


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message) -> None:
    """Welcome user.

    Rplies to a message containing the /start command
    with a welcome message.

    Args:
        message (telebot.types.Message): message with /start command.

    Returns:
        None
    """
    try:
        bot.send_message(
            message.chat.id,
            WELCOME_MESSAGE,
            parse_mode="HTML",
        )
        logger.info(f"{message.chat.username} started the bot")
    except Exception as e:
        logger.error(f"{message.chat.username} got an error: {e}")


@bot.message_handler(content_types=["text"])
def main_input(message: telebot.types.Message) -> None:
    """Provide steps to do something in minecraft.

    Receives a prompt of what to do in minecraft, replies with
    action steps required. Prompted by any text message.

    Args:
        message (telebot.types.Message): message with prompt.

    Returns:
        None
    """
    try:
        logger.info(f"{message.chat.username} subbed a prompt: {message.text}")
        sent_message = bot.reply_to(
            message,
            WAIT_MESSAGE,
            parse_mode="HTML",
        )
        response = parse_response_for_bot(message.text)
        # Телеграм не выдерживает сообщения длиннее 4096, поэтому
        # здесь сообщение при помощи bot_utils.parse_response_for_bot
        # разбивается на блоки длиной не более 4096, которые
        # отправляются как отдельные сообщения
        if response and response[0]:
            bot.edit_message_text(
                text=response[0],
                chat_id=sent_message.chat.id,
                message_id=sent_message.id,
                parse_mode="HTML",
            )
            sent_message2 = bot.reply_to(
                message,
                "processing gifs... this will take several minutes",
                parse_mode="HTML",
            )
            try:

                bot.edit_message_text(
                    text="gifs done",
                    chat_id=sent_message2.chat.id,
                    message_id=sent_message2.id,
                    parse_mode="HTML",
                )

            except:
                bot.edit_message_text(
                    text="got an error while creating gif :(",
                    chat_id=sent_message2.chat.id,
                    message_id=sent_message2.id,
                    parse_mode="HTML",
                )
        else:
            bot.edit_message_text(
                text=ERROR_MESSAGE,
                chat_id=sent_message.chat.id,
                message_id=sent_message.id,
                parse_mode="HTML",
            )
    except Exception as e:
        logger.error(f"{message.chat.username} got an error: {e}")
        bot.edit_message_text(
            text=ERROR_MESSAGE,
            chat_id=sent_message.chat.id,
            message_id=sent_message.id,
            parse_mode="HTML",
        )


# делаем так, чтобы бот постоянно запрашивал обновления от telegram
bot.infinity_polling(none_stop=True, interval=0)