from telegram.ext import Updater, CommandHandler, MessageHandler,CallbackQueryHandler, Application, filters
from config import get_token
import handlears


def main():
    TOKEN = get_token()

    dp = Application.builder().token(TOKEN).build()
    
    dp.add_handler(CommandHandler('start', handlears.start))
    dp.add_handler(CommandHandler('sendfile', handlears.admin_sendpdf))
    
    dp.add_handler(MessageHandler(filters.Document.PDF, handlears.save_document))
    dp.add_handler(MessageHandler(filters.TEXT, handlears.send_user_test))
    dp.add_handler(MessageHandler(filters.TEXT, handlears.user_register))
    dp.run_polling()


if __name__ == '__main__':
    main()  
    