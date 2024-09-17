import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

# *******************************************************
# Константы
# *******************************************************
URL = 'https://mybook.ru/catalog/books/'

# *******************************************************
# Классы парсера
# *******************************************************

class LastTenBooks:
    '''Класс парсит сайт и возвращает последние 10 книг'''
    def __init__(self):
        self.url = URL
        self.headers = {"User-Agent": UserAgent().random}

    def __request_fun(self, url):
        '''метод запроса'''
        response = requests.get(url, headers=self.headers)  # делаю запрос страницы
        self.soup = bs(response.text, 'html.parser')

    def last_ten_books(self, url=URL) -> list:
        '''Метод создает и возвращает список с последними 10 книгами на сайте'''
        self.__request_fun(url)
        content = self.soup.find_all('div', class_="e4xwgl-0 iJwsmp")
        list_with_last_books = []
        for element in content:
            book_link = f'https://mybook.ru/{element.find('a').get('href')}'
            book_name = element.find('p', class_='lnjchu-1 hhskLb').string
            book_description = element.find('p', class_='lnjchu-1 dPgoNf').string
            book_author = element.find('div', class_='dey4wx-1 jVKkXg').string
            list_with_last_books.append((book_name, book_author, book_description, book_link))
        return list_with_last_books



class LastBooksOfTheDay(LastTenBooks):
    '''Класс парсит сайт и возвращает книги для периодической отправки оповещений'''

    def __init__(self):
        super().__init__()
        self.url = URL
        #Чтобы проверить работу периодической рассылки, применить индекс -1. Для корректной работы бота применить индекс 0.
        self.presented_book = super().last_ten_books()[0] #при запуске программы считываю название последней книги на сайте
        self.unknown_books = []  # создаю пустой список, который далее буду наполнять новыми книгами
        self.page = 0  # задаю значение страницы

    def __inspection(self):
        """Метод сравнивает названия книг, появившиеся на сайте с момента последней инспекции сайта, с последней книгой, отправленной пользователям в оповещениях"""
        ten_books = super().last_ten_books(self.url)
        for i in ten_books:
            if i[0] != self.presented_book[0]: # Если книгу еще не показывали пользователю, добавляем ее в список неизвестных книг
                self.unknown_books.append(i)
            else:
                break

    def last_book_of_the_day(self) -> list:
        """Метод создает и возвращает список с книгами, появившимися после книги,
        записанной в users.json при последнем посещении бота пользователем"""

        while (self.page == 0) or (len(self.unknown_books) % 10 == 0 and len(self.unknown_books) > 0):  # Если пагинатор еще не запускался (т.е. не парсилась ни одна страница) или все 10 книг еще не показывались (т.е. все 10 книг с текущей страницы включены в словарь self.unknown_books)
            self.__inspection()  # Продолжаю сверку книг
            self.paginator()  # Перехожу на следующую страницу
        return self.unknown_books

    def paginator(self):
        self.page += 1
        self.url = f'{URL}?page={self.page}'


last_ten_books = LastTenBooks()  # экземпляр класса для отправки последних 10 книг при нажатии на кнопку пользователем
last_books_of_the_day = LastBooksOfTheDay()  # экземпляр класса для периодической рассылки

