import logging

import asyncio

from src.telegram.bot_core import *
from src.telegram.handlers.users import *
from src.telegram.state.states import *
from src.telegram.callbacks.call_user import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import os

from src.telegram.iter_chat import IterChat

from src.telegram.monitoring_telegram import MonitoringTelegram


logging.basicConfig(level=logging.CRITICAL)


def registration_all_handlers(dp):
    register_user(dp)


def registration_state(dp):
    register_state(dp)


def registration_calls(dp):
    register_callbacks(dp)


async def main():
    """@developer_telegrams разработка программ"""

    bot_start = Core()

    scheduler = AsyncIOScheduler()

    sessions_path = os.path.join(os.path.dirname(__file__), 'src', 'sessions')

    telegram_core = await MonitoringTelegram(sessions_path, bot_start.BotDB).start_tg()

    autoloads = await IterChat(telegram_core, BotDB).get_posts()

    scheduler.add_job(IterChat(telegram_core, BotDB).get_posts, 'interval', seconds=CHECK_TIME, misfire_grace_time=300)

    registration_state(bot_start.dp)
    registration_all_handlers(bot_start.dp)
    registration_calls(bot_start.dp)

    scheduler.start()

    try:
        await bot_start.dp.start_polling()
    finally:
        await bot_start.dp.storage.close()
        await bot_start.dp.storage.wait_closed()
        await bot_start.bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
