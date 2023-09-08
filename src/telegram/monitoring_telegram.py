import time

from pyrogram import Client
from pyrogram.raw.functions.messages import GetMessageReactionsList

from settings import *

from datetime import datetime, timedelta


class MonitoringTelegram:
    """@developer_telegrams разработка программ"""

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

    async def get_comments(self, message, chat_id):

        total_count = 0

        try:
            async for reply in self.app.get_discussion_replies(chat_id, message.id):

                try:
                    id_user = reply.from_user.id
                except:
                    continue

                login = reply.from_user.username

                check_payment = self.BotDB.exist_payment(id_user, message.id)

                if check_payment:
                    continue

                check_new_user = self.BotDB.check_or_add_user(id_user, login, 'no')

                date_post = message.date

                target_time = reply.date - date_post

                if reply.sticker is not None:
                    continue

                if target_time < timedelta(minutes=CHECKPOINT_ONE):
                    res_add = self.BotDB.add_balance(id_user, PAYMENT_ONE)
                    res_add = self.BotDB.add_payment(id_user, message.id, PAYMENT_ONE)

                    total_count += 1

                    continue

                if target_time < timedelta(hours=CHECKPOINT_TWO):
                    res_add = self.BotDB.add_balance(id_user, PAYMENT_TWO)
                    res_add = self.BotDB.add_payment(id_user, message.id, PAYMENT_TWO)

                    total_count += 1

                    continue

                res_add = self.BotDB.add_balance(id_user, PAYMENT_THREE)
                res_add = self.BotDB.add_payment(id_user, message.id, PAYMENT_THREE)

                total_count += 1

        except:
            pass

        return total_count

    async def start_monitoring_chat(self, chat_id):

        async for message in self.app.get_chat_history(chat_id):

            target_time = datetime.now() - message.date

            if target_time > timedelta(weeks=4):
                continue

            count_comments = await self.get_comments(message, chat_id)

            if count_comments > 0:
                print(f'{datetime.now().strftime("%H:%M:%S")} {count_comments}шт комментариев оплатил.\n'
                      f'Пост: {message.link}\n')


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
