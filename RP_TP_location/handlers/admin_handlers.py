import sqlite3

from aiogram import Bot
from aiogram import Router,F
from aiogram.filters import CommandStart,StateFilter
from aiogram.types import Message,CallbackQuery
from keyboards import other_keyboards
from lexicon.lexicon import LEXICON_TP_RP
from database.database import database_quantity_page,database_page,database
from FSM.FSM import FSM_RP_TP
from aiogram.fsm.context import FSMContext
from config_data.config import load_config,Config
from filters.IsAdmin import IsAdmin
from aiogram.fsm.state import default_state
router: Router = Router()
config: Config = load_config()
admin_id: list[int] = config.tg_bot.admin_id
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
db = sqlite3.connect('TP_RP.sql')
cur = db.cursor()


@router.callback_query(F.data == 'give_access',IsAdmin(admin_id))
async def procee_give_access(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text='<b>Введите <i>id</i> того, кому хотите <i>дать доступ</i>.</b>')
    await state.set_state(FSM_RP_TP.give_access)


@router.callback_query(F.data == 'deny_access',IsAdmin(admin_id))
async def procee_give_access(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text='<b>Введите <i>id</i> того, кому хотите <i>закрыть доступ</i>.</b>')
    await state.set_state(FSM_RP_TP.deny_access)

@router.message(lambda x: x.text.isdigit(),IsAdmin(admin_id),StateFilter(FSM_RP_TP.give_access))
async def process_enter_id(message:Message):
    await bot.send_message(chat_id=message.text,text='✅ Доступ открыт',reply_markup=other_keyboards.enter())

@router.message(lambda x: x.text.isdigit(),IsAdmin(admin_id),StateFilter(FSM_RP_TP.deny_access))
async def process_enter_id(message:Message):
    await bot.send_message(chat_id=message.text,text='❌ Доступ закрыт')


@router.message(IsAdmin(admin_id), CommandStart())
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
        cur.execute(f'''INSERT INTO user (id_user,name_user)
                       VALUES ({message.from_user.id},'{message.from_user.first_name}')
        ''')
        db.commit()
    else:
        pass
    await message.answer(text=LEXICON_TP_RP['main_menu'],reply_markup=other_keyboards.start_tp_rp_kb())
    await state.set_state(FSM_RP_TP.main_menu)

@router.message(StateFilter(default_state))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo_start'])

@router.message(~StateFilter(default_state))
async def process_echo_send(message:Message):
    await message.answer(text=LEXICON_TP_RP['echo'])