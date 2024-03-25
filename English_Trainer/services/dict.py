from database.database import async_session
from database.models import Table_All_Word,Table_New_Word,Table_Users,Table_Learned_Word
from sqlalchemy import select
from sqlalchemy.orm import contains_eager


class Dict:
    text = ''
    @classmethod
    def check_len_dict(cls) -> list:
        lists_text = []
        max_len = 4000
        if len(cls.text) > max_len:
            while True:
                if cls.text[-1] != ';':
                    max_len -= 1
                elif cls.text[max_len] == ';' and max_len <= 4000:
                    lists_text.append(cls.text[:max_len + 1])
                    lists_text.append(cls.text[max_len + 2:])
                    break
                else:
                    max_len -= 1
        else:
            lists_text.append(cls.text)
        return lists_text

    @classmethod
    async def get_dict_all_from_db(cls):
        cls.text = ''
        async with async_session() as session:
            stmt = (
                select(Table_All_Word)
            )
            res = await session.execute(stmt)
            result = res.scalars().all()
            for i in result:
                cls.text += f'{i.word_en} : {i.word_ru};\n'
        return cls.check_len_dict()

    @classmethod
    async def get_dict_new_from_db(cls,id:str):
        async with async_session() as session:
            cls.text = ''
            stmt = (
                select(Table_New_Word)
                .options(contains_eager(Table_New_Word.user))
                .filter(Table_Users.chat_id == id)
            )
            res = await session.execute(stmt)
            result = res.scalars().all()
            for i in result:
                cls.text += f'{i.word_en} : {i.word_ru};\n'
        return cls.check_len_dict()

    @classmethod
    async def get_dict_learned_from_db(cls,id:str):
        async with async_session() as session:
            cls.text = ''
            stmt = (
                select(Table_Learned_Word)
                .options(contains_eager(Table_Learned_Word.user))
                .filter(Table_Users.chat_id == id)
            )
            res = await session.execute(stmt)
            result = res.scalars().all()
            for i in result:
                cls.text += f'{i.word_en} : {i.word_ru};\n'
        return cls.check_len_dict()


