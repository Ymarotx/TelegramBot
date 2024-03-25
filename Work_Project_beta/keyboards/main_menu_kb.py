from aiogram import Bot
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_MAIN_MENU,LEXICON_MAIN_MENU_KB

async def set_main_menu(bot:Bot):
    main_menu_commands = [BotCommand(command = command,description=description) for command,description in LEXICON_MAIN_MENU.items()]
    await bot.set_my_commands(main_menu_commands)


def main_menu_kb():
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard: list[InlineKeyboardButton] = [InlineKeyboardButton(text=text,callback_data=callback) for text,callback in LEXICON_MAIN_MENU_KB.items()]
    builder.row(*keyboard,width=1)
    return builder.as_markup()


