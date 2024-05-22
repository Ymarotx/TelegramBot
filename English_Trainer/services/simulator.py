import random
import json
import pprint
import time

from database.database import async_session
from database.models import Table_New_Word,Table_Users,Table_Learned_Word
from sqlalchemy import select, insert, update, delete
from database.redis_db import Redis
from services import translator
from lexicon.lexicon import LEXICON_SIMULATOR


class Simulator:
    list_word = []
    res = []
    @classmethod
    async def create_list_new_word(cls,user_id):
        async with async_session() as session:
            storage = await Redis.redis_db_0()
            cls.list_word = []
            stmt = (
                select(Table_New_Word)
            )
            res = await session.execute(stmt)
            result_all = res.scalars().all()
            random.shuffle(result_all)
            result_15 = result_all[:15]
            await storage.set(f'last_page_simulator_{user_id}',f'{len(result_15)}')
            for i in result_15:
                cls.list_word.append(i)

    @classmethod
    async def create_dicts_new_word(cls,user_id):
        #Храним [{page : {word_en : count},word_en : word_ru},]
        await cls.create_list_new_word(user_id)
        page = 1
        dict_count_answer = {}
        dict_page_word = {}
        for i in cls.list_word:
            dict_page_word[f'{page}'] = {f'{i.word_en}':0}
            dict_count_answer[f'{i.word_en}'] = f'{i.word_ru}'
            page += 1
        cls.res = []
        cls.res.append(dict_page_word)
        cls.res.append(dict_count_answer)
        storage = await Redis.redis_db_0()
        await storage.set(f'{user_id}', json.dumps(cls.res))
        await storage.set(f'current_page_{user_id}','1')
        await storage.hset(f'message_del_{user_id}','callback_kb_simulator_new','0')

    @classmethod
    async def get_word_about_page(cls,user_id:str,page:str):
        storage = await Redis.redis_db_0()
        check_end = await cls.end_simulator(user_id,storage)
        if not check_end:
            full_dict_user = json.loads(await storage.get(f'{user_id}'))
            count = ''
            for key,value in full_dict_user[0].get(f'{page}').items():
                if value == 0:
                    count = ' '
                elif value == 1:
                    count = '.'
                elif value == 2:
                    count = '..'
                elif value == 3:
                    count = full_dict_user[1].get(key)
                elif value == 4:
                    count = full_dict_user[1].get(key)
                elif value == 5:
                    count = full_dict_user[1].get(key)
                return f'{key} - {count}'
        else:
            return check_end

    @classmethod
    async def word_translate_check(cls,answer:str,user_id:str,page:str):
        storage = await Redis.redis_db_0()
        full_dict_user = json.loads(await storage.get(f'{user_id}'))
        word_en_from_dict = ''
        word_en = ''
        for key,value in full_dict_user[0].get((await storage.get(f'current_page_{user_id}')).decode('utf-8')).items():
            word_en_from_dict = key
            word_en = key
        word_ru_from_dict = full_dict_user[1].get(word_en_from_dict)
        translate = translator.Translate(answer)
        translate_answer = translate.translate_text()
        lists = await storage.get(f'{user_id}')
        data = json.loads(lists)
        if translate_answer.text.lower() == word_en_from_dict.lower() and answer.lower() != word_ru_from_dict.lower():
            return LEXICON_SIMULATOR['simulator_check_word']
        elif answer.lower() == word_ru_from_dict.lower():
            count = data[0][f'{page}'][f'{word_en}']
            if count == 0:
                data[0][f'{page}'][f'{word_en}'] = 4
                await storage.set(f'{user_id}', json.dumps(data))
            else:
                data[0][f'{page}'][f'{word_en}'] = 5
                await storage.set(f'{user_id}', json.dumps(data))
            page = (await storage.get(f'current_page_{user_id}')).decode('utf-8')
            if int(page) < 15:
                await storage.set(f'current_page_{user_id}', f'{int(page) + 1}')
                text = await cls.get_word_about_page(user_id,str(int(page)+1))
                return text
            else:
                text = await cls.get_word_about_page(user_id, str(int(page)))
                return text
        else:
            _ = data[0][f'{page}'][f'{word_en}']
            if _ not in [3,4,5]:
                data[0][f'{page}'][f'{word_en}'] += 1
            await storage.set(f'{user_id}',json.dumps(data))
            text = await cls.get_word_about_page(user_id,page)
            return text
    @classmethod
    async def end_simulator(cls,user_id:str,storage):
        full_dict_user = json.loads(await storage.get(f'{user_id}'))
        value = 0
        lists_word_for_increase = []
        learned_word = ''
        for page,dict in full_dict_user[0].items():
            for word,count in dict.items():
                if count == 0 or count == 1 or count == 2 or count == 3:
                    value += 1
                if count == 4:
                    lists_word_for_increase.append(word)
        if value == 0:
            async with async_session() as session:
                words = await session.execute(select(Table_New_Word).filter(Table_New_Word.word_en.in_(lists_word_for_increase)))
                words = words.scalars().all()
                for word in words:
                    word.count_answer += 1
                session.add_all(words)
                await session.commit()
                words = await session.execute(select(Table_New_Word).filter(Table_New_Word.word_en.in_(lists_word_for_increase)))
                words = words.scalars().all()
                for word in words:
                    if word.count_answer == 5:
                        query = (
                            select(Table_Users)
                            .filter(Table_Users.chat_id == user_id)
                        )
                        user = await session.execute(query)
                        user = user.scalar()

                        stmt = [{'word_en': f'{word.word_en}', 'word_ru': f'{word.word_ru}',
                                 'user_id': user.id,'count_answer' : 0}]
                        insert_word = insert(Table_Learned_Word).values(stmt)
                        del_word = delete(Table_New_Word).where(Table_New_Word.word_en == f'{word.word_en}')
                        await session.execute(insert_word)
                        await session.execute(del_word)
                        await session.commit()
                        learned_word += f'{word.word_en}\n '
            for page, dict in full_dict_user[0].items():
                for word, count in dict.items():
                    full_dict_user[0][str(page)][word] = 3
            await storage.set(f'{user_id}',json.dumps(full_dict_user))
            if learned_word:
                return LEXICON_SIMULATOR['simulator_true_end_1']+learned_word + LEXICON_SIMULATOR['simulator_true_end_2']
            else:
                return LEXICON_SIMULATOR['simulator_false_end']






