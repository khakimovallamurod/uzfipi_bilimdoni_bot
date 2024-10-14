from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application
from config import get_token

app = Flask(__name__)

TOKEN = get_token() 
bot = Application.builder().token(TOKEN).build()

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    update = Update.de_json(request.get_json(), bot.bot)
    bot.process_update(update)
    return jsonify({'statust': 200})

# Flask ilovasi
if __name__ == '__main__':
    app.run(debug=True)
