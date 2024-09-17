from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Клавиатура, спрашивающая об оповещениях
button_1 = InlineKeyboardButton(
    text='✅ Да, я хочу получать оповещения',
    callback_data='button_receive')
button_2 = InlineKeyboardButton(
    text='❌ Нет, мне это не интересно',
    callback_data='button_not_receive')
keyboard_notification = InlineKeyboardMarkup(
    inline_keyboard=[[button_1],
                     [button_2]])

#Клавиатура, спрашивающая о просмотре новинок
button_3 = InlineKeyboardButton(
    text='🐵 Да, я хочу посмотреть новинки',
    callback_data='button_view')
button_4 = InlineKeyboardButton(
    text='🙈 Нет, ничего не хочу смотреть',
    callback_data='button_not_view')
keyboard_view = InlineKeyboardMarkup(
    inline_keyboard=[[button_3],
                     [button_4]])
