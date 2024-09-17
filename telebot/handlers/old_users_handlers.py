from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from lexicon.lexicon import lexicon_dict_old_users
from telebot.handlers.filters import filter_known_user
from telebot.handlers.states import FSM_old_users, FSM_new_users
from telebot.handlers.keyboards import keyboard_notification
from telebot.config_data.config import writing_a_file


router = Router() #создаем роутер
router.message.filter(filter_known_user) #фильтруем сообщения от пользователей, id которых есть в файле users.json

####################################################################################################
#Здесь будут все хэндлеры
####################################################################################################

#=========================================
#Состояние FSM_new_users.end_of_the_survey
#=========================================

@router.message(CommandStart(), StateFilter(FSM_new_users.end_of_the_survey))
async def restart(message: Message, state: FSMContext):
    context = await state.get_data()
    await message.answer(text=f'{context['user_name']}{lexicon_dict_old_users['restart']}', reply_markup=keyboard_notification) #'restart': ', привет!\nЯ рад увидеть тебя здесь снова!\n\nТы хочешь получать уведомления о новых книгах, которые появились на сайте MyBook.ru?'
    await state.set_state(FSM_old_users.fill_receive_notification) #Устанавливаем следущее состояние - получение оповещений

@router.message(StateFilter(FSM_new_users.end_of_the_survey))
async def message_not_start(message: Message):
    await message.reply(text=lexicon_dict_old_users['restart_other']) #'restart_other': 'Если ты хочешь изменить ответы на вопросы, нажми /start'

#=========================================
#Состояние FSM_old_users.fill_receive_notification
#=========================================

@router.callback_query(StateFilter(FSM_old_users.fill_receive_notification), F.data == 'button_receive')
async def press_receive_notification(callback: CallbackQuery, state: FSMContext):
    await state.update_data(notification='Y')  #Сохраняем согласие на получение оповещений по ключу notification в FSMContext

    context = await state.get_data()  # считываем контекст нового пользователя и вызываем функцию записи данных на файл
    writing_a_file(context)

    await callback.message.edit_text(text=f'{context['user_name']}, {lexicon_dict_old_users['restart']}')  #Редактируем последнее сообщение, чтобы убрать клавиатуру после нажатия на кнопку

    await callback.message.answer(text=lexicon_dict_old_users['press_receive_notification']) #'press_receive_notification': 'Прекрасно!\nЯ запомнил, что обо всех новых книгах надо тебя оповещать.\n\nЕсли ты захочешь изменить решение о периодической рассылке, введи /start.\n\nЧтобы посмотреть общую информацию обо мне, введи /help'
    await state.set_state(FSM_new_users.end_of_the_survey)  # Устанавливаем состояние - конец опроса

@router.callback_query(StateFilter(FSM_old_users.fill_receive_notification), F.data=='button_not_receive')
async def press_not_receive_notification(callback: CallbackQuery, state: FSMContext):
    await state.update_data(notification='N') #Сохраняем отказ от получения оповещений по ключу notification в FSMContext

    context = await state.get_data()  # считываем контекст пользователя и вызываем функцию записи данных на файл
    writing_a_file(context)

    context = await state.get_data()
    await callback.message.edit_text(text=f'{context['user_name']}, {lexicon_dict_old_users['restart']}')  # Редактируем последнее сообщение, чтобы убрать клавиатуру после нажатия на кнопку

    await callback.message.answer(text=lexicon_dict_old_users['press_not_receive_notification']) #'press_not_receive_notification': 'Хорошо, я не буду присылать тебе сообщения.\n\nЕсли ты захочешь изменить решение о периодической рассылке, введи /start.\n\nЧтобы посмотреть общую информацию обо мне, введи /help'
    await state.set_state(FSM_new_users.end_of_the_survey)  # Устанавливаем состояние - конец опроса

@router.message(StateFilter(FSM_old_users.fill_receive_notification))
async def process_receive_notification_other(message: Message):
    await message.reply(text=lexicon_dict_old_users['process_receive_notification_other'])
