from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from lexicon.lexicon import lexicon_help


router = Router() #создаем роутер

@router.message(Command(commands=['help']))
async def command_help(message: Message):
    await message.answer(text=lexicon_help['help'])