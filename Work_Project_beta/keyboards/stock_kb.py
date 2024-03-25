from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_APPLICATION,LEXICON_RESULT_MONTH_KB
from database.database import application_page,database,application_page_stock
from services.add_application_page import add_application_page,add_stock_page
from aiogram.filters.callback_data import CallbackData


class StockCallbackFactory(CallbackData,prefix='S'):
    name_step: str
    callback: str


def add_del_stock_kb():
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='➕ Добавить',callback_data=StockCallbackFactory(name_step='add_del',callback='add').pack()))
    builder.row(InlineKeyboardButton(text='❎ Отмена',
                                     callback_data=StockCallbackFactory(name_step='add_del', callback='cancel').pack()))

    return builder.as_markup()

def pagination_kb():
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=StockCallbackFactory(name_step='stock_press',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["quantity_page_stock"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=StockCallbackFactory(name_step='stock_press',callback='forward').pack())
    return btn1,btn2,btn3


def stock_application_kb(page):
    add_stock_page('quantity_page_stock')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in application_page_stock[page]:
        for callback in i:
            keyboard.append(InlineKeyboardButton(text=f'🔹 {callback}',
                                                 callback_data=StockCallbackFactory(name_step='s_p',callback=callback).pack()))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(*pagination_kb(),width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить на склад',callback_data=StockCallbackFactory(name_step='stock_press',callback='add').pack()),
                   InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=StockCallbackFactory(name_step='stock_press', callback='back').pack(),width=2)
                   )
    return kb_builder.as_markup()


def stock_kb_press():
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='➕ Добавить ',callback_data=StockCallbackFactory(name_step='stock_press_press',callback='add').pack()),
                InlineKeyboardButton(text='➖ Отнять',
                                     callback_data=StockCallbackFactory(name_step='stock_press_press',
                                                                        callback='take_away').pack()),
                InlineKeyboardButton(text='🗑️ Удалить',
                                     callback_data=StockCallbackFactory(name_step='stock_press_press',
                                                                        callback='delete').pack())
                )
    builder.row(InlineKeyboardButton(text='🔙 Назад',
                                     callback_data=StockCallbackFactory(name_step='stock_press_press', callback='back').pack()))

    return builder.as_markup()