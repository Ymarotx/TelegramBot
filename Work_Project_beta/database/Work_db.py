import sqlite3
def create_table(cur,db) -> None:
    pass
#     cur.execute('CREATE TABLE IF NOT EXISTS application (time text,name_department varchar(30),'
#                 'name_house varhcar(30), number_cabinet varchar(10), what_to_do varchar(300))')
#     cur.execute('CREATE TABLE IF NOT EXISTS stock (time text,unit text)')
#     cur.execute(('CREATE TABLE IF NOT EXISTS completed_application (time_open text, name_department varchar(30),'
#                  'name_house varhcar(30), number_cabinet varchar(10), what_to_do varchar(300), time_close text)'))
#     cur.execute(('CREATE TABLE IF NOT EXISTS purchase (purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,'
#                  'time DATE, purchase_application VARCHAR(50), p_to_50b VARCHAR(50), p_over_50b VARCHAR(50))'
#                  ))
#     cur.execute(('CREATE TABLE IF NOT EXISTS cancel_application (time_open text, name_department varchar(30),'
#                  'name_house varhcar(30), number_cabinet varchar(10), what_to_do varchar(300), time_close text, why_del varchar(300))'))
#     cur.execute(
#         '''CREATE TABLE IF NOT EXISTS notes_active_application (notes_active_application_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                                                 row_id_active_application INT,
#                                                                 text VARCHAR(300) )''')
#     cur.execute('''CREATE TABLE IF NOT EXISTS label (label_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                               label_name VARCHAR(30),
#                                               UNIQUE(label_name) ) ''')
#     cur.execute('''CREATE TABLE IF NOT EXISTS materials_expended (materials_expended_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                                   date DATETIME,
#                                                   name_material VARCHAR(50),
#                                                   count_material INTEGER) ''')
#
#     # Изменения ниже уже применены и на данный момент действующие.
#     # cur.execute('''ALTER TABLE application ADD COLUMN label_id INT''')
#     try:
#         cur.execute('''INSERT INTO label(label_name) VALUES('💡')''')
#         cur.execute('''INSERT INTO label(label_name) VALUES('❗️')''')
#         cur.execute('''INSERT INTO label(label_name) VALUES('⏳')''')
#     except sqlite3.IntegrityError:
#         pass
#     db.commit()
