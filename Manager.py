import os
from authenticate import authenticate
from sql import *
import getpass


def run():
    key = authenticate()
    if key == None:
        exit()
    os.system('clear')
    print('[PasswordManager] Login successful')
    opt = None
    while opt != 'Q':
        opt = input('''
1: Create new entry
2: Show all 
3: Retrive a password
4: Delete entry
Q: Exit 

Select an action: ''')
        print('-'*68)

        if opt == '1':
            username = input('[PasswordManager] Enter the username: ')
            password = getpass.getpass(
                prompt='[PasswordManager] Enter the password: ')
            url = input('[PasswordManager] Enter the url: ')
            insert(username, password, url, key)

        elif opt == '2':
            fetch_all(key)

        elif opt == '3':
            url = input('[PasswordManager] Enter the url: ')
            fetch_one(url, key)

        elif opt == '4':
            id_ = input(
                '[PasswordManager] Enter the id of the entry you would like to remove: ')
            delete(id_)

        else:
            print('[PasswordManager] Invalid entry')

    save_and_close()
    os.system('clear')
    os.system('cd ~')
    print('[PasswordManager] Exiting ...')


if __name__ == '__main__':
    if not os.path.exists('store.db'):
        try:
            os.system('sqlite3 store.db')
        except:
            print('[Error] Please install sqlite3')
    os.system('clear')
    run()
