from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import coc
import db

db.create_table()

TOKEN = 'YOUR_TOKEN'

NAME, NUMBER, MENU, TAG, CLAN_WAR_STATUS = range(5)

def start(update: Update, context: CallbackContext):
    user = db.get_user(update.effective_user.id)
    if user:
        update.message.reply_text(f"Welcome back, {user[1]}")
        return main_menu(update, context)
    
    update.message.reply_text("Ismingizni kriting 🫴")
    return NAME

def get_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    update.message.reply_text(
        "Raqaminizni kriting 🫴",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("📱 Raqamni yuborish", request_contact=True)]],
            resize_keyboard=True
        )
    )
    return NUMBER

def get_number(update: Update, context: CallbackContext):
    if not update.message.contact:
        update.message.reply_text("Iltimos, tugma orqali raqam yuboring.")
        return NUMBER

    tg_id = update.effective_user.id
    name = context.user_data["name"]
    number = update.message.contact.phone_number
    db.add_users(tg_id, name, number)

    update.message.reply_text("✅ Ro'yhatdan o'tdingiz")
    return main_menu(update, context)

def main_menu(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Asosiy menyu:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("💻 User bo'yicha ma'lumot olish")],
                     [KeyboardButton("🛡 Klan war stusi")]],
            resize_keyboard=True
        )
    )
    return MENU

def menu_choice(update: Update, context: CallbackContext):
    if update.message.text == "💻 User bo'yicha ma'lumot olish":
        update.message.reply_text("🆔 Player tag kriting")
        return TAG
    if update.message.text == "🛡 Klan war stusi":
        update.message.reply_text("🆔 Klan tagni kriting")
        return CLAN_WAR_STATUS
    update.message.reply_text("Iltimos, menyudan tanlang")
    return MENU

def get_player_tag(update: Update, context: CallbackContext):
    tag = update.message.text.strip()
    update.message.reply_text("🔎 Ma'lumot olinmoqda...")
    result = coc.get_player_info(tag)
    update.message.reply_text(result)
    return main_menu(update, context)

def get_war_status(update: Update, context: CallbackContext):
    tag =update.message.text.strip()
    update.message.reply_text("🔎 Ma'lumot olinmoqda...")
    result = coc.clan_war_status(tag)
    update.message.reply_text(result)
    return main_menu(update, context)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            NUMBER: [MessageHandler(Filters.contact, get_number)],
            MENU: [MessageHandler(Filters.text & ~Filters.command, menu_choice)],
            TAG: [MessageHandler(Filters.text & ~Filters.command, get_player_tag)],
            CLAN_WAR_STATUS: [MessageHandler(Filters.text & ~Filters.command, get_war_status)],
        },
        fallbacks=[]
    )

    dp.add_handler(conv)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()