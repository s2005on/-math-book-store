#!/usr/bin/env python3
"""Windows/Linux/macOS local launcher. No credentials embedded in the package."""
from __future__ import annotations

import getpass
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / '.venv'
VENV_PY = VENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
URL = 'http://127.0.0.1:8017/'


def installed() -> bool:
    return subprocess.call([str(VENV_PY), '-c', 'import fastapi,uvicorn,multipart,PIL,dotenv'],
                           cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL) == 0


def main() -> int:
    if sys.version_info < (3,11):
        print('Can Python 3.11+ de chay. Vui long cai Python ban moi.')
        return 1
    if '--ready' not in sys.argv:
        if not VENV_PY.is_file():
            print('[1/4] Tao moi truong Python rieng...')
            subprocess.run([sys.executable,'-m','venv',str(VENV)],check=True,cwd=ROOT)
        else:
            print('[1/4] Da co moi truong Python.')
        if not installed():
            print('[2/4] Cai thu vien (lan dau can ket noi Internet)...')
            subprocess.run([str(VENV_PY),'-m','pip','install','-r',str(ROOT/'server/requirements.txt')],check=True,cwd=ROOT)
        else:
            print('[2/4] Thu vien da duoc cai.')
        # Every package import from here onwards uses the Python inside .venv.
        return subprocess.call([str(VENV_PY),str(ROOT/'start.py'),'--ready'],cwd=ROOT)

    from server.app import database, pw_hash
    with database() as db:
        exists=db.execute("SELECT 1 FROM users WHERE role='admin' LIMIT 1").fetchone()
    if not exists:
        print('\n[3/4] Tao tai khoan QUAN TRI (lan dau)')
        while True:
            username=input('Ten dang nhap (3-60 ky tu a-z, 0-9, _): ').strip().lower()
            if re.fullmatch(r'[a-z0-9_]{3,60}',username):
                break
            print('Ten dang nhap khong hop le.')
        while True:
            password=getpass.getpass('Mat khau (toi thieu 12 ky tu): ')
            repeat=getpass.getpass('Nhap lai mat khau: ')
            if password==repeat and len(password)>=12:
                break
            print('Mat khau khong khop hoac chua du 12 ky tu.')
        with database() as db:
            if db.execute('SELECT 1 FROM users WHERE username=?',(username,)).fetchone():
                print('Tai khoan da ton tai. Hay chon ten khac hoac sao luu/xu ly du lieu.')
                return 1
            db.execute("INSERT INTO users(username,password,role) VALUES(?,?, 'admin')",
                       (username,pw_hash(password)))
        print('Da tao admin. Mat khau CHI luu duoi dang ma bam trong SQLite.')
    else:
        print('[3/4] Tai khoan admin da duoc cau hinh.')

    print('[4/4] Khoi dong website...')
    process=subprocess.Popen([str(VENV_PY),'-m','uvicorn','server.app:app',
                              '--host','127.0.0.1','--port','8017'],cwd=ROOT)
    ok=False
    for _ in range(28):
        if process.poll() is not None:
            break
        try:
            with urllib.request.urlopen(URL+'health',timeout=.8) as resp:
                if resp.status==200:
                    ok=True
                    break
        except (urllib.error.URLError,TimeoutError,OSError):
            time.sleep(.35)
    if not ok:
        if process.poll() is None: process.terminate()
        print('Khong khoi dong duoc website; thuong do cong 8017 dang ban. Xem thong bao loi o tren.')
        return 1
    print('\nWebsite: '+URL)
    print('Quan tri: '+URL+'admin.html')
    print('Du lieu luu trong: '+str(ROOT/'server/data'))
    print('Giu cua so nay mo khi dung website. Nhan Ctrl+C de dung.')
    webbrowser.open(URL)
    try:
        return process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait(timeout=5)
        return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print('Loi cai dat Python / thu vien, vui long kiem tra ket noi Internet.')
        raise SystemExit(exc.returncode or 1)
