from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder,KeyboardBuilder
from lexicon.lexicon import LEXICON_START_KB
from database.database import database_quantity_page
from services.add_page import add_page,database_page

class TP_RP_CallbackFactory(CallbackData,prefix='TP_RP'):
    name_step: str
    callback: str


def enter():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='⬅️ Вход',
                                        callback_data='enter'))

    return kb_builder.as_markup()
def start_tp_rp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard: list[InlineKeyboardButton] = []
    for text,callback in LEXICON_START_KB.items():
        keyboard.append(InlineKeyboardButton(text=f'🔹 {text}',callback_data=TP_RP_CallbackFactory(
            name_step='main_menu',callback=callback
        ).pack()))
    kb_builder.row(*keyboard,width=1)
    return kb_builder.as_markup()


def mres_rp_pagination_kb(id_user):

    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='pag_rp_mres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["mres_rp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='pag_rp_mres',callback='forward').pack())
    return btn1,btn2,btn3

def mres_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='🛖 РП',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_kb',
                                                                            callback='mres_rp_kb').pack()),
                   InlineKeyboardButton(text='🛖 ТП',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_kb',
                                                                            callback='mres_tp_kb').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres',
                                                                            callback='back').pack()))
    return kb_builder.as_markup()
def mres_rp_kb(id_user,page):
    add_page(id_user,'mres_rp','mres_rp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🏕 {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='mres_press',
                                                                                       callback=callback).pack()))
    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*mres_rp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить РП',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_rp',
                                                                              callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить РП ',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_rp',
                                                                              callback='del').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_rp',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def mres_save_rp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='✅ Сохранить',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_rp',
                                                                            callback='save').pack()),
                   InlineKeyboardButton(text='📍 Ввести новые координаты',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_rp',
                                                                            callback='new_location').pack(), width=2)
                   )
    return kb_builder.as_markup()

def mres_rp_press_kb(name):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=name,
                                        callback_data=TP_RP_CallbackFactory(name_step='none',
                                                                            callback='none').pack()))
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_rp_press',
                                                                            callback='back').pack()))

    return kb_builder.as_markup()

def del_mres_rp_kb(id_user,page):
    add_page(id_user,'mres_rp','mres_rp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❌ {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='mres_press_del',
                                                                                       callback=callback).pack()))

    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*del_mres_rp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_rp_press',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def del_mres_rp_pagination_kb(id_user):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='del_pag_rp_mres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["mres_rp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='del_pag_rp_mres',callback='forward').pack())
    return btn1,btn2,btn3

# ТП МРЭС_____________________________________________________________________________


def mres_tp_pagination_kb(id_user):

    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='pag_tp_mres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["mres_tp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='pag_tp_mres',callback='forward').pack())
    return btn1,btn2,btn3

def mres_tp_kb(id_user,page):
    add_page(id_user,'mres_tp','mres_tp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🏕 {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='mres_press_loc',
                                                                                       callback=callback).pack()))
    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*mres_tp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить ТП',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_tp',
                                                                              callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить ТП ',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_tp',
                                                                              callback='del').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_tp',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def mres_save_tp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='✅ Сохранить',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_tp',
                                                                            callback='save').pack()),
                   InlineKeyboardButton(text='📍 Ввести новые координаты',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_tp',
                                                                            callback='new_location').pack(), width=2)
                   )
    return kb_builder.as_markup()

def mres_tp_press_kb(name):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=name,
                                        callback_data=TP_RP_CallbackFactory(name_step='none',
                                                                            callback='none').pack()))
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_tp_press',
                                                                            callback='back').pack()))

    return kb_builder.as_markup()

def del_mres_tp_kb(id_user,page):
    add_page(id_user,'mres_tp','mres_tp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❌ {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='mres_tp_press_del',
                                                                                       callback=callback).pack()))

    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*del_mres_tp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='mres_tp_press',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def del_mres_tp_pagination_kb(id_user):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='del_pag_tp_mres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["mres_tp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='del_pag_tp_mres',callback='forward').pack())
    return btn1,btn2,btn3


#ЗРЭС ______________________________________________________________________________
def zres_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='🛖 РП',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_kb',
                                                                            callback='zres_rp_kb').pack()),
                   InlineKeyboardButton(text='🛖 ТП',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_kb',
                                                                            callback='zres_tp_kb').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres',
                                                                            callback='back').pack()))
    return kb_builder.as_markup()
def zres_rp_pagination_kb(id_user):

    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='pag_rp_zres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["zres_rp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='pag_rp_zres',callback='forward').pack())
    return btn1,btn2,btn3

def zres_rp_kb(id_user,page):
    add_page(id_user,'zres_rp','zres_rp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🏕 {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='zres_press',
                                                                                       callback=callback).pack()))
    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*zres_rp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить РП',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_rp',
                                                                              callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить РП ',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_rp',
                                                                              callback='del').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_rp',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def zres_save_rp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='✅ Сохранить',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_rp',
                                                                            callback='save').pack()),
                   InlineKeyboardButton(text='📍 Ввести новые координаты',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_rp',
                                                                            callback='new_location').pack(), width=2)
                   )
    return kb_builder.as_markup()

def zres_rp_press_kb(name):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=name,
                                        callback_data=TP_RP_CallbackFactory(name_step='none',
                                                                            callback='none').pack()))
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_rp_press',
                                                                            callback='back').pack()))

    return kb_builder.as_markup()

def del_zres_rp_kb(id_user,page):
    add_page(id_user,'zres_rp','zres_rp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❌ {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='zres_press_del',
                                                                                       callback=callback).pack()))

    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*del_zres_rp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_rp_press',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def del_zres_rp_pagination_kb(id_user):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='del_pag_rp_zres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["zres_rp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='del_pag_rp_zres',callback='forward').pack())
    return btn1,btn2,btn3

# ТП ЗРЭС_____________________________________________________________________________


def zres_tp_pagination_kb(id_user):

    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='pag_tp_zres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["zres_tp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='pag_tp_zres',callback='forward').pack())
    return btn1,btn2,btn3

def zres_tp_kb(id_user,page):
    add_page(id_user,'zres_tp','zres_tp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🏕 {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='zres_press_loc',
                                                                                       callback=callback).pack()))
    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*zres_tp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить ТП',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_tp',
                                                                              callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить ТП ',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_tp',
                                                                              callback='del').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_tp',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def zres_save_tp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='✅ Сохранить',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_tp',
                                                                            callback='save').pack()),
                   InlineKeyboardButton(text='📍 Ввести новые координаты',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_tp',
                                                                            callback='new_location').pack(), width=2)
                   )
    return kb_builder.as_markup()

def zres_tp_press_kb(name):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=name,
                                        callback_data=TP_RP_CallbackFactory(name_step='none',
                                                                            callback='none').pack()))
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_tp_press',
                                                                            callback='back').pack()))

    return kb_builder.as_markup()

def del_zres_tp_kb(id_user,page):
    add_page(id_user,'zres_tp','zres_tp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❌ {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='zres_tp_press_del',
                                                                                       callback=callback).pack()))

    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*del_zres_tp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='zres_tp_press',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def del_zres_tp_pagination_kb(id_user):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='del_pag_tp_zres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["zres_tp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='del_pag_tp_zres',callback='forward').pack())
    return btn1,btn2,btn3

#ПРЭС_______________________________________________________________________________

def pres_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='🛖 РП',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_kb',
                                                                            callback='pres_rp_kb').pack()),
                   InlineKeyboardButton(text='🛖 ТП',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_kb',
                                                                            callback='pres_tp_kb').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres',
                                                                            callback='back').pack()))
    return kb_builder.as_markup()

def pres_rp_pagination_kb(id_user):

    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='pag_rp_pres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["pres_rp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='pag_rp_pres',callback='forward').pack())
    return btn1,btn2,btn3

def pres_rp_kb(id_user,page):
    add_page(id_user,'pres_rp','pres_rp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🏕 {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='pres_press',
                                                                                       callback=callback).pack()))
    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*pres_rp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить РП',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_rp',
                                                                              callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить РП ',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_rp',
                                                                              callback='del').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_rp',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def pres_save_rp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='✅ Сохранить',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_rp',
                                                                            callback='save').pack()),
                   InlineKeyboardButton(text='📍 Ввести новые координаты',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_rp',
                                                                            callback='new_location').pack(), width=2)
                   )
    return kb_builder.as_markup()

def pres_rp_press_kb(name):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=name,
                                        callback_data=TP_RP_CallbackFactory(name_step='none',
                                                                            callback='none').pack()))
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_rp_press',
                                                                            callback='back').pack()))

    return kb_builder.as_markup()

def del_pres_rp_kb(id_user,page):
    add_page(id_user,'pres_rp','pres_rp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❌ {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='pres_press_del',
                                                                                       callback=callback).pack()))

    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*del_pres_rp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_rp_press',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def del_pres_rp_pagination_kb(id_user):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='del_pag_rp_pres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["pres_rp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='del_pag_rp_pres',callback='forward').pack())
    return btn1,btn2,btn3

# ТП ПРЭС_____________________________________________________________________________


def pres_tp_pagination_kb(id_user):

    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='pag_tp_pres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["pres_tp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='pag_tp_pres',callback='forward').pack())
    return btn1,btn2,btn3

def pres_tp_kb(id_user,page):
    add_page(id_user,'pres_tp','pres_tp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🏕 {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='pres_press_loc',
                                                                                       callback=callback).pack()))
    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*pres_tp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить ТП',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_tp',
                                                                              callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить ТП ',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_tp',
                                                                              callback='del').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_tp',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def pres_save_tp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='✅ Сохранить',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_tp',
                                                                            callback='save').pack()),
                   InlineKeyboardButton(text='📍 Ввести новые координаты',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_tp',
                                                                            callback='new_location').pack(), width=2)
                   )
    return kb_builder.as_markup()

def pres_tp_press_kb(name):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=name,
                                        callback_data=TP_RP_CallbackFactory(name_step='none',
                                                                            callback='none').pack()))
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_tp_press',
                                                                            callback='back').pack()))

    return kb_builder.as_markup()

def del_pres_tp_kb(id_user,page):
    add_page(id_user,'pres_tp','pres_tp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❌ {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='pres_tp_press_del',
                                                                                       callback=callback).pack()))

    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*del_pres_tp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='pres_tp_press',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def del_pres_tp_pagination_kb(id_user):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='del_pag_tp_pres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["pres_tp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='del_pag_tp_pres',callback='forward').pack())
    return btn1,btn2,btn3


#ОГРЭС________________________________________________________________________

def ogres_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='🛖 РП',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_kb',
                                                                            callback='ogres_rp_kb').pack()),
                   InlineKeyboardButton(text='🛖 ТП',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_kb',
                                                                            callback='ogres_tp_kb').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres',
                                                                            callback='back').pack()))
    return kb_builder.as_markup()

def ogres_rp_pagination_kb(id_user):

    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='pag_rp_ogres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["ogres_rp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='pag_rp_ogres',callback='forward').pack())
    return btn1,btn2,btn3

def ogres_rp_kb(id_user,page):
    add_page(id_user,'ogres_rp','ogres_rp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🏕 {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='ogres_press',
                                                                                       callback=callback).pack()))
    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*ogres_rp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить РП',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_rp',
                                                                              callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить РП ',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_rp',
                                                                              callback='del').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_rp',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def ogres_save_rp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='✅ Сохранить',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_rp',
                                                                            callback='save').pack()),
                   InlineKeyboardButton(text='📍 Ввести новые координаты',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_rp',
                                                                            callback='new_location').pack(), width=2)
                   )
    return kb_builder.as_markup()

def ogres_rp_press_kb(name):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=name,
                                        callback_data=TP_RP_CallbackFactory(name_step='none',
                                                                            callback='none').pack()))
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_rp_press',
                                                                            callback='back').pack()))

    return kb_builder.as_markup()

def del_ogres_rp_kb(id_user,page):
    add_page(id_user,'ogres_rp','ogres_rp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❌ {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='ogres_press_del',
                                                                                       callback=callback).pack()))

    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*del_ogres_rp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_rp_press',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def del_ogres_rp_pagination_kb(id_user):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='del_pag_rp_ogres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["ogres_rp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='del_pag_rp_ogres',callback='forward').pack())
    return btn1,btn2,btn3

# ТП ОГРЭС_____________________________________________________________________________


def ogres_tp_pagination_kb(id_user):

    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='pag_tp_ogres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["ogres_tp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='pag_tp_ogres',callback='forward').pack())
    return btn1,btn2,btn3

def ogres_tp_kb(id_user,page):
    add_page(id_user,'ogres_tp','ogres_tp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'🏕 {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='ogres_press_loc',
                                                                                       callback=callback).pack()))
    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*ogres_tp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить ТП',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_tp',
                                                                              callback='add').pack()),
                   InlineKeyboardButton(text='🗑️ Удалить ТП ',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_tp',
                                                                              callback='del').pack(), width=2)
                   )
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_tp',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def ogres_save_tp_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='✅ Сохранить',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_tp',
                                                                            callback='save').pack()),
                   InlineKeyboardButton(text='📍 Ввести новые координаты',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_tp',
                                                                            callback='new_location').pack(), width=2)
                   )
    return kb_builder.as_markup()

def ogres_tp_press_kb(name):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=name,
                                        callback_data=TP_RP_CallbackFactory(name_step='none',
                                                                            callback='none').pack()))
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_tp_press',
                                                                            callback='back').pack()))

    return kb_builder.as_markup()

def del_ogres_tp_kb(id_user,page):
    add_page(id_user,'ogres_tp','ogres_tp_page')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(database_page[id_user][page])):
        for callback, text in database_page[id_user][page][i].items():
            keyboard.append(InlineKeyboardButton(text=f'❌ {text}',
                                                 callback_data=TP_RP_CallbackFactory(name_step='ogres_tp_press_del',
                                                                                       callback=callback).pack()))

    kb_builder.row(*keyboard, width=1)
    kb_builder.row(*del_ogres_tp_pagination_kb(id_user), width=3)
    kb_builder.row(InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=TP_RP_CallbackFactory(name_step='ogres_tp_press',
                                                                              callback='back').pack())
                   )
    return kb_builder.as_markup()

def del_ogres_tp_pagination_kb(id_user):
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=TP_RP_CallbackFactory(name_step='del_pag_tp_ogres',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database_quantity_page[id_user]["user_page"]}/{database_quantity_page[id_user]["ogres_tp_page"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=TP_RP_CallbackFactory(name_step='del_pag_tp_ogres',callback='forward').pack())
    return btn1,btn2,btn3