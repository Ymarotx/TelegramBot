import random
import json
import pymorphy2

from database.database import async_session
from database.models import Table_New_Word,Table_Users,Table_Learned_Word
from sqlalchemy import select, insert, update, delete
from database.redis_db import Redis
from services import translator
from lexicon.lexicon import LEXICON_SIMULATOR


class CheckText:
    @classmethod
    def make_lists(cls,word_user,word_db):
        word_user,word_db = word_user.replace(',',' ').lower(),word_db.replace(',',' ').lower()
        lists_user,lists_db = word_user.split(' '),word_db.split(' ')
        for i in lists_user:
            if i in ['',' ']:
                lists_user.remove(i)
        for i in lists_db:
            if i in ['',' ']:
                lists_db.remove(i)
        # if ' ' in lists_user:
        #     lists_user.remove(' ')
        # if ' ' in lists_db:
        #     lists_db.remove(' ')
        return lists_user,lists_db
    @classmethod
    def check_len(cls,lists_user,lists_db):
        if len(lists_user) != len(lists_db):
            return True
        else:
            return False
    @classmethod
    def check_word_order(cls,lists_user,lists_db):
        if len(lists_user) < 2:
            return True if len(lists_db) == 0 else False
        else:
            if lists_user[0] in lists_db:
                lists_db.remove(lists_user[0])
                return cls.check_word_order(lists_user[1:],lists_db)
            else:
                return False

    @classmethod
    def check_word_termination(cls,lists_user,lists_db):
        morphy = pymorphy2.MorphAnalyzer()
        num = 0
        res = None
        while num != len(lists_user):
            word_user = lists_user[num]
            word_db = lists_db[num]
            first = morphy.parse(word_user)[0].normal_form
            second = morphy.parse(word_db)[0].normal_form
            if word_db == word_user:
                res = True
            elif word_db != word_user and first == second:
                res = True
            else:
                res = False
            num += 1
        return res

    @classmethod
    def main_check(cls,word_user,word_db):
        lists_user,lists_db = cls.make_lists(word_user,word_db)
        lists_user_check_1,lists_db_check_1 = lists_user,lists_db
        lists_user_check_2,lists_db_check_2 = lists_user,lists_db
        lists_user_check_3, lists_db_check_3 = lists_user, lists_db
        check_1 = cls.check_len(lists_user=lists_user_check_1,lists_db=lists_db_check_1)
        check_2 = cls.check_word_order(lists_user=lists_user_check_2,lists_db=lists_db_check_2)
        check_3 = cls.check_word_termination(lists_user=lists_user_check_3,lists_db=lists_db_check_3)
        if check_1:
            return '''<code>В моем варинате слов больше, чем в вашем. Попробуйте ещё раз.</code>'''
        elif check_2:
            return '''<code>Ваш порядок слов отличен от моего. Попробуйте другой вариант.</code>'''
        elif check_3:
            return '''<code>Перевод верный, но в вашем варинате и моём имеются различия в окончаниях, попробуйте другой вариант.\
            Также если у вас есть буква "ё" замените её на "е".</code>'''
        # str_user = ' '.join(lists_user)
        # str_db = ' '.join(lists_db)



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
        text_words = ''
        for i in cls.list_word:
            dict_page_word[f'{page}'] = {f'{i.word_en}':0}
            dict_count_answer[f'{i.word_en}'] = f'{i.word_ru}'
            text_words += f'{i.word_en} - {i.word_ru};\n'
            page += 1
        cls.res = []
        cls.res.append(dict_page_word)
        cls.res.append(dict_count_answer)
        storage = await Redis.redis_db_0()
        await storage.set(f'{user_id}', json.dumps(cls.res))
        await storage.set(f'current_page_{user_id}','1')
        await storage.hset(f'message_del_{user_id}','callback_kb_simulator_new','0')
        return text_words
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
        if answer.lower() == word_ru_from_dict.lower():
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
        elif translate_answer.text.lower() == word_en_from_dict.lower():
            check = CheckText()
            return check.main_check(word_user=answer,word_db=word_ru_from_dict)
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
                    if word.count_answer >= 5:
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






