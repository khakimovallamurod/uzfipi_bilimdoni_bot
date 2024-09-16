from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
import keyboards
import db


async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if db.is_admin(user.id):
        await update.message.reply_text(
            text=f"""Assalomu aleykum {user.full_name}. Siz ushbu botda admin huqudiga egasiz. Botga test qo'shishingiz yoki natijani olishingiz mumkin.""",
        )
    else:
        await update.message.reply_text(
            text=f"""Ma'lumotingizni kiriting bu keyingi natijalaringiz uchun kerak bo'ladi. \nNamuna: Fakultitet/Yo'nalish/Kurs/FIO (Faqat shu tarzda yozishingiz kerak)""",
        )

async def admin_sendpdf(update: Update, context: CallbackContext):
    user = update.message.from_user
    if db.is_admin(user.id):
        await update.message.reply_text(text="Test faylini yuboring faqat PDF shaklida.")

async def save_document(update: Update, context: CallbackContext):
    user = update.message.from_user
    file_id = update.message.document.file_id
    filename = update.message.document.file_name
    save_pdf = db.save_pdf(file_path=file_id, file_name = filename)
    if db.is_admin(user.id):
        if save_pdf:
            await update.message.reply_text(text=f"""✅ Muvaffaqiyatli saqlandi. \nTest nomi: {filename}. \nTEST KODI: {1001}""")

async def user_register(update: Update, context: CallbackContext):
    user = update.message.from_user
    data = update.message.text.split('/')
    if not db.is_admin(user.id):
        fakultitet = data[0].strip().title()
        yunalish = data[1].strip().title()
        kurs = data[2].strip()
        full_name = data[3].strip().title()
        db.register(str(user.id),
                    fak=fakultitet,
                    yunlish=yunalish,
                    kurs=str(kurs),
                    fullname=full_name)
        await update.message.reply_text("✅ Muvaffaqiyatli ro'yxatdan o'tdingiz. Ushbu botda test bajarish uchun TEST KODINI yuboring.")

async def send_user_test(update: Update, context: CallbackContext):
    user = update.message.from_user
    test_id = update.message.text
    if not db.is_admin(user.id):
        test_data = db.get_testid(test_id=test_id)
        if test_data != []:
            await update.message.reply_document(test_data[0]['file_path'])
        else:
            await update.message.reply_text(f"❌ {test_id}. Ushbu test kodi mavjud emas, tekshirib ko'ring.")
