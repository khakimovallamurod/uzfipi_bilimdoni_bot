from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, Filters  # importlar to'liq
from config import get_token

app = Flask(__name__)

TOKEN = get_token() 
bot = Application.builder().token(TOKEN).build()

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)  # Webhookga kelayotgan ma'lumotlarni konsolga chiqarish

    # Telegram bot yangilanishini yaratish
    update = Update.de_json(data, bot.bot)
    bot.process_update(update)
    return jsonify({'status': 200})  # 'statust' ni 'status' ga o'zgartirish

# Flask ilovasi
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Flask ilovasini ma'lum portda ishga tushirish
