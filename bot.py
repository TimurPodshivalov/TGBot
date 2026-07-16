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

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📚 О боте"), KeyboardButton("🎉 События")],
        ],
        resize_keyboard=True
    )

def get_timeframe_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("За день"), KeyboardButton("За неделю")],
            [KeyboardButton("За месяц")],
            [KeyboardButton("Вернуться в меню")]
        ],
        resize_keyboard=True
    )

def filter_events_by_period(period: str):
    today = datetime.date.today()
    filtered_events = []

    if period == "день":
        for event in EVENTS:
            if event['date_obj'] == today:
                filtered_events.append(event)
    elif period == "неделю":
        start_week = today - datetime.timedelta(days=today.weekday())  # понедельник
        end_week = start_week + datetime.timedelta(days=6)
        for event in EVENTS:
            if start_week <= event['date_obj'] <= end_week:
                filtered_events.append(event)
    elif period == "месяц":
        start_month = today.replace(day=1)
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
    name = user.first_name or user.username or "друг"
    message = greeting_template.format(name)
    await update.message.reply_text(
        message,
        reply_markup=get_main_keyboard()
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "друг"
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

async def show_events_list(update, context, events: List[Dict]):
    if not events:
        await update.message.reply_text("Нет событий для отображения.")
        return
    context.chat_data['events_list'] = events
    context.chat_data['current_index'] = 0
    event = events[0]
    message = format_event(event, 0, len(events))
    keyboard = [
        [
            InlineKeyboardButton("◀️ Назад", callback_data="nav_prev"),
            InlineKeyboardButton(f"{1}/{len(events)}", callback_data="page_info"),
            InlineKeyboardButton("Вперед ▶️", callback_data="nav_next")
        ]
    ]
    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    name = user.first_name or "друг"

    if text in ["За день", "За неделю", "За месяц"]:
        period_map = {
            "За день": "день",
            "За неделю": "неделю",
            "За месяц": "месяц"
        }
        period_str = period_map[text]
        filtered_events = filter_events_by_period(period_str)
        await show_events_list(update, context, filtered_events)
    elif text == "🎉 События":
        # показываем все события
        await show_events_list(update, context, EVENTS)
    elif text == "📚 О боте":
        await about(update, context)
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

    if 'chat_data' not in context:
        context.chat_data['events_list'] = []
        context.chat_data['current_index'] = 0

    events_list = context.chat_data.get('events_list', [])
    index = context.chat_data.get('current_index', 0)

    data = query.data

    if data == "nav_prev":
        if events_list:
            index = max(0, index - 1)
            context.chat_data['current_index'] = index
    elif data == "nav_next":
        if events_list:
            index = min(len(events_list) - 1, index + 1)
            context.chat_data['current_index'] = index
    elif data == "page_info":
        # Сообщение с текущим номером
        await query.answer(f"Событие {index + 1} из {len(events_list)}")
        return

    if events_list:
        event = events_list[index]
        message = format_event(event, index, len(events_list))
        keyboard = [
            [
                InlineKeyboardButton("◀️ Назад", callback_data="nav_prev"),
                InlineKeyboardButton(f"{index + 1}/{len(events_list)}", callback_data="page_info"),
                InlineKeyboardButton("Вперед ▶️", callback_data="nav_next")
            ]
        ]
        await query.edit_message_text(
            message,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("events", events))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    print("Бот запущен...")
    print("Доступные кнопки: 📚 О боте, 🎉 События")
    print("Для событий доступны стрелки навигации: ◀️ и ▶️")
    app.run_polling()

if __name__ == '__main__':
    main()