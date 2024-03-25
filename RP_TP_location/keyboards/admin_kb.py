from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def give_access():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='Дать доступ',callback_data='give_access')
    btn2:InlineKeyboardButton = InlineKeyboardButton(text='Запретить доступ',callback_data='deny_access')
    kb_builder.row(btn1,btn2)
    return kb_builder.as_markup()