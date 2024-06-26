from aiogram import Bot
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_MAIN_MENU

async def set_main_menu(bot:Bot):
    main_menu_commands = [BotCommand(command = command,description=description) for command,description in LEXICON_MAIN_MENU.items()]
    await bot.set_my_commands(main_menu_commands)

