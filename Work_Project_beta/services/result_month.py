
import sqlite3
from services.open_all_table import open_all_table_materials
db = sqlite3.connect('Work.sql')
cur = db.cursor()
def detail_result_month(month):
    dicts = {'January' : ['2024-01-01','2024-01-31'],
    'February': ['2024-02-01', '2024-02-31'],
    'March': ['2024-03-01', '2024-03-31'],
    'April': ['2024-04-01', '2024-04-31'],
    'May': ['2024-05-01', '2024-05-31'],
    'June': ['2024-06-01', '2024-06-31'],
    'Juli': ['2024-07-01', '2024-07-31'],
    'August': ['2024-08-01', '2024-08-31'],
    'September': ['2024-09-01', '2024-09-31'],
    'October': ['2024-10-01', '2024-10-31'],
    'November': ['2024-11-01', '2024-11-31'],
    'December': ['2024-12-01', '2024-12-31'],}

    start_time = dicts[month][0]
    end_time = dicts[month][1]
    cur.execute(f'SELECT * FROM completed_application WHERE time_close BETWEEN "{start_time}" AND "{end_time}"')
    a = cur.fetchall()
    dicts_1: dict[str,list[dict[str,str]]] = {}
    for i in a:
        try:
            dicts_1[i[2]].append({i[5]:i[4]})
        except KeyError:
            dicts_1[i[2]] = []
            dicts_1[i[2]].append({i[5]:i[4]})
    text_1 = ''
    for p in dicts_1:
        text_2 = ''
        for r in dicts_1[p]:
            for k in r:
                text_2 += f'Дата закрытия: {k}\nБыло сделано: {r[k]}\nБыло затрачено :\n{open_all_table_materials(k,cur)}'
        text_1 += (f'<i>{p}</i>:\n'
                   f'{text_2}')
    return text_1

def result_month(month):
    dicts = {'January': ['2024-01-01', '2024-01-31'],
             'February': ['2024-02-01', '2024-02-31'],
             'March': ['2024-03-01', '2024-03-31'],
             'April': ['2024-04-01', '2024-04-31'],
             'May': ['2024-05-01', '2024-05-31'],
             'June': ['2024-06-01', '2024-06-31'],
             'Juli': ['2024-07-01', '2024-07-31'],
             'August': ['2024-08-01', '2024-08-31'],
             'September': ['2024-09-01', '2024-09-31'],
             'October': ['2023-10-01', '2024-10-31'],
             'November': ['2024-11-01', '2024-11-31'],
             'December': ['2024-12-01', '2024-12-31'], }

    start_time = dicts[month][0]
    end_time = dicts[month][1]
    cur.execute(f'SELECT * FROM completed_application WHERE time_close BETWEEN "{start_time}" AND "{end_time}"')
    a = cur.fetchall()
    dicts_1: dict[str, list] = {}
    dicts_2: dict[str,dict[str,int]] = {} #Содержит имя здания со словарём какой материал и кол-во которое будет прибавляться
    for i in a:
        try:
            dicts_1[i[2]].append(i[5])
        except KeyError:
            dicts_1[i[2]] = []
            dicts_1[i[2]].append(i[5])
    text = ''
    for p in dicts_1:
        text_2 = ''
        for l in dicts_1[p]:
            if open_all_table_materials(l, cur):
                text_2 += (f'{open_all_table_materials(l,cur)}\n')
        if text_2:
            text += (f'{p}:\n'
                     f'{text_2}\n')
    return text


#БД делает выбор из словаря. Нужно в дальнейшем реализовать через выбор имён стобцов, чтобы была независимость от словаря.
    # print(dicts_1)

