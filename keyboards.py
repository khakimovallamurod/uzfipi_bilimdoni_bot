from telegram import ReplyKeyboardMarkup, KeyboardButton
button = KeyboardButton(
    [["👉 REGISTER 👈"]]
)
register_button = ReplyKeyboardMarkup(button, resize_keyboard=True)