import win32gui
import win32api
import win32com.client
import win32con
import time
import os
import utils
from steampy.guard import generate_one_time_code
import config


def start_steam_client(username, password, shared_secret):
    # Запускаем аккаунт
    os.system(
        f'start "" "{config.steam_path}" '
        f'-noverifyfiles -noreactlogin -no-browser '
        f'-login {username} {password} -language english -applaunch 730 -low -nohltv -nosound -novid '
        f'-window -nomouse -w 640 -h 480 +connect {config.server_ip} +exec autoexec.cfg -x 0 -y 0'
    )

    win_name = 'Steam Guard - Computer Authorization Required'
    success = False
    while not success:
        hwnd = win32gui.FindWindowEx(None, None, None, win_name)
        if hwnd:
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')  # Активируем окно
            # print(f'Hwnd: {guard_win_hwnd}')
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(1.5)
            guard_code = generate_one_time_code(shared_secret)
            print(f'Guard for account {username}: {guard_code}')
            for char in guard_code:
                char_code = utils.VK_CODE[char.lower()]
                win32api.SendMessage(hwnd, win32con.WM_CHAR, char_code, 0)
            win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, utils.VK_CODE['enter'], 0)
            success = True
