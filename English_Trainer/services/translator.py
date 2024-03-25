from googletrans import Translator
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import insert, select

from database.database import async_session
from database.models import Table_All_Word,Table_New_Word,Table_Users

class Translate:
    word_ru: str
    word_en: str
    ready_word: list[str]

    def __init__(self,word_ru):
        self.word_ru = word_ru
    def translate_text(self):
        translater = Translator()
        detected = translater.detect(self.word_ru)
        en_or_ru = detected.lang
        if en_or_ru == 'en':
            text_ru = translater.translate(self.word_ru,dest='ru')
            return text_ru
        if en_or_ru == 'ru':
            text_en = translater.translate(self.word_ru,dest='en')
            return text_en
    @classmethod
    def edit_text(cls,word_en,word_ru):
        cls.ready_word = []
        translater = Translator()
        detected = translater.detect(word_ru)
        if detected.lang != 'ru':
            cls.word_en = word_ru
            cls.word_ru = word_en
        else:
            cls.word_en = word_en
            cls.word_ru = word_ru
        cls.ready_word.extend([cls.word_en.capitalize(),cls.word_ru.capitalize()])

    async def add_new_word_dict(self,id:str):
        async with async_session() as session:
            query = (
                select(Table_Users)
                .filter(Table_Users.chat_id == id)
            )
            user_id = await session.execute(query)
            user_id = user_id.scalar()
            stmt = [{'word_en': f'{self.ready_word[0]}', 'word_ru': f'{self.ready_word[1]}', 'user_id' : user_id.id}]
            insert_word_all = insert(Table_All_Word).values(stmt)
            insert_word_new = insert(Table_New_Word).values(stmt)
            await session.execute(insert_word_all)
            await session.execute(insert_word_new)
            await session.commit()



def create_kb_english():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text='Добавить в словарь',callback_data='english_kb'))
    return kb_builder.as_markup()