from googletrans import Translator
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class Translate:
    word_ru: str
    word_en: str
    ready_word: str

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
        translater = Translator()
        detected = translater.detect(word_ru)
        if detected.lang != 'ru':
            cls.word_en = word_ru
            cls.word_ru = word_en
        else:
            cls.word_en = word_en
            cls.word_ru = word_ru
        cls.ready_word = f'\n{cls.word_en.capitalize()} : {cls.word_ru.capitalize()};'

    def add_new_word_dict(self):
        with open('other_file/english_dict.txt','a') as text_file:
            text_file.write(self.ready_word)



def create_kb_english():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text='Добавить в словарь',callback_data='english_kb'))
    return kb_builder.as_markup()


