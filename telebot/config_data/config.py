from environs import Env
from dataclasses import dataclass
import json

####################################################################################################
#классы и функция считывают токен из .env и создают телеграмбота
####################################################################################################
@dataclass
class Tgbot:
    token: str

@dataclass
class Config:
    tg_bot: str

def load_token(path :str|None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=Tgbot(token=env('BOT_TOKEN')))

####################################################################################################
#Функция считывает данные о пользователях из файла users.json
####################################################################################################
def reading_a_file() -> dict:
    '''Функция десериализует словарь из файла c данными пользователей, если файл существует\
    или создает новый файл'''
    with open('telebot/config_data/users.json', 'r') as file:
        data = file.read()
        if data:
            data = json.loads(data)
        else:
            data = {}
    return data

####################################################################################################
#Функция записывает данные о пользователях в файл users.json
####################################################################################################
def writing_a_file(new_user_data : dict):
    '''Функция считывает данные предыдущих пользователей бота, добавляет нового пользователя и перезаписывает файл users.json'''

    new_user_id, new_user_name, new_user_notification, new_last_book = new_user_data.values()
    previous_users_str = reading_a_file() #считываю данные предыдущих пользователей
    previous_users = {int(key): value for key, value in previous_users_str.items()}  # меняю тип ключей со str на int

    if new_user_id in previous_users:
        previous_users[new_user_id]['notification'] = new_user_notification
        previous_users[new_user_id]['last_book'] = new_last_book
    else:
        previous_users[new_user_id] = {'user_name': new_user_name, 'notification': new_user_notification, 'last_book': new_last_book}

    with open('telebot/config_data/users.json', 'w') as file:
        json.dump(previous_users, file) #сериализую и записываю данные в файл users.json