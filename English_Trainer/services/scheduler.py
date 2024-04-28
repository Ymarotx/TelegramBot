import datetime

import apscheduler.schedulers
from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from sqlalchemy import select, insert, update

from config_data.config import BOT_TOKEN
from database.database import create_tables,async_session
from database.models import Table_New_Word,Table_Learned_Word,Table_Users,Table_Reminder
from sqlalchemy.orm import contains_eager
from lexicon.lexicon import LEXICON_REMINDER

bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')



def kb():
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    btn: InlineKeyboardButton = InlineKeyboardButton(text='Start ➪',callback_data='reminder_start')
    kb_builder.row(btn)
    return kb_builder.as_markup()


class Scheduler:
    _scheduler = None

    @classmethod
    def sheduler_create(cls):
        if cls._scheduler is None:
            jobstores = {
                'default': RedisJobStore(jobs_key='dispatcher_trips_jobs',
                                         run_times_key='dispatcher_trips_running',
                                         host='localhost',
                                         db=1,
                                         port=6379)
            }
            scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone='Europe/Moscow', jobstores=jobstores))
            scheduler.ctx.add_instance(bot, declared_class=Bot)
            cls._scheduler = scheduler
        return cls._scheduler

    @classmethod
    async def sheduler_add_job(cls,chat_id):
            scheduler = cls.sheduler_create()
            async with async_session() as session:
                stmt = (
                    select(Table_Reminder)
                    .join(Table_Reminder.user)
                    .where(Table_Users.chat_id == str(chat_id))
                    .options(contains_eager(Table_Reminder.user))
                )
                res = await session.execute(stmt)
                res = res.scalar_one()
                time = res.time
                time_format = '%H:%M:%S'
                ready_time = datetime.datetime.strptime(time, time_format)
                jobs = scheduler.add_job(func=cls.send_message,trigger='cron',
                                  hour=ready_time.hour,minute=ready_time.minute,kwargs={'chat_id':res.user.chat_id})
                res.jobs_id = jobs.id
                await session.commit()
                try:
                    scheduler.start()
                except apscheduler.schedulers.SchedulerAlreadyRunningError:
                    pass

    @classmethod
    def del_sheduler(cls,jobs_id):
        scheduler = cls.sheduler_create()
        scheduler.remove_job(job_id=jobs_id)


    @classmethod
    async def send_message(cls,chat_id):
        text = LEXICON_REMINDER['reminder_send_message']
        await bot.send_message(chat_id=chat_id,text=text,reply_markup=kb())

