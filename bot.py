from dotenv import load_dotenv
import logging
import os
from storage import load_qa_from_file
from vkbottle.bot import Bot, Message
from fuzzywuzzy import process
from telegramMessage import tg_resend_message

LOG_FILE = 'vkBot.log'
logger = logging.getLogger('vkBot')
logger.setLevel(logging.INFO)
if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8', mode='a')
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Загружаем переменные из .env
load_dotenv()

TOKEN = os.environ.get("VK_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Не задана переменная окружения VK_BOT_TOKEN")
logger.info(f"Токен бота загружен")

# Загружаем вопросы и ответы из файла
answer_dict = load_qa_from_file()
logger.info(f"Загружено {len(answer_dict)} вопросов")

bot = Bot(TOKEN)

@bot.on.message(text='<any>')
async def handle_any_message(message: Message):
    message_id = str(message.id)
    user_id = str(message.peer_id)
    logger.info(message_id + ' | Получено сообщение от пользователя ' + user_id + ': ' + message.text)
    user_message = message.text.lower()
    best_match, rate = process.extractOne(user_message, list(answer_dict.keys()))
    logger.info(message_id + ' | Поиск пары вопрос-ответ: ' + best_match + ' | Схожесть: ' + str(rate) + '%')
    if rate >= 70:
        answer_key = best_match
        response = answer_dict.get(answer_key)
        if response:
            msg_response = 'Вероятно вы имели в виду: ' + answer_key + '. Ответ: ' + response
            await message.answer(msg_response)
        else:
            msg_response = 'Извините, не могу ответить.'
            await message.answer(msg_response)
    else:
        msg_response = 'Не нашел ответ. Спрошу у администратора (переслал сообщение).'
        await message.answer(msg_response)
        tg_resend_message(user_id, message_id, user_message)
        logger.info(message_id + ' | Переслал сообщение в телеграмм администратору')

    logger.info(message_id + ' | Отправлено сообщение пользователю ' + user_id + ': ' + msg_response)

if __name__ == '__main__':
    logger.info("VK-бот запущен. Ожидание сообщений...")
    bot.run_forever()