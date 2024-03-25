import sqlite3
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_APPLICATION,LEXICON_RESULT_MONTH_KB
from database.database import application_page,database
from services.add_application_page import add_application_page,add_close_application_page,add_application_page_new
from aiogram.filters.callback_data import CallbackData

class ActiveApplicationCallbackFactory(CallbackData,prefix='Active'):
    name_cb: str
    callback: str
class CancelApplicationCallbackFactory(CallbackData,prefix='Cancel'):
    name_cb: str
    callback: str
class ResultMonthCallbackFactory(CallbackData,prefix='Result'):
    name_menu: str
    name_next_step: str

def application_kb():
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard: list[InlineKeyboardButton] = [InlineKeyboardButton(text=text,callback_data=callback) for text,callback in LEXICON_APPLICATION.items()]
    builder.row(*keyboard,width=1)
    return builder.as_markup()

def save_delete_application_kb():
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='Сохранить заявку ✅',callback_data='save_application')
    btn2: InlineKeyboardButton = InlineKeyboardButton(text='Удалить заявку ❎',callback_data='delete_application')
    keyboard: list[InlineKeyboardButton] = [btn1,btn2]
    builder.row(*keyboard,width=1)
    return builder.as_markup()

def pagination_kb():
    add_application_page('application','quantity_page')
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data='backward')
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["quantity_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data='forward')
    return btn1,btn2,btn3


def active_application_kb(page):
    add_application_page_new('application','quantity_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🔘 {text}',callback_data=callback))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',callback_data='back_application'))
    kb_builder.row(*pagination_kb(),width=3)
    return kb_builder.as_markup()


def close_delete_application(id: int):
    kb_builder: InlineKeyboardBuilder= InlineKeyboardBuilder()
    keyboards: list[InlineKeyboardButton] = [InlineKeyboardButton(text='Пометка "❗️"',callback_data=f'label_1.{id}'),
                                             InlineKeyboardButton(text='Пометка "💡" ', callback_data=f'label_3.{id}'),
                                             InlineKeyboardButton(text='Пометка "⏳" ',callback_data=f'label_2.{id}'),
                                             InlineKeyboardButton(text='❌ Отменить заявку',callback_data=f'del_application.{id}'),
                                             InlineKeyboardButton(text='📌 Заметки',
                                                                  callback_data=f'notes_active_application.{id}'),
                                             InlineKeyboardButton(text='☑️ Закрыть заявку',callback_data=f'close_application.{id}'),
                                             ]
    kb_builder.row(*keyboards,width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',callback_data=ActiveApplicationCallbackFactory(
                                                 name_cb='close_delete_application',callback='back').pack()))
    return kb_builder.as_markup()


def close_pagination_kb():
    add_close_application_page()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data='backward')
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["quantity_page_close"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data='forward')
    return btn1,btn2,btn3


def completed_application_kb(page):
    add_close_application_page()
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'✅ {text}',callback_data=callback))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',callback_data='back_completed_application'))
    kb_builder.row(*close_pagination_kb(),width=3)
    return kb_builder.as_markup()

def button_back(text,callback):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text=text,callback_data=callback)
    keyboard: list[list[InlineKeyboardButton]] = [[btn1]]
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup

def cancel_pagination_kb():
    add_application_page('cancel_application','quantity_page_cancel')
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data='backward')
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["quantity_page_cancel"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data='forward')
    return btn1,btn2,btn3


def cancel_application_kb(page):
    add_application_page('cancel_application','quantity_page_cancel')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❎ {text}',callback_data=callback))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(InlineKeyboardButton(text='Назад 🔙',callback_data='back_application'))
    kb_builder.row(*cancel_pagination_kb(),width=3)
    return kb_builder.as_markup()

def cancel_application_del_kb():
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='Назад 🔙',callback_data=CancelApplicationCallbackFactory(name_cb='cancel_application',
                                                                                                                    callback='back').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text='Удалить заявку 🗑️', callback_data=CancelApplicationCallbackFactory(
        name_cb='cancel_application',
        callback='delete').pack())
    keyboard.append(btn1)
    keyboard.append(btn2)
    kb_builder.row(*keyboard,width=1)
    return kb_builder.as_markup()

def result_month_2():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboards: list[InlineKeyboardButton] = [InlineKeyboardButton(text=text,
                                                                  callback_data=ResultMonthCallbackFactory(name_menu='result_month',
                                                                                                                     name_next_step=month).pack()) for text,month in LEXICON_RESULT_MONTH_KB.items()]
    kb_builder.row(*keyboards,width=2)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',callback_data=ResultMonthCallbackFactory(name_menu='result_month',
                                                                                                name_next_step='back').pack()))
    return kb_builder.as_markup()

def resul_month_2_kb_month():
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn2: InlineKeyboardButton = InlineKeyboardButton(text='🔙 Назад',callback_data=ResultMonthCallbackFactory(name_menu='result_month_press',
                                                                                                                    name_next_step='back'
                                                                                                              ).pack())
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='ℹ️ Детальная информация',callback_data=ResultMonthCallbackFactory(name_menu='result_month_press',
                                                                                                                    name_next_step='detail_information'
                                                                                                              ).pack())
    keyboard.append(btn1)
    keyboard.append(btn2)
    kb_builder.row(*keyboard,width=1)
    return kb_builder.as_markup()

def result_month_2_kb_month_back():
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='🔙 Назад',callback_data=ResultMonthCallbackFactory(name_menu='result_month_detail_information',
                                                                                                                    name_next_step='back').pack())
    keyboard.append(btn1)
    kb_builder.row(*keyboard,width=1)
    return kb_builder.as_markup()