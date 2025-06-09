# File: bot.py
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # např. https://tvuj-bot.onrender.com

CHOOSING_SERVICE, TYPING_CRITERIA = range(2)

SERVICES = [
    "Оформление аккаунта YouTube/VK/Telegram",
    "Индивидуальный логотип",
    "Набор уникальных игровых аватарок",
    "Простая аватарка",
    "Полное оформление соцсети",
    "Отдельный ростер",
]

PRICE_LIST = """
🟢 Стоимость наших услуг по оформлению соцсетей и разработке логотипов:

- Оформление аккаунта YouTube/VK/Telegram (шапка + аватарка) — 150 💸
- Логотип индивидуальный — 200 💸
- Набор уникальных игровых аватарок — 100 💸
- Простая аватарка — 50 💸
- Полное оформление соцсети (шапка + аватарка, ростеры, баннеры до 5 штук) — 200 💸
- Отдельный ростер — 10 💸

(Дополнительно для игр: мы можем сделать ростер с вашими игроками, рангами, т.д.) — от 10 до 15 💸

💵 Оплата Тинькофф банк 💸
📞 Перевод по номеру телефона (СБП) 💸

Время выполнения: от 1 часа до 5 дней
"""

PAYMENT_INFO = """
🔸 Наши реквизиты для оплаты дизайна:

💳 Банковская карта:
Тинькофф банк 💸
2200 7019 7390 6727
Денис Р.

📞 Перевод по номеру телефона (СБП) 💸
+7 (978) 250-89-11

После оплаты отправьте скриншот и описание товара в Telegram: @EtopizdetC0o
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = ReplyKeyboardMarkup.from_column(SERVICES, resize_keyboard=True)
    await update.message.reply_text("Привет! Выбери, пожалуйста, услугу из списка ниже:", reply_markup=keyboard)
    await update.message.reply_text(PRICE_LIST)
    return CHOOSING_SERVICE

async def service_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    service = update.message.text
    context.user_data['service'] = service
    await update.message.reply_text(
        "Пожалуйста, опиши критерии для выбранной услуги (например: цвет, никнейм, кого добавить и т.д.):",
        reply_markup=None
    )
    return TYPING_CRITERIA

async def criteria_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    criteria = update.message.text
    context.user_data['criteria'] = criteria
    await update.message.reply_text(PAYMENT_INFO)
    await update.message.reply_text("Спасибо! После оплаты напишите @EtopizdetC0o со скриншотом и описанием товара. Заказ будет выполнен в течение 1 часа – 5 дней.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Заказ отменен. Если передумаете, напишите /start.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, service_choice)],
            TYPING_CRITERIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, criteria_received)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)

    app.run_webhook(
        listen='0.0.0.0',
        port=int(os.getenv('PORT', '5000')),
        url_path=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )

# File: requirements.txt
python-telegram-bot[webhooks]==20.4
