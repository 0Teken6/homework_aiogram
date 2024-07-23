from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons
from db import main_db
from aiogram.dispatcher.filters import Text


async def show_products(message: types.Message):
    products = await main_db.sql_get_products()
    if products:
        for product in products:
            await message.answer_photo(photo=product[5],
                                       caption=f'Name: {product[1]}\n'
                                               f'Size: {product[2]}\n'
                                               f'Category: {product[-2]}\n'
                                               f'Price: {product[3]}\n'
                                               f'Product ID: {product[4]}\n'
                                               f'Product Info: {product[-1]}\n')
    else:
        await message.answer(text='There is no products!')


async def show_product_by_id(message: types.Message, id=None):
    if id is None:
        id = 1
    product = await main_db.sql_get_product_by_id(id)

    keyboard = InlineKeyboardMarkup()
    next_buttons = InlineKeyboardButton('Next', callback_data=f'next_{id+1}')
    keyboard.add(next_buttons)
    await message.answer_photo(photo=product[5],
                               caption=f'Name: {product[1]}\n'
                                       f'Size: {product[2]}\n'
                                       f'Category: {product[-2]}\n'
                                       f'Price: {product[3]}\n'
                                       f'Product ID: {product[4]}\n'
                                       f'Product Info: {product[-1]}\n', reply_markup=keyboard)


async def show_next_product(callback_query: types.CallbackQuery):
    id = int(callback_query.data.split('_')[1])

    quantity_of_products = await main_db.sql_get_number_of_products()

    if quantity_of_products >= id:
        await show_product_by_id(callback_query.message, id)
    else:
        await callback_query.message.answer('No more products', reply_markup=buttons.start_buttons)


def register_products_commands(dp: Dispatcher):
    dp.register_message_handler(show_products, commands=['show_products'])
    dp.register_message_handler(show_product_by_id, commands=['show_product'])
    dp.register_callback_query_handler(show_next_product, Text(startswith='next_'))
