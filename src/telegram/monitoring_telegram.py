import time

from pyrogram import Client
from pyrogram.raw.functions.messages import GetMessageReactionsList

from settings import *

from datetime import datetime, timedelta


class MonitoringTelegram:
    def __init__(self, sessions_patch, BotDB):
        self.BotDB = BotDB
        self.path = sessions_patch + f'/{API_ID}'

    async def start_tg(self):

        print(f'{datetime.now().strftime("%H:%M:%S")} Инициализирую вход в аккаунт {API_ID}')

        try:
            self.app = Client(self.path, API_ID, API_HASH)

            await self.app.start()

        except Exception as es:
            print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка при авторизации ({API_ID}) "{es}"')

            return False

        return self

    async def get_reactions(self, chat_id, message):
        try:
            r_peer = await self.app.resolve_peer(chat_id)

            reackt_list = await self.app.invoke(GetMessageReactionsList(peer=r_peer, id=message.id,
                                                                        limit=-1))
        except Exception as es:
            print(f'Ошибка при получении реакции "{es}"')

            return []

        return reackt_list

    async def get_comments(self, message):
        async for reply in self.app.get_discussion_replies(message.chat.username, message.id):

            date_post = message.date

            target_time = reply.date - date_post

            if reply.sticker is not None:
                continue

            print(f'Коммент: {reply.text} от {reply.from_user.id}')

            if target_time < timedelta(minutes=CHECKPOINT_ONE):
                print(f'Комментарий до 5 минут')

                continue

            if target_time < timedelta(hours=CHECKPOINT_TWO):
                print(f'Комментарий до 1 часа')

                continue

            print(f'Комментарий больше 1 часа')

            print()

        return True

    async def start_monitoring_chat(self, chat_id):

        async for message in self.app.get_chat_history(chat_id):

            target_time = datetime.now() - message.date

            if target_time > timedelta(weeks=4):
                continue

            res_get_comment = await self.get_comments(message)

            print()

    async def get_id_chat(self, name_link):
        try:

            name_chat = name_link.replace('https://t.me/', '')

        except Exception as es:
            print(f'Не могу получить вырезать имя чата "{name_link}" "{es}"')

            return False

        while True:
            try:
                res_chat = await self.app.get_chat(name_chat)
            except Exception as es:
                print(f'Исключения при получение ID чат {es}')
                return False

            id_chat = res_chat.id

            return id_chat
