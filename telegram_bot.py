import os
import telebot
from dotenv import load_dotenv
import nlp_analyzer
import response_builder

# Загружаем токены из безопасного файла .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Инициализируем бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Приветственное сообщение бота при старте"""
    welcome_text = (
        "👋 Здравствуйте! Я ваш интеллектуальный аптечный справочный помощник.\n\n"
        "Вы можете спросить меня о лекарствах в свободной форме. Например:\n"
        "• *'Как принимать Аспирин?'*\n"
        "• *'Чем заменить Нурофен?'*\n"
        "• *'Можно ли совмещать Аспирин и Нурофен?'*\n"
        "• *'Что выпить от головной боли?'*"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_user_query(message):
    """Основной обработчик всех текстовых сообщений пользователя"""
    user_text = message.text
    
    # 1. Отправляем текст пользователя в модуль ИИ для анализа интента и лекарства
    ai_result = nlp_analyzer.analyze_user_message(user_text)
    
    # 2. Передаем вердикт ИИ в сборщик ответов, который пойдет в базу данных SQLite
    final_reply = response_builder.build_reply(ai_result)
    
    # 3. Отправляем сформированный красивый ответ обратно пользователю в Telegram
    bot.reply_to(message, final_reply, parse_mode="Markdown")

if __name__ == "__main__":
    print("Робот-помощник успешно запущен и ожидает сообщений в Telegram...")
    # Запуск постоянного опроса серверов Telegram (жизненный цикл бота)
    # none_stop=True позволяет боту не падать при кратковременных сбоях сети
    bot.infinity_polling()