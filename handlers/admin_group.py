import logging
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Admins, bot

spam_words = ['spam', 'follow me', 'discounts', 'fool']

user_warnings = {}


async def welcome_user(message: types.Message):
    for member in message.new_chat_members:
        await message.answer(f"Welcome {member.full_name}!\n\n"
                             f"What is forbidden:\n"
                             f"Do not spam\n"
                             f"Do not advertise\n"
                             f"Do not curse\n"
                             )


async def warn_user(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in Admins:
            await message.answer('You are not an admin')
        elif not message.reply_to_message:
            await message.answer("Command should be the answer for replayed message")
        else:
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.full_name
            user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

            if user_warnings[user_id] == 3:
                await bot.kick_chat_member(message.chat.id, user_id)
                await bot.send_message(chat_id=message.chat.id,
                                       text='User was deleted because of the number of warnings')
                for admin in Admins:
                    await bot.send_message(chat_id=admin,
                                           text=f'{user_name} has received warning ({user_warnings[user_id]}/3)')
                    await bot.send_message(chat_id=admin, text=f'{user_name} was kicked for the 3 warnings')
            for admin in Admins:
                await bot.send_message(chat_id=admin,
                                        text=f'{user_name} has received warning ({user_warnings[user_id]}/3)')


async def pin_message(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in Admins:
            await message.answer('You are not an admin')
        elif not message.reply_to_message:
            await message.answer("Command should be the answer for replayed message")
        else:
            await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)


async def delete_user_handler(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in Admins:
            await message.answer('You are not an admin')
        elif not message.reply_to_message:
            await message.answer("Command should be the answer for replayed message")
        else:
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.full_name

            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(InlineKeyboardButton("Delete", callback_data=f'delete_user {user_id}'))

            await message.answer(f'Are you sure you want delete {user_name}?', reply_markup=keyboard)
    else:
        await message.answer('This command should be used in group')


async def complete_delete_user(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.replace('delete_user ', ''))
    try:
        await bot.kick_chat_member(callback_query.message.chat.id, user_id)
        await callback_query.answer(text='User is deleted', show_alert=True)
        await bot.send_message(chat_id=callback_query.message.chat.id, text='User was deleted because admin kicked him')
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except Exception as e:
        logging.error(f'Error in complete_delete_user: {e}')
        await callback_query.answer(text='Could not delete the user', show_alert=True)


async def filter_spam(message: types.Message):
    for word in spam_words:
        if word in message.text:
            await message.delete()
            await message.answer("Don't spam and curse!")
            break


def register_admin_group(dp: Dispatcher):
    dp.register_message_handler(welcome_user, content_types=[types.ContentTypes.NEW_CHAT_MEMBERS])
    dp.register_message_handler(warn_user, commands=['warn'], commands_prefix='!/')
    dp.register_message_handler(delete_user_handler, commands=['d'], commands_prefix='!/')
    dp.register_callback_query_handler(complete_delete_user, lambda call: call.data and call.data.startswith('delete_user '))
    dp.register_message_handler(pin_message, commands=['pin'], commands_prefix='!/')
    dp.register_message_handler(filter_spam)
