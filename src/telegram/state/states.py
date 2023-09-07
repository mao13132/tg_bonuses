from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from settings import ADMIN_IMG, LOGO
from src.telegram.keyboard.keyboards import ClientKeyb
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB


class States(StatesGroup):
    add_name_product = State()

    add_descript_product = State()

    add_price_product = State()

    add_img_product = State()


async def add_name_product(message: Message, state: FSMContext):
    name_product = message.text

    async with state.proxy() as data:
        data['name_product'] = name_product

    _msg = f'📝 пришлите следующим сообщением описание товара\n\n' \
           f'Ваше имя товара "{name_product}" принято.'

    keyb = ClientKeyb().back_name_product()

    await Sendler_msg().sendler_photo_message(message, ADMIN_IMG, _msg, keyb)

    await States.add_descript_product.set()


async def add_descript_product(message: Message, state: FSMContext):
    descript_product = message.text

    async with state.proxy() as data:
        data['descript_product'] = descript_product

    _msg = f'💰 пришлите следующим сообщением цену на товар\n\n' \
           f'Ваше описание товара "{descript_product}" принято.'

    keyb = ClientKeyb().back_descript_product()

    await Sendler_msg().sendler_photo_message(message, ADMIN_IMG, _msg, keyb)

    await States.add_price_product.set()


async def add_price_product(message: Message, state: FSMContext):
    price_product = message.text

    if not price_product.isdigit():
        error = (f'⚠️ Не верно указана цена. Попробуйте ещё раз')
        print(error)

        await Sendler_msg.send_msg_message(message, error, None)

        return False

    async with state.proxy() as data:
        data['price_product'] = price_product

    _msg = f'📱 пришлите следующим сообщением изображение товара\n\n' \
           f'Ваша цена товара "{price_product}" принята.'

    keyb = ClientKeyb().back_price_product()

    await Sendler_msg().sendler_photo_message(message, ADMIN_IMG, _msg, keyb)

    await States.add_img_product.set()


async def add_img_product(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    ERROR_SCREEN = f'⚠️ Вы не верно прислали изображение товара. Попробуйте снова'

    if message.photo == []:
        keyboard = ClientKeyb().back_price_product()
        await message.reply(ERROR_SCREEN, reply_markup=keyboard)
        return False

    name_product = ''

    async with state.proxy() as data:
        file_name = (f'src/telegram/media/products/{message.photo[-1].file_unique_id}.jpg')

        try:
            await message.photo[-1].download(destination_file=file_name)
        except Exception as es:
            await message.reply(f'Не смог сохранить изображение попробуйте ещё {es}')

            return False

        name_product = data['name_product']

        res_add = BotDB.add_product(data['name_product'], data['descript_product'],
                                    data['price_product'], file_name)

    if res_add:
        GOOD_SCREEN_MSG = f'✅ "{name_product}" товар добавлен'
    else:
        GOOD_SCREEN_MSG = f'⛔️ Ошибка при добавление товара "{name_product}"'

    await Sendler_msg().sendler_photo_message(message, LOGO, GOOD_SCREEN_MSG, ClientKeyb().admin_menu())

    await state.finish()


def register_state(dp: Dispatcher):
    dp.register_message_handler(add_name_product, state=States.add_name_product)

    dp.register_message_handler(add_descript_product, state=States.add_descript_product)

    dp.register_message_handler(add_price_product, state=States.add_price_product)

    dp.register_message_handler(add_img_product, state=States.add_img_product, content_types=[types.ContentType.ANY])
