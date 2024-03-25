import sqlite3
from database.database import database_page,database_quantity_page

def add_page(id_user,table,d_b):
    db = sqlite3.connect('TP_RP.sql')
    cur = db.cursor()
    cur.execute(f'SELECT rowid,* FROM {table}')
    app = cur.fetchall()
    page = 1
    length = len(app)
    a = 0
    database_page[id_user] = {}
    while True:
        database_page[id_user][str(page)] = []
        for i in range(8):
            try:
                dicts = {f'{app[i+a][0]}': f'{app[i+a][3]}'}
                database_page[id_user][str(page)].append(dicts)
            except IndexError:
                pass
        if length > 8:
            page += 1
        length -= 8
        a += 8
        if length <= 0:
            break
    database_quantity_page[id_user][f'{d_b}'] = page
    cur.close()
    db.close()
    if database_quantity_page[id_user]['user_page'] > database_quantity_page[id_user][f'{d_b}']:
        database_quantity_page[id_user]['user_page'] = database_quantity_page[id_user][f'{d_b}']
