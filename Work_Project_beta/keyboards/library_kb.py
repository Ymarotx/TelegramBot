from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class LibraryCallbackFactory(CallbackData,prefix='Lib'):
    name_step: str
    callback: str

def library_main_menu_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='📕 Реле времени PCZ525',callback_data=LibraryCallbackFactory(name_step='library_main_menu',
                                                                                                callback='pcz525').pack())
    btn2 = InlineKeyboardButton(text='📘 Реле времени PCZ525-1',callback_data=LibraryCallbackFactory(name_step='library_main_menu',
                                                                                                callback='pcz525-1').pack())
    btn3 = InlineKeyboardButton(text='📗 ТКП-290',callback_data=LibraryCallbackFactory(name_step='library_main_menu',
                                                                                                callback='tkp_290').pack())
    btn4 = InlineKeyboardButton(text='🔙 Назад',callback_data=LibraryCallbackFactory(name_step='library_main_menu',
                                                                                  callback='back').pack())
    keyboards: list[InlineKeyboardButton] = [btn1,btn2,btn3,btn4]
    kb_builder.row(*keyboards,width=1)
    return kb_builder.as_markup()

