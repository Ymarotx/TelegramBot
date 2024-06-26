from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_KEYBOARD

class MainMenuCallbackFactory(CallbackData,prefix='main'):
    name_step: str
    callback: str

class DictCallbackFactory(CallbackData,prefix='dict'):
    name_step: str
    callback: str

class SimulatorCallbackFactory(CallbackData,prefix='simulator'):
    name_step: str
    callback: str

class ReminderCallbackFactory(CallbackData,prefix='reminder'):
    name_step: str
    callback: str



def main_menu_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton=InlineKeyboardButton(text=LEXICON_KEYBOARD['dicts'],callback_data=MainMenuCallbackFactory(name_step='menu',callback='dict').pack())
    btn2: InlineKeyboardButton=InlineKeyboardButton(text=LEXICON_KEYBOARD['simulator'],callback_data=MainMenuCallbackFactory(name_step='menu',callback='simulator').pack())
    btn3: InlineKeyboardButton=InlineKeyboardButton(text=LEXICON_KEYBOARD['reminder'],callback_data=MainMenuCallbackFactory(name_step='menu',callback='reminder').pack())
    kb_builder.row(*[btn1,btn2,btn3],width=1)
    return kb_builder.as_markup()

def dict_kb():
    kb_buidler: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['dict_all'],
                                                      callback_data=DictCallbackFactory(name_step='dict',
                                                                                            callback='dict_all').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['dict_new'],
                                                      callback_data= DictCallbackFactory(name_step='dict',
                                                                                             callback='dict_new').pack())
    btn3: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['dict_learned'],
                                                      callback_data= DictCallbackFactory(name_step='dict',
                                                                                             callback='dict_learned').pack())
    btn4: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['back'],
                                                      callback_data=DictCallbackFactory(name_step='dict',
                                                                                            callback='back').pack())
    kb_buidler.row(*[btn1,btn2,btn3,btn4],width=1)
    return kb_buidler.as_markup()

def simulator_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['simulator_all'],
                                                      callback_data=SimulatorCallbackFactory(name_step='simulator',
                                                                                            callback='simulator_all').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['simulator_new'],
                                                      callback_data= SimulatorCallbackFactory(name_step='simulator',
                                                                                             callback='simulator_new').pack())
    btn3: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['simulator_gpt'],
                                                      callback_data= SimulatorCallbackFactory(name_step='simulator',
                                                                                             callback='simulator_gpt').pack())
    btn4: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['back'],
                                                      callback_data=SimulatorCallbackFactory(name_step='simulator',
                                                                                            callback='back').pack())
    kb_builder.row(*[btn1,btn2,btn3,btn4],width=1)
    return kb_builder.as_markup()

def simulator_new_pagination_kb(page,last_page):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='<<',callback_data=SimulatorCallbackFactory(name_step='simulator_new',
                                                                                            callback='backward').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=f'{page}/{last_page}',callback_data='None')
    btn3:InlineKeyboardButton = InlineKeyboardButton(text='>>',callback_data=SimulatorCallbackFactory(name_step='simulator_new',
                                                                                            callback='forward').pack())
    kb_builder.row(*[btn1,btn2,btn3],width=3)
    return kb_builder.as_markup()


def reminder_true_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['reminder_true_kb'],
                                                      callback_data=ReminderCallbackFactory(name_step='reminder',
                                                                                            callback='off').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['back'],
                                                      callback_data=ReminderCallbackFactory(name_step='reminder',
                                                                                            callback='back').pack())
    kb_builder.row(*[btn1,btn2],width=1)
    return kb_builder.as_markup()

def reminder_false_kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['reminder_false_kb'],
                                                      callback_data=ReminderCallbackFactory(name_step='reminder',
                                                                                            callback='on').pack())
    btn2: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_KEYBOARD['back'],
                                                      callback_data=ReminderCallbackFactory(name_step='reminder',
                                                                                            callback='back').pack())
    kb_builder.row(*[btn1,btn2],width=1)
    return kb_builder.as_markup()

def scheduler_kb():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=LEXICON_KEYBOARD['scheduler_kb'], callback_data=SimulatorCallbackFactory(name_step='simulator',
                                                                                             callback='simulator_new').pack()))
    return kb_builder.as_markup()


def simulator_new_start_kb():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=LEXICON_KEYBOARD['simulator_new_start_kb'], callback_data=SimulatorCallbackFactory(name_step='simulator',
                                                                                             callback='simulator_new_start').pack()))
    return kb_builder.as_markup()
