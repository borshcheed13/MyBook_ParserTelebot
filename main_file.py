import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from telebot.config_data.config import load_token
from telebot.handlers import new_users_handlers, old_users_handlers, help_handlers #для регистрации роутеров
from telebot.periodic_sending.sending import instance_sending, coroutine_sending

async def start_my_book_parsertelebot():
    config = load_token('.env') #Создаем объект, хранящий в себе токен из виртуального окружения
    bot = Bot(token=config.tg_bot.token) #Инициализируем бот
    storage = MemoryStorage() #Инициализируем хранилище данных о пользователях
    dp = Dispatcher(storage=storage) #Инициализируем диспетчер

    #Регистрируем роутеры
    dp.include_router(help_handlers.router)
    dp.include_router(old_users_handlers.router)
    dp.include_router(new_users_handlers.router)


    #пропускаем, накопившиеся за время отсутствия бота в сети, апдейты
    await bot.delete_webhook(drop_pending_updates=True)

    #добавляю бот в качестве атрибута класса, который автоматически рассылает сообщения с новыми книгами на сайте
    instance_sending.add_bot(bot)

    #создаю асинхронную задачу с корутиной периодической рассылки и вношу ее в список задач
    tasks = [asyncio.create_task(coroutine_sending)]

    #добавляю в список задач корутину работы бота в режиме опроса
    tasks.append(dp.start_polling(bot))

    #запускаю список асинхронных задач
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(start_my_book_parsertelebot())