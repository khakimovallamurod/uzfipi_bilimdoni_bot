from telegram.ext import Updater, CommandHandler, MessageHandler,CallbackQueryHandler, Application, filters, ConversationHandler
from config import get_token
import handlears


def main():
    TOKEN = get_token()

    dp = Application.builder().token(TOKEN).build()
    
    dp.add_handler(CommandHandler('start', handlears.start))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', handlears.user_register)],
        states={
            handlears.FAK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_fak)],
            handlears.YUN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_yun)],
            handlears.KURS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_kurs)],
            handlears.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.ask_name)],
        },
        fallbacks=[CommandHandler('cancel', handlears.cancel)]
    )

    #Admin
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
    dp.add_handler(conv_handler)
    dp.add_handler(admin_conv_handler)
    dp.add_handler(MessageHandler(filters.TEXT, handlears.send_user_test))
    dp.run_polling()


if __name__ == '__main__':
    main()  
    