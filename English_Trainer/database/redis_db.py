import aioredis

class Redis:
    # База данных для тренажёра
    @staticmethod
    async def redis_db_0():
        storage = await aioredis.from_url(url='redis://localhost',port=6379,db=0)
        return storage
    # База данных для schedule
    @staticmethod
    async def redis_db_1():
        storage = await aioredis.from_url(url='redis://localhost',port=6379,db=1)
        return storage



