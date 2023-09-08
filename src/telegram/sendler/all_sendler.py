import os

from aiogram import types


class AllSendler:
    """@developer_telegrams разработка программ"""

    def __init__(self, BotDB, call: types.CallbackQuery, data):
        self.BotDB = BotDB
        self.call = call
        self.data = data

    async def send_group(self):

        list_client = self.BotDB.get_all_users()

        good_count = 0

        for client in list_client:
            id_tg = int(client[1])

            try:
                with open(self.data['add_image'], 'rb') as file:
                    to_pin = await self.call.bot.send_photo(id_tg, file, caption=self.data['text_send'])

                    good_count += 1

                    try:
                        await self.call.bot.pin_chat_message(chat_id=id_tg,
                                                             message_id=to_pin['message_id'])
                    except:
                        pass

            except Exception as es:
                print(f'Ошибка при рассылке ({id_tg}) всем {es}')
                continue

        os.remove(self.data['add_image'])

        return good_count
