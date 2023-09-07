from aiogram import Dispatcher, types

from src.telegram.logic._start import start

from src.telegram.sendler.sendler import *

from src.telegram.keyboard.keyboards import *

from src.telegram.bot_core import BotDB

from aiogram.dispatcher import FSMContext

from src.telegram.state.states import States


async def admin_panel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await Sendler_msg.log_client_call(call)

    id_user = call.message.chat.id

    if str(id_user) not in ADMIN:
        return False

    keyb = ClientKeyb().admin_menu()

    text_admin = 'Админ панель:'

    await Sendler_msg().sendler_photo_call(call, ADMIN_IMG, text_admin, keyb)


async def balance(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    id_user = call.message.chat.id

    balance = BotDB.get_balance(id_user)

    _msg = f'🍀 Ваш баланс: {balance} ₽'

    keyb = ClientKeyb().menu_back()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)


async def menu_back(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    await start(call.message)

    return True


async def ower_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await Sendler_msg.log_client_call(call)

    await start(call.message)


async def add_product(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    admin_text = (f'🔫 Пришлите наименование товара или нажмите отмена')

    keyboard = ClientKeyb().admin_back()

    try:
        await call.message.reply(admin_text, reply_markup=keyboard)

    except Exception as es:
        print(f'Ошибка отправки сообщение о add_product "{es}"')

    await States.add_name_product.set()


async def back_name_product(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    admin_text = (f'🔫 Пришлите наименование товара или нажмите отмена')

    keyboard = ClientKeyb().admin_back()

    await States.add_name_product.set()

    await call.message.reply(admin_text, reply_markup=keyboard)


async def back_name_descript(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    admin_text = f'📝 пришлите следующим сообщением описание товара\n\n'

    keyboard = ClientKeyb().back_name_product()

    await States.add_descript_product.set()

    await call.message.reply(admin_text, reply_markup=keyboard)


async def back_price_descript(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    admin_text = f'💰 пришлите следующим сообщением цену на товар'

    keyboard = ClientKeyb().back_descript_product()

    await States.add_descript_product.set()

    await call.message.reply(admin_text, reply_markup=keyboard)


async def salle(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    product_list_ = BotDB.get_all_products()

    if product_list_ == []:

        text_admin = (f'⛔️ В настоящий момент наша витрина пуста, пожалуйста попробуйте позже')

    else:

        text_admin = (f'Каталог:\n\n')

        for product in product_list_:
            text_admin += f'{product[1]}  {product[2]}  {product[3]} ₽\n\n'

    keyb = ClientKeyb().products_all(product_list_)

    await Sendler_msg().sendler_photo_call(call, LOGO, text_admin, keyb)


async def go(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    id_user = call.message.chat.id

    try:

        _, id_product = str(call.data).split('_')

    except:

        error = (f'Ошибка при разборе go_')

        print(error)

        await Sendler_msg.send_msg_call(call, error, None)

        return False

    tur_name = BotDB.get_products_by_id(id_product)

    name_product = tur_name[1]

    descript_product = tur_name[2]

    price_product = tur_name[3]

    img_product = tur_name[4]

    _product_text = (f'<b>{name_product}</b>\n\n'
                     f'{descript_product}\n\n'
                     f'<b>{price_product} ₽</b>')

    keyb = ClientKeyb().buy_menu(id_product, id_user)

    await Sendler_msg().sendler_photo_call(call, img_product, _product_text, keyb)


async def buy_(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    id_user = call.message.chat.id

    try:

        _, id_product = str(call.data).split('_')

    except:

        error = (f'Ошибка при разборе buy_')

        print(error)

        await Sendler_msg.send_msg_call(call, error, None)

        return False

    _product = BotDB.get_products_by_id(id_product)

    name_product = _product[1]

    descript_product = _product[2]

    price_product = _product[3]

    img_product = _product[4]

    balance = BotDB.get_balance(id_user)

    balance = int(balance)

    price_product = int(price_product)

    if price_product > balance:
        _product_text = (f'⚠️ К сожалению, я не могу выполнить вашу покупку на данный момент, '
                         f'так как у вас недостаточно средств на балансе для покупки.\n\n'
                         f'Ваш баланс: {balance}')

        print(f'{id_user} {_product_text}')

        keyb = ClientKeyb().buy_menu(id_product, id_user)

        await Sendler_msg().new_sendler_photo_call(call, img_product, _product_text, keyb)

        return False

    # TODO списать баланс

    # TODO запросить ссылку

    _product_text = (f'🔥 Укажите трейд-ссылку для получения товара')

    keyb = ClientKeyb().ower_state()

    await Sendler_msg().sendler_photo_call(call, img_product, _product_text, keyb)

    await States.add_traide_lik.set()

    async with state.proxy() as data:
        data['id_product'] = id_product
        data['product'] = _product
        data['balance'] = balance


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(admin_panel, text_contains='admin_panel', state='*')
    dp.register_callback_query_handler(ower_state, text_contains='ower_state', state='*')
    dp.register_callback_query_handler(menu_back, text_contains='menu_back')

    dp.register_callback_query_handler(balance, text_contains='balance')

    dp.register_callback_query_handler(add_product, text='add_product')

    dp.register_callback_query_handler(salle, text='salle')

    dp.register_callback_query_handler(back_name_product, text_contains='back_name_product', state='*')
    dp.register_callback_query_handler(back_name_descript, text_contains='back_name_descript', state='*')
    dp.register_callback_query_handler(back_price_descript, text_contains='back_price_descript', state='*')

    dp.register_callback_query_handler(go, text_contains='go_')

    dp.register_callback_query_handler(buy_, text_contains='buy_')
