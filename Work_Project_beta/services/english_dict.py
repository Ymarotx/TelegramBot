import random

class EnglishDict:
    dicts = {}
    list_questions = []
    text = ''
    def create_english_dict(self):
        self.list_key_values = []
        with open('other_file/english_dict.txt','r') as file:
            text = file.read()
            new_text = text.replace('\n','')
            new_text = new_text.replace('\t', '')
            self.list_key_values_all = new_text.split(';')
            for i in self.list_key_values_all[:-1]:   #Потому что последний элемент None
                key_values = i.split(':')
                key = key_values[0].lower()
                values = key_values[1].lower()
                self.dicts[key] = values
    def create_lists_questions(self):
        for key in self.dicts.keys():
            self.list_questions.append(key)
        random.shuffle(self.list_questions)

class Russian_Eng_Dict:
    dicts = {}
    list_questions = []
    text = ''
    def create_english_dict(self):
        self.list_key_values = []
        with open('other_file/english_dict.txt', 'r') as file:
            text = file.read()
            new_text = text.replace('\n', '')
            new_text = new_text.replace('\t', '')
            self.list_key_values_all = new_text.split(';')
            for i in self.list_key_values_all[:-1]:  # Потому что последний элемент None
                key_values = i.split(':')
                key = key_values[1].lower()
                values = key_values[0].lower()
                self.dicts[key] = values
    def create_lists_questions(self):
        for key in self.dicts.keys():
            self.list_questions.append(key)
        random.shuffle(self.list_questions)

def check_len_dict(text) -> list:
    lists_text = []
    lenghth = len(text)
    new_text = text
    end_len = 0
    while True:
        max_len = 4000
        if lenghth > max_len:
            while True:
                if new_text[max_len] != ';':
                    max_len -= 1
                else:
                    lists_text.append(new_text[:max_len+1])
                    break
            lenghth -= len(new_text[:max_len])
            new_text = text[max_len+1:]
            end_len += max_len+1
        else:
            lists_text.append(text[end_len+1:])
            break
    return lists_text