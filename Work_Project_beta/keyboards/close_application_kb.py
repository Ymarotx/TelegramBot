import copy
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.database import application_page,database_2,database_3,application_page_stock,database
from services.add_application_page import add_application_page
from aiogram.filters.callback_data import CallbackData
from services.add_application_page import add_stock_page

class Closing_Applicatin_Factory(CallbackData,prefix='clos'):
    name_step: str
    callback: str

def closing_application_pagination_kb():
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=Closing_Applicatin_Factory(name_step='closing_press',callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{database["user_page"]}/{database["quantity_page_stock"]}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=Closing_Applicatin_Factory(name_step='closing_press',callback='forward').pack())
    return btn1,btn2,btn3

def closing_application_kb(page):
    add_stock_page('quantity_page_stock')
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in application_page_stock[page]:
        for callback in i:
            keyboard.append(InlineKeyboardButton(text=f'🔹 {callback}',
                                                 callback_data=Closing_Applicatin_Factory(name_step='c_a',callback=callback).pack()))
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(*closing_application_pagination_kb(),width=3)
    kb_builder.row(InlineKeyboardButton(text='➕ Добавить на склад',callback_data=Closing_Applicatin_Factory(name_step='closing_app',callback='add').pack()),
                   InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=Closing_Applicatin_Factory(name_step='closing_app', callback='back').pack()),
                   InlineKeyboardButton(text='✅ Закрыть заявку',
                                        callback_data=Closing_Applicatin_Factory(name_step='closing_app', callback='closing').pack()),width=3)
    return kb_builder.as_markup()

def press_material():
    btn: InlineKeyboardButton=InlineKeyboardButton(text='🔙 Назад',
                                        callback_data=Closing_Applicatin_Factory(name_step='press_material', callback='back').pack())
    keyboard: list[InlineKeyboardButton] = []
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(btn)
    return kb_builder.as_markup()


def continue_close_application_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard: list[InlineKeyboardButton] = [*(InlineKeyboardButton(text=text,callback_data=callback) for text,callback in
                                              LEXICON_CONTINUE_CLOSE_APPLICATION_KB.items())]
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(InlineKeyboardButton(text='Назад 🔙',callback_data='back_active_application'))
    b = ''
    materials = ['cable_kb','internal_sockets_kb','external_sockets_kb','cable_channel_kb',
                 'count_a_s_p_kb','count_a_t_p_kb','count_d_s_p_kb','count_d_t_p_kb',
                 'count_mounting_boxes_kb','count_internal_switch_kb','count_external_switch_kb','lightbulbs_kb'
                 ]
    LEXICON = [LEXICON_CABLE_KB, LEXICON_INTERNAL_SOCKETS_KB, LEXICON_EXTERNAL_SOCKETS_KB,
               LEXICON_CABEL_CHANNEL_KB, LEXICON_AUTOMATIC_SWITCH_SINGLE_KB,
               LEXICON_AUTOMATIC_SWITCH_TRIPLE_KB, LEXICON_DIFF_AUTOMATIC_SINGLE_KB,
               LEXICON_DIFF_AUTOMATIC_TRIPLE_KB, LEXICON_MOUNTING_BOXES_KB, LEXICON_SWITCH_EXTERNAL_KB,
               LEXICON_SWITCH_INTERNAL_KB, LEXICON_LIGHTBULB_KB]

    for p in LEXICON:
        try:
            for i in p:
                try:
                    for k in materials:
                        try:
                            if p[i] == database_2[k]:
                                b = i
                                database_3.append(p)
                                break
                        except KeyError:
                            continue
                except KeyError:
                    continue
            p[f'{b.replace("⚜️","✔️")}'] = p.pop(b)
        except KeyError:
            continue
    return kb_builder.as_markup()

def close_application_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard: list[InlineKeyboardButton] = [*(InlineKeyboardButton(text=text,callback_data=callback) for text,callback in
                                              LEXICON_CLOSE_APPLICATION_KB.items())]
    kb_builder.row(*keyboard,width=1)
    kb_builder.row(InlineKeyboardButton(text='Назад 🔙',callback_data='back_active_application'))
    return kb_builder.as_markup()


def close_or_continue_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard: list[InlineKeyboardButton] = [InlineKeyboardButton(text='✔️ Закрыть заявку.',callback_data='close_application'),
                                            InlineKeyboardButton(text='⬅️ К материалам.',callback_data='continue_application'),
                                            InlineKeyboardButton(text='❌ Отменить изменения.',callback_data='cancel_edit')]
    kb_builder.row(*keyboard,width=2)
    kb_builder.row()
    return kb_builder.as_markup()




