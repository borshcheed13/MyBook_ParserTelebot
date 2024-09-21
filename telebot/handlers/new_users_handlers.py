from asyncio import sleep
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import lexicon_dict_new_users
from telebot.handlers.states import FSM_new_users
from parser.parser_my_book import last_ten_books
from telebot.config_data.config import writing_a_file
from telebot.handlers.keyboards import keyboard_notification, keyboard_view
from telebot.handlers.filters import filter_known_user


router = Router() #создаем роутер


####################################################################################################
#Здесь будут все функции
####################################################################################################
async def show_books(callback):
    for name, author, description, link in last_ten_books.last_ten_books()[:5]:
        await callback.message.answer(text=f'{'_' * 30}\nНазвание: {name}\nАвтор: {author}\nОписание: {description}\n{link}\n{'_' * 30}\n')

####################################################################################################
#Здесь будут все хэндлеры
####################################################################################################

#=========================================
#Состояние default_state
#=========================================
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_bot(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)  # Сохраняем id пользователя по ключу user_id в FSMContext
    await message.answer(text=lexicon_dict_new_users['/start']) #'/start': 'Привет!\nЯ бот, который показывает последние книги с сайта MyBook.ru.\nДавай знакомиться!\n\nКак тебя зовут?',
    await state.set_state(FSM_new_users.fill_name) #Устанавливаем состояние - ввод имени

@router.message(StateFilter(default_state))
async def any_message_from_a_new_user(message: Message):
    await message.answer(text=lexicon_dict_new_users['any_message_from_a_new_user']) #'Я всего лишь бот. Я не могу ответить на все твои сообщения.\n\nДля того, чтобы пройти опрос, тебе надо введи команду "/start".\n\nЧтобы посмотреть общую информацию обо мне, введи "/help"',

#=========================================
#Состояние FSM_new_users.fill_name
#=========================================
@router.message(StateFilter(FSM_new_users.fill_name), lambda x: x.text is not None and x.text.isalpha())
async def name_entered(message, state):
    await state.update_data(user_name=message.text) #Сохраняем имя пользователя по ключу name в FSMContext
    context = await state.get_data()
    await message.answer(text=f'{context['user_name']}, {lexicon_dict_new_users['name_entered']}', reply_markup=keyboard_notification) #'name_entered': 'Приятно познакомиться!\n\nЯ могу за тебя просматривать сайт MyBook.ru, и если появится новая книга, присылать тебе оповещение в чат.\n\nТы хочешь получать от меня сообщения?'
    await state.set_state(FSM_new_users.fill_receive_notification) #Устанавливаем следущее состояние - получение оповещений

@router.message(StateFilter(FSM_new_users.fill_name), lambda x: x.text is not None and any(map(lambda y: y.isdigit(), x.text)))
async def name_is_digit(message):
    await message.answer(text=lexicon_dict_new_users['name_is_digit'])

@router.message(StateFilter(FSM_new_users.fill_name))
async def name_is_other(message: Message):
    await message.reply(text=lexicon_dict_new_users['name_is_other'])

#=========================================
#Состояние FSM_new_users.fill_receive_notification
#=========================================

@router.callback_query(StateFilter(FSM_new_users.fill_receive_notification), F.data == 'button_receive')
async def press_receive_notification(callback: CallbackQuery, state: FSMContext):
    await state.update_data(notification='Y')  #Сохраняем согласие на получение оповещений по ключу notification в FSMContext
    context = await state.get_data()
    await callback.message.edit_text(text=f'{context['user_name']}, {lexicon_dict_new_users['name_entered']}')  #Редактируем последнее сообщение, чтобы убрать клавиатуру после нажатия на кнопку
    await callback.message.answer(text=lexicon_dict_new_users['press_receive_notification'], reply_markup=keyboard_view)
    await state.set_state(FSM_new_users.fill_view_the_books)  #Устанавливаем состояние - показ книг

@router.callback_query(StateFilter(FSM_new_users.fill_receive_notification), F.data == 'button_not_receive')
async def press_not_receive_notification(callback: CallbackQuery, state: FSMContext):
    await state.update_data(notification='N')  #Сохраняем отказ на получение оповещений по ключу notification в FSMContext
    context = await state.get_data()
    await callback.message.edit_text(text=f'{context['user_name']}, {lexicon_dict_new_users['name_entered']}') #Редактируем последнее сообщение, чтобы убрать клавиатуру после нажатия на кнопку
    await callback.message.answer(text=lexicon_dict_new_users['press_not_receive_notification'], reply_markup=keyboard_view)
    await state.set_state(FSM_new_users.fill_view_the_books)  #Устанавливаем состояние - показ книг

@router.message(StateFilter(FSM_new_users.fill_receive_notification))
async def process_receive_notification_other(message: Message):
    await message.reply(text=lexicon_dict_new_users['process_receive_notification_other'])

#=========================================
#Состояние FSM_new_users.fill_view_the_books
#=========================================

@router.callback_query(StateFilter(FSM_new_users.fill_view_the_books), F.data == 'button_view')
async def press_button_view(callback: CallbackQuery, state: FSMContext):
    context = await state.get_data()
    if context['notification'] == 'Y':
        await callback.message.edit_text(text=lexicon_dict_new_users['press_receive_notification'])  # Редактируем последнее сообщение, чтобы убрать клавиатуру после нажатия на кнопку
    else:
        await callback.message.edit_text(text=lexicon_dict_new_users['press_not_receive_notification'])

    await sleep(1) #выжидаем паузу

    #Отправляю в чат сообщения с 5 последними книгами и сообщение с финальной фразой
    await show_books(callback)
    await callback.message.answer(text=lexicon_dict_new_users['final_phrase']) #'final_phrase': 'Если ты захочешь изменить ответ на какой-то вопрос, введи "/start".\n\nЧтобы посмотреть общую информацию обо мне, введи "/help"',

    last_book = last_ten_books.last_ten_books()[0][0]
    await state.update_data(last_book=last_book) # Сохраняем последнюю книгу, показанную пользователю, по ключу last_book в FSMContext

    context = await state.get_data() #считываем контекст нового пользователя и вызываем функцию записи данных на файл
    writing_a_file(context)

    await state.set_state(FSM_new_users.end_of_the_survey)  #Устанавливаем состояние - конец опроса

@router.callback_query(StateFilter(FSM_new_users.fill_view_the_books), F.data == 'button_not_view')
async def press_button_not_view(callback: CallbackQuery, state: FSMContext):
    context = await state.get_data()
    if context['notification'] == 'Y':
        await callback.message.edit_text(text=lexicon_dict_new_users['press_receive_notification'])  # Редактируем последнее сообщение, чтобы убрать клавиатуру после нажатия на кнопку
    else:
        await callback.message.edit_text(text=lexicon_dict_new_users['press_not_receive_notification'])
        
    await callback.message.answer(text=lexicon_dict_new_users['press_button_not_view'])

    # Пользователь отказался в этот раз смотреть последние книги, но мы сохраняем в FSMContext по ключу last_book название последней книги для возможности показа последних книг в следующий раз
    name_last_book = last_ten_books.last_ten_books()[0][0]
    await state.update_data(last_book=name_last_book)

    context = await state.get_data()  # считываем контекст нового пользователя и вызываем функцию записи данных на файл
    writing_a_file(context)
    filter_known_user.read_id() #актуализирую список id пользователей на workflow_data

    await state.set_state(FSM_new_users.end_of_the_survey)  #Устанавливаем состояние - конец опроса

@router.message(StateFilter(FSM_new_users.fill_view_the_books))
async def process_view_the_book_other(message: Message):
    await message.reply(text=lexicon_dict_new_users['process_view_the_book_other']) #'process_view_the_book_other': 'Что-то не ладится у нас диалог.\n\nТебе всего лишь надо нажать на одну из кнопок в сообщении выше.'
