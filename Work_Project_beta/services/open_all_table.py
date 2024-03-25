
def open_all_table_materials(time,cur):
    cur.execute(f'SELECT * FROM materials_expended WHERE date = "{time}"')
    data = cur.fetchall()
    text = ''
    for i in data:
        text += f'<u>{i[2]}:  {i[3]} (м/шт)</u>\n'
    return text
