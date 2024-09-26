from flask import Flask, request
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from config import get_token
import handlears

app = Flask(__name__)

# Telegram bot setup
TOKEN = get_token()
bot_app = Application.builder().token(TOKEN).build()

# Define the same handlers
bot_app.add_handler(CommandHandler('start', handlears.start))

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & filters.Regex('👉 REGISTER 👈'), handlears.user_register)],
    states={
        handlears.FAK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_fak)],
        handlears.YUN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_yun)],
        handlears.KURS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_kurs)],
        handlears.TEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_tel)],
        handlears.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_name)],
    },
    fallbacks=[CommandHandler('cancel', handlears.cancel)]
)

admin_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('create', handlears.admin_creat_test)],
    states={
        handlears.T_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_testID)],
        handlears.T_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_testNAME)],
        handlears.T_FILE: [MessageHandler(filters.Document.ALL & ~filters.COMMAND, handlears.ask_testFILE)], 
        handlears.T_ANS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_testANSWER)],
    },
    fallbacks=[CommandHandler('cancel', handlears.cancel)]
)

user_test_handler = ConversationHandler(
    entry_points=[CommandHandler('tests', handlears.tests_command)],
    states={
        handlears.T_SEND: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.send_user_test)],
        handlears.T_CHECK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.user_test_check)],
    },
    fallbacks=[CommandHandler('cancel', handlears.cancel)]
)

admin_get_results = ConversationHandler(
    entry_points=[CommandHandler('results', handlears.admin_get_results)],
    states={
        handlears.RES_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.get_results_user)],
    },
    fallbacks=[CommandHandler('cancel', handlears.cancel)]
)

bot_app.add_handler(conv_handler)
bot_app.add_handler(admin_conv_handler)
bot_app.add_handler(user_test_handler)
bot_app.add_handler(admin_get_results)

# Webhook route
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """Process incoming updates from Telegram."""
    update = request.get_json()
    bot_app.update_queue.put(update)  # Send update to the bot
    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    """Set the webhook for Telegram bot."""
    webhook_url = f'https://<your-domain>.pythonanywhere.com/{TOKEN}'
    bot_app.bot.set_webhook(url=webhook_url)
    return f'Webhook set to {webhook_url}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
