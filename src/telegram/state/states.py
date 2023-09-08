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

    add_traide_lik = State()

    sendler_photo = State()

    ad_text = State()

    zero = State()


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


async def add_traide_lik(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    traide_link = message.text

    id_product = ''

    _product = ''

    balance = ''

    id_user = message.chat.id

    async with state.proxy() as data:
        id_product = data['id_product']

        _product = data['product']

        balance = data['balance']

    name_product = _product[1]

    descript_product = _product[2]

    price_product = _product[3]

    img_product = _product[4]

    total_balance = balance - int(price_product)

    res_refresh_balance = BotDB.update_balance(id_user, total_balance)

    _msg = f'✅ Покупка успешна совершена. Ожидайте выдачу товара'

    keyb = ClientKeyb().start_keyb(id_user)

    await Sendler_msg().sendler_photo_message(message, LOGO, _msg, keyb)

    await state.finish()

    _msg_admin = f'🛎 Совершена покупка\n\n' \
                 f'Пользователь "{id_user}"\n' \
                 f'Товар "{name_product}"\n' \
                 f'Цена: {price_product} ₽\n\n' \
                 f'Трейд-ссылка: {traide_link}'

    await Sendler_msg.sendler_to_admin(message, _msg_admin, None)


async def sendler_photo(message: Message, state: FSMContext):
    ERROR_SCREEN = f'⚠️ Вы не верно прислали скриншот подтверждения оплаты!\n\n' \
                   f'Пришлите мне следующим сообщением скриншот Вашего перевода\n\n'

    keyboard = ClientKeyb().admin_back()

    if message.photo == []:
        await message.reply(ERROR_SCREEN, reply_markup=keyboard)
        return False

    GOOD_SCREEN_MSG = f'Изображения для сообщения принято, пришлите следующим сообщением текст для рассылки'

    await Sendler_msg.send_msg_message(message, GOOD_SCREEN_MSG, keyboard)

    async with state.proxy() as data:
        file_name = (f'src/telegram/media/sendler/{message.photo[-1].file_unique_id}.jpg')

        try:
            await message.photo[-1].download(destination_file=file_name)
        except Exception as es:
            await message.reply(f'Не смог сохранить изображение попробуйте ещё {es}')

        data['add_image'] = file_name

    await States.ad_text.set()


async def ad_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_send'] = message.text

    send_text = f'Вы ввели текст:\n\n***{data["text_send"]}***\n\nПодтверждаете отправку?'

    keyb = ClientKeyb().sendler_mitting_start_keyb()

    await Sendler_msg().sendler_photo_message(message, data['add_image'], send_text, keyb)

    await States.ad_text.set()


async def zero(message: Message, state: FSMContext):
    id_user_zero = message.text

    if not id_user_zero.isdigit():
        error = (f'⚠️ Не верно указан ID пользователя. Попробуйте ещё раз')
        print(error)

        await Sendler_msg.send_msg_message(message, error, None)

        return False

    check_user = BotDB.exist_id_user(id_user_zero)

    if not check_user:
        error = (f'⚠️ Указан несуществующий ID пользователя. Попробуйте ещё раз')
        print(error)

        await Sendler_msg.send_msg_message(message, error, None)

        return False

    res_add = BotDB.zero_balance(id_user_zero)

    if res_add:
        _MSG = f'✅ Обнулил баланс у {id_user_zero}'
    else:
        _MSG = f'🚫️ ошибка при обнуление баланса у {id_user_zero}'

    keyb = ClientKeyb().admin_menu()

    await Sendler_msg().sendler_photo_message(message, ADMIN_IMG, _MSG, keyb)

    await state.finish()


def register_state(dp: Dispatcher):
    """@developer_telegrams разработка программ"""

    dp.register_message_handler(add_name_product, state=States.add_name_product)

    dp.register_message_handler(add_descript_product, state=States.add_descript_product)

    dp.register_message_handler(add_price_product, state=States.add_price_product)

    dp.register_message_handler(add_traide_lik, state=States.add_traide_lik)

    dp.register_message_handler(add_img_product, state=States.add_img_product, content_types=[types.ContentType.ANY])

    dp.register_message_handler(sendler_photo, state=States.sendler_photo, content_types=[types.ContentType.ANY])

    dp.register_message_handler(ad_text, state=States.ad_text)

    dp.register_message_handler(zero, state=States.zero)
