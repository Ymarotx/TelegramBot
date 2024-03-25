from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from aiogram import Bot
from datetime import datetime

from keyboards.user_keyboards import scheduler_kb


class Scheduler():

    def __init__(self,time:str,bot,chat_id:int):
        self.time = time
        self.bot = bot
        self.chat_id = chat_id
    async def send_message(self):
        text = 'Время пройти тест по новым словам.'
        await self.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=scheduler_kb())
    async def add_shedule(self):
        time_format = '%H:%M:%S'
        jobstores = {
            'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                     run_times_key='dispatched_trips_running',
                                     host='localhost',
                                     db=1,
                                     port=6379)
        }
        scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone='Europe/Moscow', jobstores=jobstores))
        time_object = datetime.strptime(self.time,time_format).time()
        scheduler.ctx.add_instance(self.bot, declared_class=Bot)
        scheduler.add_job(func=self.send_message,trigger='cron',hour=time_object.hour,minute=time_object.minute,start_date=datetime.utcnow())
        scheduler.start()
