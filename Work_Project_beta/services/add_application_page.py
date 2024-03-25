import sqlite3
from database.database import application_page,database,application_page_stock

def add_application_page_new(table,d_b):
    db = sqlite3.connect('Work.sql')
    cur = db.cursor()
    cur.execute(f'SELECT rowid,* FROM {table} ORDER BY time DESC')
    app = cur.fetchall()
    cur.execute(f'SELECT * FROM {table} LEFT JOIN label USING(label_id) ORDER BY time DESC')
    app_label = cur.fetchall()
    page = 1
    length = len(app)
    a = 0
    while True:
        application_page[str(page)] = []
        for i in range(9):
            try:
                if app_label[i+a][-1]:
                    dicts = {f'{app[i+a][0]}': f'({app_label[i+a][-1]}) {app[i+a][3]} {app[i+a][2]} {app[i+a][5]}'}
                    application_page[str(page)].append(dicts)
                else:
                    dicts = {
                        f'{app[i + a][0]}': f'{app[i + a][3]} {app[i + a][2]} {app[i + a][5]}'}
                    application_page[str(page)].append(dicts)
            except IndexError:
                pass
        if length > 9:
            page += 1
        length -= 9
        a += 9
        if length <= 0:
            break
    database[f'{d_b}'] = page
    cur.close()
    db.close()



def add_application_page(table,d_b):
    db = sqlite3.connect('Work.sql')
    cur = db.cursor()
    cur.execute(f'SELECT rowid,* FROM {table} ORDER BY time DESC')
    app = cur.fetchall()
    page = 1
    length = len(app)
    a = 0
    while True:
        application_page[str(page)] = []
        for i in range(9):
            try:
                dicts = {f'{app[i+a][0]}': f'{app[i+a][3]} {app[i+a][2]} {app[i+a][5]}'}
                application_page[str(page)].append(dicts)
            except IndexError:
                pass
        if length > 9:
            page += 1
        length -= 9
        a += 9
        if length <= 0:
            break
    database[f'{d_b}'] = page
    cur.close()
    db.close()


def add_close_application_page():
    db = sqlite3.connect('Work.sql')
    cur = db.cursor()
    cur.execute('SELECT rowid,* FROM completed_application ORDER BY time_close DESC')
    app = cur.fetchall()
    length = len(app)
    page = 1
    a = 0
    while True:
        application_page[str(page)] = []
        for i in range(9):
            try:
                dicts = {f'{app[i+a][0]}': f'{app[i+a][3]} {app[i+a][2]} {app[i+a][4]}'}
                application_page[str(page)].append(dicts)
            except IndexError:
                pass
        if length > 9:
            page += 1
        length -= 9
        a += 9
        if length <= 0:
            break
    database['quantity_page_close'] = page
    cur.close()
    db.close()


def add_stock_page(d_b):
    db = sqlite3.connect('Work.sql')
    cur = db.cursor()
    cur.execute('PRAGMA table_info("stock")')
    column_names = [i[1] for i in cur.fetchall()]
    column_names = sorted(column_names[2:])
    page = 1
    length = len(column_names)
    a = 0
    while True:
        application_page_stock[str(page)] = []
        lists = []
        for i in range(9):
            try:
                lists.append(column_names[i+a])
            except IndexError:
                pass
        application_page_stock[str(page)].append(lists)
        if length > 9:
            page += 1
        length -= 9
        a += 9
        if length <= 0:
            break
    database[f'{d_b}'] = page
    cur.close()
    db.close()

def add_purchase_page(table,d_b,column):
    db = sqlite3.connect('Work.sql')
    cur = db.cursor()
    cur.execute(f'''SELECT rowid,{column} FROM {table} 
                    WHERE {column} IS NOT NULL 
                    ORDER BY {column} ASC''')
    app = cur.fetchall()
    page = 1
    length = len(app)
    a = 0
    while True:
        application_page[str(page)] = []
        for i in range(9):
            try:
                dicts = {f'{app[i+a][0]}': f'{app[i+a][1]}'}
                application_page[str(page)].append(dicts)
            except IndexError:
                pass
        if length > 9:
            page += 1
        length -= 9
        a += 9
        if length <= 0:
            break
    database[f'{d_b}'] = page
    cur.close()
    db.close()


