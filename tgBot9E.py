from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '7738219240:AAFymFxObtawZ-_49U1hydZD_juPcMQhPDU'  # ← Вставь сюда токен от BotFather

# Информация о друзьях
friends = {
    "санжар": {
        "name": "Санжар",
        "age": 15,
        "hobby": "играет в бравл и клеш",
        "fun_fact": "фанат Гитлера, 24 апреля был у него ДР",
        "school": "учится на 4, любит бездельничать",
        "music": "Шаровая молния"
    },
    "султан": {
        "name": "Султан",
        "age": 15,
        "hobby": "любит играть в майнкрафт, почти что универсал шарит игры",
        "fun_fact": "Зачем тебе узнать инфу про него все же мы знаем что он настоящий ЕВРЕЙ",
        "school": "учится на 4, обожает англиский язык",
        "music": "Как воити в состояние потока"
    },
    "салим": {
        "name": "Салим",
        "age": 16,
        "hobby": "любит играть в футбик",
        "fun_fact": "Хз че писать, живой щит короче",
        "school": "учится на 4, крутой в алгебре(благодаря телефону) ",
        "music": "Салим жертва, под себя - под себя"
    }
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /run, чтобы выбрать себя из списка друзей [и не забывем про создателя)) ] 😊")

# Команда /run — выбор друга
async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(friend["name"], callback_data=f"user_{key}")]
        for key, friend in friends.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Добро пожаловать в мой ТГ БОТ! Выбери себя из списка:", reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("user_"):
        user_key = data.replace("user_", "")
        context.user_data["current_user"] = user_key

        section_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📄 Информация", callback_data="info"),
                InlineKeyboardButton("🎯 Хобби", callback_data="hobby")
            ],
            [
                InlineKeyboardButton("🤪 Факт", callback_data="fact"),
                InlineKeyboardButton("🏫 Учёба", callback_data="school"),
                InlineKeyboardButton("🤣 Мем", callback_data="music")
            ]
        ])
        await query.edit_message_text(
            f"Вы выбрали: {friends[user_key]['name']}. Выбери раздел:",
            reply_markup=section_keyboard
        )

    elif data in ["info", "hobby", "fact", "school", "music"]:
        user_key = context.user_data.get("current_user")
        if not user_key:
            await query.edit_message_text("Сначала выбери себя с помощью команды /run.")
            return

        user = friends[user_key]
        if data == "info":
            msg = f"📄 Имя: {user['name']}\n🎂 Возраст: {user['age']}"
        elif data == "hobby":
            msg = f"🎯 Хобби: {user['hobby']}"
        elif data == "fact":
            msg = f"🤪 Факт: {user['fun_fact']}"
        elif data == "school":
            msg = f"🏫 Учёба: {user['school']}"
        elif data == "music":
            msg = f"🤣 Мем: {user['music']}"

        await query.edit_message_text(msg)

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("run", run))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ Бот запущен!")
app.run_polling()
