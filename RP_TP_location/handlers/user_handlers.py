import sqlite3

from aiogram import Bot
from aiogram import Router,F
from aiogram.filters import CommandStart,StateFilter,Command
from aiogram.types import Message,CallbackQuery
from keyboards import other_keyboards
from lexicon.lexicon import LEXICON_TP_RP
from database.database import database_quantity_page,database_page,database
from FSM.FSM import FSM_RP_TP
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from services.add_page import add_page
from config_data.config import load_config,Config
from keyboards.admin_kb import give_access
from aiogram.fsm.state import default_state

router: Router = Router()
db = sqlite3.connect('TP_RP.sql')
cur = db.cursor()
config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

@router.message(lambda x: x.from_user.id != 1071147158 and x.from_user.id != 854222736, CommandStart())
async def process_start_command(message:Message,state:FSMContext):
    database[str(message.from_user.id)] = {}
    database_page[str(message.from_user.id)] = {}
    database_quantity_page[str(message.from_user.id)] = {}
    database_quantity_page[str(message.from_user.id)]["user_page"] = 1
    cur.execute('''CREATE TABLE IF NOT EXISTS user (user_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                 id_user INT,
                                                 name_user VARCHAR(50))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS mres_rp (mres_rp_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                            who_add VARCHAR(50),
                                                            name VARCHAR(50),
                                                            location VARCHAR(70))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS mres_tp (mres_tp_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                            who_add VARCHAR(50),
                                                            name VARCHAR(50),
                                                            location VARCHAR(70))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS zres_rp (zres_rp_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                            who_add VARCHAR(50),
                                                            name VARCHAR(50),
                                                            location VARCHAR(70))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS zres_tp (zres_tp_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                            who_add VARCHAR(50),
                                                            name VARCHAR(50),
                                                            location VARCHAR(70))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS ogres_rp (ogres_rp_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                            who_add VARCHAR(50),
                                                            name VARCHAR(50),
                                                            location VARCHAR(70))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS ogres_tp (ogres_tp_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                            who_add VARCHAR(50),
                                                            name VARCHAR(50),
                                                            location VARCHAR(70))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS pres_rp (pres_rp_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                            who_add VARCHAR(50),
                                                            name VARCHAR(50),
                                                            location VARCHAR(70))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS pres_tp (pres_tp_id INT AUTO_INCREMENT PRIMARY KEY ,
                                                            who_add VARCHAR(50),
                                                            name VARCHAR(50),
                                                            location VARCHAR(70))''')

    db.commit()
    cur.execute('''SELECT id_user FROM user ''')
    a = cur.fetchall()
    lists = []
    for i in a:
        for p in i:
            lists.append(p)
    if message.from_user.id not in lists:
        await bot.send_message(chat_id=1071147158,text=f'Пользователь {message.from_user.first_name} ({message.from_user.id}) запрашивает доступ.',reply_markup=give_access())
        await message.answer(text='Ожидайте получение доступа')
        await state.set_state(FSM_RP_TP.start)
    else:
        await message.answer(text=LEXICON_TP_RP['main_menu'], reply_markup=other_keyboards.start_tp_rp_kb())
        await state.set_state(FSM_RP_TP.main_menu)


@router.message(Command(commands='main_menu'),~StateFilter(FSM_RP_TP.start),~StateFilter(default_state))
async def process_main_menu_command(message:Message,state:FSMContext):
    await message.answer(text=LEXICON_TP_RP['main_menu'],reply_markup=other_keyboards.start_tp_rp_kb())
    await state.set_state(FSM_RP_TP.main_menu)
@router.message(Command(commands='instruction'),~StateFilter(FSM_RP_TP.start))
async def process_main_menu_command(message:Message,state:FSMContext):
    await message.answer(text=LEXICON_TP_RP['instruction'])
    await state.set_state(FSM_RP_TP.main_menu)

@router.callback_query(F.data == 'enter',StateFilter(FSM_RP_TP.start))
async def process_enter_command(callback:CallbackQuery,state:FSMContext):
    cur.execute('''SELECT id_user FROM user ''')
    a = cur.fetchall()
    lists = []
    for i in a:
        for p in i:
            lists.append(p)
    if callback.from_user.id not in lists:
        cur.execute(f'''INSERT INTO user (id_user,name_user)
                       VALUES ({callback.from_user.id},'{callback.from_user.first_name}')
        ''')
        db.commit()
    else:
        pass
    await callback.message.delete()
    await callback.answer(text='Доступ открыт',show_alert=True)
    await callback.message.answer(text=LEXICON_TP_RP['main_menu'],reply_markup=other_keyboards.start_tp_rp_kb())
    await state.set_state(FSM_RP_TP.main_menu)


@router.callback_query(other_keyboards.TP_RP_CallbackFactory.filter(),StateFilter(FSM_RP_TP.main_menu))
async def process_press_callback_factory_tp_rp(callback:CallbackQuery,
                                               callback_data:other_keyboards.TP_RP_CallbackFactory,
                                               state:FSMContext):
    if callback_data.name_step == 'main_menu' and callback_data.callback == 'mres':
        await callback.message.edit_text(text=LEXICON_TP_RP['mres'],reply_markup=other_keyboards.mres_kb())
    if callback_data.name_step == 'main_menu' and callback_data.callback == 'pres':
        await callback.message.edit_text(text=LEXICON_TP_RP['pres'],reply_markup=other_keyboards.pres_kb())
    if callback_data.name_step == 'main_menu' and callback_data.callback == 'zres':
        await callback.message.edit_text(text=LEXICON_TP_RP['zres'],reply_markup=other_keyboards.zres_kb())
    if callback_data.name_step == 'main_menu' and callback_data.callback == 'ogres':
        await callback.message.edit_text(text=LEXICON_TP_RP['ogres'],reply_markup=other_keyboards.ogres_kb())
    if callback_data.name_step == 'mres_kb' and callback_data.callback == 'mres_rp_kb':
        await callback.message.edit_text(text=LEXICON_TP_RP['mres_rp'],reply_markup=other_keyboards.mres_rp_kb(str(callback.from_user.id),
                                                                                                            str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'pres_kb' and callback_data.callback == 'pres_rp_kb':
        await callback.message.edit_text(text=LEXICON_TP_RP['pres_rp'],reply_markup=other_keyboards.pres_rp_kb(str(callback.from_user.id),
                                                                                                            str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'zres_kb' and callback_data.callback == 'zres_rp_kb':
        await callback.message.edit_text(text=LEXICON_TP_RP['zres_rp'],reply_markup=other_keyboards.zres_rp_kb(str(callback.from_user.id),
                                                                                                            str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'ogres_kb' and callback_data.callback == 'ogres_rp_kb':
        await callback.message.edit_text(text=LEXICON_TP_RP['ogres_rp'],reply_markup=other_keyboards.ogres_rp_kb(str(callback.from_user.id),
                                                                                                            str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'mres_kb' and callback_data.callback == 'mres_tp_kb':
        await callback.message.edit_text(text=LEXICON_TP_RP['mres_tp'],reply_markup=other_keyboards.mres_tp_kb(str(callback.from_user.id),
                                                                                                            str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'pres_kb' and callback_data.callback == 'pres_tp_kb':
        await callback.message.edit_text(text=LEXICON_TP_RP['pres_tp'],reply_markup=other_keyboards.pres_tp_kb(str(callback.from_user.id),
                                                                                                            str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'zres_kb' and callback_data.callback == 'zres_tp_kb':
        await callback.message.edit_text(text=LEXICON_TP_RP['zres_tp'],reply_markup=other_keyboards.zres_tp_kb(str(callback.from_user.id),
                                                                                                            str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'ogres_kb' and callback_data.callback == 'ogres_tp_kb':
        await callback.message.edit_text(text=LEXICON_TP_RP['ogres_rp'],reply_markup=other_keyboards.ogres_tp_kb(str(callback.from_user.id),
                                                                                                            str(database_quantity_page[str(callback.from_user.id)]['user_page'])))


    if callback_data.name_step == 'mres_rp' and callback_data.callback == 'add':
        database[str(callback.from_user.id)].clear()
        database[str(callback.from_user.id)]['name_user'] = callback.from_user.first_name
        await callback.message.edit_text(text=LEXICON_TP_RP['mres_rp_name_add'])
        await state.set_state(FSM_RP_TP.name_rp_mres)
    if callback_data.name_step == 'zres_rp' and callback_data.callback == 'add':
        database[str(callback.from_user.id)].clear()
        database[str(callback.from_user.id)]['name_user'] = callback.from_user.first_name
        await callback.message.edit_text(text=LEXICON_TP_RP['zres_rp_name_add'])
        await state.set_state(FSM_RP_TP.name_rp_zres)
    if callback_data.name_step == 'pres_rp' and callback_data.callback == 'add':
        database[str(callback.from_user.id)].clear()
        database[str(callback.from_user.id)]['name_user'] = callback.from_user.first_name
        await callback.message.edit_text(text=LEXICON_TP_RP['pres_rp_name_add'])
        await state.set_state(FSM_RP_TP.name_rp_pres)
    if callback_data.name_step == 'ogres_rp' and callback_data.callback == 'add':
        database[str(callback.from_user.id)].clear()
        database[str(callback.from_user.id)]['name_user'] = callback.from_user.first_name
        await callback.message.edit_text(text=LEXICON_TP_RP['ogres_rp_name_add'])
        await state.set_state(FSM_RP_TP.name_rp_ogres)

    if callback_data.name_step == 'mres_tp' and callback_data.callback == 'add':
        database[str(callback.from_user.id)].clear()
        database[str(callback.from_user.id)]['name_user'] = callback.from_user.first_name
        await callback.message.edit_text(text=LEXICON_TP_RP['mres_tp_name_add'])
        await state.set_state(FSM_RP_TP.name_tp_mres)
    if callback_data.name_step == 'zres_tp' and callback_data.callback == 'add':
        database[str(callback.from_user.id)].clear()
        database[str(callback.from_user.id)]['name_user'] = callback.from_user.first_name
        await callback.message.edit_text(text=LEXICON_TP_RP['zres_tp_name_add'])
        await state.set_state(FSM_RP_TP.name_tp_zres)
    if callback_data.name_step == 'pres_tp' and callback_data.callback == 'add':
        database[str(callback.from_user.id)].clear()
        database[str(callback.from_user.id)]['name_user'] = callback.from_user.first_name
        await callback.message.edit_text(text=LEXICON_TP_RP['pres_tp_name_add'])
        await state.set_state(FSM_RP_TP.name_tp_pres)
    if callback_data.name_step == 'ogres_tp' and callback_data.callback == 'add':
        database[str(callback.from_user.id)].clear()
        database[str(callback.from_user.id)]['name_user'] = callback.from_user.first_name
        await callback.message.edit_text(text=LEXICON_TP_RP['ogres_tp_name_add'])
        await state.set_state(FSM_RP_TP.name_tp_ogres)


    if callback_data.name_step == 'mres_rp' and callback_data.callback == 'save':
        cur.execute(f'''INSERT INTO mres_rp (who_add,name,location)
                       VALUES ('{database[str(callback.from_user.id)]['name_user']}',
                              '{database[str(callback.from_user.id)]['name_rp']}',
                               '{database[str(callback.from_user.id)]['location']}')
        ''')
        db.commit()
        await callback.answer(text=LEXICON_TP_RP['save_success'],show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['mres_rp'],
                                         reply_markup=other_keyboards.mres_rp_kb(str(callback.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(callback.from_user.id)][
                                                                                         'user_page'])))
    if callback_data.name_step == 'pres_rp' and callback_data.callback == 'save':
        cur.execute(f'''INSERT INTO pres_rp (who_add,name,location)
                       VALUES ('{database[str(callback.from_user.id)]['name_user']}',
                              '{database[str(callback.from_user.id)]['name_rp']}',
                               '{database[str(callback.from_user.id)]['location']}')
        ''')
        db.commit()
        await callback.answer(text=LEXICON_TP_RP['save_success'],show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['pres_rp'],
                                         reply_markup=other_keyboards.pres_rp_kb(str(callback.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(callback.from_user.id)][
                                                                                         'user_page'])))
    if callback_data.name_step == 'zres_rp' and callback_data.callback == 'save':
        cur.execute(f'''INSERT INTO zres_rp (who_add,name,location)
                       VALUES ('{database[str(callback.from_user.id)]['name_user']}',
                              '{database[str(callback.from_user.id)]['name_rp']}',
                               '{database[str(callback.from_user.id)]['location']}')
        ''')
        db.commit()
        await callback.answer(text=LEXICON_TP_RP['save_success'],show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['zres_rp'],
                                         reply_markup=other_keyboards.zres_rp_kb(str(callback.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(callback.from_user.id)][
                                                                                         'user_page'])))
    if callback_data.name_step == 'ogres_rp' and callback_data.callback == 'save':
        cur.execute(f'''INSERT INTO ogres_rp (who_add,name,location)
                       VALUES ('{database[str(callback.from_user.id)]['name_user']}',
                              '{database[str(callback.from_user.id)]['name_rp']}',
                               '{database[str(callback.from_user.id)]['location']}')
        ''')
        db.commit()
        await callback.answer(text=LEXICON_TP_RP['save_success'],show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['ogres_rp'],
                                         reply_markup=other_keyboards.ogres_rp_kb(str(callback.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(callback.from_user.id)][
                                                                                         'user_page'])))

    if callback_data.name_step == 'mres_tp' and callback_data.callback == 'save':
        cur.execute(f'''INSERT INTO mres_tp (who_add,name,location)
                       VALUES ('{database[str(callback.from_user.id)]['name_user']}',
                              '{database[str(callback.from_user.id)]['name_rp']}',
                               '{database[str(callback.from_user.id)]['location']}')
        ''')
        db.commit()
        await callback.answer(text=LEXICON_TP_RP['save_success'],show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['mres_tp'],
                                         reply_markup=other_keyboards.mres_tp_kb(str(callback.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(callback.from_user.id)][
                                                                                         'user_page'])))
    if callback_data.name_step == 'pres_tp' and callback_data.callback == 'save':
        cur.execute(f'''INSERT INTO pres_tp (who_add,name,location)
                       VALUES ('{database[str(callback.from_user.id)]['name_user']}',
                              '{database[str(callback.from_user.id)]['name_rp']}',
                               '{database[str(callback.from_user.id)]['location']}')
        ''')
        db.commit()
        await callback.answer(text=LEXICON_TP_RP['save_success'],show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['pres_tp'],
                                         reply_markup=other_keyboards.pres_tp_kb(str(callback.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(callback.from_user.id)][
                                                                                         'user_page'])))
    if callback_data.name_step == 'zres_tp' and callback_data.callback == 'save':
        cur.execute(f'''INSERT INTO zres_tp (who_add,name,location)
                       VALUES ('{database[str(callback.from_user.id)]['name_user']}',
                              '{database[str(callback.from_user.id)]['name_rp']}',
                               '{database[str(callback.from_user.id)]['location']}')
        ''')
        db.commit()
        await callback.answer(text=LEXICON_TP_RP['save_success'],show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['zres_tp'],
                                         reply_markup=other_keyboards.zres_tp_kb(str(callback.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(callback.from_user.id)][
                                                                                         'user_page'])))
    if callback_data.name_step == 'ogres_tp' and callback_data.callback == 'save':
        cur.execute(f'''INSERT INTO ogres_tp (who_add,name,location)
                       VALUES ('{database[str(callback.from_user.id)]['name_user']}',
                              '{database[str(callback.from_user.id)]['name_rp']}',
                               '{database[str(callback.from_user.id)]['location']}')
        ''')
        db.commit()
        await callback.answer(text=LEXICON_TP_RP['save_success'],show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['ogres_tp'],
                                         reply_markup=other_keyboards.ogres_tp_kb(str(callback.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(callback.from_user.id)][
                                                                                         'user_page'])))



    if callback_data.name_step == 'mres_press':
        cur.execute(f'SELECT name,location FROM mres_rp WHERE rowid = {callback_data.callback}')
        a = cur.fetchall()
        coordinate = a[0][1].split(',')
        await callback.message.delete()
        await callback.message.answer_location(latitude=float(coordinate[0]),longitude=float(coordinate[1]),reply_markup=other_keyboards.mres_rp_press_kb(a[0][0]))
    if callback_data.name_step == 'mres_press_loc':
        cur.execute(f'SELECT name,location FROM mres_tp WHERE rowid = {callback_data.callback}')
        a = cur.fetchall()
        coordinate = a[0][1].split(',')
        await callback.message.delete()
        await callback.message.answer_location(latitude=float(coordinate[0]),longitude=float(coordinate[1]),reply_markup=other_keyboards.mres_tp_press_kb(a[0][0]))
    if callback_data.name_step == 'pres_press':
        cur.execute(f'SELECT name,location FROM pres_rp WHERE rowid = {callback_data.callback}')
        a = cur.fetchall()
        coordinate = a[0][1].split(',')
        await callback.message.delete()
        await callback.message.answer_location(latitude=float(coordinate[0]),longitude=float(coordinate[1]),reply_markup=other_keyboards.pres_rp_press_kb(a[0][0]))
    if callback_data.name_step == 'pres_press_loc':
        cur.execute(f'SELECT name,location FROM pres_tp WHERE rowid = {callback_data.callback}')
        a = cur.fetchall()
        coordinate = a[0][1].split(',')
        await callback.message.delete()
        await callback.message.answer_location(latitude=float(coordinate[0]),longitude=float(coordinate[1]),reply_markup=other_keyboards.pres_tp_press_kb(a[0][0]))
    if callback_data.name_step == 'zres_press':
        cur.execute(f'SELECT name,location FROM zres_rp WHERE rowid = {callback_data.callback}')
        a = cur.fetchall()
        coordinate = a[0][1].split(',')
        await callback.message.delete()
        await callback.message.answer_location(latitude=float(coordinate[0]),longitude=float(coordinate[1]),reply_markup=other_keyboards.zres_rp_press_kb(a[0][0]))
    if callback_data.name_step == 'zres_press_loc':
        cur.execute(f'SELECT name,location FROM zres_tp WHERE rowid = {callback_data.callback}')
        a = cur.fetchall()
        coordinate = a[0][1].split(',')
        await callback.message.delete()
        await callback.message.answer_location(latitude=float(coordinate[0]),longitude=float(coordinate[1]),reply_markup=other_keyboards.zres_tp_press_kb(a[0][0]))
    if callback_data.name_step == 'ogres_press':
        cur.execute(f'SELECT name,location FROM ogres_rp WHERE rowid = {callback_data.callback}')
        a = cur.fetchall()
        coordinate = a[0][1].split(',')
        await callback.message.delete()
        await callback.message.answer_location(latitude=float(coordinate[0]),longitude=float(coordinate[1]),reply_markup=other_keyboards.ogres_rp_press_kb(a[0][0]))
    if callback_data.name_step == 'ogres_press_loc':
        cur.execute(f'SELECT name,location FROM ogres_tp WHERE rowid = {callback_data.callback}')
        a = cur.fetchall()
        coordinate = a[0][1].split(',')
        await callback.message.delete()
        await callback.message.answer_location(latitude=float(coordinate[0]),longitude=float(coordinate[1]),reply_markup=other_keyboards.ogres_tp_press_kb(a[0][0]))




    if callback_data.name_step == 'mres_rp_press' and callback_data.callback == 'back':
        try:
            await callback.message.delete()
            await callback.message.answer(text=LEXICON_TP_RP['mres_rp'],
                                             reply_markup=other_keyboards.mres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        except TelegramBadRequest:
            pass
    if callback_data.name_step == 'mres_tp_press' and callback_data.callback == 'back':
        try:
            await callback.message.delete()
            await callback.message.answer(text=LEXICON_TP_RP['mres_tp'],
                                             reply_markup=other_keyboards.mres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        except TelegramBadRequest:
            pass
    if callback_data.name_step == 'zres_rp_press' and callback_data.callback == 'back':
        try:
            await callback.message.delete()
            await callback.message.answer(text=LEXICON_TP_RP['zres_rp'],
                                             reply_markup=other_keyboards.zres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        except TelegramBadRequest:
            pass
    if callback_data.name_step == 'zres_tp_press' and callback_data.callback == 'back':
        try:
            await callback.message.delete()
            await callback.message.answer(text=LEXICON_TP_RP['zres_tp'],
                                             reply_markup=other_keyboards.zres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        except TelegramBadRequest:
            pass
    if callback_data.name_step == 'pres_rp_press' and callback_data.callback == 'back':
        try:
            await callback.message.delete()
            await callback.message.answer(text=LEXICON_TP_RP['pres_rp'],
                                             reply_markup=other_keyboards.pres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        except TelegramBadRequest:
            pass
    if callback_data.name_step == 'pres_tp_press' and callback_data.callback == 'back':
        try:
            await callback.message.delete()
            await callback.message.answer(text=LEXICON_TP_RP['pres_tp'],
                                             reply_markup=other_keyboards.pres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        except TelegramBadRequest:
            pass
    if callback_data.name_step == 'ogres_rp_press' and callback_data.callback == 'back':
        try:
            await callback.message.delete()
            await callback.message.answer(text=LEXICON_TP_RP['ogres_rp'],
                                             reply_markup=other_keyboards.ogres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        except TelegramBadRequest:
            pass
    if callback_data.name_step == 'ogres_tp_press' and callback_data.callback == 'back':
        try:
            await callback.message.delete()
            await callback.message.answer(text=LEXICON_TP_RP['ogres_tp'],
                                             reply_markup=other_keyboards.ogres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        except TelegramBadRequest:
            pass




    if callback_data.name_step == 'mres_rp' and callback_data.callback == 'del':
        await callback.message.edit_text(text=LEXICON_TP_RP['del_rp'],reply_markup=other_keyboards.del_mres_rp_kb(str(callback.from_user.id),
                                                                                                                  str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'mres_tp' and callback_data.callback == 'del':
        await callback.message.edit_text(text=LEXICON_TP_RP['del_tp'],reply_markup=other_keyboards.del_mres_tp_kb(str(callback.from_user.id),
                                                                                                                  str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'zres_rp' and callback_data.callback == 'del':
        await callback.message.edit_text(text=LEXICON_TP_RP['del_rp'],reply_markup=other_keyboards.del_zres_rp_kb(str(callback.from_user.id),
                                                                                                                  str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'zres_tp' and callback_data.callback == 'del':
        await callback.message.edit_text(text=LEXICON_TP_RP['del_tp'],reply_markup=other_keyboards.del_zres_tp_kb(str(callback.from_user.id),
                                                                                                                  str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'pres_rp' and callback_data.callback == 'del':
        await callback.message.edit_text(text=LEXICON_TP_RP['del_rp'],reply_markup=other_keyboards.del_pres_rp_kb(str(callback.from_user.id),
                                                                                                                  str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'pres_tp' and callback_data.callback == 'del':
        await callback.message.edit_text(text=LEXICON_TP_RP['del_tp'],reply_markup=other_keyboards.del_pres_tp_kb(str(callback.from_user.id),
                                                                                                                  str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'ogres_rp' and callback_data.callback == 'del':
        await callback.message.edit_text(text=LEXICON_TP_RP['del_rp'],reply_markup=other_keyboards.del_ogres_rp_kb(str(callback.from_user.id),
                                                                                                                  str(database_quantity_page[str(callback.from_user.id)]['user_page'])))
    if callback_data.name_step == 'ogres_tp' and callback_data.callback == 'del':
        await callback.message.edit_text(text=LEXICON_TP_RP['del_tp'],reply_markup=other_keyboards.del_ogres_tp_kb(str(callback.from_user.id),
                                                                                                                  str(database_quantity_page[str(callback.from_user.id)]['user_page'])))




    if callback_data.name_step == 'mres_press_del':
        cur.execute(f'''DELETE FROM mres_rp
                       WHERE rowid = {callback_data.callback}''')
        db.commit()
        add_page(str(callback.from_user.id),'mres_rp','mres_rp_page')
        await callback.message.edit_text(text=LEXICON_TP_RP['del_rp'],
                                         reply_markup=other_keyboards.del_mres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
    if callback_data.name_step == 'mres_tp_press_del':
        cur.execute(f'''DELETE FROM mres_tp
                       WHERE rowid = {callback_data.callback}''')
        db.commit()
        add_page(str(callback.from_user.id),'mres_tp','mres_tp_page')
        await callback.message.edit_text(text=LEXICON_TP_RP['del_tp'],
                                         reply_markup=other_keyboards.del_mres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
    if callback_data.name_step == 'zres_press_del':
        cur.execute(f'''DELETE FROM zres_rp
                       WHERE rowid = {callback_data.callback}''')
        db.commit()
        add_page(str(callback.from_user.id),'zres_rp','zres_rp_page')
        await callback.message.edit_text(text=LEXICON_TP_RP['del_rp'],
                                         reply_markup=other_keyboards.del_zres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
    if callback_data.name_step == 'zres_tp_press_del':
        cur.execute(f'''DELETE FROM zres_tp
                       WHERE rowid = {callback_data.callback}''')
        db.commit()
        add_page(str(callback.from_user.id),'zres_tp','zres_tp_page')
        await callback.message.edit_text(text=LEXICON_TP_RP['del_tp'],
                                         reply_markup=other_keyboards.del_zres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
    if callback_data.name_step == 'pres_press_del':
        cur.execute(f'''DELETE FROM pres_rp
                       WHERE rowid = {callback_data.callback}''')
        db.commit()
        add_page(str(callback.from_user.id),'pres_rp','pres_rp_page')
        await callback.message.edit_text(text=LEXICON_TP_RP['del_rp'],
                                         reply_markup=other_keyboards.del_pres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
    if callback_data.name_step == 'pres_tp_press_del':
        cur.execute(f'''DELETE FROM pres_tp
                       WHERE rowid = {callback_data.callback}''')
        db.commit()
        add_page(str(callback.from_user.id),'pres_tp','pres_tp_page')
        await callback.message.edit_text(text=LEXICON_TP_RP['del_tp'],
                                         reply_markup=other_keyboards.del_pres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
    if callback_data.name_step == 'ogres_press_del':
        cur.execute(f'''DELETE FROM ogres_rp
                       WHERE rowid = {callback_data.callback}''')
        db.commit()
        add_page(str(callback.from_user.id),'ogres_rp','ogres_rp_page')
        await callback.message.edit_text(text=LEXICON_TP_RP['del_rp'],
                                         reply_markup=other_keyboards.del_ogres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
    if callback_data.name_step == 'ogres_tp_press_del':
        cur.execute(f'''DELETE FROM ogres_tp
                       WHERE rowid = {callback_data.callback}''')
        db.commit()
        add_page(str(callback.from_user.id),'ogres_tp','ogres_tp_page')
        await callback.message.edit_text(text=LEXICON_TP_RP['del_tp'],
                                         reply_markup=other_keyboards.del_ogres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))




    if callback_data.name_step == 'pag_rp_mres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['mres_rp'],
                                             reply_markup=other_keyboards.mres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'pag_tp_mres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['mres_tp'],
                                             reply_markup=other_keyboards.mres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'pag_rp_zres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['zres_rp'],
                                             reply_markup=other_keyboards.zres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'pag_tp_zres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['zres_tp'],
                                             reply_markup=other_keyboards.zres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'pag_rp_pres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['pres_rp'],
                                             reply_markup=other_keyboards.pres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'pag_tp_pres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['pres_tp'],
                                             reply_markup=other_keyboards.pres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'pag_rp_ogres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['ogres_rp'],
                                             reply_markup=other_keyboards.ogres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'pag_tp_ogres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['ogres_tp'],
                                             reply_markup=other_keyboards.ogres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)





    if callback_data.name_step == 'pag_rp_mres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['mres_rp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['mres_rp'],
                                             reply_markup=other_keyboards.mres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'pag_tp_mres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['mres_tp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['mres_tp'],
                                             reply_markup=other_keyboards.mres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'pag_rp_zres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['zres_rp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['zres_rp'],
                                             reply_markup=other_keyboards.zres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'pag_tp_zres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['zres_tp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['zres_tp'],
                                             reply_markup=other_keyboards.zres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'pag_rp_pres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['pres_rp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['pres_rp'],
                                             reply_markup=other_keyboards.pres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'pag_tp_pres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['pres_tp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['pres_tp'],
                                             reply_markup=other_keyboards.pres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'pag_rp_ogres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['ogres_rp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['ogres_rp'],
                                             reply_markup=other_keyboards.ogres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'pag_tp_ogres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['ogres_tp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['ogres_tp'],
                                             reply_markup=other_keyboards.ogres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass





    if callback_data.name_step == 'del_pag_rp_mres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['mres_rp'],
                                             reply_markup=other_keyboards.del_mres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'del_pag_tp_mres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['mres_tp'],
                                             reply_markup=other_keyboards.del_mres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'del_pag_rp_zres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['zres_rp'],
                                             reply_markup=other_keyboards.del_zres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'del_pag_tp_zres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['zres_tp'],
                                             reply_markup=other_keyboards.del_zres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'del_pag_rp_pres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['pres_rp'],
                                             reply_markup=other_keyboards.del_pres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'del_pag_tp_pres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['pres_tp'],
                                             reply_markup=other_keyboards.del_pres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'del_pag_rp_ogres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['ogres_rp'],
                                             reply_markup=other_keyboards.del_ogres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'del_pag_tp_ogres' and callback_data.callback == 'backward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] != 1:
            database_quantity_page[str(callback.from_user.id)]['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_TP_RP['ogres_tp'],
                                             reply_markup=other_keyboards.del_ogres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)




    if callback_data.name_step == 'del_pag_rp_mres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['mres_rp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['mres_rp'],
                                             reply_markup=other_keyboards.del_mres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'del_pag_tp_mres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['mres_tp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['mres_tp'],
                                             reply_markup=other_keyboards.del_mres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'del_pag_rp_zres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['zres_rp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['zres_rp'],
                                             reply_markup=other_keyboards.del_zres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'del_pag_tp_zres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['zres_tp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['zres_tp'],
                                             reply_markup=other_keyboards.del_zres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'del_pag_rp_pres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['pres_rp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['pres_rp'],
                                             reply_markup=other_keyboards.del_pres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'del_pag_tp_pres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['pres_tp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['pres_tp'],
                                             reply_markup=other_keyboards.del_pres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'del_pag_rp_ogres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['ogres_rp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['ogres_rp'],
                                             reply_markup=other_keyboards.del_ogres_rp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass
    if callback_data.name_step == 'del_pag_tp_ogres' and callback_data.callback == 'forward':
        if database_quantity_page[str(callback.from_user.id)]['user_page'] < database_quantity_page[str(callback.from_user.id)]['ogres_tp_page']:
            database_quantity_page[str(callback.from_user.id)]['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_TP_RP['ogres_tp'],
                                             reply_markup=other_keyboards.del_ogres_tp_kb(str(callback.from_user.id),
                                                                                     str(database_quantity_page[
                                                                                             str(callback.from_user.id)][
                                                                                             'user_page'])))
        else:
            pass


    if callback_data.name_step == 'mres_rp' and callback_data.callback == 'new_location':
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['new_location'])
        await state.set_state(FSM_RP_TP.location_rp_mres)
    if callback_data.name_step == 'mres_tp' and callback_data.callback == 'new_location':
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_TP_RP['new_location'])
        await state.set_state(FSM_RP_TP.location_tp_mres)

    if callback_data.callback == 'none':
        await callback.answer()
    if callback_data.name_step == 'mres' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_TP_RP['main_menu'], reply_markup=other_keyboards.start_tp_rp_kb())
    if callback_data.name_step == 'zres' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_TP_RP['main_menu'], reply_markup=other_keyboards.start_tp_rp_kb())
    if callback_data.name_step == 'pres' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_TP_RP['main_menu'], reply_markup=other_keyboards.start_tp_rp_kb())
    if callback_data.name_step == 'ogres' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_TP_RP['main_menu'], reply_markup=other_keyboards.start_tp_rp_kb())
    if callback_data.name_step == 'mres_rp' and callback_data.callback == 'back' \
            or callback_data.name_step == 'mres_tp' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_TP_RP['mres'], reply_markup=other_keyboards.mres_kb())
    if callback_data.name_step == 'zres_rp' and callback_data.callback == 'back' \
            or callback_data.name_step == 'zres_tp' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_TP_RP['zres'], reply_markup=other_keyboards.zres_kb())
    if callback_data.name_step == 'pres_rp' and callback_data.callback == 'back' \
            or callback_data.name_step == 'pres_tp' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_TP_RP['pres'], reply_markup=other_keyboards.pres_kb())
    if callback_data.name_step == 'ogres_rp' and callback_data.callback == 'back' \
            or callback_data.name_step == 'ogres_tp' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_TP_RP['ogres'], reply_markup=other_keyboards.ogres_kb())


@router.message(StateFilter(FSM_RP_TP.name_rp_mres))
async def process_message_name_rp_mres(message:Message,state:FSMContext):
    database[str(message.from_user.id)]['name_rp'] = message.text.upper()
    cur.execute(f"SELECT name FROM mres_rp WHERE name LIKE '{message.text.upper()}' ")
    a = cur.fetchall()
    if a:
        await message.answer(text=LEXICON_TP_RP['error_repeat'])
        await message.answer(text=LEXICON_TP_RP['mres_rp'],
                                         reply_markup=other_keyboards.mres_rp_kb(str(message.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(message.from_user.id)][
                                                                                         'user_page'])))#Было mres_rp_page
        await state.set_state(FSM_RP_TP.main_menu)
    else:
        await message.answer(text=LEXICON_TP_RP['mres_rp_location_add'])
        await state.set_state(FSM_RP_TP.location_rp_mres)


@router.message(StateFilter(FSM_RP_TP.location_rp_mres))
async def process_message_end_rp_mres(message:Message,state:FSMContext):
    try:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            text = f'{latitude},{longitude}'
            database[str(message.from_user.id)]['location'] = text

            await message.answer_location(latitude=latitude,longitude=longitude,reply_markup=other_keyboards.mres_save_rp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
        else:
            database[str(message.from_user.id)]['location'] = message.text
            lists = database[str(message.from_user.id)]['location'].split(',')

            await message.answer_location(latitude=float(lists[0]),longitude=float(lists[1]),reply_markup=other_keyboards.mres_save_rp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
    except:
        await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.name_tp_mres))
async def process_message_name_rp_mres(message:Message,state:FSMContext):
    database[str(message.from_user.id)]['name_rp'] = message.text.upper()#Остаёте всегда name_rp чтобы не исправлять везде уже.
    cur.execute(f"SELECT name FROM mres_tp WHERE name LIKE '{message.text.upper()}' ")
    a = cur.fetchall()
    if a:
        await message.answer(text=LEXICON_TP_RP['error_repeat'])
        await message.answer(text=LEXICON_TP_RP['mres_tp'],
                                         reply_markup=other_keyboards.mres_tp_kb(str(message.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(message.from_user.id)][
                                                                                         'user_page'])))#Было mres_rp_page
        await state.set_state(FSM_RP_TP.main_menu)
    else:
        await message.answer(text=LEXICON_TP_RP['mres_tp_location_add'])
        await state.set_state(FSM_RP_TP.location_tp_mres)


@router.message(StateFilter(FSM_RP_TP.location_tp_mres))
async def process_message_end_rp_mres(message:Message,state:FSMContext):
    try:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            text = f'{latitude},{longitude}'
            database[str(message.from_user.id)]['location'] = text

            await message.answer_location(latitude=latitude,longitude=longitude,reply_markup=other_keyboards.mres_save_tp_kb())
            await state.set_state(FSM_RP_TP.main_menu)

        else:
            database[str(message.from_user.id)]['location'] = message.text
            lists = database[str(message.from_user.id)]['location'].split(',')

            await message.answer_location(latitude=float(lists[0]),longitude=float(lists[1]),reply_markup=other_keyboards.mres_save_tp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
    except:
        await message.answer(text=LEXICON_TP_RP['echo'])


@router.message(StateFilter(FSM_RP_TP.name_rp_zres))
async def process_message_name_rp_zres(message:Message,state:FSMContext):
    database[str(message.from_user.id)]['name_rp'] = message.text.upper()
    cur.execute(f"SELECT name FROM zres_rp WHERE name LIKE '{message.text.upper()}' ")
    a = cur.fetchall()
    if a:
        await message.answer(text=LEXICON_TP_RP['error_repeat'])
        await message.answer(text=LEXICON_TP_RP['zres_rp'],
                                         reply_markup=other_keyboards.zres_rp_kb(str(message.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(message.from_user.id)][
                                                                                         'user_page'])))#Было mres_rp_page
        await state.set_state(FSM_RP_TP.main_menu)
    else:
        await message.answer(text=LEXICON_TP_RP['zres_rp_location_add'])
        await state.set_state(FSM_RP_TP.location_rp_zres)


@router.message(StateFilter(FSM_RP_TP.location_rp_zres))
async def process_message_end_rp_zres(message:Message,state:FSMContext):
    try:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            text = f'{latitude},{longitude}'
            database[str(message.from_user.id)]['location'] = text

            await message.answer_location(latitude=latitude, longitude=longitude,
                                          reply_markup=other_keyboards.zres_save_rp_kb())
            await state.set_state(FSM_RP_TP.main_menu)

        else:
            database[str(message.from_user.id)]['location'] = message.text
            lists = database[str(message.from_user.id)]['location'].split(',')

            await message.answer_location(latitude=float(lists[0]),longitude=float(lists[1]),reply_markup=other_keyboards.zres_save_rp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
    except:
        await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.name_tp_zres))
async def process_message_name_tp_zres(message:Message,state:FSMContext):
    database[str(message.from_user.id)]['name_rp'] = message.text.upper()#Остаёте всегда name_rp чтобы не исправлять везде уже.
    cur.execute(f"SELECT name FROM zres_tp WHERE name LIKE '{message.text.upper()}' ")
    a = cur.fetchall()
    if a:
        await message.answer(text=LEXICON_TP_RP['error_repeat'])
        await message.answer(text=LEXICON_TP_RP['zres_tp'],
                                         reply_markup=other_keyboards.zres_tp_kb(str(message.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(message.from_user.id)][
                                                                                         'user_page'])))#Было mres_rp_page
        await state.set_state(FSM_RP_TP.main_menu)
    else:
        await message.answer(text=LEXICON_TP_RP['zres_tp_location_add'])
        await state.set_state(FSM_RP_TP.location_tp_zres)


@router.message(StateFilter(FSM_RP_TP.location_tp_zres))
async def process_message_end_tp_zres(message:Message,state:FSMContext):
    try:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            text = f'{latitude},{longitude}'
            database[str(message.from_user.id)]['location'] = text

            await message.answer_location(latitude=latitude, longitude=longitude,
                                          reply_markup=other_keyboards.zres_save_tp_kb())
            await state.set_state(FSM_RP_TP.main_menu)

        else:
            database[str(message.from_user.id)]['location'] = message.text
            lists = database[str(message.from_user.id)]['location'].split(',')

            await message.answer_location(latitude=float(lists[0]),longitude=float(lists[1]),reply_markup=other_keyboards.zres_save_tp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
    except:
        await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.location_rp_zres))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.location_tp_zres))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])



@router.message(StateFilter(FSM_RP_TP.name_rp_pres))
async def process_message_name_rp_zres(message:Message,state:FSMContext):
    database[str(message.from_user.id)]['name_rp'] = message.text.upper()
    cur.execute(f"SELECT name FROM pres_rp WHERE name LIKE '{message.text.upper()}' ")
    a = cur.fetchall()
    if a:
        await message.answer(text=LEXICON_TP_RP['error_repeat'])
        await message.answer(text=LEXICON_TP_RP['pres_rp'],
                                         reply_markup=other_keyboards.pres_rp_kb(str(message.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(message.from_user.id)][
                                                                                         'user_page'])))#Было mres_rp_page
        await state.set_state(FSM_RP_TP.main_menu)
    else:
        await message.answer(text=LEXICON_TP_RP['pres_rp_location_add'])
        await state.set_state(FSM_RP_TP.location_rp_pres)


@router.message(StateFilter(FSM_RP_TP.location_rp_pres))
async def process_message_end_rp_pres(message:Message,state:FSMContext):
    try:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            text = f'{latitude},{longitude}'
            database[str(message.from_user.id)]['location'] = text

            await message.answer_location(latitude=latitude, longitude=longitude,
                                          reply_markup=other_keyboards.pres_save_rp_kb())
            await state.set_state(FSM_RP_TP.main_menu)

        else:
            database[str(message.from_user.id)]['location'] = message.text
            lists = database[str(message.from_user.id)]['location'].split(',')

            await message.answer_location(latitude=float(lists[0]),longitude=float(lists[1]),reply_markup=other_keyboards.pres_save_rp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
    except:
        await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.name_tp_pres))
async def process_message_name_tp_pres(message:Message,state:FSMContext):
    database[str(message.from_user.id)]['name_rp'] = message.text.upper()#Остаёте всегда name_rp чтобы не исправлять везде уже.
    cur.execute(f"SELECT name FROM pres_tp WHERE name LIKE '{message.text.upper()}' ")
    a = cur.fetchall()
    if a:
        await message.answer(text=LEXICON_TP_RP['error_repeat'])
        await message.answer(text=LEXICON_TP_RP['pres_tp'],
                                         reply_markup=other_keyboards.pres_tp_kb(str(message.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(message.from_user.id)][
                                                                                         'user_page'])))#Было mres_rp_page
        await state.set_state(FSM_RP_TP.main_menu)
    else:
        await message.answer(text=LEXICON_TP_RP['pres_tp_location_add'])
        await state.set_state(FSM_RP_TP.location_tp_pres)


@router.message(StateFilter(FSM_RP_TP.location_tp_pres))
async def process_message_end_tp_pres(message:Message,state:FSMContext):
    try:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            text = f'{latitude},{longitude}'
            database[str(message.from_user.id)]['location'] = text

            await message.answer_location(latitude=latitude, longitude=longitude,
                                          reply_markup=other_keyboards.pres_save_tp_kb())
            await state.set_state(FSM_RP_TP.main_menu)

        else:
            database[str(message.from_user.id)]['location'] = message.text
            lists = database[str(message.from_user.id)]['location'].split(',')

            await message.answer_location(latitude=float(lists[0]),longitude=float(lists[1]),reply_markup=other_keyboards.pres_save_tp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
    except:
        await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.name_rp_ogres))
async def process_message_name_rp_ogres(message:Message,state:FSMContext):
    database[str(message.from_user.id)]['name_rp'] = message.text.upper()
    cur.execute(f"SELECT name FROM ogres_rp WHERE name LIKE '{message.text.upper()}' ")
    a = cur.fetchall()
    if a:
        await message.answer(text=LEXICON_TP_RP['error_repeat'])
        await message.answer(text=LEXICON_TP_RP['ogres_rp'],
                                         reply_markup=other_keyboards.ogres_rp_kb(str(message.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(message.from_user.id)][
                                                                                         'user_page'])))#Было mres_rp_page
        await state.set_state(FSM_RP_TP.main_menu)
    else:
        await message.answer(text=LEXICON_TP_RP['zres_rp_location_add'])
        await state.set_state(FSM_RP_TP.location_rp_ogres)


@router.message(StateFilter(FSM_RP_TP.location_rp_ogres))
async def process_message_end_rp_zres(message:Message,state:FSMContext):
    try:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            text = f'{latitude},{longitude}'
            database[str(message.from_user.id)]['location'] = text

            await message.answer_location(latitude=latitude, longitude=longitude,
                                          reply_markup=other_keyboards.ogres_save_rp_kb())
            await state.set_state(FSM_RP_TP.main_menu)

        else:
            database[str(message.from_user.id)]['location'] = message.text
            lists = database[str(message.from_user.id)]['location'].split(',')

            await message.answer_location(latitude=float(lists[0]),longitude=float(lists[1]),reply_markup=other_keyboards.ogres_save_rp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
    except:
        await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.name_tp_ogres))
async def process_message_name_tp_ogres(message:Message,state:FSMContext):
    database[str(message.from_user.id)]['name_rp'] = message.text.upper()#Остаёте всегда name_rp чтобы не исправлять везде уже.
    cur.execute(f"SELECT name FROM ogres_tp WHERE name LIKE '{message.text.upper()}' ")
    a = cur.fetchall()
    if a:
        await message.answer(text=LEXICON_TP_RP['error_repeat'])
        await message.answer(text=LEXICON_TP_RP['ogres_tp'],
                                         reply_markup=other_keyboards.ogres_tp_kb(str(message.from_user.id),
                                                                                 str(database_quantity_page[
                                                                                         str(message.from_user.id)][
                                                                                         'user_page'])))#Было mres_rp_page
        await state.set_state(FSM_RP_TP.main_menu)
    else:
        await message.answer(text=LEXICON_TP_RP['ogres_tp_location_add'])
        await state.set_state(FSM_RP_TP.location_tp_ogres)


@router.message(StateFilter(FSM_RP_TP.location_tp_ogres))
async def process_message_end_tp_ogres(message:Message,state:FSMContext):
    try:
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            text = f'{latitude},{longitude}'
            database[str(message.from_user.id)]['location'] = text

            await message.answer_location(latitude=latitude, longitude=longitude,
                                          reply_markup=other_keyboards.ogres_save_tp_kb())
            await state.set_state(FSM_RP_TP.main_menu)

        else:
            database[str(message.from_user.id)]['location'] = message.text
            lists = database[str(message.from_user.id)]['location'].split(',')

            await message.answer_location(latitude=float(lists[0]),longitude=float(lists[1]),reply_markup=other_keyboards.ogres_save_tp_kb())
            await state.set_state(FSM_RP_TP.main_menu)
    except:
        await message.answer(text=LEXICON_TP_RP['echo'])


@router.message(StateFilter(FSM_RP_TP.location_rp_mres))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.location_tp_mres))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.location_rp_ogres))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.location_tp_ogres))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.location_rp_pres))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])

@router.message(StateFilter(FSM_RP_TP.location_tp_pres))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])