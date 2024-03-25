from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_kb_schedule():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text='✔️',callback_data='schedule_kb'))
    return kb_builder.as_markup()
class ClassScheduler:
    def __init__(self,date,text:str,bot,chat_id:int):
        self.date = date
        self.text = text
        self.bot = bot
        self.chat_id = chat_id
    async def send_message(self):
        await self.bot.send_message(chat_id=self.chat_id,text=self.text,reply_markup=create_kb_schedule())
    async def schedule(self):
        scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        scheduler.add_job(func=self.send_message,trigger='date',
                          run_date=self.date)
        scheduler.start()