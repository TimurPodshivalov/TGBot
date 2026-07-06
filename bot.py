from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import random

TOKEN = '8620451284:AAGjDUSu7GoZ1DYka3Qo_19wUfC_AENw85o'

# Список приветствий
GREETINGS = [
    "Привет, {}! 👋",
    "Здравствуй, {}! 😊",
    "Добро пожаловать, {}! 🎉",
    "Рад видеть тебя, {}! 🤗",
    "Салют, {}! ✨"
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Выбираем случайное приветствие
    greeting_template = random.choice(GREETINGS)

    # Определяем как обращаться к пользователю
    if user.first_name:
        name = user.first_name
    elif user.username:
        name = f"@{user.username}"
    else:
        name = "друг"

    message = greeting_template.format(name)
    message += "\n\nВыберите раздел:\n/events - События\n/about - О боте\n/me - Обо мне"

    await update.message.reply_text(message)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user.first_name else "друг"

    response = f"""
    {name}, вот информация обо мне:

    Я - демонстрационный бот
    Версия: 1.0
    Создан для обучения
    """
    await update.message.reply_text(response)


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user.first_name else "друг"

    response = f"""
    {name}, вот предстоящие события:

    1. Вебинар по Python - 15 декабря
    2. Хакатон - 20-22 декабря
    3. Новогодняя вечеринка - 31 декабря
    """
    await update.message.reply_text(response)


async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    user_info = f"""
    📋 Информация о вас:

    Имя: {user.first_name or 'Не указано'}
    Фамилия: {user.last_name or 'Не указана'}
    Username: @{user.username or 'Не указан'}
    ID: {user.id}
    Язык: {user.language_code or 'Не определен'}
    """

    await update.message.reply_text(user_info)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user.first_name else "друг"

    await update.message.reply_text(f"{name}, я понимаю только команды. Используйте /start для начала.")


def main():
    # Создаем приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("events", events))
    app.add_handler(CommandHandler("me", me_command))

    # Обработчик для всех сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == '__main__':
    main()