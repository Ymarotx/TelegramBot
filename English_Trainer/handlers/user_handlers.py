import asyncio
import time

from aiogram import Router, F,Bot
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from aiogram.exceptions import TelegramBadRequest

from database.database import create_tables,async_session
from database.models import Table_New_Word,Table_Learned_Word,Table_Users
from lexicon.lexicon import LEXICON_MAIN
from keyboards import user_keyboards
from FSM.fsm import FSMMainMenu,FSMSimulator
from services.reminder import Reminder
from services.dict import Dict
from services import translator
from services.simulator import Simulator
from database.redis_db import Redis
from aiogram.fsm.state import default_state
from services.scheduler import Scheduler

router: Router = Router()
@router.message(CommandStart(),StateFilter(default_state))
async def command_start(message:Message,state:FSMContext):
    await create_tables()
    try:
        async with async_session() as session:
            stmt = ({'name':message.from_user.username,'chat_id':str(message.from_user.id)})
            query = (
                insert(Table_Users).values(stmt)
            )
            await session.execute(query)
            await session.commit()
    except IntegrityError:
        pass
    await message.delete()
    await message.answer(text=LEXICON_MAIN['main_menu'],reply_markup=user_keyboards.main_menu_kb())
    await state.set_state(FSMMainMenu.main_menu)

@router.message(Command(commands='main_menu'),StateFilter(FSMSimulator.simulator_new))
async def process_command_main_menu(message:Message,state:FSMContext,bot:Bot):
    await message.delete()
    mes_del = await message.answer(text='Если вы выйдите из симулятора, ваш результат будет потерян. Используйте /main_menu ещё раз чтобы выйти.')
    await asyncio.sleep(3)
    await bot.delete_message(chat_id=message.from_user.id,message_id=mes_del.message_id)
    await state.set_state(FSMSimulator.simulator_end)
@router.message(Command(commands='main_menu'),~StateFilter(FSMSimulator.simulator_new))
async def process_command_main_menu(message:Message,state:FSMContext,bot:Bot):
    storage = await Redis.redis_db_0()
    await message.delete()
    try:
        mes_del = await storage.hget(f'message_del_{message.from_user.id}', 'callback_kb_simulator_new')
        await bot.delete_message(chat_id=message.from_user.id,message_id=int(mes_del.decode('utf-8')))
    except TelegramBadRequest:
        pass
    await message.answer(text=LEXICON_MAIN['main_menu'],reply_markup=user_keyboards.main_menu_kb())
    await state.set_state(FSMMainMenu.main_menu)

@router.callback_query(user_keyboards.MainMenuCallbackFactory.filter(),StateFilter(FSMMainMenu.main_menu))
async def process_main_menu_factory(callback:CallbackQuery,
                                    callback_data: user_keyboards.MainMenuCallbackFactory,
                                    state:FSMContext,
                                    bot:Bot):
    if callback_data.name_step == 'menu' and callback_data.callback == 'dict':
        await callback.message.edit_text(text=LEXICON_MAIN['dict'],reply_markup=user_keyboards.dict_kb())
        await state.set_state(FSMMainMenu.dict)
    if callback_data.name_step == 'menu' and callback_data.callback == 'simulator':
        await callback.message.edit_text(text=LEXICON_MAIN['simulator'],reply_markup=user_keyboards.simulator_kb())
        await state.set_state(FSMMainMenu.simulator)
    if callback_data.name_step == 'menu' and callback_data.callback == 'reminder':
        a = Scheduler('23:36:00',bot,callback.from_user.id)
        await a.add_shedule()

@router.callback_query(user_keyboards.DictCallbackFactory.filter(),StateFilter(FSMMainMenu.dict))
async def process_main_menu_factory(callback:CallbackQuery,
                                    callback_data: user_keyboards.DictCallbackFactory,
                                    state:FSMContext):
    if callback_data.name_step == 'dict' and callback_data.callback == 'dict_all':
        list_messages = await Dict.get_dict_all_from_db()
        await callback.message.delete()
        try:
            for message in list_messages:
                await callback.message.answer(text=message)
                await asyncio.sleep(1)
                await state.set_state(FSMMainMenu.dict_all)
        except TelegramBadRequest:
            await callback.message.answer(text='На данный момент словарь пуст')
            await state.set_state(FSMMainMenu.dict_all)
    if callback_data.name_step == 'dict' and callback_data.callback == 'dict_new':
        list_messages = await Dict.get_dict_new_from_db(str(callback.from_user.id))
        await callback.message.delete()
        try:
            for message in list_messages:
                await callback.message.answer(text=message)
                await asyncio.sleep(1)
        except TelegramBadRequest:
            await callback.message.answer(text='На данный момент словарь пуст')
    if callback_data.name_step == 'dict' and callback_data.callback == 'dict_learned':
        list_messages = await Dict.get_dict_learned_from_db(str(callback.from_user.id))
        await callback.message.delete()
        try:
            for message in list_messages:
                await callback.message.answer(text=message)
                await asyncio.sleep(1)
        except TelegramBadRequest:
            await callback.message.answer(text='На данный момент словарь пуст')

@router.callback_query(user_keyboards.SimulatorCallbackFactory.filter(),StateFilter(FSMMainMenu.simulator))
async def process_main_menu_factory(callback:CallbackQuery,
                                    callback_data: user_keyboards.DictCallbackFactory,
                                    state:FSMContext,
                                    ):
    storage = await Redis.redis_db_0()
    if callback_data.name_step == 'simulator' and callback_data.callback == 'simulator_all':
        pass
    if callback_data.name_step == 'simulator' and callback_data.callback == 'simulator_new':
        await Simulator.create_dicts_new_word(callback.from_user.id)
        page = (await storage.get(f'current_page_{callback.from_user.id}')).decode('utf-8')
        last_page = (await storage.get(f'last_page_simulator_{callback.from_user.id}')).decode('utf-8')
        text = await Simulator.get_word_about_page(callback.from_user.id,page)
        mes_edit = await callback.message.edit_text(text=text,reply_markup=user_keyboards.simulator_new_pagination_kb(page,last_page))
        await storage.hset(f'message_del_{callback.from_user.id}', 'callback_kb_simulator_new', f'{mes_edit.message_id}')
        await state.set_state(FSMSimulator.simulator_new)
    if callback_data.name_step == 'simulator' and callback_data.callback == 'simulator_gpt':
        pass
    if callback_data.name_step == 'simulator' and callback_data.callback == 'forward':
        page = (await storage.get(f'current_page_{callback.from_user.id}')).decode('utf-8')
        last_page = (await storage.get(f'last_page_simulator_{callback.from_user.id}')).decode('utf-8')
        if page == last_page:
            await callback.answer(text='Вы уже находитесь на последней странице')
        else:
            page += 1
            await storage.set(f'current_page_{callback.from_user.id}', f'{page}')
            text = await Simulator.get_word_about_page(callback.from_user.id, page)
            mes_edit = await callback.message.edit_text(text=text,
                                                        reply_markup=user_keyboards.simulator_new_pagination_kb(page,
                                                                                                            last_page))
            await storage.hset(f'message_del_{callback.from_user.id}', 'callback_kb_simulator_new',
                               f'{mes_edit.message_id}')

    if callback_data.name_step == 'simulator' and callback_data.callback == 'back':
        await callback.message.edit_text(text=LEXICON_MAIN['main_menu'], reply_markup=user_keyboards.main_menu_kb())
        await state.set_state(FSMMainMenu.main_menu)

@router.callback_query(user_keyboards.SimulatorCallbackFactory.filter(),StateFilter(FSMSimulator.simulator_new))
async def process_main_menu_factory(callback:CallbackQuery,
                                    callback_data: user_keyboards.DictCallbackFactory,
                                    state:FSMContext,
                                    ):
    storage = await Redis.redis_db_0()
    if callback_data.name_step == 'simulator_new' and callback_data.callback == 'forward':
        page = (await storage.get(f'current_page_{callback.from_user.id}')).decode('utf-8')
        last_page = (await storage.get(f'last_page_simulator_{callback.from_user.id}')).decode('utf-8')
        if page == last_page:
            await callback.answer(text='Вы уже находитесь на последней странице')
        else:
            page = str(int(page)+1)
            await storage.set(f'current_page_{callback.from_user.id}', f'{page}')
            text = await Simulator.get_word_about_page(callback.from_user.id, page)
            mes_edit = await callback.message.edit_text(text=text,
                                                        reply_markup=user_keyboards.simulator_new_pagination_kb(page,
                                                                                                            last_page))
            await storage.hset(f'message_del_{callback.from_user.id}', 'callback_kb_simulator_new',
                               f'{mes_edit.message_id}')
    if callback_data.name_step == 'simulator_new' and callback_data.callback == 'backward':
        page = (await storage.get(f'current_page_{callback.from_user.id}')).decode('utf-8')
        last_page = (await storage.get(f'last_page_simulator_{callback.from_user.id}')).decode('utf-8')
        if page == '1':
            await callback.answer(text='Вы уже находитесь на первой странице')
        else:
            page = str(int(page)-1)
            await storage.set(f'current_page_{callback.from_user.id}', f'{page}')
            text = await Simulator.get_word_about_page(callback.from_user.id, page)
            mes_edit = await callback.message.edit_text(text=text,
                                                        reply_markup=user_keyboards.simulator_new_pagination_kb(page,
                                                                                                            last_page))
            await storage.hset(f'message_del_{callback.from_user.id}', 'callback_kb_simulator_new',
                               f'{mes_edit.message_id}')


@router.message(StateFilter(FSMSimulator))
async def process_simulator_new_session(message:Message,
                                        state:FSMContext,
                                        bot: Bot,
                                        ):
    storage = await Redis.redis_db_0()
    res = await Simulator.word_translate_check(message.text,str(message.from_user.id),(await storage.get(f'current_page_{message.from_user.id}')).decode('utf-8'))
    page = (await storage.get(f'current_page_{message.from_user.id}')).decode('utf-8')
    last_page = (await storage.get(f'last_page_simulator_{message.from_user.id}')).decode('utf-8')
    await message.delete()
    mes_del = await storage.hget(f'message_del_{message.from_user.id}', 'callback_kb_simulator_new')
    await bot.edit_message_text(text=res,chat_id=message.from_user.id,message_id=int(mes_del.decode('utf-8')),reply_markup=user_keyboards.simulator_new_pagination_kb(page,last_page))
    await state.set_state(FSMSimulator.simulator_new)
    if 'Тест завершён' in res:
        await state.set_state(FSMMainMenu.main_menu)


@router.callback_query(F.data == 'english_kb',StateFilter(FSMMainMenu.dict_all))
async def process_add_new_word(callback:CallbackQuery):
    translate = translator.Translate('...')
    await translate.add_new_word_dict(str(callback.from_user.id))
    await callback.answer('Message added successfully')


@router.message(StateFilter(FSMMainMenu.dict_all))
async def process_translate_ru_en(message:Message,bot:Bot):
    translate = translator.Translate(message.text)
    translated_text = translate.translate_text()
    translator.Translate.edit_text(translated_text.text,message.text)
    mes_del = await message.answer(text=translated_text.text,reply_markup=translator.create_kb_english())
    await asyncio.sleep(5)
    await bot.delete_message(chat_id=message.chat.id,message_id=mes_del.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@router.message()
async def message_delete(message:Message):
    await message.delete()


