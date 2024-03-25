import asyncio
import logging
from aiogram import Bot,Dispatcher,F
from aiogram.types import Message
from config_data.config import load_config,Config
from aiogram.filters import CommandStart
from aiogram import BaseMiddleware
from typing import Awaitable,Callable,Any,Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import TelegramObject
from datetime import datetime,timedelta
config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher=Dispatcher()
logger = logging.getLogger(__name__)


async def send_message_middleware(bot:Bot,chat_id:int):
    await bot.send_message(chat_id=chat_id,text='Hello i am middleware')

@dp.message(CommandStart())
async def send_message_before_middleware(message:Message,apscheduler:AsyncIOScheduler,bot:Bot):
    await message.answer('Hello i am before middleware')
    apscheduler.add_job(send_message_middleware,trigger='date',run_date=datetime.now() + timedelta(seconds=3),kwargs={'bot':bot,'chat_id':message.from_user.id})

# class SchedulerMiddleware(BaseMiddleware):
#     def __init__(self,scheduler:AsyncIOScheduler):
#         self.scheduler = scheduler
#
#     async def __call__(self,
#                        handler:Callable[[TelegramObject,Dict[str,Any]],Awaitable[Any]],
#                        event: TelegramObject,
#                        data: Dict[str,Any],
#                        ):
#         data['apscheduler'] = self.scheduler
#         return await handler(event,data)



async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s'
                               '[%(asctime)s] - %(name)s - %(message)s')
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    logger.info('Starting bot')
    # dp.update.middleware.register(SchedulerMiddleware(scheduler))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

