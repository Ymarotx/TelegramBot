from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_GAME,FIELD_SIZE,FIELD,LEXICON_SHIPS,GAME_LEXICON_SHIPS
from database.database import users_id,user_ships,players_id,game_field_ships
from aiogram.utils.keyboard import InlineKeyboardBuilder

#Создаём наш класс коллбэков
class GameCallbackFactory(CallbackData,prefix='game'):
    x: int
    y: int
#Создаём игровую клавиатуру
def set_game_keyboard_ships(user_id: int) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []
    for i in range(FIELD_SIZE):
        array_buttons.append([])
        for j in range(FIELD_SIZE):
            array_buttons[i].append(InlineKeyboardButton(text=LEXICON_SHIPS[users_id[user_id]['ships'][i][j]],
                                                         callback_data = GameCallbackFactory(x=i,y=j).pack()))
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup

def choose_ships(user_id: int) -> InlineKeyboardMarkup:
    if user_ships[user_id]['трёхпалубные'] == 0 and user_ships[user_id]['двухпалубные'] == 0 and user_ships[user_id]['однопалубныe'] == 0:
        btn4: InlineKeyboardButton = InlineKeyboardButton(text='Сохранить поле',
                                                      callback_data = 'save_field')

        keyboard: list[list[InlineKeyboardButton]] = [[btn4]]
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup
    else:
        btn1: InlineKeyboardButton = InlineKeyboardButton(text='Трёхпалубные🚢🚢🚢',
                                                          callback_data = 'three-deck')
        btn2: InlineKeyboardButton = InlineKeyboardButton(text='Двухпалубные🚢🚢',
                                                          callback_data = 'two-deck')
        btn3: InlineKeyboardButton = InlineKeyboardButton(text='Однопалубные🚢',
                                                          callback_data='one-deck')
        keyboard: list[list[InlineKeyboardButton]] = [[btn1],[btn2],[btn3]]
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup

def choose_view_three_ships()-> InlineKeyboardMarkup:
    btn1: InlineKeyboardButton=InlineKeyboardButton(text='Установить корабль горизонтально👉',
                                                    callback_data='choose_horizontally_ships')
    btn2: InlineKeyboardButton=InlineKeyboardButton(text='Установить корабль вертикально☝',
                                                    callback_data='choose_vertically_ships')
    keyboard: list[list[InlineKeyboardButton]] = [[btn1],[btn2]]
    markup: InlineKeyboardMarkup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup
def choose_view_two_ships()-> InlineKeyboardMarkup:
    btn1: InlineKeyboardButton=InlineKeyboardButton(text='Установить корабль горизонтально👉',
                                                    callback_data='choose_horizontally_ships_2')
    btn2: InlineKeyboardButton=InlineKeyboardButton(text='Установить корабль вертикально☝',
                                                    callback_data='choose_vertically_ships_2')
    keyboard: list[list[InlineKeyboardButton]] = [[btn1],[btn2]]
    markup: InlineKeyboardMarkup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup



def choose_players_kb(user_id: int,**kwargs) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for name,id in kwargs.items():
        if id == user_id:
            continue
        else:
            kb_builder.row(InlineKeyboardButton(text=name,callback_data=str(id)))
    return kb_builder.as_markup()

def are_your_ready() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn1: InlineKeyboardButton=InlineKeyboardButton(text='Готов',callback_data='ready')
    btn2: InlineKeyboardButton = InlineKeyboardButton(text='Не готов', callback_data='not_ready')
    kb_builder.row(btn1,btn2,width=2)
    return kb_builder.as_markup()

def game_keyboard_ships(num_id: int) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []
    for i in range(FIELD_SIZE):
        array_buttons.append([])
        for j in range(FIELD_SIZE):
            array_buttons[i].append(InlineKeyboardButton(text=LEXICON_SHIPS[game_field_ships[num_id]['ships'][i][j]],
                                                         callback_data = GameCallbackFactory(x=i,y=j).pack()))
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup

def game_keyboard_field(num_id: int) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []
    for i in range(FIELD_SIZE):
        array_buttons.append([])
        for j in range(FIELD_SIZE):
            array_buttons[i].append(InlineKeyboardButton(text=LEXICON_GAME[game_field_ships[num_id]['field'][i][j]],
                                                         callback_data=GameCallbackFactory(x=i, y=j).pack()))
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup


def game_keyboard_ships_0123(num_id: int) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []
    for i in range(FIELD_SIZE):
        array_buttons.append([])
        for j in range(FIELD_SIZE):
            array_buttons[i].append(InlineKeyboardButton(text=GAME_LEXICON_SHIPS[game_field_ships[num_id]['ships'][i][j]],
                                                         callback_data='1'))

    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup


