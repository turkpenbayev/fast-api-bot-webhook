from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.effective_user)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


bot = ApplicationBuilder().token("6026174140:AAFK-yv9KjrazxhjK-SD1WN4IAk5TJfF3Qw").build()

bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

bot.run_polling()