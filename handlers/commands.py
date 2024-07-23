import glob
import os
import random
import buttons
from aiogram import types, Dispatcher
from aiogram.types import InputFile

from config import bot


async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет! {message.from_user.first_name}', reply_markup=buttons.start_buttons)


async def mem(message: types.Message):
    path = 'media/'
    files = glob.glob(os.path.join(path, "*"))
    random_photo = random.choice(files)
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=InputFile(random_photo))


async def file(message: types.Message):
    path = 'files/'
    files = glob.glob(os.path.join(path, '*'))
    random_file = random.choice(files)
    await message.answer_document(document=InputFile(random_file))


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(mem, commands=['mem'])
    dp.register_message_handler(file, commands=['file'])
