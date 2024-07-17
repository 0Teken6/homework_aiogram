from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons


class RegisterProduct(StatesGroup):
    name = State()
    size = State()
    category = State()
    price = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    await RegisterProduct.name.set()
    await message.answer(text='Write the name of product:', reply_markup=buttons.cancel)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await RegisterProduct.next()
    await message.answer(text='Write size:')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await RegisterProduct.next()
    await message.answer(text='Write category:')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await RegisterProduct.next()
    await message.answer(text='Write price:')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await RegisterProduct.next()
    await message.answer(text='Send photo:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    keyboard = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(text='Yes', callback_data='confirm_yes')
    no_button = InlineKeyboardButton(text='No', callback_data='confirm_no')
    keyboard.add(yes_button, no_button)

    await RegisterProduct.next()
    await message.answer_photo(photo=data['photo'],
                               caption=f'Name: {data["name"]}\n'
                                       f'Size: {data["size"]}\n'
                                       f'Category: {data["category"]}\n'
                                       f'Price: {data["price"]}\n\n'
                                       f'<b>Is it correct?</b>',
                               reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


async def cancel_sfm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Canceled', reply_markup=buttons.start_buttons)


async def submit(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirm_yes':
        await callback_query.message.answer(text='Data is saved!', reply_markup=buttons.start_buttons)
        await state.finish()
    elif callback_query.data == 'confirm_no':
        await callback_query.message.answer(text='Canceled', reply_markup=buttons.start_buttons)
        await state.finish()
    else:
        await callback_query.message.answer(text='Tap on a button')


def register_fsm_for_prod(dp: Dispatcher):
    dp.register_message_handler(cancel_sfm, Text(equals='Cancel', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['register_product'])
    dp.register_message_handler(load_name, state=RegisterProduct.name)
    dp.register_message_handler(load_size, state=RegisterProduct.size)
    dp.register_message_handler(load_category, state=RegisterProduct.category)
    dp.register_message_handler(load_price, state=RegisterProduct.price)
    dp.register_message_handler(load_photo, state=RegisterProduct.photo, content_types=['photo'])
    dp.register_callback_query_handler(submit, state=RegisterProduct.submit)

