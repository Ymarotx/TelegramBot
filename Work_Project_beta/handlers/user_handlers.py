import sqlite3
import datetime
import time
import time as t
from aiogram.exceptions import TelegramBadRequest
from aiogram import F,Router
from aiogram.types import Message,CallbackQuery,FSInputFile
from aiogram.filters import StateFilter,Command,CommandStart
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram import Bot

import services.schedule
from services import google_translate

from FSM.FSM import FSMWork,FSMCloseApplication,FSMWork_stock,FSMWork_purchase,FSMWork_library,FSMWork_phonebook,\
    FSMWork_schedule
from lexicon.lexicon import LEXICON_WORK,LEXICON_PHONEBOOK_SHORT
from keyboards.main_menu_kb import main_menu_kb
from keyboards.other_keyboards import application_kb,save_delete_application_kb,active_application_kb,\
close_delete_application,completed_application_kb,button_back,cancel_application_kb,cancel_application_del_kb,result_month_2,\
resul_month_2_kb_month,result_month_2_kb_month_back
from database.database import application,database,db_name_materials,database_materials,database_time,db_material_table,database_2,database_3,\
    database_4,database_5,database_str,database_6,database_del,database_english_dict,database_english_list,database_english_answer,\
    database_closing_app
from database.Work_db import create_table
from keyboards.close_application_kb import close_application_kb,continue_close_application_kb,closing_application_kb,\
    press_material,Closing_Applicatin_Factory
from services.open_all_table import open_all_table_materials
from filters.IsAdmin import IsAdmin
from filters.EntryName import EntryName
from keyboards.other_keyboards import ActiveApplicationCallbackFactory,CancelApplicationCallbackFactory,ResultMonthCallbackFactory
from services.result_month import result_month,detail_result_month
from services import stock,english_dict,delete_message
from keyboards import stock_kb
from keyboards.stock_kb import StockCallbackFactory,add_del_stock_kb
from keyboards import purchase_kb,library_kb
from config_data.config import Config,load_config
from keyboards import phonebook_kb


router: Router=Router()
db = sqlite3.connect('Work.sql')
cur = db.cursor()
config: Config = load_config()
admin_id: list[int] = config.tg_bot.admin_id
bot: Bot=Bot(token=config.tg_bot.token)



@router.message(CommandStart(),StateFilter(default_state),IsAdmin(admin_id))
async def process_start_command(message:Message,state:FSMContext):
    create_table(cur,db)
    cur.execute('SELECT * FROM label')
    database['user_page'] = 1
    await message.answer(text=LEXICON_WORK['main_menu'],reply_markup=main_menu_kb())
    await state.set_state(FSMWork.main_menu)

@router.message(Command(commands='main_menu'),~StateFilter(default_state))
async def process_main_menu_commands(message:Message,state:FSMContext):
    database.clear()
    db_name_materials.clear()
    database_materials.clear()
    db_material_table.clear()
    database_time.clear()
    if database_3:
        for i in database_3:
            lists = []
            for k in i:
                if "✔️" in k and k not in lists:
                    lists.append(k)
            if lists:
                for p in range(len(lists)):
                    i[f'{lists[p].replace("✔️", "⚜️")}'] = i.pop(lists[p])
    for i in database_del:
        try:
            if i:
                await bot.delete_message(chat_id=message.from_user.id, message_id=i)
        except TelegramBadRequest:
            pass

    database_del.clear()
    database_2.clear()
    database_3.clear()
    database_english_answer.clear()
    database_english_dict.clear()
    database_english_list.clear()
    database_materials.clear()
    await message.answer(text=LEXICON_WORK['main_menu'],reply_markup=main_menu_kb())
    await state.set_state(FSMWork.main_menu)
@router.callback_query(F.data == 'application',StateFilter(FSMWork.main_menu))
async def process_application_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_WORK['application'],reply_markup=application_kb())
    await state.set_state(FSMWork.application)
@router.callback_query(F.data == 'back_main_menu',StateFilter(FSMWork.application))
async def process_application_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_WORK['main_menu'], reply_markup=main_menu_kb())
    await state.set_state(FSMWork.main_menu)
@router.callback_query(F.data == 'add_application',StateFilter(FSMWork.application))
async def process_add_application_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_WORK['name_department'])
    await state.set_state(FSMWork.name_department)

@router.message(StateFilter(FSMWork.name_department))
async def process_name_department(message:Message,state:FSMContext):
    application['name_department'] = message.text.upper()
    await message.answer(text=LEXICON_WORK['name_house'])
    await state.set_state(FSMWork.name_house)

@router.message(StateFilter(FSMWork.name_house))
async def process_name_house(message:Message,state:FSMContext):
    application['name_house'] = message.text.upper()
    await message.answer(text=LEXICON_WORK['number_cabinet'])
    await state.set_state(FSMWork.number_cabinet)

@router.message(StateFilter(FSMWork.number_cabinet))
async def process_number_cabinet(message:Message,state:FSMContext):
    application['number_cabinet'] = message.text
    await message.answer(text=LEXICON_WORK['what_to_do'])
    await state.set_state(FSMWork.what_to_do)

@router.message(StateFilter(FSMWork.what_to_do))
async def process_what_to_do(message:Message,state:FSMContext):
    application['what_to_do'] = message.text
    await message.answer(text=LEXICON_WORK['full_application'],reply_markup=save_delete_application_kb())
    await state.set_state(FSMWork.save_delete_application)

@router.callback_query(F.data == 'save_application',StateFilter(FSMWork.save_delete_application))
async def process_save_press(callback:CallbackQuery,state:FSMContext):
    time = datetime.datetime.now()
    now_time = str(time).split('.')
    cur.execute('INSERT INTO application VALUES ("%s","%s","%s","%s","%s","%s")'%(now_time[0],application['name_department'],application['name_house'],
                                                                        application['number_cabinet'],application['what_to_do'],0))
    db.commit()

    await callback.message.edit_text(text=LEXICON_WORK['save_application'],reply_markup=button_back('Главное меню','application'))
    await state.set_state(FSMWork.main_menu)
@router.callback_query(F.data == 'delete_application',StateFilter(FSMWork.save_delete_application))
async def process_save_press(callback:CallbackQuery,state:FSMContext):
    application.clear()
    await callback.answer(text=LEXICON_WORK['delete_application'],show_alert=True)
    await callback.message.edit_text(text=LEXICON_WORK['application'], reply_markup=application_kb())
    await state.set_state(FSMWork.application)

@router.callback_query(F.data == 'active_application',StateFilter(FSMWork.application))
async def process_active_application_press(callback:CallbackQuery,state:FSMContext):
    database['user_page'] = 1
    cur.execute('SELECT * FROM application')
    a = cur.fetchall()
    if a:
        await callback.message.edit_text(text=LEXICON_WORK['active_application'],reply_markup=active_application_kb(str(database['user_page'])))
    else:
        await callback.answer(text='На данный момент нет действующих заявок.',show_alert=True)

@router.callback_query(F.data == 'forward',StateFilter(FSMWork.application))
async def process_forward_press(callback:CallbackQuery):
    if database['user_page'] < database['quantity_page']:
        database['user_page'] += 1
        await callback.message.edit_text(text=LEXICON_WORK['active_application'],
                                      reply_markup=active_application_kb(str(database['user_page'])))
    else:
        pass

@router.callback_query(F.data == 'backward',StateFilter(FSMWork.application))
async def process_forward_press(callback:CallbackQuery):
    if database['user_page'] != 1:
        database['user_page'] -= 1
        await callback.message.edit_text(text=LEXICON_WORK['active_application'],
                                      reply_markup=active_application_kb(str(database['user_page'])))
    else:
        await callback.answer(text='Вы находитесь на первой странице',show_alert=True)

@router.callback_query(F.data == 'forward',StateFilter(FSMWork.completed_application))
async def process_forward_press(callback:CallbackQuery):
    if database['user_page'] < database['quantity_page_close']:
        database['user_page'] += 1
        await callback.message.edit_text(text=LEXICON_WORK['completed_application'],
                                      reply_markup=completed_application_kb(str(database['user_page'])))
    else:
        pass


@router.callback_query(F.data == 'backward',StateFilter(FSMWork.completed_application))
async def process_forward_press(callback:CallbackQuery):
    if database['user_page'] != 1:
        database['user_page'] -= 1
        await callback.message.edit_text(text=LEXICON_WORK['completed_application'],
                                      reply_markup=completed_application_kb(str(database['user_page'])))
    else:
        await callback.answer(text='Вы находитесь на первой странице',show_alert=True)

@router.callback_query(lambda x: x.data.isdigit(),StateFilter(FSMWork.completed_application))
async def process_application_id_press(callback:CallbackQuery):
    db = sqlite3.connect('Work.sql')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM completed_application WHERE rowid == {callback.data}')
    a = cur.fetchall()
    texts = open_all_table_materials(a[0][5],cur)
    database['db_id'] = int(callback.data)
    text = (f'<b><code>Заявка от {a[0][0]};\n'
            f'Служба: {a[0][1]};\n'
            f'Здание: {a[0][2]};\n'
            f'Кабинет: {a[0][3]};\n'
            f'Текст заявки: {a[0][4]};\n'
            f'Заявка закрыта - {a[0][5]};\n'
            f'Затраченные материалы:</code> \n'
            f'{texts}</b>')
    await callback.message.edit_text(text=text,reply_markup=button_back('Назад','back_completed_application_2'))
    cur.close()
    db.close()

@router.callback_query(F.data == 'back_application')
async def process_application_id_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_WORK['application'], reply_markup=application_kb())
    await state.set_state(FSMWork.application)

@router.callback_query(F.data == 'back_active_application',StateFilter(FSMCloseApplication.close_application))
async def process_application_id_press(callback:CallbackQuery,state:FSMContext):
    database['user_page'] = 1
    database_materials.clear()
    cur.execute('SELECT * FROM application')
    a = cur.fetchall()
    if a:
        await callback.message.edit_text(text=LEXICON_WORK['active_application'],
                                         reply_markup=active_application_kb(str(database['user_page'])))
        await state.set_state(FSMWork.application)
    else:
        await callback.message.edit_text(text=LEXICON_WORK['application'], reply_markup=application_kb())
        await state.set_state(FSMWork.application)


@router.callback_query(lambda x: x.data.isdigit(),StateFilter(FSMWork.application))
async def process_application_id_press(callback:CallbackQuery):
    cur.execute(f'SELECT * FROM application WHERE rowid == {callback.data}')
    a = cur.fetchall()
    database['db_id'] = int(callback.data)
    cur.execute(f'SELECT text FROM notes_active_application WHERE row_id_active_application = {int(callback.data)}')
    text_notes = cur.fetchone()
    text = (f'<code>Заявка от {a[0][0]};\n'
            f'Служба: {a[0][1]};\n'
            f'Здание: {a[0][2]};\n'
            f'Кабинет: {a[0][3]};\n'
            f'Текст заявки: {a[0][4]}.</code>')
    if text_notes:
        await callback.answer(text=f'📌 Заметки:\n{text_notes[0]}',show_alert=True)
    await callback.message.edit_text(text=text, reply_markup=close_delete_application(int(callback.data)))

@router.callback_query(lambda x: x.data.split('.')[0] == 'del_application',StateFilter(FSMWork.application))
async def process_del_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text='Введите причину отмены.')
    await state.set_state(FSMCloseApplication.delete_application)

@router.callback_query(lambda x: x.data.split('.')[0] in ['label_1','label_2','label_3'],StateFilter(FSMWork.application))
async def process_label_1_press(callback:CallbackQuery):
    id = callback.data.split('.')[1]
    if callback.data.split('.')[0] == 'label_1':
        cur.execute(f'''UPDATE application 
                       SET label_id=1
                       WHERE rowid={id}''')
    if callback.data.split('.')[0] == 'label_2':
        cur.execute(f'''UPDATE application 
                       SET label_id=2
                       WHERE rowid={id}''')
    if callback.data.split('.')[0] == 'label_3':
        cur.execute(f'''UPDATE application 
                       SET label_id=3
                       WHERE rowid={id}''')
    db.commit()
    await callback.answer()
@router.callback_query(lambda x: x.data.split('.')[0] == 'notes_active_application',StateFilter(FSMWork.application))
async def process_notes_active_application_press(callback:CallbackQuery,state:FSMContext):
    id = callback.data.split('.')[1]
    database['id_notes'] = int(id)
    cur.execute(f'SELECT text FROM notes_active_application WHERE row_id_active_application = {int(id)}')
    text = cur.fetchone()
    if text:
        await callback.message.edit_text(text=text[0])
    else:
        await callback.message.edit_text(text=LEXICON_WORK['enter_notes'])
    await state.set_state(FSMWork.notes)

@router.message(StateFilter(FSMWork.notes))
async def process_update_notes_active_application(message:Message,state:FSMContext):
    cur.execute(f'''SELECT text FROM notes_active_application WHERE row_id_active_application = {database['id_notes']}''')
    text = cur.fetchone()
    if text:
        cur.execute(f'''UPDATE notes_active_application
                       SET text = '{message.text}'
                       WHERE text = (SELECT text
                                     FROM notes_active_application
                                     WHERE row_id_active_application = {database['id_notes']}) ''')

    else:
        cur.execute(f'''INSERT INTO notes_active_application (row_id_active_application,text) 
                           VALUES ({database['id_notes']},'{message.text}') ''')

    cur.execute(f'''SELECT * FROM application WHERE rowid == {database['db_id']}''')
    a = cur.fetchall()
    db.commit()
    text = f'<code><i>{a[0][0]}</i> заявка от <i>{a[0][1]}</i>, в <i>{a[0][2]}</i>, <i>{a[0][3]}</i> кабинет, нужно <i>{a[0][4]}</i></code>'
    await message.answer(text=text,reply_markup=close_delete_application(database['db_id']))
    await state.set_state(FSMWork.application)


@router.message(StateFilter(FSMCloseApplication.delete_application))
async def process_del_application_message(message:Message,state:FSMContext):
    why_del = message.text
    d = datetime.datetime.now()
    time = str(d).split('.')
    id = database['db_id']
    cur.execute(f'SELECT * FROM application WHERE rowid={id}')
    lists = cur.fetchall()
    lists.append(str(time[0]))
    cur.execute(
        f'INSERT INTO cancel_application VALUES ("{str(lists[0][0])}","{lists[0][1]}","{lists[0][2]}","{lists[0][3]}","{lists[0][4]}","{str(lists[1])}","{why_del}")')
    cur.execute(f'DELETE FROM application WHERE rowid={id}')
    db.commit()
    db_name_materials.clear()
    await message.answer(text='Заявка успешно отменена.')
    await message.answer(text=LEXICON_WORK['main_menu'],reply_markup=main_menu_kb())
    await state.set_state(FSMWork.main_menu)
@router.callback_query(ActiveApplicationCallbackFactory.filter(),FSMWork.application)
async def process_back_press(callback:CallbackQuery,
                             callback_data:ActiveApplicationCallbackFactory):
    if callback_data.name_cb == 'close_delete_application' and callback_data.callback == 'back':
        database['user_page'] = 1
        cur.execute('SELECT * FROM application')
        a = cur.fetchall()
        if a:
            await callback.message.edit_text(text=LEXICON_WORK['active_application'],reply_markup=active_application_kb(str(database['user_page'])))
        else:
            await callback.answer(text='На данный момент нет действующих заявок.',show_alert=True)



@router.callback_query(F.data == 'Back_materials')
async def process_back_materials_press(callback:CallbackQuery,state:FSMContext):
    db_name_materials.clear()
    await callback.message.edit_text(text=LEXICON_WORK['choose_material'],
                                     reply_markup=close_application_kb())
    await state.set_state(FSMCloseApplication.close_application)

@router.callback_query(lambda x: x.data.split('.')[0] == 'close_application',StateFilter(FSMWork.application))
async def process_close_application_press(callback:CallbackQuery,state:FSMContext):
    cur.execute(f'''SELECT text FROM notes_active_application WHERE row_id_active_application = {int(callback.data.split('.')[1])}''')
    database['db_id'] = int(callback.data.split('.')[1])
    text_notes = cur.fetchone()
    database_time['time'] = ''
    if text_notes:
        await callback.message.delete()
        notes_del = await callback.message.answer(text=f'Примечание:\n{text_notes[0]}')
        database['notes_del'] = notes_del.message_id
        await callback.message.answer(text=LEXICON_WORK['choose_material'], reply_markup=closing_application_kb(str(database['user_page'])))
    else:
        await callback.message.edit_text(text=LEXICON_WORK['choose_material'],reply_markup=closing_application_kb(str(database['user_page'])))
    await state.set_state(FSMCloseApplication.close_application)


@router.callback_query(Closing_Applicatin_Factory.filter(), StateFilter(FSMCloseApplication.close_application))
async def process_press_material(callback: CallbackQuery,
                                 callback_data: Closing_Applicatin_Factory,
                                 state: FSMContext):
    if callback_data.name_step == 'c_a':
        database_2['closing_app'] = callback_data.callback
        await callback.message.edit_text(text=LEXICON_WORK['closing_app_count'], reply_markup=press_material())
        await state.set_state(FSMCloseApplication.entry_count)
    if callback_data.name_step == 'closing_app' and callback_data.callback == 'closing':
        d = datetime.datetime.now()
        time = str(d).split('.')
        text = ''
        for name,count in  database_closing_app.items():
            stock.open_table_stock(cur, name)
            cur.execute(f'''INSERT INTO materials_expended(date,name_material,count_material)
                            VALUES ('{time[0]}','{name}',{count}) ''')
            num = int(database_6['last_num']) - count
            if num <= 0:
                num = 0
                text += f'- На складе больше не осталось {name}\n'
            if num <= 10:
                text += f'- На складе осталось {name} - {num}{database_6["unit"]}\n'
            cur.execute(
                f'INSERT INTO stock (time,unit,"{name}") VALUES ("{time[0]}","{database_6["unit"]}","{num}")')
            db.commit()
            db.commit()
        id = database['db_id']
        cur.execute(f'SELECT * FROM application WHERE rowid={id}')
        lists = cur.fetchall()
        lists.append(str(time[0]))
        cur.execute(
            f'INSERT INTO completed_application VALUES ("{str(lists[0][0])}","{lists[0][1]}","{lists[0][2]}","{lists[0][3]}","{lists[0][4]}","{str(lists[1])}")')
        cur.execute(f'DELETE FROM application WHERE rowid={id}')
        cur.execute(f'DELETE FROM notes_active_application WHERE row_id_active_application={id}')
        db.commit()
        try:
            if database['notes_del']:
                await bot.delete_message(chat_id=callback.from_user.id, message_id=database['notes_del'])
        except KeyError:
            pass
        # if database_3:
        #     for i in database_3:
        #         lists = []
        #         for k in i:
        #             if "✔️" in k and k not in lists:
        #                 lists.append(k)
        #         if lists:
        #             for p in range(len(lists)):
        #                 i[f'{lists[p].replace("✔️", "⚜️")}'] = i.pop(lists[p])
        await callback.answer(text=f'Заявка успешно закрыта.\n{text}', show_alert=True)
        await callback.message.edit_text(text=LEXICON_WORK['main_menu'], reply_markup=main_menu_kb())
        await state.set_state(FSMWork.main_menu)
        database_closing_app.clear()
    if callback_data.name_step == 'closing_app' and callback_data.callback == 'add':
        mes_del = await callback.message.edit_text(text=LEXICON_WORK['closing_add_material'])
        await state.set_state(FSMCloseApplication.entry_name)
        database_del.append(mes_del.message_id)
    if callback_data.name_step == 'closing_press' and callback_data.callback == 'backward':
        if database['user_page'] != 1:
            database['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_WORK['choose_material'],
                                          reply_markup=closing_application_kb(str(database['user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'closing_press' and callback_data.callback == 'forward':
        if database['user_page'] < database['quantity_page_stock']:
            database['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_WORK['choose_material'],
                                          reply_markup=closing_application_kb(str(database['user_page'])))
        else:
            pass
    if callback_data.name_step == 'closing_app' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['active_application'],
                                         reply_markup=active_application_kb(str(database['user_page'])))
        await state.set_state(FSMWork.application)


@router.message(EntryName(),StateFilter(FSMCloseApplication.entry_name))
async def process_entry_name(message:Message,state:FSMContext):
    lists = message.text.split(';')
    cur.execute(f''' ALTER TABLE stock ADD COLUMN "{lists[0]}" ''')
    db.commit()
    d = datetime.datetime.now()
    times = str(d).split('.')
    cur.execute(
        f'INSERT INTO stock (time,unit,"{lists[0]}") VALUES ("{times[0]}","{lists[1]}","{lists[2]}")')
    db.commit()
    mes_del = await message.answer(text=LEXICON_WORK['add_stock'])
    database_del.append(mes_del.message_id)
    database_del.append(message.message_id)
    time.sleep(2)
    await services.delete_message.delete_messages(bot,database_del,message.chat.id)
    await state.set_state(FSMCloseApplication.close_application)
    await message.answer(text=LEXICON_WORK['choose_material'],
                                  reply_markup=closing_application_kb(str(database['user_page'])))

@router.message(~EntryName(),StateFilter(FSMCloseApplication.entry_name))
async def process_entry_name(message:Message):
    mes_del = await message.answer(text=LEXICON_WORK['error_entry_name'])
    database_del.append(mes_del.message_id)
    database_del.append(message.message_id)




@router.message(lambda x: x.text.isdigit(), StateFilter(FSMCloseApplication.entry_count))
async def process_entry_count(message: Message,
                        state: FSMContext):
    database_closing_app[database_2['closing_app']] = int(message.text)
    await message.answer(text=LEXICON_WORK['choose_material'], reply_markup=closing_application_kb(str(database['user_page'])))
    await state.set_state(FSMCloseApplication.close_application)


@router.message(lambda x: not x.text.isdigit(), StateFilter(FSMCloseApplication.entry_count))
async def process_entry_count(message: Message):
    await message.answer(text=LEXICON_WORK['error_int'])




@router.callback_query(F.data == 'continue_application',StateFilter(FSMCloseApplication.other_count))
async def process_close_application_press(callback:CallbackQuery,state:FSMContext):
    name_table = str(db_name_materials[0])
    name_column = str(db_name_materials[1])
    name_materials = db_name_materials[2]
    count = db_name_materials[3]
    try:
        database_materials[name_column][name_table].append(name_materials)
        database_materials[name_column][name_table].append(count)
    except KeyError:
        database_materials[name_column] = {}
        database_materials[name_column][name_table] = []
        database_materials[name_column][name_table].append(name_materials)
        database_materials[name_column][name_table].append(count)
    db_name_materials.clear()
    await callback.message.edit_text(text=LEXICON_WORK['choose_material'],reply_markup=continue_close_application_kb())
    await state.set_state(FSMCloseApplication.close_application)


@router.callback_query(F.data == 'continue_application',StateFilter(FSMCloseApplication.close_or_continue_kb))
async def process_close_application_press(callback:CallbackQuery,state:FSMContext):
    name_table = str(db_name_materials[0])
    name_column = str(db_name_materials[1])
    count = db_name_materials[2]
    database_materials[name_column] = {}
    database_materials[name_column][name_table] = count
    await callback.message.edit_text(text=LEXICON_WORK['choose_material'],reply_markup=continue_close_application_kb())
    await state.set_state(FSMCloseApplication.close_application)
    db_name_materials.clear()

@router.callback_query(F.data == 'completed_application',StateFilter(FSMWork.application))
async def process_close_application_press(callback:CallbackQuery,state:FSMContext):
    database['user_page'] = 1
    cur.execute('SELECT * FROM completed_application')
    a = cur.fetchall()
    if a:
        await callback.message.edit_text(text=LEXICON_WORK['completed_application'],
                                         reply_markup=completed_application_kb(str(database['user_page'])))
        await state.set_state(FSMWork.completed_application)
    else:
        await callback.answer(text='На данный момент нету выполненных заявок.',show_alert=True)

@router.callback_query(F.data == 'back_completed_application',StateFilter(FSMWork.completed_application))
async def process_application_id_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_WORK['application'], reply_markup=application_kb())
    await state.set_state(FSMWork.application)
@router.callback_query(F.data == 'back_completed_application_2',StateFilter(FSMWork.completed_application))
async def process_application_id_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_WORK['completed_application'],
                                     reply_markup=completed_application_kb(str(database['user_page'])))
    await state.set_state(FSMWork.completed_application)

@router.callback_query(F.data == 'cancel_application',StateFilter(FSMWork.application))
async def process_close_application_press(callback:CallbackQuery,state:FSMContext):
    database['user_page'] = 1
    cur.execute('SELECT * FROM cancel_application')
    a = cur.fetchall()
    if a:
        await callback.message.edit_text(text=LEXICON_WORK['cancel_application'],
                                         reply_markup=cancel_application_kb(str(database['user_page'])))
        await state.set_state(FSMWork.cancel_application)
    else:
        await callback.answer(text='На данный момент нету отменённых заявок.',show_alert=True)


@router.callback_query(F.data == 'forward',StateFilter(FSMWork.cancel_application))
async def process_forward_press(callback:CallbackQuery):
    if database['user_page'] < database['quantity_page_cancel']:
        database['user_page'] += 1
        await callback.message.edit_text(text=LEXICON_WORK['cancel_application'],
                                      reply_markup=cancel_application_kb(str(database['user_page'])))
    else:
        pass

@router.callback_query(F.data == 'backward',StateFilter(FSMWork.cancel_application))
async def process_forward_press(callback:CallbackQuery):
    if database['user_page'] != 1:
        database['user_page'] -= 1
        await callback.message.edit_text(text=LEXICON_WORK['cancel_application'],
                                      reply_markup=cancel_application_kb(str(database['user_page'])))
    else:
        await callback.answer(text='Вы находитесь на первой странице',show_alert=True)

@router.callback_query(lambda x: x.data.isdigit(),StateFilter(FSMWork.cancel_application))
async def process_application_id_press(callback:CallbackQuery):
    db = sqlite3.connect('Work.sql')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM cancel_application WHERE rowid == {callback.data}')
    a = cur.fetchall()
    database['db_id'] = int(callback.data)
    text = (f'<code>Заявка от {a[0][0]};\n'
            f'Служба: {a[0][1]};\n'
            f'Здание: {a[0][2]};\n'
            f'Кабинет: {a[0][3]};\n'
            f'Текст заявки: {a[0][4]}.\n'
            f'Заявка отменена {a[0][5]};\n'
            f'По причине {a[0][6]}.</code>')
    await callback.message.edit_text(text=text,reply_markup=cancel_application_del_kb())
    cur.close()
    db.close()

@router.callback_query(CancelApplicationCallbackFactory.filter(),StateFilter(FSMWork.cancel_application))
async def procee_back_or_delete_cancel_application_press(callback:CallbackQuery,
                                                         callback_data:CancelApplicationCallbackFactory,
                                                         state:FSMContext):
    if callback_data.name_cb == 'cancel_application' and callback_data.callback == 'back':
        database['user_page'] = 1
        cur.execute('SELECT * FROM cancel_application')
        a = cur.fetchall()
        if a:
            await callback.message.edit_text(text=LEXICON_WORK['cancel_application'],
                                             reply_markup=cancel_application_kb(str(database['user_page'])))
            await state.set_state(FSMWork.cancel_application)
        else:
            await callback.answer(text='На данный момент нету отменённых заявок.',show_alert=True)
    if callback_data.name_cb == 'cancel_application' and callback_data.callback == 'delete':
        cur.execute(f'DELETE FROM cancel_application WHERE rowid == {database["db_id"]}')
        db.commit()
        await callback.answer(text='Заявка успешно удалена 🗑️',show_alert=True)
        database['user_page'] = 1
        cur.execute('SELECT * FROM cancel_application')
        a = cur.fetchall()
        if a:
            await callback.message.edit_text(text=LEXICON_WORK['cancel_application'],
                                             reply_markup=cancel_application_kb(str(database['user_page'])))
            await state.set_state(FSMWork.cancel_application)
        else:
            await callback.message.edit_text(text=LEXICON_WORK['application'], reply_markup=application_kb())
            await state.set_state(FSMWork.application)


@router.callback_query(F.data == 'back_cancel_application',StateFilter(FSMWork.cancel_application))
async def process_application_id_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.delete()


@router.callback_query(F.data == 'result_month',StateFilter(FSMWork.application))
async def process_result_month_press(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_WORK['result_month'],reply_markup=result_month_2())
    await state.set_state(FSMWork.result_month)

@router.callback_query(ResultMonthCallbackFactory.filter(),StateFilter(FSMWork.result_month))
async def process_result_month_factory(callback:CallbackQuery,
                                             callback_data:ResultMonthCallbackFactory,
                                             state:FSMContext):
    if callback_data.name_menu == 'result_month' and callback_data.name_next_step != 'back':
        if result_month(callback_data.name_next_step):
            await callback.message.edit_text(text=f'<b>Результаты за {callback_data.name_next_step}:</b>\n{result_month(callback_data.name_next_step)}',
                                             reply_markup=resul_month_2_kb_month())
            database_4['month'] = callback_data.name_next_step
            await state.set_state(FSMWork.result_month_press)
        else:
            try:
                await callback.answer(text='В этом месяце работы не выполнялись',show_alert=True)
                await callback.message.edit_text(text=LEXICON_WORK['result_month'], reply_markup=result_month_2())
                await state.set_state(FSMWork.result_month)
            except TelegramBadRequest:
                pass


    if callback_data.name_menu == 'result_month' and callback_data.name_next_step == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['application'], reply_markup=application_kb())
        await state.set_state(FSMWork.application)

@router.callback_query(ResultMonthCallbackFactory.filter(),StateFilter(FSMWork.result_month_press))
async def process_result_month_factory_press(callback:CallbackQuery,
                                             callback_data:ResultMonthCallbackFactory,
                                             state:FSMContext):
    if callback_data.name_menu == 'result_month_press' and callback_data.name_next_step == 'detail_information':
        await callback.message.edit_text(text=f'<b>Детальная информация за {database_4["month"]}:</b>\n{detail_result_month(database_4["month"])}',
                                         reply_markup=result_month_2_kb_month_back())
    if callback_data.name_menu == 'result_month_press' and callback_data.name_next_step == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['result_month'], reply_markup=result_month_2())
        await state.set_state(FSMWork.result_month)
    if callback_data.name_menu == 'result_month_detail_information' and callback_data.name_next_step == 'back':
        await callback.message.edit_text(
            text=f'<b>Результаты за {database_4["month"]}:</b>\n{result_month(database_4["month"])}',
            reply_markup=resul_month_2_kb_month())
        await state.set_state(FSMWork.result_month_press)




@router.callback_query(F.data == 'stock',StateFilter(FSMWork.main_menu))
async def process_stock_press(callback:CallbackQuery,state:FSMContext):
    database['user_page'] = 1
    database['quantity_page_stock'] = 1
    await callback.message.edit_text(text=LEXICON_WORK['stock'],reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
    await state.set_state(FSMWork_stock.main_menu)


@router.callback_query(StockCallbackFactory.filter(),StateFilter(FSMWork_stock.main_menu))
async def process_press_factory_stock(callback:CallbackQuery,
                                             callback_data:StockCallbackFactory,
                                             state:FSMContext):
    if callback_data.name_step == 'stock_press' and callback_data.callback == 'add':
        await callback.message.edit_text(text=LEXICON_WORK['stock_add_column'])
        await state.set_state(FSMWork_stock.add_column)
    if callback_data.name_step == 'stock_press' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['main_menu'], reply_markup=main_menu_kb())
        await state.set_state(FSMWork.main_menu)
    if callback_data.name_step == 'stock_press' and callback_data.callback == 'backward':
        if database['user_page'] != 1:
            database['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_WORK['stock'],
                                             reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'stock_press' and callback_data.callback == 'forward':
        if database['user_page'] < database['quantity_page_stock']:
            database['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_WORK['stock'],
                                             reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
        else:
            pass

    if callback_data.name_step == 'add_del' and callback_data.callback == 'add':
        cur.execute(f''' ALTER TABLE stock ADD COLUMN "{database_5['column']}" ''')
        db.commit()
        d = datetime.datetime.now()
        time = str(d).split('.')
        cur.execute(f'INSERT INTO stock (time,unit,"{database_5["column"]}") VALUES ("{time[0]}","{database_5["unit"]}","{database_5["count"]}")')
        db.commit()
        await callback.answer(text=LEXICON_WORK['add_stock'],show_alert=True)
        await callback.message.edit_text(text=LEXICON_WORK['stock'], reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
        await state.set_state(FSMWork_stock.main_menu)
        database_5.clear()

    if callback_data.name_step == 'add_del' and callback_data.callback == 'cancel':
        database_5.clear()
        await callback.answer(text=LEXICON_WORK['cancel_stock'],show_alert=True)
        await callback.message.edit_text(text=LEXICON_WORK['stock'], reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
        await state.set_state(FSMWork_stock.main_menu)
    if callback_data.name_step == 's_p' and callback_data.callback != 'add' and callback_data.callback != 'back'\
            and callback_data.callback != 'forward' and callback_data.callback != 'backward':
        text = stock.open_table_stock(cur,callback_data.callback)
        database_str['callback'] = callback_data.callback
        await callback.message.edit_text(text=f'🔹 {callback_data.callback}:\n{text}',reply_markup=stock_kb.stock_kb_press())
    if callback_data.name_step == 'stock_press_press' and callback_data.callback == 'add':
        await callback.message.edit_text(text=f'<code>Введите какое кол-во {database_str["callback"]} хотите добавить.</code>')
        await state.set_state(FSMWork_stock.press_add_count)
    if callback_data.name_step == 'stock_press_press' and callback_data.callback == 'take_away':
        await callback.message.edit_text(text=f'<code>Введите какое кол-во {database_str["callback"]} хотите отнять.</code>')
        await state.set_state(FSMWork_stock.press_take_away_count)
    if callback_data.name_step == 'stock_press_press' and callback_data.callback == 'delete':
        cur.execute(f'ALTER TABLE stock DROP COLUMN "{database_str["callback"]}"')
        db.commit()
        database['user_page'] = 1
        database['quantity_page_stock'] = 1
        await callback.answer(text=LEXICON_WORK['delete_stock'],show_alert=True)
        await callback.message.edit_text(text=LEXICON_WORK['stock'],
                                         reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
        await state.set_state(FSMWork_stock.main_menu)
    if callback_data.name_step == 'stock_press_press' and callback_data.callback == 'back':
        database['user_page'] = 1
        await callback.message.edit_text(text=LEXICON_WORK['stock'],
                                         reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
        await state.set_state(FSMWork_stock.main_menu)



@router.message(lambda x: x.text.isdigit(),StateFilter(FSMWork_stock.press_add_count))
async def process_stock_press_add_count(message:Message,state:FSMContext):
    num = int(database_6['last_num']) + int(message.text)
    d = datetime.datetime.now()
    time = str(d).split('.')
    cur.execute(f'INSERT INTO stock (time,unit,"{database_str["callback"]}") VALUES ("{time[0]}","{database_6["unit"]}","{num}")')
    db.commit()
    await message.answer(text=LEXICON_WORK['add_success'])
    await message.answer(text=LEXICON_WORK['stock'],
                                     reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
    await state.set_state(FSMWork_stock.main_menu)
@router.message(lambda x: not x.text.isdigit(),StateFilter(FSMWork_stock.press_add_count))
async def process_stock_press_add_count_err(message:Message,state:FSMContext):
    await message.answer(text='Вы ввели данные некорректно,используйте только число. Введите ещё раз.')
@router.message(lambda x: x.text.isdigit(),StateFilter(FSMWork_stock.press_take_away_count))
async def process_stock_press_take_away_count(message:Message,state:FSMContext):
    num = int(database_6['last_num']) - int(message.text)
    if num <= 0:
        await message.answer(text=f'На складе больше не осталось {database_str["callback"]}')
    d = datetime.datetime.now()
    time = str(d).split('.')
    cur.execute(f'INSERT INTO stock (time,unit,"{database_str["callback"]}") VALUES ("{time[0]}","{database_6["unit"]}","{num}")')
    db.commit()
    await message.answer(text=LEXICON_WORK['take_away_success'])
    await message.answer(text=LEXICON_WORK['stock'],
                                     reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
    await state.set_state(FSMWork_stock.main_menu)
@router.message(lambda x: not x.text.isdigit(),StateFilter(FSMWork_stock.press_take_away_count))
async def process_stock_press_take_away_count_err(message:Message,state:FSMContext):
    await message.answer(text='Вы ввели данные некорректно,используйте только число. Введите ещё раз.')

@router.message(lambda x: x.text.isalpha(),StateFilter(FSMWork_stock.add_unit))
async def process_stock_add_unit(message:Message,state:FSMContext):
    database_5['unit'] = message.text
    await message.answer(text=LEXICON_WORK['stock_add_count'])
    await state.set_state(FSMWork_stock.add_count)
@router.message(lambda x: not x.text.isalpha(),StateFilter(FSMWork_stock.add_unit))
async def process_stock_add_unit_err(message:Message,state:FSMContext):
    await message.answer(text='Вы ввели данные некорректно,используйте ед.измерения (Например: шт, м и т.д.). Введите ещё раз.')
@router.message(StateFilter(FSMWork_stock.add_column))
async def process_send_column_stock(message:Message,state:FSMContext):
        cur.execute('PRAGMA table_info("stock")')
        column_names = [i[1].lower() for i in cur.fetchall()]
        if message.text.lower() in column_names:
            await message.answer(text=LEXICON_WORK['sqlite3.OperationalError'])
            await message.answer(text=LEXICON_WORK['stock'],
                                 reply_markup=stock_kb.stock_application_kb(str(database['user_page'])))
            await state.set_state(FSMWork_stock.main_menu)
            database_5.clear()
        else:
            if len(message.text) > 30:
                await message.answer(text=LEXICON_WORK['error_len_32'])
            else:
                database_5['column'] = message.text
                await message.answer(text=LEXICON_WORK['stock_add_unit'])
                await state.set_state(FSMWork_stock.add_unit)



@router.message(lambda x: x.text.isdigit(),StateFilter(FSMWork_stock.add_count))
async def process_add_del_stock(message:Message,state:FSMContext):
    database_5['count'] = message.text
    await message.answer(text=LEXICON_WORK['add_del_stock'],reply_markup=add_del_stock_kb())
    await state.set_state(FSMWork_stock.main_menu)
@router.message(lambda x: not x.text.isdigit(),StateFilter(FSMWork_stock.add_count))
async def process_add_del_stock_err(message:Message,state:FSMContext):
    await message.answer(text='Вы ввели данные некорректно,используйте только число. Введите ещё раз.')


@router.callback_query(F.data == 'purchase',StateFilter(FSMWork.main_menu))
async def process_purchase_press(callback:CallbackQuery,state:FSMContext):
    database['user_page'] = 1
    await callback.message.edit_text(text=LEXICON_WORK['purchase'],reply_markup=purchase_kb.purchase_kb())
    await state.set_state(FSMWork_purchase.main_menu)


@router.callback_query(purchase_kb.PurchaseCallbackFactory.filter(),StateFilter(FSMWork_purchase.main_menu))
async def process_press_factory_purchase(callback:CallbackQuery,
                                             callback_data:purchase_kb.PurchaseCallbackFactory,
                                             state:FSMContext):
    if callback_data.name_step == 'p_main_menu' and callback_data.callback == 'application':
        await callback.message.edit_text(text=LEXICON_WORK['p_application'],reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
    if callback_data.name_step == 'p_materials' and callback_data.callback == 'add':
        await callback.message.edit_text(text=LEXICON_WORK['p_materials_add'])
        await state.set_state(FSMWork_purchase.materials_add)
    if callback_data.name_step == 'p_pagination_mat' and callback_data.callback == 'backward':
        if database['user_page'] != 1:
            database['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_WORK['p_materials_add'],
                                             reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'p_pagination_mat' and callback_data.callback == 'forward':
        if database['user_page'] < database['purchase_page_application']:
            database['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_WORK['p_materials_add'],
                                             reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
        else:
            pass
    if callback_data.name_step == 'activate' and callback_data.callback.isdigit():
        cur.execute(f'SELECT purchase_application FROM purchase WHERE rowid={callback_data.callback}')
        b = cur.fetchone()
        if '✅' not in b[0]:
            cur.execute(f'UPDATE purchase SET purchase_application = "{b[0]} ✅"  '
                        f'WHERE rowid={callback_data.callback}')
            db.commit()
        elif '✅' in b[0]:
            cur.execute(f'UPDATE purchase SET purchase_application = "{b[0].replace("✅","")}"  '
                        f'WHERE rowid={callback_data.callback}')
            db.commit()
        await callback.message.edit_text(text=LEXICON_WORK['p_application'],reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
    if callback_data.name_step == 'p_materials' and callback_data.callback == 'del':
        cur.execute('SELECT purchase_application FROM purchase')
        a = cur.fetchall()
        try:
            if a:
                await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],reply_markup=purchase_kb.purchase_materials_kb_delete(str(database['user_page'])))
            else:
                await callback.answer(text=LEXICON_WORK['error_del'],show_alert=True)
                await callback.message.edit_text(text=LEXICON_WORK['p_application'],
                                                 reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
        except TelegramBadRequest:
            await callback.answer()
    if callback_data.name_step == 'p_materials_del' and callback_data.callback.isdigit():
        cur.execute(f'DELETE FROM purchase WHERE purchase_application IN (SELECT purchase_application FROM purchase WHERE rowid={callback_data.callback})')
        db.commit()
        cur.execute('SELECT purchase_application FROM purchase')
        a = cur.fetchall()
        try:
            if a:
                await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],reply_markup=purchase_kb.purchase_materials_kb_delete(str(database['user_page'])))
            else:
                await callback.answer(text=LEXICON_WORK['error_del'],show_alert=True)
                await callback.message.edit_text(text=LEXICON_WORK['p_application'],
                                                 reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
        except TelegramBadRequest:
            await callback.answer()
    if callback_data.name_step == 'p_materials_del' and callback_data.callback == 'all_delete':
        cur.execute(f'DELETE FROM purchase WHERE purchase_application IN (SELECT purchase_application FROM purchase)')
        db.commit()
        await callback.answer(text=LEXICON_WORK['error_del'], show_alert=True)
        await callback.message.edit_text(text=LEXICON_WORK['p_application'],
                                         reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
    if callback_data.name_step == 'p_pagination_mat_del' and callback_data.callback == 'backward':
        if database['user_page'] != 1:
            database['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],
                                             reply_markup=purchase_kb.purchase_materials_kb_delete(str(database['user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'p_pagination_mat_del' and callback_data.callback == 'forward':
        if database['user_page'] < database['purchase_page']:
            database['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],
                                             reply_markup=purchase_kb.purchase_materials_kb_delete(str(database['user_page'])))
        else:
            pass
    if callback_data.name_step == 'p_materials_del' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['p_application'],reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
    if callback_data.name_step == 'p_materials' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['purchase'], reply_markup=purchase_kb.purchase_kb())
    if callback_data.name_step == 'p_main_menu' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['main_menu'], reply_markup=main_menu_kb())
        await state.set_state(FSMWork.main_menu)


    if callback_data.name_step == 'p_main_menu' and callback_data.callback == 'p_to_50b':
        await callback.message.edit_text(text=LEXICON_WORK['p_to_50b'],reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
    if callback_data.name_step == 'p_to_50b' and callback_data.callback == 'add':
        await callback.message.edit_text(text=LEXICON_WORK['p_to_50b_add'])
        await state.set_state(FSMWork_purchase.to_50b_add)
    if callback_data.name_step == 'p_pag_to_50b' and callback_data.callback == 'backward':
        if database['user_page'] != 1:
            database['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_WORK['p_to_50b'],
                                             reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'p_pag_to_50b' and callback_data.callback == 'forward':
        if database['user_page'] < database['purchase_page_to_50b']:
            database['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_WORK['p_to_50b'],
                                             reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
        else:
            pass
    if callback_data.name_step == 'activate_to_50b' and callback_data.callback.isdigit():
        cur.execute(f'SELECT p_to_50b FROM purchase WHERE rowid={callback_data.callback}')
        b = cur.fetchone()
        if '✅' not in b[0]:
            cur.execute(f'UPDATE purchase SET p_to_50b = "{b[0]} ✅"  '
                        f'WHERE rowid={callback_data.callback}')
            db.commit()
        elif '✅' in b[0]:
            cur.execute(f'UPDATE purchase SET p_to_50b = "{b[0].replace("✅","")}"  '
                        f'WHERE rowid={callback_data.callback}')
            db.commit()
        await callback.message.edit_text(text=LEXICON_WORK['p_to_50b'],reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
    if callback_data.name_step == 'p_to_50b' and callback_data.callback == 'del':
        cur.execute('SELECT p_to_50b FROM purchase')
        a = cur.fetchall()
        try:
            if a:
                await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],reply_markup=purchase_kb.purchase_to_50b_kb_delete(str(database['user_page'])))
            else:
                await callback.answer(text=LEXICON_WORK['error_del'],show_alert=True)
                await callback.message.edit_text(text=LEXICON_WORK['p_to_50b'],
                                                 reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
        except TelegramBadRequest:
            await callback.answer()
    if callback_data.name_step == 'p_to_50b_del' and callback_data.callback.isdigit():
        cur.execute(f'DELETE FROM purchase WHERE p_to_50b IN (SELECT p_to_50b FROM purchase WHERE rowid={callback_data.callback})')
        db.commit()
        cur.execute('SELECT p_to_50b FROM purchase')
        a = cur.fetchall()
        try:
            if a:
                await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],reply_markup=purchase_kb.purchase_to_50b_kb_delete(str(database['user_page'])))
            else:
                await callback.answer(text=LEXICON_WORK['error_del'],show_alert=True)
                await callback.message.edit_text(text=LEXICON_WORK['p_to_50b'],
                                                 reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
        except TelegramBadRequest:
            await callback.answer()
    if callback_data.name_step == 'p_to_50b_del' and callback_data.callback == 'all_delete':
        cur.execute(f'DELETE FROM purchase WHERE p_to_50b IN (SELECT p_to_50b FROM purchase)')
        db.commit()
        await callback.answer(text=LEXICON_WORK['error_del'], show_alert=True)
        await callback.message.edit_text(text=LEXICON_WORK['p_to_50b'],
                                         reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
    if callback_data.name_step == 'p_pag_to_50b_del' and callback_data.callback == 'backward':
        if database['user_page'] != 1:
            database['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],
                                             reply_markup=purchase_kb.purchase_to_50b_kb_delete(str(database['user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'p_pag_to_50b_del' and callback_data.callback == 'forward':
        if database['user_page'] < database['purchase_page']:
            database['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],
                                             reply_markup=purchase_kb.purchase_to_50b_kb_delete(str(database['user_page'])))
        else:
            pass
    if callback_data.name_step == 'p_to_50b_del' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['p_to_50b'],reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
        database["user_page"] = 1
    if callback_data.name_step == 'p_to_50b' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['purchase'], reply_markup=purchase_kb.purchase_kb())
        database["user_page"] = 1




    if callback_data.name_step == 'p_main_menu' and callback_data.callback == 'p_over_50b':
        await callback.message.edit_text(text=LEXICON_WORK['p_over_50b'],
                                         reply_markup=purchase_kb.purchase_materials_kb_over_50b(
                                             str(database['user_page'])))
    if callback_data.name_step == 'p_over_50b' and callback_data.callback == 'add':
        await callback.message.edit_text(text=LEXICON_WORK['p_over_50b_add'])
        await state.set_state(FSMWork_purchase.over_50b_add)
    if callback_data.name_step == 'p_pag_over_50b' and callback_data.callback == 'backward':
        if database['user_page'] != 1:
            database['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_WORK['p_over_50b'],
                                             reply_markup=purchase_kb.purchase_materials_kb_over_50b(
                                                 str(database['user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'p_pag_over_50b' and callback_data.callback == 'forward':
        if database['user_page'] < database['purchase_page_over_50b']:
            database['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_WORK['p_over_50b'],
                                             reply_markup=purchase_kb.purchase_materials_kb_over_50b(
                                                 str(database['user_page'])))
        else:
            pass
    if callback_data.name_step == 'activate_over_50b' and callback_data.callback.isdigit():
        cur.execute(f'SELECT p_over_50b FROM purchase WHERE rowid={callback_data.callback}')
        b = cur.fetchone()
        if '✅' not in b[0]:
            cur.execute(f'UPDATE purchase SET p_over_50b = "{b[0]} ✅"  '
                        f'WHERE rowid={callback_data.callback}')
            db.commit()
        elif '✅' in b[0]:
            cur.execute(f'UPDATE purchase SET p_over_50b = "{b[0].replace("✅", "")}"  '
                        f'WHERE rowid={callback_data.callback}')
            db.commit()
        await callback.message.edit_text(text=LEXICON_WORK['p_over_50b'],
                                         reply_markup=purchase_kb.purchase_materials_kb_over_50b(
                                             str(database['user_page'])))
    if callback_data.name_step == 'p_over_50b' and callback_data.callback == 'del':
        cur.execute('SELECT p_over_50b FROM purchase')
        a = cur.fetchall()
        try:
            if a:
                await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],
                                                 reply_markup=purchase_kb.purchase_over_50b_kb_delete(
                                                     str(database['user_page'])))
            else:
                await callback.answer(text=LEXICON_WORK['error_del'], show_alert=True)
                await callback.message.edit_text(text=LEXICON_WORK['p_over_50b'],
                                                 reply_markup=purchase_kb.purchase_materials_kb_over_50b(
                                                     str(database['user_page'])))
        except TelegramBadRequest:
            await callback.answer()
    if callback_data.name_step == 'p_over_50b_del' and callback_data.callback.isdigit():
        cur.execute(
            f'DELETE FROM purchase WHERE p_over_50b IN (SELECT p_over_50b FROM purchase WHERE rowid={callback_data.callback})')
        db.commit()
        cur.execute('SELECT p_over_50b FROM purchase')
        a = cur.fetchall()
        try:
            if a:
                await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],
                                                 reply_markup=purchase_kb.purchase_over_50b_kb_delete(
                                                     str(database['user_page'])))
            else:
                await callback.answer(text=LEXICON_WORK['error_del'], show_alert=True)
                await callback.message.edit_text(text=LEXICON_WORK['p_over_50b'],
                                                 reply_markup=purchase_kb.purchase_materials_kb_over_50b(
                                                     str(database['user_page'])))
        except TelegramBadRequest:
            await callback.answer()
    if callback_data.name_step == 'p_over_50b_del' and callback_data.callback == 'all_delete':
        cur.execute(f'DELETE FROM purchase WHERE p_over_50b IN (SELECT p_over_50b FROM purchase)')
        db.commit()
        await callback.answer(text=LEXICON_WORK['error_del'], show_alert=True)
        await callback.message.edit_text(text=LEXICON_WORK['p_over_50b'],
                                         reply_markup=purchase_kb.purchase_materials_kb_over_50b(
                                             str(database['user_page'])))
    if callback_data.name_step == 'p_pag_over_50b_del' and callback_data.callback == 'backward':
        if database['user_page'] != 1:
            database['user_page'] -= 1
            await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],
                                             reply_markup=purchase_kb.purchase_over_50b_kb_delete(
                                                 str(database['user_page'])))
        else:
            await callback.answer(text='Вы находитесь на первой странице', show_alert=True)
    if callback_data.name_step == 'p_pag_over_50b_del' and callback_data.callback == 'forward':
        if database['user_page'] < database['purchase_page']:
            database['user_page'] += 1
            await callback.message.edit_text(text=LEXICON_WORK['delete_materials'],
                                             reply_markup=purchase_kb.purchase_over_50b_kb_delete(
                                                 str(database['user_page'])))
        else:
            pass
    if callback_data.name_step == 'p_over_50b_del' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['p_over_50b'],
                                         reply_markup=purchase_kb.purchase_materials_kb_over_50b(
                                             str(database['user_page'])))
        database["user_page"] = 1
    if callback_data.name_step == 'p_over_50b' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_WORK['purchase'], reply_markup=purchase_kb.purchase_kb())
        database["user_page"] = 1







@router.message(StateFilter(FSMWork_purchase.materials_add))
async def process_send_materials_purchase(message:Message,state:FSMContext):
    if message.text:
        if len(message.text) > 35:
            await message.answer(text=LEXICON_WORK['error_len_35'])
        else:
            cur.execute(f'''SELECT * FROM purchase
                            WHERE purchase_application LIKE ('{message.text.capitalize()}')''')
            check = cur.fetchall()
            if check:
                await message.answer(text=LEXICON_WORK['add_err'])
                await message.answer(text=LEXICON_WORK['p_application'],
                                     reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
                await state.set_state(FSMWork_purchase.main_menu)
            else:
                d = datetime.datetime.now()
                time = str(d).split('.')
                cur.execute(f'INSERT INTO purchase (time,purchase_application) '
                            f'VALUES ("{time[0]}","{message.text.capitalize()}")')
                db.commit()
                await message.answer(text=LEXICON_WORK['add_stock'])
                await message.answer(text=LEXICON_WORK['p_application'],
                                                 reply_markup=purchase_kb.purchase_materials_kb(str(database['user_page'])))
                await state.set_state(FSMWork_purchase.main_menu)

    else:
        await message.answer(text=LEXICON_WORK['error_len_35'])

@router.message(StateFilter(FSMWork_purchase.to_50b_add))
async def process_send_to_50b_purchase(message: Message, state: FSMContext):
    if message.text:
        if len(message.text) > 35:
            await message.answer(text=LEXICON_WORK['error_len_35'])
        else:
            cur.execute(f'''SELECT * FROM purchase
                                        WHERE p_to_50b LIKE ('{message.text.capitalize()}')''')
            check = cur.fetchall()
            if check:
                await message.answer(text=LEXICON_WORK['add_err'])
                await message.answer(text=LEXICON_WORK['p_to_50b'],
                                     reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
                await state.set_state(FSMWork_purchase.main_menu)
            else:
                d = datetime.datetime.now()
                time = str(d).split('.')
                cur.execute(f'INSERT INTO purchase (time,p_to_50b) '
                            f'VALUES ("{time[0]}","{message.text.capitalize()}")')
                db.commit()
                await message.answer(text=LEXICON_WORK['add_stock'])
                await message.answer(text=LEXICON_WORK['p_to_50b'],reply_markup=purchase_kb.purchase_materials_kb_to_50b(str(database['user_page'])))
                await state.set_state(FSMWork_purchase.main_menu)
    else:
        await message.answer(text=LEXICON_WORK['error_len_35'])

@router.message(StateFilter(FSMWork_purchase.over_50b_add))
async def process_send_over_50b_purchase(message: Message, state: FSMContext):
    if message.text:
        if len(message.text) > 35:
            await message.answer(text=LEXICON_WORK['error_len_35'])
        else:
            cur.execute(f'''SELECT * FROM purchase
                                                    WHERE p_to_50b LIKE ('{message.text.capitalize()}')''')
            check = cur.fetchall()
            if check:
                await message.answer(text=LEXICON_WORK['add_err'])
                await message.answer(text=LEXICON_WORK['p_over_50b'],
                                     reply_markup=purchase_kb.purchase_materials_kb_over_50b(str(database['user_page'])))
                await state.set_state(FSMWork_purchase.main_menu)
            else:
                d = datetime.datetime.now()
                time = str(d).split('.')
                cur.execute(f'INSERT INTO purchase (time,p_over_50b) '
                            f'VALUES ("{time[0]}","{message.text}")')
                db.commit()
                await message.answer(text=LEXICON_WORK['add_stock'])
                await message.answer(text=LEXICON_WORK['p_over_50b'],
                                     reply_markup=purchase_kb.purchase_materials_kb_over_50b(str(database['user_page'])))
                await state.set_state(FSMWork_purchase.main_menu)
    else:
        await message.answer(text=LEXICON_WORK['error_len_35'])



@router.callback_query(F.data == 'library',StateFilter(FSMWork.main_menu))
async def process_library_command(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_WORK['library_main_menu'],reply_markup=library_kb.library_main_menu_kb())
    await state.set_state(FSMWork_library.main_menu)

@router.callback_query(library_kb.LibraryCallbackFactory.filter(),StateFilter(FSMWork_library.main_menu))
async def process_callback_factory_library(callback:CallbackQuery,
                                           callback_data:library_kb.LibraryCallbackFactory,
                                           state:FSMContext):
    if callback_data.name_step == 'library_main_menu' and callback_data.callback == 'pcz525':
        file = FSInputFile('other_file/pcz_525.pdf')
        await callback.message.delete()
        message_del = await callback.message.answer_document(file)
        database_del.append(message_del.message_id)
        await callback.message.answer(text=LEXICON_WORK['library_main_menu'],
                                         reply_markup=library_kb.library_main_menu_kb())
        await state.set_state(FSMWork_library.main_menu)
    if callback_data.name_step == 'library_main_menu' and callback_data.callback == 'tkp_290':
        file = FSInputFile('other_file/TKP_290.pdf')
        await callback.message.delete()
        message_del = await callback.message.answer_document(file)
        database_del.append(message_del.message_id)
        await callback.message.answer(text=LEXICON_WORK['library_main_menu'],
                                         reply_markup=library_kb.library_main_menu_kb())
        await state.set_state(FSMWork_library.main_menu)
    if callback_data.name_step == 'library_main_menu' and callback_data.callback == 'pcz525-1':
        file = FSInputFile('other_file/pcz_525-1.pdf')
        await callback.message.delete()
        message_del = await callback.message.answer_document(file)
        database_del.append(message_del.message_id)
        await callback.message.answer(text=LEXICON_WORK['library_main_menu'],
                                         reply_markup=library_kb.library_main_menu_kb())
        await state.set_state(FSMWork_library.main_menu)
    if callback_data.name_step == 'library_main_menu' and callback_data.callback == 'back':
        for i in database_del:
            if i:
                await bot.delete_message(chat_id=callback.from_user.id,message_id=i)
        await callback.message.edit_text(text=LEXICON_WORK['main_menu'], reply_markup=main_menu_kb())
        await state.set_state(FSMWork.main_menu)
        database_del.clear()

@router.callback_query(F.data == 'phonebook',StateFilter(FSMWork.main_menu))
async def process_library_command(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text=LEXICON_PHONEBOOK_SHORT['short_list'],reply_markup=phonebook_kb.kb_phonebook())
    await state.set_state(FSMWork_phonebook.main_menu)

@router.callback_query(phonebook_kb.PhonebookCallbackFactory.filter(),StateFilter(FSMWork_phonebook.main_menu))
async def process_phonebook_command(callback:CallbackQuery,
                                    callback_data:phonebook_kb.PhonebookCallbackFactory,
                                    state:FSMContext):
    if callback_data.name_step == 'main_menu' and callback_data.callback == 'phonebook_pdf':
        file = FSInputFile('''other_file/Телефонный справочник МЭС.pdf''')
        await callback.message.delete()
        message_del = await callback.message.answer_document(file)
        await callback.message.answer(text=LEXICON_PHONEBOOK_SHORT['short_list'],
                                         reply_markup=phonebook_kb.kb_phonebook())
        database_del.append(message_del.message_id)
    if callback_data.name_step == 'main_menu' and callback_data.callback == 'back':
        for i in database_del:
            if i:
                await bot.delete_message(chat_id=callback.from_user.id,message_id=i)
        await callback.message.edit_text(text=LEXICON_WORK['main_menu'], reply_markup=main_menu_kb())
        await state.set_state(FSMWork.main_menu)
        database_del.clear()


@router.message(Command(commands='en_ru_dict_simulator'),StateFilter(FSMWork.main_menu))
async def process_english_dict_simulator_commands(message:Message,state:FSMContext):
    database['count_incorr_answer'] = 3
    english = english_dict.EnglishDict()
    english.create_english_dict()
    english.create_lists_questions()
    database_english_list.extend(english.list_questions.copy())
    database_english_dict.update(english.dicts.copy())
    database_english_answer.append(database_english_list[-1])
    database_del.append(message.message_id)
    mes_del = await message.answer(text=f'{database_english_list[-1]}',reply_markup=None)
    database_del.append(mes_del.message_id)
    await state.set_state(FSMWork.english_dict_simulator)

@router.message(lambda x: isinstance(x.text,str), StateFilter(FSMWork.english_dict_simulator))
async def english_answer(message:Message):
    database_del.append(message.message_id)
    if message.text.lower() in database_english_dict[database_english_answer[-1]].strip().split(','):
        database['count_incorr_answer'] = 3
        database_english_list.pop()
        database_english_answer.clear()
        database_english_answer.append(database_english_list[-1])
        mes_del = await message.answer(text=f'{database_english_list[-1]}',reply_markup=None)
        database_del.append(mes_del.message_id)
    else:
        database['count_incorr_answer'] -= 1
        if database['count_incorr_answer'] > 0:
            mes_del_1 = await message.answer(text=LEXICON_WORK['english_dict_not_correct_answer'])
            database_del.append(mes_del_1.message_id)
        else:
            database['count_incorr_answer'] = 3
            mes_del_2 = await message.answer(text=database_english_dict[database_english_answer[-1]])
            database_del.append(mes_del_2.message_id)


@router.message(Command(commands='ru_en_dict_simulator'),StateFilter(FSMWork.main_menu))
async def process_ru_en_dict_simulator_commands(message:Message,state:FSMContext):
    database['count_incorr_answer'] = 3
    english = english_dict.Russian_Eng_Dict()
    english.create_english_dict()
    english.create_lists_questions()
    database_english_list.extend(english.list_questions.copy())
    database_english_dict.update(english.dicts.copy())
    database_english_answer.append(database_english_list[-1])
    database_del.append(message.message_id)
    mes_del = await message.answer(text=f'{database_english_list[-1]}',reply_markup=None)
    database_del.append(mes_del.message_id)
    await state.set_state(FSMWork.ru_en_dict_simulator)

@router.message(lambda x: isinstance(x.text,str), StateFilter(FSMWork.ru_en_dict_simulator))
async def ru_en_answer(message:Message):
    database_del.append(message.message_id)
    if message.text.lower() in database_english_dict[database_english_answer[-1]].strip().split(','):
        database['count_incorr_answer'] = 3
        database_english_list.pop()
        database_english_answer.clear()
        database_english_answer.append(database_english_list[-1])
        mes_del = await message.answer(text=f'{database_english_list[-1]}',reply_markup=None)
        database_del.append(mes_del.message_id)
    else:
        database['count_incorr_answer'] -= 1
        if database['count_incorr_answer'] > 0:
            mes_del_1 = await message.answer(text=LEXICON_WORK['english_dict_not_correct_answer'])
            database_del.append(mes_del_1.message_id)
        else:
            database['count_incorr_answer'] = 3
            mes_del_2 = await message.answer(text=database_english_dict[database_english_answer[-1]])
            database_del.append(mes_del_2.message_id)

@router.message(Command(commands='english_dict'),StateFilter(FSMWork.main_menu))
async def process_english_dict_command(message:Message,state:FSMContext):
    with open('other_file/english_dict.txt','r') as file:
        text = file.read()
    lists_text = english_dict.check_len_dict(text)
    for new_text in lists_text:
        mes_del_3 = await message.answer(text=new_text)
        database_del.append(mes_del_3.message_id)
    await state.set_state(FSMWork.english_dict)

@router.message(StateFilter(FSMWork.english_dict))
async def process_translate_ru_en(message:Message):
    translate = google_translate.Translate(message.text)
    translated_text = translate.translate_text()
    google_translate.Translate.edit_text(translated_text.text,message.text)
    mes_del = await message.answer(text=translated_text.text,reply_markup=google_translate.create_kb_english())
    t.sleep(5)
    await bot.delete_message(chat_id=message.chat.id,message_id=mes_del.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@router.callback_query(F.data == 'english_kb',StateFilter(FSMWork.english_dict))
async def process_add_word_dict(callback:CallbackQuery):
    translate = google_translate.Translate('...')
    translate.add_new_word_dict()
    await callback.answer('Message added successfully')


@router.message(Command(commands='add_schedule'),StateFilter(FSMWork.main_menu))
async def process_schedule_command(message:Message,state:FSMContext):
    mes_del = await message.answer(text='Введите на какую дату и время установить напоминание(Например: 01.01.21 08:00:00')
    database_del.append(mes_del.message_id)
    await state.set_state(FSMWork_schedule.send_date)

@router.message(StateFilter(FSMWork_schedule.send_date))
async def schedule_send_date(message:Message,state:FSMContext):
    try:
        date = datetime.datetime.strptime(message.text,'%d.%m.%y %H:%M')
        database_str['time_schedule'] = message.text
        mes_del = await message.answer(text='Введите текст напоминания')
        database_del.append(mes_del.message_id)
        await state.set_state(FSMWork_schedule.send_text)
    except ValueError:
        mes_del = await message.answer(text='Дата должны быть в формате d.m.y H:M(01.01.21 08:00)')
        database_del.append(mes_del.message_id)
    database_del.append(message.message_id)


@router.message(StateFilter(FSMWork_schedule.send_text))
async def schedule_send_text(message:Message,state:FSMContext):
    date = datetime.datetime.strptime(database_str['time_schedule'], '%d.%m.%y %H:%M')
    sheduler = services.schedule.ClassScheduler(date,message.text,bot,admin_id[0])
    database_del.append(message.message_id)
    await sheduler.schedule()

@router.callback_query(F.data == 'schedule_kb')
async def process_schedule_kb_press(callback:CallbackQuery):
    await callback.message.delete()


@router.message(StateFilter(default_state))
async def echo_send(message:Message):
    await message.answer(text='❔ <b>Используйте команду /start для начала работы.</b>')

@router.message(~StateFilter(default_state,FSMWork.english_dict_simulator))
async def echo_send(message:Message):
    await message.delete()