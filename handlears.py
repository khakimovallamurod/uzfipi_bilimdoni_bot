from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import keyboards
import db


FAK, YUN, KURS, TEL, NAME = range(5)
T_ID, T_NAME, T_FILE, T_ANS = range(4)
# User TEST Check
T_SEND, T_CHECK = range(2)
# Admin TEST Result
RES_ID = range(1)

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if db.is_admin(user.id):
        await update.message.reply_text(
            text=f"""Assalomu aleykum {user.full_name}. Siz ushbu botda admin huqudiga egasiz. Botga test qo'shish /create va natija olish /results""",
        )
    else:
        if db.is_start(str(user.id)):
            await update.message.reply_text(
                text=f"""Xush kelibsiz. Bu bot orqali onlayn test yechishingiz mumkin, buning uchun register tugmasini bosing.""",
                reply_markup=keyboards.register_button
            )
        else:
            await update.message.reply_text("Test bajarish uchun /tests commandasini yuboring!")


async def user_register(update: Update, context: CallbackContext):
    user = update.message.from_user
    if db.user_search(user.id) == None:
        await update.message.reply_text("Fakultetingizni kiriting:")
        return FAK
    else:
        await update.message.reply_text("Siz ro'yxatdan o'tgansiz.")

async def ask_fak(update: Update, context: CallbackContext):
    context.user_data['fakultitet'] = update.message.text.strip().title()
    await update.message.reply_text("Yo'nalishingizni kiriting:")
    return YUN

async def ask_yun(update: Update, context: CallbackContext):
    context.user_data['yunalish'] = update.message.text.strip().title()
    await update.message.reply_text("Kursingizni kiriting:")
    return KURS

async def ask_kurs(update: Update, context: CallbackContext):
    context.user_data['kurs'] = update.message.text.strip()
    await update.message.reply_text("Telafon nomeringizni kiriting: ")
    return TEL

async def ask_tel(update: Update, context: CallbackContext):
    context.user_data['tel'] = update.message.text.strip()
    await update.message.reply_text("To'liq ism-familiyangizni kiriting:")
    return NAME

async def ask_name(update: Update, context: CallbackContext):
    context.user_data['fullname'] = update.message.text.strip().title()

    fakultitet = context.user_data['fakultitet']
    yunalish = context.user_data['yunalish']
    kurs = context.user_data['kurs']
    nomer = context.user_data['tel']
    full_name = context.user_data['fullname']
    user_id = update.message.from_user.id

    db.register(str(user_id),
                fak=fakultitet,
                yunlish=yunalish,
                kurs=str(kurs),
                nomer=str(nomer),
                fullname=full_name)

    await update.message.reply_text("✅ Muvaffaqiyatli ro'yxatdan o'tdingiz. Test bajarish uchun /tests commandasini yuboring!")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text('Amalyot bajarilmadi!')
    return ConversationHandler.END

# User test check
async def tests_command(update: Update, context: CallbackContext):
    await update.message.reply_text("TEST KODI ni yuboring:")
    return T_SEND

async def send_user_test(update: Update, context: CallbackContext):
    test_id = update.message.text.strip()
    user = update.message.from_user
    if not db.is_admin(user.id):
        test_data = db.get_testid(test_id=test_id)
        if test_data != []:
            await update.message.reply_document(test_data[0]['file_path'], caption=f"""Testning javoblarini ushbu botga @uzfipi_bilimdoni_bot
Maskur ✍️ Test kodi: {test_id}.\nNamuna: {test_id}*addabba ... db yoki {test_id}*1a2b3a4d.....29a30c(Ortiqcha belgilar va bosh joy bo'lmasligi kerak)""")
            return T_CHECK
        else:
            await update.message.reply_text(f"❌ Ushbu test kodi mavjud emas, tekshirib ko'ring.")
            return T_SEND

async def user_test_check(update: Update, context: CallbackContext):
    user_answers_data = update.message.text.strip()
    user_id = update.message.from_user.id
    user_answers = db.check_user_test(test_answer=user_answers_data, chat_id=str(user_id))
    
    user_data = db.user_search(chat_id=str(user_id))
    if user_answers == "error_testid":
        await update.message.reply_text("Testni yuborishda xato qildingiz test kodi bilan yuborganizga ishonch hosil qiling.")
        return T_CHECK 
    if user_answers != None:
        true_total, false_total, test_count = user_answers
        await update.message.reply_text(f"""Ismingiz: {user_data['fullname']}.
✅ To'g'ri yechilgan masala soni: {true_total}.
❌ Xato yechilgan masala soni: {false_total}.
Jami masalalar soni: {test_count}.""")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Test javoblarini yuborishda xatolik!(Namunadagidek yuborilganligiga ishonch hosil qiling.)")
        return T_CHECK


# Admin 
async def admin_creat_test(update: Update, context: CallbackContext):
    user = update.message.from_user
    if db.is_admin(user.id):
        await update.message.reply_text("TEST KODI ni yarating:")
        return T_ID
    else:
        await update.message.reply_text("❌ Siz admin emassiz!")
        return ConversationHandler.END

async def ask_testID(update: Update, context: CallbackContext):
    test_ID = update.message.text
    check_testID = db.get_testid(str(test_ID))
    if check_testID == []:
        context.user_data['testID'] = test_ID
        await update.message.reply_text("TEST ga nom kiriting(Test nima haqidaligini):")
        return T_NAME
    else:
        await update.message.reply_text("Siz yuborgan TEST KODI mavjud, iltimos yangi yarating:")
        return T_ID

async def ask_testNAME(update: Update, context: CallbackContext):
    context.user_data['testNAME'] = update.message.text.strip().capitalize()
    await update.message.reply_text("Iltimos, PDF formatida test faylini yuboring:")
    return T_FILE

async def ask_testFILE(update: Update, context: CallbackContext):
    context.user_data['testFILE'] = update.message.document.file_id
    await update.message.reply_text("TEST Javoblarini yuboring xatolik yo'qligiga ishonch hosil qiling bu tekshirishda katta ahamiyatga ega.\nNamuna: abcdaadd...d(Kichik harflarda ketma-ket kiriting).")
    return T_ANS
async def ask_testANSWER(update: Update, context: CallbackContext):
    context.user_data['testANSWER'] = update.message.text
    user_id = update.message.from_user.id
    test_id = context.user_data['testID']
    test_name = context.user_data['testNAME']
    file_path = context.user_data['testFILE']
    test_answer = context.user_data['testANSWER']
    if db.is_admin(user_id):
        db.save_pdf(
            test_id=test_id,
            test_name=test_name,
            file_path=file_path,
            test_answer=test_answer
        )
        await update.message.reply_document(file_path, caption=f"✅ Muvaffaqiyatli saqlandi. \nTest nomi: {test_name}. \nTEST KODI: {test_id}")
    else:
        await update.message.reply_text("❌ Siz admin emassiz!")

    return ConversationHandler.END

# Admin get  results
async def admin_get_results(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if db.is_admin(user_id):
        await update.message.reply_text("TEST KODI ni yuboring:")
        return RES_ID
    else:
        await update.message.reply_text("❌ Siz admin emassiz!")
        return ConversationHandler.END

async def get_results_user(update: Update, context: CallbackContext):
    test_ID = update.message.text
    user = update.message.from_user
    if db.is_admin(user.id):
        users_data = db.admin_get_result(str(test_ID))
        result_data = """"""
        if users_data!=[]:
            for idx, user_res in enumerate(users_data):
                if idx==0:
                    result_data += f"🥇 Fakultitet: {user_res['fakultitet']}, Yo'nalish: {user_res['yunalish']}, Kurs: {user_res['kurs']}, Telafon nomer: {user_res['nomer']}, FIO: {user_res['fullname']}, Natija: {user_res['true_total']} ta\n"
                elif idx==1:
                    result_data += f"🥈 Fakultitet: {user_res['fakultitet']}, Yo'nalish: {user_res['yunalish']}, Kurs: {user_res['kurs']}, Telafon nomer: {user_res['nomer']}, FIO: {user_res['fullname']}, Natija: {user_res['true_total']} ta\n"
                elif idx == 2:
                    result_data += f"🥉 Fakultitet: {user_res['fakultitet']}, Yo'nalish: {user_res['yunalish']}, Kurs: {user_res['kurs']}, Telafon nomer: {user_res['nomer']}, FIO: {user_res['fullname']}, Natija: {user_res['true_total']} ta\n"
                else:
                    result_data += f"{idx+1}. Fakultitet: {user_res['fakultitet']}, Yo'nalish: {user_res['yunalish']}, Kurs: {user_res['kurs']}, Telafon nomer: {user_res['nomer']}, FIO: {user_res['fullname']}, Natija: {user_res['true_total']} ta\n"
        else:
            result_data = "Siz yuborgan test kodida natijalar yo'q."
        await update.message.reply_text(result_data)
    else:
        await update.message.reply_text("❌ Siz admin emassiz!")
    return ConversationHandler.END