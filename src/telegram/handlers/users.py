from aiogram.types import Message

from aiogram import Dispatcher

from settings import *
from src.telegram.logic._start import start


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start')
