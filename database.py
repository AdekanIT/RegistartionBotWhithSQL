import sqlite3

base = sqlite3.connect('data.db', check_same_thread=False)
sql = base.cursor()
sql.execute('CREATE TABLE IF NOT EXISTS bot_users'
            '(id INTEGER, name TEXT, phone_num TEXT, location TEXT);')

def register(id, name, phone_num, location):
    sql.execute('INSERT INTO bot_users(id, name, phone_num, location) '
                'VALUES(?, ?, ?, ?);', (id, name, phone_num, location))
    base.commit()

def checker(id):
    check = sql.execute('SELECT id FROM bot_users WHERE id=?;', (id, ))
    if check.fetchone():
        return True
    else:
        return False


def show_info(id):
    sql.execute('SELECT name, phone_num, location FROM bot_users WHERE id=?;', (id,))
    user_info = sql.fetchone()
    return user_info

