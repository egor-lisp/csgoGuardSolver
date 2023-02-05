import json
import config
import os
import time
import ctypes
import sys
from start_steam import start_steam_client


def main():
    accs = []
    with open('accs.txt', 'r') as f:
        for line in f.read().split('\n'):
            if bool(line):
                accs.append(line)

    mafiles = {}  # Key: account name
    for file in os.listdir(config.mafiles_path):
        if file.endswith('maFile'):
            with open(os.path.join(config.mafiles_path, file)) as f:
                data = json.load(f)
                mafiles[data['account_name']] = data

    for n, acc in enumerate(accs):
        username, password = acc.split(':')
        if not mafiles.get('username'):
            print(f'Не найден мафайл для аккаунта {username}')
            continue
        if not mafiles[username].get('shared_secret'):
            print(f'В мафайле отсутствует ключ shared_secret')
            continue
        shared_secret = mafiles[username]['shared_secret']
        print(n+1, username, password, shared_secret)
        start_steam_client(username, password, shared_secret)
        time.sleep(5)


if __name__ == '__main__':
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        exit()
