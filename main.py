import logging

import asyncio

import os

from src.sql.bot_connector import BotDB
from src.telegram.iter_chat import IterChat

from src.telegram.monitoring_telegram import MonitoringTelegram


# logging.basicConfig(level=logging.CRITICAL)


async def main():
    sessions_path = os.path.join(os.path.dirname(__file__), 'src', 'sessions')

    telegram_core = await MonitoringTelegram(sessions_path, BotDB).start_tg()

    dict_posts = await IterChat(telegram_core, BotDB).get_posts()

    print()


if __name__ == '__main__':
    asyncio.run(main())
