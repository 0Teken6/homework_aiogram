import random
from asyncio import sleep

from aiogram import types, Dispatcher
from config import bot


async def echo(message: types.Message):
    if message.text.isdigit():
        await message.answer(int(message.text)**2)
    elif message.text == 'game':
        emoji = random.choice(['⚽', '🎰', '🏀', '🎯', '🎳', '🎲'])
        await bot.send_dice(chat_id=message.from_user.id, emoji=emoji)
    else:
        await message.answer(message.text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo)
