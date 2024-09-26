import asyncio

from parser.parser_my_book import last_books_of_the_day
from telebot.config_data.config import reading_a_file, writing_a_file
from telebot.config_data.config import configuration


####################################################################################################
#Здесь будут все функции
####################################################################################################
def format_text(book):
    '''функция преобразует информацию о книге в формат для отправки сообщения'''
    name, author, description, link = book
    return f'{'_' * 30}\nНазвание: {name}\nАвтор: {author}\nОписание: {description}\n{link}\n{'_' * 30}\n'

####################################################################################################
#Здесь будут все классы
####################################################################################################
class Sending():
    '''Класс для периодической отправки оповещений о появлении новых книг'''
    def __init__(self):
        self.time_interval = configuration.time_interval #устанавливаем интервал периодической рассылки

    def add_bot(self, bot):
        self.bot = bot

    async def sending(self):
        while True:
            all_last_books = last_books_of_the_day.last_book_of_the_day()
            users = reading_a_file()
            for id, data in users.items():
                if data['notification'] == 'Y':
                    for book in all_last_books:
                        if book[0] != data['last_book']: #если названия книг не равны, отправляем сообщение
                            text = format_text(book)
                            await self.bot.send_message(chat_id=id,text=text)
                if all_last_books:
                    writing_a_file({'user_id': int(id), 'user_name': data['user_name'], 'notification': data['notification'], 'last_book': all_last_books[0][0]})

            await asyncio.sleep(self.time_interval)

####################################################################################################
#Здесь экземпляры классов
####################################################################################################
instance_sending = Sending()
coroutine_sending = instance_sending.sending()