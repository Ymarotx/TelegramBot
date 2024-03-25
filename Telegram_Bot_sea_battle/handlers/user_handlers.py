import asyncio
import sqlite3
from datetime import datetime
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router,F,Bot
from aiogram.filters import CommandStart,Command,StateFilter
from aiogram.types import CallbackQuery,Message,InputMediaAnimation
from services.get_field import get_field_start
from services.check_ships import check_ships_all,check_ships_straight,check_ships_oblique,check_ships_straight_max_null,check_ships_oblique_max_null,check_ships_all_start,\
check_ships_all_for_player_1,check_ships_all_new_horizontally,check_ships_all_new_vertically,check_ships_all_new_horizontally_6,\
check_ships_all_new_horizontally_1,check_ships_all_new_vertically_6,check_ships_all_new_vertically_1,check_ships_all_new_vertically_0,\
check_ships_all_new_vertically_7,check_ships_all_new_horizontally_0,check_ships_all_new_horizontally_7,\
check_ships_all_new_horizontally_two,check_ships_all_new_vertically_two,check_ships_all_new_horizontally_6_two,\
check_ships_all_new_horizontally_1_two,check_ships_all_new_vertically_6_two,check_ships_all_new_vertically_1_two,check_ships_all_new_vertically_0_two,\
check_ships_all_new_vertically_7_two,check_ships_all_new_horizontally_0_two,check_ships_all_new_horizontally_7_two,check_cells_on_availability_ships
from lexicon.lexicon import LEXICON_GAME,START_SHIPS_COUNT,FIELD
from database.database import users_id,user_ships,user_press_three_two_one,players_id,game_field_ships,game_field_ships_name_players,\
    game_field_ships_id_players,game_message_id_field_user,message_id_delete,state_wait,user_id_win,user_state
from keyboards.battle_keyboards import set_game_keyboard_ships,GameCallbackFactory,choose_ships,choose_players_kb,are_your_ready,\
game_keyboard_ships,game_keyboard_field,game_keyboard_ships_0123,choose_view_three_ships,choose_view_two_ships
from keyboards.main_menu import main_menu_kb,first_main_menu_kb
from FSM.FSM import FSMFillShipsGame
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from copy import deepcopy
from services.Who_one import who_one
from services.Choose_id import choose_id
from config_data.config import Config,load_config
# from aiogram.fsm.storage.redis import Redis,RedisStorage


config: Config = load_config()
router: Router = Router()

bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


@router.message(CommandStart(),StateFilter(default_state))
async def process_start_command(message:Message,state:FSMContext):
    if message.from_user.id not in users_id:
        users_id[message.from_user.id] = {}
        players_id[message.from_user.first_name] = message.from_user.id
    id = message.from_user.id
    file = open('database.txt', 'r+')
    text = file.read()
    if str(id) not in text.split('.'):
        file.write(f'{id}.')
    file.close()
    if message.from_user.id not in user_id_win:
        user_id_win[message.from_user.id] = []
    get_field_start(message.from_user.id)
    users_id[message.from_user.id]['ships'] = [[0 for _ in range(8)] for _ in range(8)]
    user_ships[message.from_user.id] = deepcopy(START_SHIPS_COUNT)
    await message.answer(text=LEXICON_GAME['/start'],reply_markup=first_main_menu_kb())
    await state.set_state(FSMFillShipsGame.main_menu)

@router.message(Command(commands='help'),StateFilter(FSMFillShipsGame.main_menu))
async def process_help_command(message:Message):
    await message.answer(text=LEXICON_GAME['/help'])
@router.callback_query(F.data=='/help',StateFilter(FSMFillShipsGame.main_menu))
async def process_help_command(callback:CallbackQuery):
    await callback.message.answer(text=LEXICON_GAME['/help'])

@router.message(Command(commands='set_ships'),StateFilter(FSMFillShipsGame.main_menu))
async def process_set_ships_command(message:Message,state:FSMContext):
    set_game_keyboard_ships(message.from_user.id)
    user_press_three_two_one[message.from_user.id] = {}
    if user_ships[message.from_user.id]['трёхпалубные'] == 0 and user_ships[message.from_user.id]['двухпалубные'] == 0 and user_ships[message.from_user.id][
        'однопалубныe'] == 0:
        await message.answer(text='<b>Поле уже создана,используйте команду /delete_field,'
                                  'чтобы <i>удалить поле</i> и команду /set_ships, чтобы <i>создать новое поле</i>.</b>', reply_markup=choose_ships(message.from_user.id))
    else:
        await message.answer(text=LEXICON_GAME['/set_ships'],reply_markup=choose_ships(message.from_user.id))
    await state.set_state(FSMFillShipsGame.choose_ships)
    current_state = await state.get_state()
    user_state[message.from_user.id] = current_state
@router.callback_query(F.data=='/set_ships',StateFilter(FSMFillShipsGame.main_menu))
async def process_set_ships_command(callback:CallbackQuery,state:FSMContext):
    set_game_keyboard_ships(callback.from_user.id)
    user_press_three_two_one[callback.from_user.id] = {}
    await callback.message.answer(text=LEXICON_GAME['/set_ships'],reply_markup=choose_ships(callback.from_user.id))
    await state.set_state(FSMFillShipsGame.choose_ships)

@router.callback_query(F.data == 'three-deck',StateFilter(FSMFillShipsGame.choose_ships))
async def process_three_deck_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text='<b>Сделайте выбор</b>',
                                  reply_markup=choose_view_three_ships())
    # await state.set_state(FSMFillShipsGame.three_view)
@router.callback_query(F.data == 'choose_horizontally_ships',~StateFilter(FSMFillShipsGame.main_menu))
async def process_horizontally_three_press(callback:CallbackQuery,state:FSMContext):
    a = await state.get_state()
    if a == 'FSMFillShipsGame:three_view_vertically':
        await callback.message.edit_text(
            text=f'Вы можете установить {user_ships[callback.from_user.id]["трёхпалубные"]} трёхпалубных корабля',
            reply_markup=set_game_keyboard_ships(callback.from_user.id))
    else:
        await callback.message.answer(
            text=f'Вы можете установить {user_ships[callback.from_user.id]["трёхпалубные"]} трёхпалубных корабля',
            reply_markup=set_game_keyboard_ships(callback.from_user.id))

    await state.set_state(FSMFillShipsGame.three_view_horizontally)

@router.callback_query(F.data == 'choose_vertically_ships',~StateFilter(FSMFillShipsGame.main_menu))
async def process_horizontally_three_press(callback:CallbackQuery,state:FSMContext):
    a = await state.get_state()
    if a == 'FSMFillShipsGame:three_view_horizontally':
        await callback.message.edit_text(
            text=f'Вы можете установить {user_ships[callback.from_user.id]["трёхпалубные"]} трёхпалубных корабля',
            reply_markup=set_game_keyboard_ships(callback.from_user.id))
    else:
        await callback.message.answer(
            text=f'Вы можете установить {user_ships[callback.from_user.id]["трёхпалубные"]} трёхпалубных корабля',
            reply_markup=set_game_keyboard_ships(callback.from_user.id))
    await state.set_state(FSMFillShipsGame.three_view_vertically)


@router.callback_query(GameCallbackFactory.filter(), StateFilter(FSMFillShipsGame.three_view_vertically))
async def process_button_set__three_ships_press(callback: CallbackQuery,
                                                callback_data: GameCallbackFactory,
                                                state: FSMContext):
    if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1:
        await callback.answer(text='Здесь уже стоит корабль.')
    elif user_ships[callback.from_user.id]['трёхпалубные'] != 0:
        try:
            if callback_data.x == 0 or callback_data.x == 7:
                await callback.answer(text='Здесь ставить нельзя')
            elif callback_data.y == 7:
                if check_ships_all_new_vertically_7(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            elif callback_data.y == 0:
                if check_ships_all_new_vertically_0(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            elif callback_data.x == 1:
               if check_ships_all_new_vertically_1(callback, callback_data):
                   await callback.answer(text='Здесь ставить нельзя')
               else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            elif callback_data.x == 6:
                if check_ships_all_new_vertically_6(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            elif check_ships_all_new_vertically(callback, callback_data) or check_ships_all(callback, callback_data):
                await callback.answer(text='Рядом корабль')

            else:
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] = 1
                users_id[callback.from_user.id]['ships'][callback_data.x-1][callback_data.y] = 1
                user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            try:
                a = await callback.message.edit_text(
                    text=f'Вы можете установить {user_ships[callback.from_user.id]["трёхпалубные"]} трёхпалубных корабля',
                    reply_markup=set_game_keyboard_ships(callback.from_user.id))
                message_id_delete['vertically'] = a.message_id
            except TelegramBadRequest:
                pass
        except IndexError:
            await callback.answer(text='Здесь ставить нельзя')
    else:
        await callback.message.edit_text(
            text='Вы не можете установить больше трёхпалубных кораблей.Выберите другой тип корабля.',
            reply_markup=choose_ships(callback.from_user.id))
        await state.set_state(FSMFillShipsGame.choose_ships)


@router.callback_query(GameCallbackFactory.filter(),StateFilter(FSMFillShipsGame.three_view_horizontally))
async def process_button_set__three_ships_press(callback:CallbackQuery,
                                         callback_data:GameCallbackFactory,
                                         state:FSMContext):
    if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1:
        await callback.answer(text='Здесь уже стоит корабль.')
    elif user_ships[callback.from_user.id]['трёхпалубные'] != 0:
        try:
            if callback_data.y == 0 or callback_data.y == 7:
                await callback.answer(text='Здесь ставить нельзя')
            elif callback_data.x == 7:
                if check_ships_all_new_horizontally_7(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] = 1
                    user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            elif callback_data.x == 0:
                if check_ships_all_new_horizontally_0(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] = 1
                    user_ships[callback.from_user.id]['трёхпалубные'] -= 1

            elif callback_data.y == 6:
               if check_ships_all_new_horizontally_6(callback, callback_data):
                   await callback.answer(text='Здесь ставить нельзя')
               else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] = 1
                    user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            elif callback_data.y == 1:
                if check_ships_all_new_horizontally_1(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] = 1
                    user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            elif check_ships_all_new_horizontally(callback,callback_data) or check_ships_all(callback,callback_data):
                await callback.answer(text='Рядом корабль')

            else:
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] = 1
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] = 1
                user_ships[callback.from_user.id]['трёхпалубные'] -= 1
            try:
                a = await callback.message.edit_text(
                        text=f'Вы можете установить {user_ships[callback.from_user.id]["трёхпалубные"]} трёхпалубных корабля',
                        reply_markup=set_game_keyboard_ships(callback.from_user.id))
                message_id_delete['horizontally'] = a.message_id
            except TelegramBadRequest:
                pass
        except IndexError:
            await callback.answer(text='Здесь ставить нельзя')
    else:
        await callback.message.edit_text(
            text='Вы не можете установить больше трёхпалубных кораблей.Выберите другой тип корабля.',
            reply_markup=choose_ships(callback.from_user.id))
        await state.set_state(FSMFillShipsGame.choose_ships)




#Сделал трёхпалубные корабли,осталось сделать такие же двухпалубные.

@router.callback_query(F.data == 'two-deck',StateFilter(FSMFillShipsGame.choose_ships))
async def process_three_deck_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text='<b>Сделайте выбор</b>',
                                  reply_markup=choose_view_two_ships())
    # await state.set_state(FSMFillShipsGame.three_view)
@router.callback_query(F.data == 'choose_horizontally_ships_2',~StateFilter(FSMFillShipsGame.main_menu))
async def process_horizontally_three_press(callback:CallbackQuery,state:FSMContext):
    a = await state.get_state()
    if a == 'FSMFillShipsGame:two_view_vertically':
        await callback.message.edit_text(
            text=f'Вы можете установить {user_ships[callback.from_user.id]["двухпалубные"]} двухпалубных корабля',
            reply_markup=set_game_keyboard_ships(callback.from_user.id))
    else:
        await callback.message.answer(
            text=f'Вы можете установить {user_ships[callback.from_user.id]["двухпалубные"]} двухпалубных корабля',
            reply_markup=set_game_keyboard_ships(callback.from_user.id))
    await state.set_state(FSMFillShipsGame.two_view_horizontally)

@router.callback_query(F.data == 'choose_vertically_ships_2',~StateFilter(FSMFillShipsGame.main_menu))
async def process_horizontally_three_press(callback:CallbackQuery,state:FSMContext):
    a = await state.get_state()
    if a == 'FSMFillShipsGame:two_view_horizontally':
        await callback.message.edit_text(
            text=f'Вы можете установить {user_ships[callback.from_user.id]["двухпалубные"]} двухпалубных корабля',
            reply_markup=set_game_keyboard_ships(callback.from_user.id))
    else:
        await callback.message.answer(
            text=f'Вы можете установить {user_ships[callback.from_user.id]["двухпалубные"]} двухпалубных корабля',
            reply_markup=set_game_keyboard_ships(callback.from_user.id))
    await state.set_state(FSMFillShipsGame.two_view_vertically)


@router.callback_query(GameCallbackFactory.filter(), StateFilter(FSMFillShipsGame.two_view_vertically))
async def process_button_set_two_ships_press(callback: CallbackQuery,
                                                callback_data: GameCallbackFactory,
                                                state: FSMContext):
    if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1:
        await callback.answer(text='Здесь уже стоит корабль.')
    elif user_ships[callback.from_user.id]['двухпалубные'] != 0:
        try:
            if callback_data.x == 0:
                await callback.answer(text='Здесь ставить нельзя')
            elif callback_data.x == 7:
                if check_ships_all_new_horizontally_7_two(callback, callback_data):
                    await callback.answer(text='Рядом корабль')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.y == 7:
                if check_ships_all_new_vertically_7_two(callback,callback_data):
                    await callback.answer(text='Рядом корабль')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.y == 0:
                if check_ships_all_new_vertically_0_two(callback,callback_data):
                    await callback.answer(text='Рядом корабль')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.x == 1:
               if check_ships_all_new_vertically_1_two(callback, callback_data):
                   await callback.answer(text='Рядом корабль')
               else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.x == 6:
                if check_ships_all_new_vertically_6_two(callback,callback_data):
                    await callback.answer(text='Рядом корабль')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif check_ships_all_new_vertically_two(callback, callback_data) or check_ships_all(callback, callback_data):
                await callback.answer(text='Рядом корабль')
            else:
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                users_id[callback.from_user.id]['ships'][callback_data.x-1][callback_data.y] = 1
                user_ships[callback.from_user.id]['двухпалубные'] -= 1
            try:
                a = await callback.message.edit_text(
                    text=f'Вы можете установить {user_ships[callback.from_user.id]["двухпалубные"]} двухпалубных корабля',
                    reply_markup=set_game_keyboard_ships(callback.from_user.id))
                message_id_delete['vertically'] = a.message_id
            except TelegramBadRequest:
                pass
        except IndexError:
            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] = 1
            user_ships[callback.from_user.id]['двухпалубные'] -= 1
    else:
        await callback.message.edit_text(
            text='Вы не можете установить больше двухпалубных кораблей.Выберите другой тип корабля.',
            reply_markup=choose_ships(callback.from_user.id))
        await state.set_state(FSMFillShipsGame.choose_ships)


@router.callback_query(GameCallbackFactory.filter(),StateFilter(FSMFillShipsGame.two_view_horizontally))
async def process_button_set_two_ships_press(callback:CallbackQuery,
                                         callback_data:GameCallbackFactory,
                                         state:FSMContext):
    if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1:
        await callback.answer(text='Здесь уже стоит корабль.')
    elif user_ships[callback.from_user.id]['двухпалубные'] != 0:
        try:
            if callback_data.y == 7:
                await callback.answer(text='Здесь ставить нельзя')
            elif callback_data.x == 0 and callback_data.y == 0:
                if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 2] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 2] == 1:
                    await callback.answer(text='Рядом корабль')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.x == 7 and callback_data.y == 0:
                if users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 2] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y+1] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 2] == 1:
                    await callback.answer(text='Рядом корабль')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.y == 0:
                if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 2] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 2] == 1 or \
                        users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 2] == 1:
                    await callback.answer(text='Рядом корабль')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.x == 7:
                if check_ships_all_new_horizontally_7_two(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.x == 0:
                if check_ships_all_new_horizontally_0_two(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1

            elif callback_data.y == 6:
               if check_ships_all_new_horizontally_6_two(callback, callback_data):
                   await callback.answer(text='Здесь ставить нельзя')
               else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif callback_data.y == 1:
                if check_ships_all_new_horizontally_1_two(callback,callback_data):
                    await callback.answer(text='Здесь ставить нельзя')
                else:
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                    users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] = 1
                    user_ships[callback.from_user.id]['двухпалубные'] -= 1
            elif check_ships_all_new_horizontally_two(callback,callback_data) or check_ships_all(callback,callback_data):
                await callback.answer(text='Рядом корабль')

            else:
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] = 1
                user_ships[callback.from_user.id]['двухпалубные'] -= 1
            try:
                a = await callback.message.edit_text(
                        text=f'Вы можете установить {user_ships[callback.from_user.id]["двухпалубные"]} двухпалубных корабля',
                        reply_markup=set_game_keyboard_ships(callback.from_user.id))
                message_id_delete['horizontally'] = a.message_id
            except TelegramBadRequest:
                pass
        except IndexError:
            await callback.answer(text='Здесь ставить нельзя')
    else:
        await callback.message.edit_text(
            text='Вы не можете установить больше двухпалубных кораблей.Выберите другой тип корабля.',
            reply_markup=choose_ships(callback.from_user.id))
        await state.set_state(FSMFillShipsGame.choose_ships)



#
# @router.callback_query(F.data == 'three-deck',StateFilter(FSMFillShipsGame.choose_ships))
# async def process_three_deck_press(callback:CallbackQuery,state:FSMContext):
#     user_press_three_two_one[callback.from_user.id][3] = 3
#     await callback.message.edit_text(text=f'Вы можете установить {user_ships[callback.from_user.id]["трёхпалубные"]} трёхпалубных корабля',
#                                   reply_markup=set_game_keyboard_ships(callback.from_user.id))
#     await state.set_state(FSMFillShipsGame.set_ships_three_deck)
#     current_state = await state.get_state()
#     user_state[callback.from_user.id] = current_state
#
#
# @router.callback_query(GameCallbackFactory.filter(),StateFilter(FSMFillShipsGame.set_ships_three_deck))
# async def process_button_set__three_ships_press(callback:CallbackQuery,
#                                          callback_data:GameCallbackFactory,
#                                          state:FSMContext):
#     if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1:
#         await callback.answer(text='Здесь уже стоит корабль.')
#     elif user_ships[callback.from_user.id]['трёхпалубные'] != 0:
#         if user_press_three_two_one[callback.from_user.id][3] == 3:
#             try:
#                 if check_ships_all(callback,callback_data):
#                     if callback_data.x == 0 and callback_data.y == 0:
#                         if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
#                             users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
#                             users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1:
#                             await callback.answer(text='Рядом корабль')
#                         else:
#                             users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                             user_press_three_two_one[callback.from_user.id][3] -= 1
#                     elif callback_data.x == 0:
#                         if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] == 1 or \
#                                 users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] == 1 or\
#                                 users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] == 1 or \
#                                 users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1 or \
#                                 users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1:
#                             await callback.answer(text='Рядом корабль')
#                         else:
#                             users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                             user_press_three_two_one[callback.from_user.id][3] -= 1
#                     elif callback_data.y == 0:
#                         if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
#                         users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
#                         users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1:
#                             await callback.answer(text='Рядом корабль')
#                         else:
#                             users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                             user_press_three_two_one[callback.from_user.id][3] -= 1
#                     else:
#                         await callback.answer(text='Рядом корабль')
#                 else:
#                     users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                     user_press_three_two_one[callback.from_user.id][3] -= 1
#
#             except IndexError:
#                 if check_ships_straight_max_null(callback, callback_data) or check_ships_oblique_max_null(callback,
#                                                                                                           callback_data):
#                     await callback.answer(text='Рядом корабль')
#                 else:
#                     users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                     user_press_three_two_one[callback.from_user.id][3] -= 1
#
#         elif 0 < user_press_three_two_one[callback.from_user.id][3] < 3:
#             try:
#                 if callback_data.x != 0 and callback_data.y != 0:
#                     if check_ships_oblique(callback, callback_data):
#                         await callback.answer(text='Здесь ставить нельзя')
#                     elif check_ships_straight(callback, callback_data):
#                         users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                         user_press_three_two_one[callback.from_user.id][3] -= 1
#                     else:
#                         await callback.answer(text='Рядом нет вашего корабля')
#                 else:
#                     if check_ships_oblique_max_null(callback, callback_data):
#                         await callback.answer(text='Здесь ставить нельзя')
#                     elif check_ships_straight_max_null(callback, callback_data):
#                         users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                         user_press_three_two_one[callback.from_user.id][3] -= 1
#                     else:
#                         await callback.answer(text='Рядом нет вашего корабля')
#
#             except IndexError:
#                 if check_ships_oblique_max_null(callback,callback_data):
#                     await callback.answer(text='Здесь ставить нельзя')
#                 elif check_ships_straight_max_null(callback,callback_data) :
#                     users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                     user_press_three_two_one[callback.from_user.id][3] -= 1
#                 else:
#                     await callback.answer(text='Рядом нет вашего корабля')
#
#
#         if user_press_three_two_one[callback.from_user.id][3] == 0:
#             user_press_three_two_one[callback.from_user.id][3] = 3
#             user_ships[callback.from_user.id]['трёхпалубные'] -= 1
#         try:
#             await callback.message.edit_text(
#                 text=f'Вы можете установить {user_ships[callback.from_user.id]["трёхпалубные"]} трёхпалубных корабля',
#                 reply_markup=set_game_keyboard_ships(callback.from_user.id))
#         except TelegramBadRequest:
#             pass
#
#     else:
#         await callback.message.edit_text(text='Вы не можете установить больше трёхпалубных кораблей.Выберите другой тип корабля.',reply_markup=choose_ships(callback.from_user.id))
#         await state.set_state(FSMFillShipsGame.choose_ships)
#         current_state = await state.get_state()
#         user_state[callback.from_user.id] = current_state

#
# @router.callback_query(F.data == 'two-deck',StateFilter(FSMFillShipsGame.choose_ships))
# async def process_three_deck_press(callback:CallbackQuery,state:FSMContext):
#     user_press_three_two_one[callback.from_user.id][2] = 2
#     await callback.message.edit_text(text=f'Вы можете установить {user_ships[callback.from_user.id]["двухпалубные"]} двухпалубных кораблей',
#                                   reply_markup=set_game_keyboard_ships(callback.from_user.id))
#     await state.set_state(FSMFillShipsGame.set_ships_two_deck)
#     current_state = await state.get_state()
#     user_state[callback.from_user.id] = current_state
#
#
#
# @router.callback_query(GameCallbackFactory.filter(),StateFilter(FSMFillShipsGame.set_ships_two_deck))
# async def process_button_set_two_ships_press(callback:CallbackQuery,
#                                          callback_data:GameCallbackFactory,
#                                          state:FSMContext):
#     if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1:
#         await callback.answer(text='Здесь уже стоит корабль.')
#     elif user_ships[callback.from_user.id]['двухпалубные'] != 0:
#         if user_press_three_two_one[callback.from_user.id][2] == 2:
#             try:
#                 if check_ships_all(callback,callback_data):
#                     if callback_data.x == 0 and callback_data.y == 0:
#                         if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
#                             users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
#                             users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1:
#                             await callback.answer(text='Рядом корабль')
#                         else:
#                             users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                             user_press_three_two_one[callback.from_user.id][2] -= 1
#                     elif callback_data.x == 0:
#                         if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y+1] == 1 or \
#                                 users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y-1] == 1 or\
#                                 users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y] == 1 or \
#                                 users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y - 1] == 1 or \
#                                 users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1:
#                             await callback.answer(text='Рядом корабль')
#                         else:
#                             users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                             user_press_three_two_one[callback.from_user.id][2] -= 1
#                     elif callback_data.y == 0:
#                         if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
#                         users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
#                         users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
#                         users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y + 1] == 1 or \
#                         users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y + 1] == 1:
#                             await callback.answer(text='Рядом корабль')
#                         else:
#                             users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                             user_press_three_two_one[callback.from_user.id][2] -= 1
#                     else:
#                         await callback.answer(text='Рядом корабль')
#                 else:
#                     users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                     user_press_three_two_one[callback.from_user.id][2] -= 1
#             except IndexError:
#                 if check_ships_straight_max_null(callback, callback_data) or check_ships_oblique_max_null(callback,callback_data):
#                     await callback.answer(text='Рядом корабль')
#                 else:
#                     users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                     user_press_three_two_one[callback.from_user.id][2] -= 1
#
#
#         elif 0 < user_press_three_two_one[callback.from_user.id][2] < 2:
#             try:
#                 if callback_data.x != 0 and callback_data.y != 0:
#                     if check_ships_oblique(callback,callback_data):
#                         await callback.answer(text='Здесь ставить нельзя')
#                     elif check_ships_straight(callback, callback_data):
#                         users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                         user_press_three_two_one[callback.from_user.id][2] -= 1
#                     else:
#                         await callback.answer(text='Рядом нет вашего корабля')
#                 else:
#                     if check_ships_oblique_max_null(callback, callback_data):
#                         await callback.answer(text='Здесь ставить нельзя')
#                     elif check_ships_straight_max_null(callback, callback_data):
#                         users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                         user_press_three_two_one[callback.from_user.id][2] -= 1
#                     else:
#                         await callback.answer(text='Рядом нет вашего корабля')
#
#             except IndexError:
#                 if check_ships_oblique_max_null(callback, callback_data):
#                     await callback.answer(text='Здесь ставить нельзя')
#                 elif check_ships_straight_max_null(callback, callback_data):
#                     users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
#                     user_press_three_two_one[callback.from_user.id][2] -= 1
#                 else:
#                     await callback.answer(text='Рядом нет вашего корабля')
#
#         if user_press_three_two_one[callback.from_user.id][2] == 0:
#             user_press_three_two_one[callback.from_user.id][2] = 2
#             user_ships[callback.from_user.id]['двухпалубные'] -= 1
#         try:
#             await callback.message.edit_text(
#                 text=f'Вы можете установить {user_ships[callback.from_user.id]["двухпалубные"]} двухпалубных корабля',
#                 reply_markup=set_game_keyboard_ships(callback.from_user.id))
#         except TelegramBadRequest:
#             pass
#
#     else:
#         await callback.message.edit_text(text='Вы не можете установить больше двухпалубных кораблей.Выберите другой тип корабля.',reply_markup=choose_ships(callback.from_user.id))
#         await state.set_state(FSMFillShipsGame.choose_ships)
#         current_state = await state.get_state()
#         user_state[callback.from_user.id] = current_state


@router.callback_query(F.data == 'one-deck',StateFilter(FSMFillShipsGame.choose_ships))
async def process_one_deck_press(callback:CallbackQuery,state:FSMContext):
    user_press_three_two_one[callback.from_user.id][1] = 1
    await callback.message.edit_text(
        text=f'Вы можете установить {user_ships[callback.from_user.id]["однопалубныe"]} однопалубных корабля',
        reply_markup=set_game_keyboard_ships(callback.from_user.id))
    await state.set_state(FSMFillShipsGame.set_ships_one_deck)
    current_state = await state.get_state()
    user_state[callback.from_user.id] = current_state



@router.callback_query(GameCallbackFactory.filter(),StateFilter(FSMFillShipsGame.set_ships_one_deck))
async def process_button_set_one_ships_press(callback:CallbackQuery,
                                         callback_data:GameCallbackFactory,
                                         state:FSMContext):
    if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] == 1:
        await callback.answer(text='Здесь уже стоит корабль.')
    elif user_ships[callback.from_user.id]['однопалубныe'] != 0:
        try:
            if check_ships_all(callback, callback_data):
                if callback_data.x == 0:
                    if users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1 or \
                            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y - 1] == 1 or \
                            users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1:
                        await callback.answer(text='Рядом корабль')
                    elif users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y-1] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y+1] == 1:
                        await callback.answer(text='Рядом корабль')
                    else:
                        users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                        user_ships[callback.from_user.id]['однопалубныe'] -= 1
                elif callback_data.y == 0:
                    if users_id[callback.from_user.id]['ships'][callback_data.x + 1][callback_data.y] == 1 or \
                            users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y] == 1 or \
                            users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y + 1] == 1:
                        await callback.answer(text='Рядом корабль')
                    elif users_id[callback.from_user.id]['ships'][callback_data.x+1][callback_data.y + 1] == 1 or \
                users_id[callback.from_user.id]['ships'][callback_data.x - 1][callback_data.y+1] == 1:
                        await callback.answer(text='Рядом корабль')
                    else:
                        users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                        user_ships[callback.from_user.id]['однопалубныe'] -= 1

                else:
                    await callback.answer(text='Рядом корабль')
            else:
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                user_ships[callback.from_user.id]['однопалубныe'] -= 1
        except IndexError:
            if check_ships_straight_max_null(callback, callback_data) or check_ships_oblique_max_null(callback,
                                                                                                      callback_data):
                await callback.answer(text='Рядом корабль')
            else:
                users_id[callback.from_user.id]['ships'][callback_data.x][callback_data.y] = 1
                user_ships[callback.from_user.id]['однопалубныe'] -= 1
        try:
            await callback.message.edit_text(
                text=f'Вы можете установить {user_ships[callback.from_user.id]["однопалубныe"]} однопалубных корабля',
                reply_markup=set_game_keyboard_ships(callback.from_user.id))
        except TelegramBadRequest:
            pass
    else:
        await callback.message.edit_text(
            text='Вы не можете установить больше однопалубных кораблей.Выберите другой тип корабля.',
            reply_markup=choose_ships(callback.from_user.id))
        await state.set_state(FSMFillShipsGame.choose_ships)
        current_state = await state.get_state()
        user_state[callback.from_user.id] = current_state


@router.callback_query(F.data == 'save_field',StateFilter(FSMFillShipsGame.choose_ships))
async def process_one_deck_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_GAME['save_field'])
    await state.set_state(FSMFillShipsGame.main_menu)
    current_state = await state.get_state()
    user_state[callback.from_user.id] = current_state

@router.message(Command(commands='delete_field'))
async def process_one_deck_press(message:Message,state:FSMContext):
    try:
        users_id[message.from_user.id]['ships'] = [[0 for _ in range(8)] for _ in range(8)]
        user_ships[message.from_user.id] = deepcopy(START_SHIPS_COUNT)
        get_field_start(message.from_user.id)
        await message.answer(text=LEXICON_GAME['delete_field'])
        await state.set_state(FSMFillShipsGame.main_menu)
        current_state = await state.get_state()
        user_state[message.from_user.id] = current_state
    except KeyError:
        await message.answer(text='⚠️ Поле и так пустое')

@router.callback_query(F.data=='/delete_field')
async def process_one_deck_press(callback:CallbackQuery,state:FSMContext):
    try:
        users_id[callback.from_user.id]['ships'] = [[0 for _ in range(8)] for _ in range(8)]
        user_ships[callback.from_user.id] = deepcopy(START_SHIPS_COUNT)
        get_field_start(callback.from_user.id)
        await callback.message.answer(text=LEXICON_GAME['delete_field'])
        await state.set_state(FSMFillShipsGame.main_menu)
    except KeyError:
        await callback.message.answer(text='⚠️ Поле и так пустое ')


@router.message(Command(commands='find_opponent'),StateFilter(FSMFillShipsGame.main_menu))
async def process_find_opponent_commands(message:Message,state:FSMContext):
    if user_ships[message.from_user.id]['трёхпалубные'] == START_SHIPS_COUNT['трёхпалубные'] and\
            user_ships[message.from_user.id]['двухпалубные'] == START_SHIPS_COUNT['двухпалубные'] and\
            user_ships[message.from_user.id]['однопалубныe'] == START_SHIPS_COUNT['однопалубныe']:
        await message.answer(text=LEXICON_GAME['full_field'])
        await state.set_state(FSMFillShipsGame.main_menu)
    elif user_ships[message.from_user.id]['трёхпалубные'] == 0 and\
            user_ships[message.from_user.id]['двухпалубные'] == 0 and user_ships[message.from_user.id]['однопалубныe'] == 0:
        keyboard = choose_players_kb(message.from_user.id,**players_id)
        game_field_ships[1] = {}
        game_field_ships[2] = {}
        game_field_ships[1]['field'] = deepcopy(users_id[message.from_user.id]['field'])
        game_field_ships[1]['ships'] = deepcopy(users_id[message.from_user.id]['ships'])
        game_field_ships_id_players[1] = message.from_user.id
        game_field_ships_name_players[1] = message.from_user.first_name
        if len(players_id) > 1:
            await message.answer(text=LEXICON_GAME['find_opponent'],reply_markup=keyboard)
            await state.set_state(FSMFillShipsGame.find_opponent)
            current_state = await state.get_state()
            user_state[message.from_user.id] = current_state
        else:
            await message.answer(text=LEXICON_GAME['list_opponent_null'])
            await state.set_state(FSMFillShipsGame.main_menu)
            current_state = await state.get_state()
            user_state[message.from_user.id] = current_state
    else:
        await message.answer(text=LEXICON_GAME['partially_field'])
        await state.set_state(FSMFillShipsGame.main_menu)

@router.callback_query(F.data=='/find_opponent',StateFilter(FSMFillShipsGame.main_menu))
async def process_find_opponent_commands(callback:CallbackQuery,state:FSMContext):
    if user_ships[callback.from_user.id]['трёхпалубные'] == START_SHIPS_COUNT['трёхпалубные'] and\
            user_ships[callback.from_user.id]['двухпалубные'] == START_SHIPS_COUNT['двухпалубные'] and\
            user_ships[callback.from_user.id]['однопалубныe'] == START_SHIPS_COUNT['однопалубныe']:
        await callback.message.answer(text=LEXICON_GAME['full_field'])
        await state.set_state(FSMFillShipsGame.main_menu)
    elif user_ships[callback.from_user.id]['трёхпалубные'] == 0 and\
            user_ships[callback.from_user.id]['двухпалубные'] == 0 and user_ships[callback.from_user.id]['однопалубныe'] == 0:
        keyboard = choose_players_kb(callback.from_user.id,**players_id)
        game_field_ships[1] = {}
        game_field_ships[2] = {}
        game_field_ships[1]['field'] = deepcopy(users_id[callback.from_user.id]['field'])
        game_field_ships[1]['ships'] = deepcopy(users_id[callback.from_user.id]['ships'])
        game_field_ships_id_players[1] = callback.from_user.id
        game_field_ships_name_players[1] = callback.from_user.first_name
        if len(players_id) > 1:
            await callback.message.answer(text=LEXICON_GAME['find_opponent'],reply_markup=keyboard)
            await state.set_state(FSMFillShipsGame.find_opponent)
            current_state = await state.get_state()
            user_state[callback.from_user.id] = current_state
        else:
            await callback.message.answer(text=LEXICON_GAME['list_opponent_null'])
            await state.set_state(FSMFillShipsGame.main_menu)
            current_state = await state.get_state()
            user_state[callback.from_user.id] = current_state
    else:
        await callback.message.answer(text=LEXICON_GAME['partially_field'])
        await state.set_state(FSMFillShipsGame.main_menu)

@router.callback_query(lambda x: x.data.isdigit(),StateFilter(FSMFillShipsGame.find_opponent))
async def process_find_opponent_press(callback:CallbackQuery,state:FSMContext):
    id = int(callback.data)
    name = callback.from_user.first_name
    state_wait[callback.from_user.id] = True
    await callback.message.delete()
    wait_opponent = await callback.message.answer(text=LEXICON_GAME['wait_opponent'])
    message_id_delete['wait_opponent'] = wait_opponent.message_id
    messages = await bot.send_message(chat_id=id, text=f'{name} хочет пригласить вас в игру.', reply_markup=are_your_ready())
    answer = ''
    answer_bot = ''
    for i in range(800):
        if not state_wait[callback.from_user.id]:
            await state.set_state(FSMFillShipsGame.player_1)
            current_state = await state.get_state()
            user_state[callback.from_user.id] = current_state
            answer = ' '
            answer_bot = ' '
            break
        else:
            await state.set_state(FSMFillShipsGame.main_menu)
            current_state = await state.get_state()
            user_state[callback.from_user.id] = current_state
            answer = LEXICON_GAME['wait_time_answer']
            answer_bot = LEXICON_GAME['timeout']
        await asyncio.sleep(1)
    try:
        await callback.message.answer(text=answer)
        await bot.edit_message_text(chat_id=id,message_id=messages.message_id,text=answer_bot)
        user_state[callback.from_user.id] = None
    except TelegramBadRequest:
        pass

@router.message(Command(commands='main_menu'))
async def process_main_menu_command(message:Message,state:FSMContext):
    try:
        if game_field_ships[1] and game_field_ships[2]:
            current_state_1 = await state.get_state()
            if current_state_1 == 'FSMFillShipsGame:player_1':
                await message.answer(text='Если вы покините эту игру,вам будет засчитано поражение.',reply_markup=main_menu_kb())
                await state.set_state(FSMFillShipsGame.main_menu_kb)
            else:
                await message.answer(text=LEXICON_GAME['main_menu'],reply_markup=first_main_menu_kb())
                await state.set_state(FSMFillShipsGame.main_menu)
                game_message_id_field_user.clear()
                current_state = await state.get_state()
                user_state[message.from_user.id] = current_state
        else:
            await message.answer(text=LEXICON_GAME['main_menu'],reply_markup=first_main_menu_kb())
            await state.set_state(FSMFillShipsGame.main_menu)
            game_message_id_field_user.clear()
    except KeyError:
        await message.answer(text=LEXICON_GAME['main_menu'], reply_markup=first_main_menu_kb())
        await state.set_state(FSMFillShipsGame.main_menu)
        game_message_id_field_user.clear()




@router.callback_query(F.data == 'exit_game',StateFilter(FSMFillShipsGame.main_menu_kb))
async def process_exit_game_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_GAME['exit_game'])
    await bot.send_animation(choose_id(callback.from_user.id), r'https://gifer.com/ru/7DZz')
    await bot.send_message(chat_id=choose_id(callback.from_user.id),text=LEXICON_GAME['exit_game_for_second_player'])
    await state.set_state(FSMFillShipsGame.main_menu)
    d = datetime.now()
    a = str(d).split('.')
    if callback.from_user.first_name == game_field_ships_name_players[1]:
        user_id_win[callback.from_user.id].append(
            f'{a[0]} вы потерпели поражение от Адмирала {game_field_ships_name_players[2]}')
        user_id_win[choose_id(callback.from_user.id)].append(
            f'{a[0]} вы одержали победу над Адмиралом {game_field_ships_name_players[1]}')
    else:
        user_id_win[callback.from_user.id].append(
            f'{a[0]} вы потерпели поражение от Адмирала {game_field_ships_name_players[1]}')
        user_id_win[choose_id(callback.from_user.id)].append(
            f'{a[0]} вы одержали победу над Адмиралом {game_field_ships_name_players[2]}')
    game_field_ships[1] = {}
    game_field_ships[2] = {}
    game_message_id_field_user.clear()

@router.callback_query(F.data == 'cancel',StateFilter(FSMFillShipsGame.main_menu_kb))
async def process_cancel_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.delete()
    await state.set_state(FSMFillShipsGame.player_1)



@router.callback_query(F.data == 'ready',StateFilter(FSMFillShipsGame.main_menu))
async def process_redy_press(callback:CallbackQuery,state:FSMContext):
    if user_ships[callback.from_user.id]['трёхпалубные'] == START_SHIPS_COUNT['трёхпалубные'] and\
            user_ships[callback.from_user.id]['двухпалубные'] == START_SHIPS_COUNT['двухпалубные'] and\
            user_ships[callback.from_user.id]['однопалубныe'] == START_SHIPS_COUNT['однопалубныe']:
        await callback.message.answer(text=LEXICON_GAME['full_field'])
        await state.set_state(FSMFillShipsGame.main_menu)
    elif user_ships[callback.from_user.id]['трёхпалубные'] == 0 and \
            user_ships[callback.from_user.id]['двухпалубные'] == 0 and \
            user_ships[callback.from_user.id]['однопалубныe'] == 0:
        state_wait[choose_id(callback.from_user.id)] = False
        game_field_ships[2]['field'] = deepcopy(users_id[callback.from_user.id]['field'])
        game_field_ships[2]['ships'] = deepcopy(users_id[callback.from_user.id]['ships'])
        game_field_ships_id_players[2] = callback.from_user.id
        game_field_ships_name_players[2] = callback.from_user.first_name
        #Получаем числа первого и второго игрока и имя кто победит
        players_1,players_2,players_win = who_one(game_field_ships_name_players[1],game_field_ships_name_players[2])
        await callback.message.edit_text(text=f'{game_field_ships_name_players[1]} выпало число {players_1}\n'
                                           f'{game_field_ships_name_players[2]} выпало число {players_2}\n'
                                           f'Победил(а) - {players_win}.Его(её) ход первый')
        await bot.send_message(chat_id=choose_id(callback.from_user.id),text=f'{game_field_ships_name_players[1]} выпало число {players_1}\n'
                                           f'{game_field_ships_name_players[2]} выпало число {players_2}\n'
                                           f'Победил(а) - {players_win}.Его(её) ход первый')
        msg_1_id = await callback.message.answer(text='Ваше поле', reply_markup=game_keyboard_ships_0123(2))
        await bot.delete_message(chat_id=choose_id(callback.from_user.id),message_id=message_id_delete['wait_opponent'])
        msg_2_id = await bot.send_message(chat_id=choose_id(callback.from_user.id),text='Ваше поле',reply_markup=game_keyboard_ships_0123(1))
        game_message_id_field_user.append(msg_1_id.message_id)
        game_message_id_field_user.append(msg_2_id.message_id)
        if game_field_ships_name_players[1] == players_win:
            msg_3_id = await callback.message.answer(text='Сейчас ходит ваш оппонент')
            message_id_delete['msg_3_id'] = msg_3_id.message_id # Под номером два в списке
            await bot.send_message(chat_id=choose_id(callback.from_user.id), text='Делайте ход.Это поле вашего соперника.',reply_markup=game_keyboard_field(1))
            await state.set_state(FSMFillShipsGame.player_1)
            current_state = await state.get_state()
            user_state[callback.from_user.id] = current_state
        else:
            await callback.message.answer(text='Поле оппонента', reply_markup=game_keyboard_field(2))
            msg_4_id = await bot.send_message(chat_id=choose_id(callback.from_user.id), text='Сейчас ходит ваш оппонент')
            message_id_delete['msg_4_id'] = msg_4_id.message_id
            await state.set_state(FSMFillShipsGame.player_1)
            current_state = await state.get_state()
            user_state[callback.from_user.id] = current_state
    else:
        await callback.message.answer(text=LEXICON_GAME['partially_field'])
        await state.set_state(FSMFillShipsGame.main_menu)


@router.callback_query(GameCallbackFactory.filter(),StateFilter(FSMFillShipsGame.player_1),lambda x: x.from_user.id == game_field_ships_id_players[1])
async def process_button_press(callback:CallbackQuery,
                               callback_data: GameCallbackFactory,
                               state:FSMContext):
    result = None
    for p in game_field_ships[2]['ships']:
        for j in p:
            if j == 1:
                result = True
                break
    if not result:
        await bot.send_animation(callback.from_user.id, r'https://gifer.com/ru/7DZz')
        await callback.message.answer(text=LEXICON_GAME['win'])
        await bot.send_message(chat_id=choose_id(callback.from_user.id),text=LEXICON_GAME['lose'])
        current_state = await state.get_state()
        user_state[callback.from_user.id] = current_state
        user_state[choose_id(callback.from_user.id)] = current_state
        d = datetime.now()
        a = str(d).split('.')
        user_id_win[callback.from_user.id].append(f'{a[0]} вы одержали победу над Адмиралом {game_field_ships_name_players[2]}')
        user_id_win[choose_id(callback.from_user.id)].append(f'{a[0]} вы потерпели поражение от Адмирала {game_field_ships_name_players[1]}')
    else:

        if game_field_ships[1]['field'][callback_data.x][callback_data.y] == 0 and \
            game_field_ships[2]['ships'][callback_data.x][callback_data.y] == 0:
            answer = LEXICON_GAME['miss']
            game_field_ships[1]['field'][callback_data.x][callback_data.y] = 1
            game_field_ships[2]['ships'][callback_data.x][callback_data.y] = 3
        elif game_field_ships[1]['field'][callback_data.x][callback_data.y] == 0 and \
            game_field_ships[2]['ships'][callback_data.x][callback_data.y] == 1:
            if check_ships_all_for_player_1(2,callback_data):
                answer = LEXICON_GAME['hit']
                game_field_ships[1]['field'][callback_data.x][callback_data.y] = 3
                game_field_ships[2]['ships'][callback_data.x][callback_data.y] = 2
            else:
                check_cells_on_availability_ships(callback_data)
                answer = LEXICON_GAME['kill']
                game_field_ships[1]['field'][callback_data.x][callback_data.y] = 2
                game_field_ships[2]['ships'][callback_data.x][callback_data.y] = 2
        else:
            answer = LEXICON_GAME['used']
        try:
            if answer == LEXICON_GAME['hit'] or answer == LEXICON_GAME['used'] or answer == LEXICON_GAME['kill'] :
                await callback.message.edit_text(text='Ваш ход.',reply_markup=game_keyboard_field(1))
            else:
                msg_5_id = await callback.message.edit_text(text='Сейчас ходит ваш соперник')
                message_id_delete['msg_5_id'] = msg_5_id.message_id
                try:
                    await bot.edit_message_text(chat_id=choose_id(callback.from_user.id), text='Делайте ход.Это поле вашего соперника',
                                           reply_markup=game_keyboard_field(2),message_id=message_id_delete['msg_6_id'])
                except KeyError:
                    await bot.send_message(chat_id=choose_id(callback.from_user.id),
                                                text='Делайте ход.Это поле вашего соперника',
                                                reply_markup=game_keyboard_field(2),
                                                )

            await state.set_state(FSMFillShipsGame.player_1)
            current_state = await state.get_state()
            user_state[callback.from_user.id] = current_state
        except TelegramBadRequest:
            pass
        await callback.answer(answer)
        await bot.edit_message_text(chat_id=choose_id(callback.from_user.id),message_id=game_message_id_field_user[0],text='Ваше поле',reply_markup=game_keyboard_ships_0123(2))


@router.callback_query(GameCallbackFactory.filter(),StateFilter(FSMFillShipsGame.player_1),lambda x: x.from_user.id == game_field_ships_id_players[2])
async def process_button_press(callback:CallbackQuery,
                               callback_data: GameCallbackFactory,
                               state:FSMContext):
    result = None
    for p in game_field_ships[1]['ships']:
        for j in p:
            if j == 1:
                result = True
                break
    if not result:
        await bot.send_animation(callback.from_user.id, r'https://gifer.com/ru/7DZz')
        await callback.message.answer(text=LEXICON_GAME['win'])
        await bot.send_message(chat_id=choose_id(callback.from_user.id),text=LEXICON_GAME['lose'])
        current_state = await state.get_state()
        user_state[callback.from_user.id] = current_state
        user_state[choose_id(callback.from_user.id)] = current_state
        d = datetime.now()
        a = str(d).split('.')
        user_id_win[callback.from_user.id].append(
            f'{a[0]} вы одержали победу над Адмиралом {game_field_ships_name_players[1]}')
        user_id_win[choose_id(callback.from_user.id)].append(
            f'{a[0]} вы потерпели поражение от Адмирала {game_field_ships_name_players[2]}')
    else:

        if game_field_ships[2]['field'][callback_data.x][callback_data.y] == 0 and\
            game_field_ships[1]['ships'][callback_data.x][callback_data.y] == 0:
            answer = LEXICON_GAME['miss']
            game_field_ships[2]['field'][callback_data.x][callback_data.y] = 1
            game_field_ships[1]['ships'][callback_data.x][callback_data.y] = 3
        elif game_field_ships[2]['field'][callback_data.x][callback_data.y] == 0 and\
            game_field_ships[1]['ships'][callback_data.x][callback_data.y] == 1:
            if check_ships_all_for_player_1(1, callback_data):
                answer = LEXICON_GAME['hit']
                game_field_ships[2]['field'][callback_data.x][callback_data.y] = 3
                game_field_ships[1]['ships'][callback_data.x][callback_data.y] = 2
            else:
                check_cells_on_availability_ships(callback_data)
                answer = LEXICON_GAME['kill']
                game_field_ships[2]['field'][callback_data.x][callback_data.y] = 2
                game_field_ships[1]['ships'][callback_data.x][callback_data.y] = 2
        else:
            answer = LEXICON_GAME['used']
        try:
            if answer == LEXICON_GAME['hit'] or answer == LEXICON_GAME['used'] or answer == LEXICON_GAME['kill'] :
                await callback.message.edit_text(text='Ваш ход.',reply_markup=game_keyboard_field(2))
            else:
                try:
                    await bot.edit_message_text(chat_id=choose_id(callback.from_user.id), text='Делайте ход.Это поле вашего соперника',
                                           reply_markup=game_keyboard_field(1),message_id=message_id_delete['msg_5_id'])
                except KeyError:
                    await bot.send_message(chat_id=choose_id(callback.from_user.id),
                                                text='Делайте ход.Это поле вашего соперника',
                                                reply_markup=game_keyboard_field(1),
                                                )

                msg_6_id = await callback.message.edit_text(text='Сейчас ходит ваш соперник')
                message_id_delete['msg_6_id'] = msg_6_id.message_id
            await state.set_state(FSMFillShipsGame.player_1)
            # current_state = await state.get_state()
            # user_state[callback.from_user.id] = current_state
        except TelegramBadRequest:
            pass
        await callback.answer(answer)
        await bot.edit_message_text(chat_id=choose_id(callback.from_user.id), message_id=game_message_id_field_user[1],
                                    text='Ваше поле', reply_markup=game_keyboard_ships_0123(1))

@router.message(Command(commands='history_game'))
async def process_history_game_command(message:Message):
    result = ''
    try:
        for i in user_id_win[message.from_user.id]:
            result += i + '\n'
        await message.answer(text= result)
    except KeyError:
        await message.answer(text=LEXICON_GAME['history_game'])
@router.callback_query(F.data =='/history_game')
async def process_history_game_command(callback:CallbackQuery):
    result = ''
    try:
        for i in user_id_win[callback.from_user.id]:
            result += i + '\n'
        await callback.message.answer(text= result)
    except KeyError:
        await callback.message.answer(text=LEXICON_GAME['history_game'])

@router.callback_query(F.data == '/main_menu')
async def process_main_menu_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text=LEXICON_GAME['main_menu'],reply_markup=first_main_menu_kb())
    await state.set_state(FSMFillShipsGame.main_menu)
    game_message_id_field_user.clear()
@router.message(Command(commands='send_message_all'))
async def process_send_message_all_command(message:Message):
    await message.answer(text=LEXICON_GAME['admin_echo'])

@router.message(Command(commands='instruction'))
async def process_instruction_command(message:Message):
    await message.answer(text=LEXICON_GAME['/instruction'])
@router.callback_query(F.data =='/instruction')
async def process_instruction_command(callback:CallbackQuery):
    await callback.message.answer(text=LEXICON_GAME['/instruction'])

@router.message(StateFilter(FSMFillShipsGame.player_1))
async def process_send_message_in_game(message:Message):
    await bot.send_message(chat_id=choose_id(message.from_user.id),text=message.text)


@router.message(~StateFilter(default_state))
async def process_echo(message:Message,state:FSMContext):
    await message.answer(text=LEXICON_GAME['echo_main_menu'])
@router.callback_query(~StateFilter(default_state),~StateFilter(FSMFillShipsGame.player_1))
async def process_echo(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text=LEXICON_GAME['echo_main_menu'])
@router.message(StateFilter(default_state))
async def process_echo(message:Message):
    await message.answer(text=LEXICON_GAME['echo_start'])
@router.callback_query(StateFilter(default_state))
async def process_echo(callback:CallbackQuery):
    await callback.message.answer(text=LEXICON_GAME['echo_start'])


#После окончания игры,после выхода в меню очищать все игровые данные которые получены внутри сражения