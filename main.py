from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Xin chào {update.effective_user.first_name}')


app = ApplicationBuilder().token("8614538054:AAEg6MiwHoagYfLPn0gnbISx7RG6fEgGuKE").build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()