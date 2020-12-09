import sqlite3
from cryptography.fernet import Fernet, InvalidToken
import subprocess
import os
if not os.path.exists('store.db'):
    print('[PasswordManager] Intializing ...')
    try:
        os.system('sqlite3 store.db')
    except:
        print('[Error] Please install sqlite3')
        exit()
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE DB (id INTEGER, username TEXT, password TEXT, url TEXT);')
else:
    conn = sqlite3.connect('store.db')
    c = conn.cursor()


def reset_table():
    c.execute('DELETE FROM DB')


def insert(username, password, url, key):
    c.execute('SELECT MAX(id) FROM DB')
    id_ = c.fetchone()[0]
    if id_ == None:
        id_ = 0
    id_ = id_ + 1
    f = Fernet(key)
    password = f.encrypt(password.encode()).decode()
    c.execute(
        f"INSERT INTO DB VALUES ({id_}, '{username}', '{password}', '{url}')")
    print('[PasswordManager] Entry successfully added')


def fetch_all(key):
    f = Fernet(key)
    print("|%4s|%30s|%30s|%30s|" % ('id', 'username', 'password', 'url'))
    print('-'*99)
    for row in c.execute("SELECT * FROM DB ORDER BY id"):
        print("|%4s|%30s|%30s|%30s|" %
              (row[0], row[1], f.decrypt(row[2].encode()).decode("utf-8"), row[3]))
    print('-'*99)
    sel = input('[PasswordManager] Enter id to copy to clipboard: ')
    copy_password(sel, key)


def fetch_one(url, key):
    f = Fernet(key)
    t = (url,)
    c.execute('SELECT * FROM DB WHERE url=? ORDER BY id', t)
    print("|%4s|%30s|%30s|%30s|" % ('id', 'username', 'password', 'url'))
    print('-'*99)
    for row in c.fetchall():
        print("|%4s|%30s|%30s|%30s|" %
              (row[0], row[1], f.decrypt(row[2].encode()).decode('utf-8'), row[3]))
    print('-'*99)
    sel = input('[PasswordManager] Enter id to copy to clipboard: ')
    copy_password(sel, key)


def delete(id_):
    try:
        c.execute('DELETE FROM DB WHERE ID=?', id_)
        print(f"[PasswordManager] Removed successfully")
    except:
        print('[PasswordManager] ID not found')


def copy_password(id_, key):
    f = Fernet(key)
    try:
        c.execute('SELECT * FROM DB WHERE ID=?', id_)
        passw = c.fetchone()
        passw = f.decrypt(passw[2].encode()).decode("utf-8")
        print(f"[PasswordManager] password >> {passw}")
        import subprocess
        # subprocess.run("pbcopy", universal_newlines=True, input=passw)
        print('[PasswordManager] Password copied to clipboard [Not Working :( ]')
    except:
        print('[PasswordManager] ID not found')


def save_and_close():
    conn.commit()
    conn.close()
