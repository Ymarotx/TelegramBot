from aiogram import Bot
from aiogram.types import BotCommand,InlineKeyboardMarkup,InlineKeyboardButton
from lexicon.lexicon import LEXICON_COMMANDS
from aiogram.utils.keyboard import InlineKeyboardBuilder
async def set_main_menu(bot:Bot):
    main_menu_commands = [BotCommand(command=commands,description=description) for commands,description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)

def main_menu_kb() -> InlineKeyboardMarkup:
    btn1: InlineKeyboardButton = InlineKeyboardButton(text='Выйти из сражения',callback_data='exit_game')
    btn2: InlineKeyboardButton = InlineKeyboardButton(text='Отмена',callback_data = 'cancel')
    keyboard: list[list[InlineKeyboardButton]] = [[btn1],[btn2]]
    reply: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply

def first_main_menu_kb():
    builder: InlineKeyboardBuilder=InlineKeyboardBuilder()
    keyboard: list[InlineKeyboardButton] = [InlineKeyboardButton(text=i,callback_data=j) for j,i in LEXICON_COMMANDS.items()]
    builder.row(*keyboard,width=1)
    return builder.as_markup()
