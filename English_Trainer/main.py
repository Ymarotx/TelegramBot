import asyncio
import logging
import aiomultiprocess
from multiprocessing import Process

from aiogram import Bot, Dispatcher

from config_data.config import BOT_TOKEN
from handlers import user_handlers
from keyboards.main_menu_kb import set_main_menu
from services.scheduler import Scheduler
from database.redis_db import Redis



logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.INFO,
                        filename='logs.log',
                        format='%(filename)s:%(lineno)d #%(levelname)-8s'
                               '[%(asctime)s] - %(name)s - %(message)s'
                        )
    logger.info('Starting bot')
    storage_2 = Redis.redis_db_2()
    bot: Bot=Bot(token=BOT_TOKEN,parse_mode='HTML')
    dp: Dispatcher=Dispatcher(storage=storage_2)
    scheduler = Scheduler.sheduler_create()
    scheduler.start()
    dp.include_router(user_handlers.router)
    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

