from datetime import datetime

from settings import TELEGRAM_CHANNELS


class IterChat:
    """@developer_telegrams разработка программ"""

    def __init__(self, telegram_core, BotDB):
        self.telegram_core = telegram_core
        self.BotDB = BotDB

    async def get_posts(self):
        id_chat = await self.telegram_core.get_id_chat(TELEGRAM_CHANNELS)

        if not id_chat:
            return False

        print(f'\n{datetime.now().strftime("%H:%M:%S")} запускаю анализ комментариев')

        dict_post = await self.telegram_core.start_monitoring_chat(id_chat)

        return True
