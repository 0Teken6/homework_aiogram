from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def webapp_inline(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('Geeks online', web_app=types.WebAppInfo(url='https://online.geeks.kg')),
                 InlineKeyboardButton('Kaktus Media', web_app=types.WebAppInfo(url='https://kaktus.media')),
                 InlineKeyboardButton('Netflix', web_app=types.WebAppInfo(url='https://www.netflix.com/kg-ru/')),
                 InlineKeyboardButton('Youtube', web_app=types.WebAppInfo(url='https://www.youtube.com/')),
                 InlineKeyboardButton('Instagram', web_app=types.WebAppInfo(url='https://www.instagram.com/'))
                 )

    await message.answer('Tap on a button below to enter the site:', reply_markup=keyboard)


def register_webapp(dp: Dispatcher):
    dp.register_message_handler(webapp_inline, commands=['webinline'])