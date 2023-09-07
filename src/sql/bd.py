import datetime
import sqlite3
from datetime import datetime


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"users (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_user TEXT, login TEXT, status TEXT, join_date DATETIME, balance INT  DEFAULT 0, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table users {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"products (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"name TEXT, descript TEXT, price INT, img TEXT, other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table products {es}')

    def check_or_add_user(self, id_user, login, status):

        result = self.cursor.execute(f"SELECT * FROM users WHERE id_user='{id_user}'")

        response = result.fetchall()

        if response == []:
            now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute("INSERT OR IGNORE INTO users ('id_user', 'login',"
                                "'status', "
                                "'join_date') VALUES (?,?,?,?)",
                                (id_user, login, status,
                                 now_date))

            self.conn.commit()

            return True

        return False

    def add_product(self, name, descript, price, image_patch):
        try:
            self.cursor.execute("INSERT OR IGNORE INTO products ('name', 'descript',"
                                "'price', 'img') VALUES (?,?,?,?)",
                                (name, descript, price, image_patch))

            self.conn.commit()
        except:
            return False

        return True

    def get_balance(self, id_user):

        result = self.cursor.execute(f"SELECT balance FROM users WHERE id_user='{id_user}'")

        response = result.fetchall()

        try:
            response = response[0][0]
        except:
            return False

        return response

    def get_all_products(self):
        result = self.cursor.execute("SELECT id_pk, name, descript, price, img FROM products")

        response = result.fetchall()

        return response

    def get_products_by_id(self, id_k):
        result = self.cursor.execute(f"SELECT id_pk, name, descript, price, img FROM products WHERE id_pk = '{id_k}'")

        response = result.fetchall()[0]

        return response

    def close(self):
        # Закрытие соединения
        self.conn.close()
        print('Отключился от SQL BD')
