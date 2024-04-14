import asyncio
import time

from aiogram.exceptions import TelegramBadRequest
from database.redis_db import Redis



class DeleteMessage():
    @staticmethod
    async def get_list_delete_message(chat_id:int):
        storage = await Redis.redis_db_0()
        try:
            lists_b = await storage.lrange(f'message_delete_{chat_id}',1,-1)
            lists = [int(item.decode('utf-8')) for item in lists_b]
        except AttributeError:
            lists = []
        return lists
    @staticmethod
    async def add_to_redis_delete_message(chat_id: int,mes_id: int):
        storage = await Redis.redis_db_0()
        lists = await DeleteMessage.get_list_delete_message(chat_id)
        if mes_id not in lists:
            await storage.lpush(f'message_delete_{chat_id}', str(mes_id))


    @staticmethod
    async def message_delete(chat_id:int,bot):
        lists = await DeleteMessage.get_list_delete_message(chat_id)
        for i in lists:
            try:
                await bot.delete_message(message_id=int(i),chat_id=chat_id)
            except TelegramBadRequest:
                continue



