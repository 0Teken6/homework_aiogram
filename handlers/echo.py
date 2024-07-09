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
    elif message.text == 'game_2':
        await bot.send_message(chat_id=message.from_user.id, text='First, your turn!')
        msg_user = await bot.send_dice(chat_id=message.from_user.id)
        await sleep(4)
        await bot.send_message(chat_id=message.from_user.id, text=f'Your score: {msg_user.dice.value}')
        await sleep(1)
        await bot.send_message(chat_id=message.from_user.id, text='My turn!')
        msg_bot = await bot.send_dice(chat_id=message.from_user.id)
        await sleep(4)
        await bot.send_message(chat_id=message.from_user.id, text=f'My score: {msg_bot.dice.value}')
        if msg_user.dice.value > msg_bot.dice.value:
            await message.answer(text=f'{msg_user.dice.value} > {msg_bot.dice.value}\nYou won!')
        elif msg_user.dice.value < msg_bot.dice.value:
            await message.answer(text=f'{msg_user.dice.value} < {msg_bot.dice.value}\nI won!')
        else:
            await message.answer(text=f'{msg_user.dice.value} = {msg_bot.dice.value}\nIt\'s a draw!')
    else:
        await message.answer(message.text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo)
