from src.telegram.keyboard.keyboards import ClientKeyb
from src.telegram.sendler.sendler import Sendler_msg

from aiogram.types import Message

from src.telegram.bot_core import BotDB

from settings import START_MESSAGE, LOGO


async def start(message: Message):
    await Sendler_msg.log_client_message(message)

    id_user = message.chat.id

    login = message.chat.username

    check_new_user = BotDB.check_or_add_user(id_user, login, 'new')

    keyb = ClientKeyb().start_keyb(id_user)

    await Sendler_msg().sendler_photo_message(message, LOGO, START_MESSAGE, keyb)
