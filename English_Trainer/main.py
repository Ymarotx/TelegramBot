import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import BOT_TOKEN
from handlers import user_handlers
from keyboards.main_menu_kb import set_main_menu


logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.DEBUG,
                        # filename='logs.log',
                        format='%(filename)s:%(lineno)d #%(levelname)-8s'
                               '[%(asctime)s] - %(name)s - %(message)s'
                        )
    logger.info('Starting bot')

    bot: Bot=Bot(token=BOT_TOKEN,parse_mode='HTML')
    dp: Dispatcher=Dispatcher()

    dp.include_router(user_handlers.router)
    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

