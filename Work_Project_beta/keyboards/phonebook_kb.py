from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class PhonebookCallbackFactory(CallbackData,prefix='phonebook'):
    name_step: str
    callback: str


def kb_phonebook():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text='📓 Телефонный справочник МЭС',callback_data=PhonebookCallbackFactory(
            name_step='main_menu',callback='phonebook_pdf').pack()),
        InlineKeyboardButton(text='🔙 Назад',callback_data=PhonebookCallbackFactory(
            name_step='main_menu',callback='back').pack())]
    kb_builder.row(*keyboard,width=1)
    return kb_builder.as_markup()