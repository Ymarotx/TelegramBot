import aioredis
from aiogram.fsm.storage.redis import RedisStorage


class Redis:
    _storage_0 = None
    _storage_1 = None
    _storage_2 = None
    # База данных для тренажёра
    @classmethod
    async def redis_db_0(cls):
        if cls._storage_0 is None:
            cls._storage_0 = await aioredis.from_url(url='redis://localhost',port=6379,db=0)
        return cls._storage_0
    # База данных для schedule
    @classmethod
    async def redis_db_1(cls):
        if cls._storage_1 is None:
            cls._storage_1 = await aioredis.from_url(url='redis://localhost',port=6379,db=1)
        return cls._storage_1
    #БД для состояний
    @classmethod
    def redis_db_2(cls):
        if cls._storage_2 is None:
            cls._storage_2 = RedisStorage.from_url(url='redis://localhost:6379/2')
        return cls._storage_2


