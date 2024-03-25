from database.database import database_6


def open_table_stock(cur,callback):
    cur.execute(f'SELECT rowid,"{callback}",time,unit FROM stock')
    a = cur.fetchall()
    text = ''
    for i in a:
        num = 0
        lists = []
        for p in i:
            if p:
                num += 1
        if num == 4:
            for k in i:
                lists.append(k)
            database_6['last_num'] = lists[1]
            database_6['unit'] = lists[3]
            text += f'{lists[2]} - {lists[1]} {lists[3]}.\n'
    return text





