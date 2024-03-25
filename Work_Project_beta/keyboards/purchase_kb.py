from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_APPLICATION,LEXICON_RESULT_MONTH_KB
from database.database import application_page,database,application_page_stock
from services.add_application_page import add_purchase_page
from aiogram.filters.callback_data import CallbackData


class PurchaseCallbackFactory(CallbackData,prefix='Pur'):
    name_step: str
    callback: str


def purchase_kb():
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='🔸 Заявка на материалы',callback_data=PurchaseCallbackFactory(name_step='p_main_menu',callback='application').pack()),
                InlineKeyboardButton(text='🔸 Несметка до 50б',
                                     callback_data=PurchaseCallbackFactory(name_step='p_main_menu',
                                                                        callback='p_to_50b').pack()),
                InlineKeyboardButton(text='🔸 Несметка свыше 50б',
                                     callback_data=PurchaseCallbackFactory(name_step='p_main_menu',
                                                                        callback='p_over_50b').pack()),width=1
                )
    builder.row(InlineKeyboardButton(text='🔙 Назад',
                                     callback_data=PurchaseCallbackFactory(name_step='p_main_menu', callback='back').pack()))

    return builder.as_markup()


def purchase_pagination_kb_materials():
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=PurchaseCallbackFactory(name_step='p_pagination_mat',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["purchase_page_application"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=PurchaseCallbackFactory(name_step='p_pagination_mat',callback='forward').pack())
    return btn1,btn2,btn3


def purchase_materials_kb(page):
    add_purchase_page('purchase','purchase_page_application','purchase_application')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🔹 {text}',
                                                 callback_data=PurchaseCallbackFactory(name_step='activate',callback=callback).pack()))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(*purchase_pagination_kb_materials(),width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить материал',callback_data=PurchaseCallbackFactory(name_step='p_materials',callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить материал ',
                                        callback_data=PurchaseCallbackFactory(name_step='p_materials', callback='del').pack(),width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=PurchaseCallbackFactory(name_step='p_materials', callback='back').pack())
                   )
    return kb_builder.as_markup()

def purchase_pagination_kb_materials_del():
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=PurchaseCallbackFactory(name_step='p_pagination_mat_del',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["purchase_page_application"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=PurchaseCallbackFactory(name_step='p_pagination_mat_del',callback='forward').pack())
    return btn1,btn2,btn3

def purchase_materials_kb_delete(page):
    add_purchase_page('purchase','purchase_page_application','purchase_application')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🗑️ {text}',
                                                 callback_data=PurchaseCallbackFactory(name_step='p_materials_del',callback=callback).pack()))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(*purchase_pagination_kb_materials_del(),width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=PurchaseCallbackFactory(name_step='p_materials_del', callback='back').pack()),
                   InlineKeyboardButton(text='🆑 Очистить всё',
                                        callback_data=PurchaseCallbackFactory(name_step='p_materials_del',
                                                                              callback='all_delete').pack()),width=2
                   )
    return kb_builder.as_markup()










def purchase_pagination_kb_to_50b():
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=PurchaseCallbackFactory(name_step='p_pag_to_50b',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["purchase_page_to_50b"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=PurchaseCallbackFactory(name_step='p_pag_to_50b',callback='forward').pack())
    return btn1,btn2,btn3


def purchase_materials_kb_to_50b(page):
    add_purchase_page('purchase','purchase_page_to_50b','p_to_50b')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🔻 {text}',
                                                 callback_data=PurchaseCallbackFactory(name_step='activate_to_50b',callback=callback).pack()))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(*purchase_pagination_kb_to_50b(),width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить материал',callback_data=PurchaseCallbackFactory(name_step='p_to_50b',callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить материал ',
                                        callback_data=PurchaseCallbackFactory(name_step='p_to_50b', callback='del').pack(),width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=PurchaseCallbackFactory(name_step='p_to_50b', callback='back').pack())
                   )
    return kb_builder.as_markup()

def purchase_pagination_kb_to_50b_del():
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=PurchaseCallbackFactory(name_step='p_pag_to_50b_del',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["purchase_page_to_50b"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=PurchaseCallbackFactory(name_step='p_pag_to_50b_del',callback='forward').pack())
    return btn1,btn2,btn3

def purchase_to_50b_kb_delete(page):
    add_purchase_page('purchase','purchase_page_to_50b','p_to_50b')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🗑️ {text}',
                                                 callback_data=PurchaseCallbackFactory(name_step='p_to_50b_del',callback=callback).pack()))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(*purchase_pagination_kb_to_50b_del(),width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=PurchaseCallbackFactory(name_step='p_to_50b_del', callback='back').pack()),
                   InlineKeyboardButton(text='🆑 Очистить всё',
                                        callback_data=PurchaseCallbackFactory(name_step='p_to_50b_del',
                                                                              callback='all_delete').pack()),width=2
                   )
    return kb_builder.as_markup()






def purchase_pagination_kb_over_50b():
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=PurchaseCallbackFactory(name_step='p_pag_over_50b',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["purchase_page_over_50b"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=PurchaseCallbackFactory(name_step='p_pag_over_50b',callback='forward').pack())
    return btn1,btn2,btn3


def purchase_materials_kb_over_50b(page):
    add_purchase_page('purchase','purchase_page_over_50b','p_over_50b')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🔺 {text}',
                                                 callback_data=PurchaseCallbackFactory(name_step='activate_over_50b',callback=callback).pack()))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(*purchase_pagination_kb_over_50b(),width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить материал',callback_data=PurchaseCallbackFactory(name_step='p_over_50b',callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить материал ',
                                        callback_data=PurchaseCallbackFactory(name_step='p_over_50b', callback='del').pack(),width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=PurchaseCallbackFactory(name_step='p_over_50b', callback='back').pack())
                   )
    return kb_builder.as_markup()

def purchase_pagination_kb_over_50b_del():
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=PurchaseCallbackFactory(name_step='p_pag_over_50b_del',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["purchase_page_over_50b"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=PurchaseCallbackFactory(name_step='p_pag_over_50b_del',callback='forward').pack())
    return btn1,btn2,btn3

def purchase_over_50b_kb_delete(page):
    add_purchase_page('purchase','purchase_page_over_50b','p_over_50b')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(application_page[page])):
        for callback,text in application_page[page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🗑️ {text}',
                                                 callback_data=PurchaseCallbackFactory(name_step='p_over_50b_del',callback=callback).pack()))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(*purchase_pagination_kb_over_50b_del(),width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=PurchaseCallbackFactory(name_step='p_over_50b_del', callback='back').pack()),
                   InlineKeyboardButton(text='🆑 Очистить всё',
                                        callback_data=PurchaseCallbackFactory(name_step='p_over_50b_del',
                                                                              callback='all_delete').pack()),width=2
                   )
    return kb_builder.as_markup()