from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, ConversationHandler
import keyboards
import db


FAK, YUN, KURS, NAME = range(4)
T_ID, T_NAME, T_FILE = range(3)

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if db.is_admin(user.id):
        await update.message.reply_text(
            text=f"""Assalomu aleykum {user.full_name}. Siz ushbu botda admin huqudiga egasiz. Botga test qo'shish /create va natija olish /results""",
        )
    else:
        if db.is_start(str(user.id)):
            await update.message.reply_text(
                text=f"""Xush kelibsiz. Bu bot orqali onlayn test yechishingiz mumkin, buning uchun /register comandasini bosing.""",
            )
        else:
            await update.message.reply_text("Test bajarish uchun TEST KODINI yuboring.")


async def user_register(update: Update, context: CallbackContext):
    await update.message.reply_text("Fakultetingizni kiriting:")
    return FAK

async def ask_fak(update: Update, context: CallbackContext):
    context.user_data['fakultitet'] = update.message.text.strip().title()
    await update.message.reply_text("Yunalishingizni kiriting:")
    return YUN

async def ask_yun(update: Update, context: CallbackContext):
    context.user_data['yunalish'] = update.message.text.strip().title()
    await update.message.reply_text("Kursingizni kiriting:")
    return KURS

async def ask_kurs(update: Update, context: CallbackContext):
    context.user_data['kurs'] = update.message.text.strip()
    await update.message.reply_text("To'liq ism-familiyangizni kiriting:")
    return NAME

async def ask_name(update: Update, context: CallbackContext):
    context.user_data['fullname'] = update.message.text.strip().title()

    fakultitet = context.user_data['fakultitet']
    yunalish = context.user_data['yunalish']
    kurs = context.user_data['kurs']
    full_name = context.user_data['fullname']
    user_id = update.message.from_user.id

    db.register(str(user_id),
                fak=fakultitet,
                yunlish=yunalish,
                kurs=str(kurs),
                fullname=full_name)

    await update.message.reply_text("✅ Muvaffaqiyatli ro'yxatdan o'tdingiz. Test bajarish uchun TEST KODINI yuboring.")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text('Ro\'yxatdan o\'tish bekor qilindi.')
    return ConversationHandler.END

async def send_user_test(update: Update, context: CallbackContext):
    user = update.message.from_user
    test_id = update.message.text
    if not db.is_admin(user.id):
        test_data = db.get_testid(test_id=test_id)
        if test_data != []:
            await update.message.reply_document(test_data[0]['file_path'])
        else:
            await update.message.reply_text(f"❌, Ushbu test kodi mavjud emas, tekshirib ko'ring.")

# Admin 

async def admin_creat_test(update: Update, context: CallbackContext):
    await update.message.reply_text("TEST KODI ni yarating:")
    return T_ID

async def ask_testID(update: Update, contesxt: CallbackContext):
    contesxt.user_data['testID'] = update.message.text
    await update.message.reply_text("TEST ga nom kiriting(Test nima haqidaligini):")
    return T_NAME

async def ask_testNAME(update: Update, context: CallbackContext):
    context.user_data['testNAME'] = update.message.text.strip().capitalize()
    return T_FILE

async def ask_testFILE(update: Update, context: CallbackContext):
    context.user_data['testFILE'] = update.message.document.file_id
    user = update.message.from_user.id
    test_id = context.user_data['testID']
    test_name = context.user_data['testNAME']
    file_path = context.user_data['testFILE']
    if db.is_admin(user.id):
        db.save_pdf(
            test_id=test_id,
            test_name=test_name,
            file_path=file_path
        )
        await update.message.reply_document(file_path, caption=f"✅ Muvaffaqiyatli saqlandi. \nTest nomi: {test_name}. \nTEST KODI: {test_id}")
    return ConversationHandler.END