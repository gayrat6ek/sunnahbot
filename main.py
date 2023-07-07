"""
This is a echo bot.
It echoes any incoming text messages.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import requests
import psycopg2
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from datetime import datetime
#conn = psycopg2.connect(host="0.0.0.0", port=5432, database="ankalif1_sunnah",
#                        user="ankalif1_nortoy", password="JaG~4L^8,(k#")
#cur = conn.cursor()

API_TOKEN = '6013264958:AAGV29YVD_JHdV335krVxsnmfLwlGTvnadA'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
b5 = KeyboardButton("Raqamni ulashish", request_contact=True)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b5)


channel_link = f'https://t.me/Sunnahproductsuz'


# Create an InlineKeyboardButton with the channel link
channel_button = InlineKeyboardButton(text='Telegram kanal🔔', url=channel_link)
keyboard_inline = InlineKeyboardMarkup().add(channel_button)

url = f"https://api.telegram.org/bot6013264958:AAGV29YVD_JHdV335krVxsnmfLwlGTvnadA/sendMessage"


class Form(StatesGroup):
    phone_number = State()  # Will be represented in storage as 'Form:name'
    first_name = State()  # Will be represented in storage as 'Form:age'
    user_id = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    await Form.phone_number.set()

    await message.answer("Assalomu alaykum😊\n\nSunnah Products aloqa botiga xush kelibsiz! ")
    if message.chat.type == 'private':
        await message.answer('Biz siz bilan bog’lanishimiz uchun kontaktingizni qoldiring📥', reply_markup=kb_client)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone_number)
async def contacts(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
        data['user_id'] = message.from_user.id
    await Form.next()
    ReplyKeyboardRemove()
    # await state.finish()
    await message.answer('Iltimos ismingizni kiriting!', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Form.first_name)
async def echo(message: types.Message, state: FSMContext):
    date = datetime.now().date()
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    async with state.proxy() as data:
        data['first_name'] = message.text

        body = {'chat_id': -1001658409739,
                'text': "<b>Ismi:</b>  {},\n<b>Telefon raqami:</b>  {}".format(data['first_name'], data['phone_number']), 'parse_mode': 'HTML'}
        requests.post(url=url, json=body)
       # try:
       #     cur.execute("INSERT INTO \"user_data\" (user_id,first_name,phone_number,date) VALUES (%s,%s,%s,%s);",
       #                 (data['user_id'], data['first_name'], data['phone_number'],  date))
       #     conn.commit()
       # except:
       #     conn.commit()

        await message.answer('Murojaatingiz uchun rahmat\n\n😊 Mutaxassisimiz tez fursatda siz bilan bog’lanadi')
        await message.answer('Foydali ma’lumotlarni o’tkazib yubormaslik uchun Telegram kanalimizga obuna bo’ling👇🏻', reply_markup=keyboard_inline)
        await state.finish()


@dp.message_handler(commands=['count'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    if message.from_user.id in [2075574834, 1054132889]:
       # cur.execute(
       #     "SELECT COUNT(*) FROM \"user_data\" WHERE date >= current_date - interval '30' day;")
       # result = cur.fetchone()
       # cur.close
        await message.answer('Ohirgi 30 kunda royhatdan otgan foydalanuvchilar soni', parse_mode="HTML")
    else:
        await message.answer("Afsuski bu funksiyadan foydalanish uchun siz admin emassiz ;)")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,loop=None)
