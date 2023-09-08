import random

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from settings import ADMIN


class Call_admin:

    def admin(self):
        self._admin = CallbackData('adm', 'type', 'number', 'id')

        return self._admin


class ClientKeyb(Call_admin):
    """@developer_telegrams разработка программ"""

    def start_keyb(self, id_user):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🍭‍ Витрина', callback_data='salle'))

        self._start_key.add(InlineKeyboardButton(text=f'💵‍ Баланс', callback_data='balance'))

        if str(id_user) in ADMIN:
            self._start_key.add(InlineKeyboardButton(text=f'👨‍💻 Админ панель', callback_data='admin_panel'))

        return self._start_key

    def admin_back(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='admin_panel'))

        return self._start_key

    def menu_back(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='menu_back'))

        return self._start_key

    def admin_menu(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔖 Добавить товар', callback_data='add_product'))

        self._start_key.add(InlineKeyboardButton(text=f'📨 Рассылка', callback_data='allsendler'))

        self._start_key.add(InlineKeyboardButton(text=f'🕳 Обнулить баланс', callback_data='zero'))

        self._start_key.add(InlineKeyboardButton(text=f'👨‍👩‍👧‍👦 Пользователи', callback_data='list_users'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='menu_back'))

        return self._start_key

    def ower_state(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'❌ Отмена', callback_data=f'ower_state'))

        return self._start_key

    def back_name_product(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='back_name_product'))

        return self._start_key

    def back_descript_product(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='back_name_descript'))

        return self._start_key

    def back_price_product(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='back_price_descript'))

        return self._start_key

    def products_all(self, products_list):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        icon_list = ['🔪', '🔫', '💣', '🗡']

        for product in products_list:
            id_prodict = product[0]
            icon_ = random.choice(icon_list)
            name_product = f"{icon_} {product[1]}"

            self._start_key.insert(InlineKeyboardButton(text=f'{name_product}', callback_data=f'go_{id_prodict}'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='menu_back'))

        return self._start_key

    def buy_menu(self, id_pk, id_user):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'💎 Купить', callback_data=f'buy_{id_pk}'))

        if str(id_user) in ADMIN:
            self._start_key.add(InlineKeyboardButton(text=f'🗑 Удалить', callback_data=f'del_{id_pk}'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='salle'))

        return self._start_key

    def sendler_mitting_start_keyb(self):
        self._pass_keyb = InlineKeyboardMarkup(row_width=1)

        self._pass_keyb.add(InlineKeyboardButton(text=f'✅ Отправить', callback_data='ye_se_mit'))

        self._pass_keyb.add(InlineKeyboardButton(text=f'❌ Отмена', callback_data='admin_panel'))

        return self._pass_keyb
