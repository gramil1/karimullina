import logging, os
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот, который поможет тебе с макияжем.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Подбор макияжа", callback_data='makeup_selection')],
            [InlineKeyboardButton("Советы по макияжу", callback_data='makeup_tips')],
            [InlineKeyboardButton("Уход за кожей", callback_data='skincare')]
        ])
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'makeup_selection':
        await query.edit_message_text(text="Выбери свой цветотип:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Весна", callback_data='spring')],
            [InlineKeyboardButton("Лето", callback_data='summer')],
            [InlineKeyboardButton("Осень", callback_data='autumn')],
            [InlineKeyboardButton("Зима", callback_data='winter')]
        ]))
    elif query.data == 'makeup_tips':
        await query.edit_message_text(text="**Советы по макияжу:**\n\n1. **Подготовка кожи:** Используйте праймер для лучшего нанесения макияжа и более стойкого результата.\n2. **Тональное средство:** Подбирайте тональное средство под свой тон кожи.  Тестируйте его на линии челюсти при дневном освещении.\n3. **Румяна:**  Наносите румяна на яблочки щек для придания свежести лицу.\n4. **Тушь:**  Наносите тушь зигзагообразными движениями для разделения ресниц.\n5. **Снятие макияжа:**  Не забывайте тщательно смывать макияж перед сном.")
    elif query.data == 'skincare':
        await query.edit_message_text(text="Информация об уходе за кожей пока недоступна.")
    elif query.data in ['spring', 'summer', 'autumn', 'winter']:
        await handle_color_type(query, query.data)


async def handle_color_type(query, color_type):
    suggestions = {
        'spring': "Для весеннего цветотипа подойдут теплые, светлые тона: персиковые, бежевые, коралловые румяна; золотистые тени;  розовые и бежевые помады.",
        'summer': "Для летнего цветотипа подойдут холодные, светлые тона: розовые, сиреневые, голубые тени;  розовые и бежевые помады с холодным подтоном.",
        'autumn': "Для осеннего цветотипа подойдут теплые, насыщенные тона: коричневые, золотистые, бронзовые тени;  терракотовые, бежевые помады.",
        'winter': "Для зимнего цветотипа подойдут яркие, холодные тона: красные, фиолетовые, черные тени; красные, винные помады."
    }
    await query.edit_message_text(text=f"Рекомендации для цветотипа {color_type}:\n\n{suggestions[color_type]}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


if __name__ == '__main__':
    application = ApplicationBuilder().token("6235787065:AAFnJEsKJhIT0eyT74ZIF9HZPUB3yGqvCuQ").build() # Замените YOUR_TELEGRAM_BOT_TOKEN на ваш токен

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()