from telegram.constants import ParseMode
import os
from telegram import ReplyKeyboardMarkup,Update,WebAppInfo,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,PicklePersistence

)
from dotenv import load_dotenv
import requests
load_dotenv()
telegram_link = 'https://t.me/Sunnahproductsuz'

#Base.metadata.create_all(bind=engine)
BOTTOKEN = os.environ.get('BOT_TOKEN')
BITRIX = os.environ.get('BITRIX')
url = f"https://api.telegram.org/bot{BOTTOKEN}/sendMessage"
PHONENUMBER,FULLNAME,= range(2)
persistence = PicklePersistence(filepath='hello.pickle')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    keyboard =[[KeyboardButton(text='Raqamni ulashish', request_contact=True)]]
    await update.message.reply_text('Assalomu alaykum😊\n\nSunnah Products aloqa botiga xush kelibsiz!')
    await update.message.reply_text('Biz siz bilan bog’lanishimiz uchun kontaktingizni qoldiring📥',reply_markup=ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True))

    return PHONENUMBER




async def phonenumber(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['phone_number'] = update.message.contact.phone_number
    await update.message.reply_text('Ismingizni kiriting📝',reply_markup=ReplyKeyboardRemove())
    return FULLNAME


async def fullname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['full_name'] = update.message.text
    await update.message.reply_text('Murojaatingiz uchun rahmat\n\n😊 Mutaxassisimiz tez fursatda siz bilan bog’lanadi')
    await update.message.reply_text('Foydali ma’lumotlarni o’tkazib yubormaslik uchun Telegram kanalimizga obuna bo’ling👇🏻\n',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Посмотреть фото/видео',url=telegram_link)]]))
    body = {'chat_id': -1001658409739,
                'text': "<b>Ismi:</b>  {},\n<b>Telefon raqami:</b>  {}".format(context.user_data['full_name'], context.user_data['phone_number']), 'parse_mode': 'HTML'}
    requests.post(url=url, json=body)
    bitrix = f"{BITRIX}/crm.lead.add.json?FIELDS[TITLE]=TELEGRAM&FIELDS[NAME]={context.user_data['full_name']}&FIELDS[LAST_NAME]={context.user_data['full_name']}&FIELDS[PHONE][0][VALUE]={context.user_data['phone_number']}&FIELDS[PHONE][0][VALUE_TYPE]=Telegram bot"

    data = requests.post(url=bitrix)
    print(data.content)
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    #add states phone fullname category desction and others 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            #LANGUAGE: [MessageHandler(filters.TEXT,language)],
            PHONENUMBER:[MessageHandler(filters.CONTACT,phonenumber)],
            FULLNAME:[MessageHandler(filters.TEXT,fullname)],

        },
        fallbacks=[CommandHandler('start',start)],
        allow_reentry=True,
        name="my_conversation",
        persistent=True,

    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
