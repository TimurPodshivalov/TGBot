from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import os
import random
from typing import List, Dict
import datetime

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")


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
        "date": "14.07.2026",
        "date_obj": datetime.date(2026, 7, 14),
        "time": "10:00",
        "description": "Презентация новых возможностей бота",
        "location": "Онлайн",
        "speaker": "Команда разработки"
    },
    {
        "id": 2,
        "title": "🎓 Мастер-класс по Python",
        "date": "15.07.2026",
        "date_obj": datetime.date(2026, 7, 15),
        "time": "14:00",
        "description": "Практическое занятие по асинхронному программированию",
        "location": "Конференц-зал А",
        "speaker": "Иван Петров"
    },
    {
        "id": 3,
        "title": "🤖 AI в Telegram ботах",
        "date": "16.07.2026",
        "date_obj": datetime.date(2026, 7, 16),
        "time": "18:30",
        "description": "Как интегрировать искусственный интеллект в Telegram ботов",
        "location": "Онлайн",
        "speaker": "Анна Сидорова"
    },
    {
        "id": 4,
        "title": "📊 Аналитика данных",
        "date": "16.07.2026",
        "date_obj": datetime.date(2026, 7, 16),
        "time": "11:00",
        "description": "Сбор и анализ данных из Telegram каналов",
        "location": "Конференц-зал Б",
        "speaker": "Михаил Козлов"
    },
    {
        "id": 5,
        "title": "🔧 Техническое обслуживание",
        "date": "16.07.2026",
        "date_obj": datetime.date(2026, 7, 16),
        "time": "03:00-05:00",
        "description": "Плановые работы на серверах",
        "location": "Дата-центр",
        "speaker": "Техническая поддержка"
    },
    {
        "id": 6,
        "title": "🎉 Итоговый митап",
        "date": "18.07.2026",
        "date_obj": datetime.date(2026, 7, 18),
        "time": "19:00",
        "description": "Подведение итогов недели, награждение активных участников",
        "location": "Главный зал",
        "speaker": "Организаторы"
    },
    {
        "id": 7,
        "title": "📝 Обновление документации",
        "date": "25.07.2026",
        "date_obj": datetime.date(2026, 7, 25),
        "time": "09:00",
        "description": "Обновление и публикация технической документации проекта",
        "location": "Онлайн",
        "speaker": "Алексей Иванов"
    },
    {
        "id": 8,
        "title": "🎤 Вебинар по безопасности",
        "date": "27.07.2026",
        "date_obj": datetime.date(2026, 7, 27),
        "time": "16:00",
        "description": "Обучающий вебинар по кибербезопасности и защите данных",
        "location": "Зал конференций",
        "speaker": "Елена Петрова"
    },
    {
        "id": 9,
        "title": "🤝 Встреча команды",
        "date": "28.07.2026",
        "date_obj": datetime.date(2026, 7, 28),
        "time": "15:00",
        "description": "Встреча команды разработчиков и менеджеров",
        "location": "Коворкинг-центр",
        "speaker": "Команда проекта"
    },
    {
        "id": 10,
        "title": "🌐 Обзор новых технологий",
        "date": "29.07.2026",
        "date_obj": datetime.date(2026, 7, 29),
        "time": "11:30",
        "description": "Обзор современных технологий и трендов в области ИИ",
        "location": "Онлайн",
        "speaker": "Сергей Смирнов"
    },
    {
        "id": 11,
        "title": "🎉 Итоговая презентация месяца",
        "date": "31.07.2026",
        "date_obj": datetime.date(2026, 7, 31),
        "time": "18:00",
        "description": "Обзор достижений за месяц и планы на следующий",
        "location": "Главный зал",
        "speaker": "Руководство"
    }
]

user_positions = {}
user_states = {}

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

def get_timeframe_menu():
    keyboard = [
        [KeyboardButton("За день"), KeyboardButton("За неделю")],
        [KeyboardButton("За месяц")],
        [KeyboardButton("Вернуться в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def filter_events_by_period(period: str):
    today = datetime.date.today()
    filtered_events = []

    if period == "день":
        for event in EVENTS:
            if event['date_obj'] == today:
                filtered_events.append(event)
    elif period == "неделю":
        start_week = today - datetime.timedelta(days=today.weekday())  # начало текущей недели
        end_week = start_week + datetime.timedelta(days=6)
        for event in EVENTS:
            if start_week <= event['date_obj'] <= end_week:
                filtered_events.append(event)
    elif period == "месяц":
        start_month = today.replace(day=1)
        # следующий месяц
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        for event in EVENTS:
            if start_month <= event['date_obj'] < next_month:
                filtered_events.append(event)
    return filtered_events

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

    if user_id not in user_states:
        # Если пользователь не выбирал период, ничего не делаем
        return

    state = user_states[user_id]
    period_str = state['period']
    filtered_events = filter_events_by_period(period_str)
    total = len(filtered_events)

    data = query.data

    if data.startswith("prev_"):
        new_index = max(0, state['index'] - 1)
        state['index'] = new_index

    elif data.startswith("next_"):
        new_index = min(total - 1, state['index'] + 1)
        state['index'] = new_index

    elif data == "page_info":
        await query.answer(f"Событие {state['index'] + 1} из {total}")
        return

    # Обновляем сообщение с текущим событием
    if total > 0:
        message = format_event(filtered_events[state['index']], state['index'], total)
        await query.edit_message_text(
            message,
            parse_mode='Markdown',
            reply_markup=get_events_keyboard(state['index'], total)
        )
    else:
        await query.edit_message_text(
            f"Нет событий за период: {period_str}.",
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    user_id = user.id
    name = user.first_name if user.first_name else "друг"

    if text in ["За день", "За неделю", "За месяц"]:
        period_map = {
            "За день": "день",
            "За неделю": "неделю",
            "За месяц": "месяц"
        }
        period_str = period_map[text]
        filtered_events = filter_events_by_period(period_str)
        total_events = len(filtered_events)

        # Сохраняем состояние пользователя
        user_states[user_id] = {'period': period_str, 'index': 0}

        # Отправляем первое событие этого периода
        if total_events > 0:
            message = format_event(filtered_events[0], 0, total_events)
            await update.message.reply_text(
                message,
                parse_mode='Markdown',
                reply_markup=get_events_keyboard(0, total_events)
            )
        else:
            await update.message.reply_text(
                f"Нет событий за период: {period_str}."
            )
    elif text == "📚 О боте":
        await about(update, context)
    elif text == "🎉 События":
        # Показываем меню с "За день", "За неделю", "За месяц"
        await events(update, context)
        await update.message.reply_text(
            "Выберите период:",
            reply_markup=get_timeframe_menu()
        )
    elif text == "Вернуться в меню":
        await update.message.reply_text(
            f"{name}, возвращаюсь в главное меню.",
            reply_markup=get_main_keyboard()
        )
    else:
        await update.message.reply_text(
            f"{name}, я понимаю только команды. Используйте кнопки ниже или /start для начала.",
            reply_markup=get_main_keyboard()
        )

async def handle_callback_query(update, context):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    data = query.data

    # Обработка навигации по событиям
    if user_id not in user_states:
        # Если пользователь не выбирал период, ничего не делаем
        return

    state = user_states[user_id]
    period_str = state['period']
    filtered_events = filter_events_by_period(period_str)
    total = len(filtered_events)

    if total == 0:
        await query.edit_message_text(f"Нет событий за период: {period_str}.")
        return

    if data.startswith("prev_"):
        new_index = max(0, state['index'] - 1)
        state['index'] = new_index
    elif data.startswith("next_"):
        new_index = min(total - 1, state['index'] + 1)
        state['index'] = new_index
    elif data == "page_info":
        await query.answer(f"Событие {state['index'] + 1} из {total}")
        return

    # Обновляем сообщение с текущим событием
    message = format_event(filtered_events[state['index']], state['index'], total)
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=get_events_keyboard(state['index'], total)
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