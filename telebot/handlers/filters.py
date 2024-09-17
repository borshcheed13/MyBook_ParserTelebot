from aiogram import F
from aiogram.filters import BaseFilter

from telebot.config_data.config import reading_a_file

class Filter_known_user(BaseFilter):
    def __init__(self):
        self.read_id()

    def read_id(self):
        '''Метод актуализирует атрибут users_data.
        Вызывается в модуле old_users_handlers после сохранения в файле users.json данных о новом пользователе'''

        users_data_str = reading_a_file()  # Присваиваем переменной словарь с данными о пользователях
        self.users_data = {int(key) for key in users_data_str.keys()}  # Меняем тип данных ключа с str на int

    async def __call__(self, *args, **kwargs):
        return F.from_user.id.in_(self.users_data)

filter_known_user = Filter_known_user()