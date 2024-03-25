import sqlite3
from aiogram import Bot,Router,F
from config_data.config import Config,load_config
from aiogram.filters import Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from FSM.FSM import FSMFillShipsGame



config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
router: Router = Router()

@router.message(lambda message: int(message.from_user.id) == int(config.tg_bot.admin_ids),Command(commands='send_message_all'))
async def process_send_message_all_command(message:Message,state:FSMContext):
    await message.answer(text='Введите текст для отправки')
    await state.set_state(FSMFillShipsGame.admin)

@router.message(StateFilter(FSMFillShipsGame.admin))
async def process_send_message(message:Message,state:FSMContext):
    file = open('database.txt')
    text = file.read()
    try:
        for i in text.split('.'):
            await bot.send_message(chat_id=int(i),text=message.text)
    except ValueError:
        pass
    await state.set_state(FSMFillShipsGame.main_menu)
@router.callback_query(F.data == '/send_message_all',StateFilter(FSMFillShipsGame.admin))
async def process_send_message(callback:CallbackQuery,state:FSMContext):
    file = open('database.txt')
    text = file.read()
    try:
        for i in text.split('.'):
            await bot.send_message(chat_id=int(i),text=callback.message.text)
    except ValueError:
        pass
    await state.set_state(FSMFillShipsGame.main_menu)



