from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import os
import random
from typing import List, Dict

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

GREETINGS = [
    "Привет, {}! 👋",
    "Здравствуй, {}! 😊",
    "Добро пожаловать, {}! 🎉",
    "Рад видеть тебя, {}! 🤗"
]

EVENTS: List[Dict] = [
    {
        "id": 1,
        "title": "🚀 Запуск нового функционала",
        "date": "15.01.2024",
        "time": "10:00",
        "description": "Презентация новых возможностей бота",
        "location": "Онлайн",
        "speaker": "Команда разработки"
    },
    {
        "id": 2,
        "title": "🎓 Мастер-класс по Python",
        "date": "16.01.2024",
        "time": "14:00",
        "description": "Практическое занятие по асинхронному программированию",
        "location": "Конференц-зал А",
        "speaker": "Иван Петров"
    },
    {
        "id": 3,
        "title": "🤖 AI в Telegram ботах",
        "date": "17.01.2024",
        "time": "18:30",
        "description": "Как интегрировать искусственный интеллект в Telegram ботов",
        "location": "Онлайн",
        "speaker": "Анна Сидорова"
    },
    {
        "id": 4,
        "title": "📊 Аналитика данных",
        "date": "18.01.2024",
        "time": "11:00",
        "description": "Сбор и анализ данных из Telegram каналов",
        "location": "Конференц-зал Б",
        "speaker": "Михаил Козлов"
    },
    {
        "id": 5,
        "title": "🔧 Техническое обслуживание",
        "date": "19.01.2024",
        "time": "03:00-05:00",
        "description": "Плановые работы на серверах",
        "location": "Дата-центр",
        "speaker": "Техническая поддержка"
    },
    {
        "id": 6,
        "title": "🎉 Итоговый митап",
        "date": "20.01.2024",
        "time": "19:00",
        "description": "Подведение итогов недели, награждение активных участников",
        "location": "Главный зал",
        "speaker": "Организаторы"
    }
]

user_positions = {}


def get_main_keyboard():
    keyboard = [
        [KeyboardButton("📚 О боте"), KeyboardButton("🎉 События")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def get_events_keyboard(event_index: int = 0, total_events: int = len(EVENTS)):
    keyboard = []

    # Кнопки навигации
    nav_buttons = []

    if event_index > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Назад", callback_data=f"prev_{event_index}"))

    # Номер события
    nav_buttons.append(InlineKeyboardButton(f"{event_index + 1}/{total_events}", callback_data="page_info"))

    if event_index < total_events - 1:
        nav_buttons.append(InlineKeyboardButton("Вперед ▶️", callback_data=f"next_{event_index}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(keyboard)


def format_event(event: Dict, index: int, total: int) -> str:
    return f"""
🎉 *Событие {index + 1} из {total}*

*{event['title']}*
📅 Дата: {event['date']}
⏰ Время: {event['time']}
📍 Место: {event['location']}
👤 Ведущий: {event['speaker']}

📝 *Описание:*
{event['description']}

🆔 ID события: {event['id']}
    """


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    greeting_template = random.choice(GREETINGS)

    if user.first_name:
        name = user.first_name
    elif user.username:
        name = f"@{user.username}"
    else:
        name = "друг"

    message = greeting_template.format(name)

    await update.message.reply_text(
        message,
        reply_markup=get_main_keyboard()
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user.first_name else "друг"

    response = f"""{name}, вот информация обо мне:

Я - тренировочный бот для практики Росстелеком.
Показываю список событий и информацию о себе.
Разработчик: Подшивалов Тимур"""

    if update.message:
        await update.message.reply_text(
            response,
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            response,
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Устанавливаем начальную позицию
    user_positions[user_id] = 0

    # Получаем первое событие
    event = EVENTS[0]
    message_text = format_event(event, 0, len(EVENTS))

    if update.message:
        await update.message.reply_text(
            message_text,
            parse_mode='Markdown',
            reply_markup=get_events_keyboard(0, len(EVENTS))
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            message_text,
            parse_mode='Markdown',
            reply_markup=get_events_keyboard(0, len(EVENTS))
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    data = query.data

    # Инициализируем позицию пользователя, если ее нет
    if user_id not in user_positions:
        user_positions[user_id] = 0

    current_index = user_positions[user_id]

    # Обработка навигации
    if data.startswith("prev_"):
        # Листаем назад
        new_index = max(0, current_index - 1)
        user_positions[user_id] = new_index

    elif data.startswith("next_"):
        # Листаем вперед
        new_index = min(len(EVENTS) - 1, current_index + 1)
        user_positions[user_id] = new_index

    elif data == "page_info":
        # Просто показываем номер страницы
        await query.answer(f"Событие {current_index + 1} из {len(EVENTS)}")
        return

    # Обновляем отображаемое событие
    new_index = user_positions[user_id]
    event = EVENTS[new_index]
    message_text = format_event(event, new_index, len(EVENTS))

    await query.edit_message_text(
        message_text,
        parse_mode='Markdown',
        reply_markup=get_events_keyboard(new_index, len(EVENTS))
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    name = user.first_name if user.first_name else "друг"

    if text == "📚 О боте":
        await about(update, context)
    elif text == "🎉 События":
        await events(update, context)
    else:
        await update.message.reply_text(
            f"{name}, я понимаю только команды. Используйте кнопки ниже или /start для начала.",
            reply_markup=get_main_keyboard()
        )


def main():
    # Создаем приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("events", events))

    # Обработчик нажатий на inline-кнопки (стрелки)
    app.add_handler(CallbackQueryHandler(button_handler))

    # Обработчик для текстовых сообщений (кнопки "О боте" и "События")
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    print("Доступные кнопки: 📚 О боте, 🎉 События")
    print("Для событий доступны стрелки навигации: ◀️ и ▶️")
    app.run_polling()


if __name__ == '__main__':
    main()