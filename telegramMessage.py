import telebot
from dotenv import load_dotenv
import os

def tg_resend_message(user_from, message_id, message_text):
    load_dotenv()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Не задана переменная окружения TELEGRAM_BOT_TOKEN")

    user_to = os.environ.get("TELEGRAM_USER_RESEND")
    if not user_to:
        raise ValueError("Не задана переменная окружения TELEGRAM_USER_RESEND")

    bot = telebot.TeleBot(token)

    message = 'Получено сообщение в VK без подходящего ответа в словаре.\nДетали:\nid пользователя: ' + user_from + '\nid сообщения: ' + message_id + '\ntext сообщения: ' + message_text

    bot.send_message(chat_id=user_to, text=message)

    return 0

if __name__ == '__main__':
    print ()