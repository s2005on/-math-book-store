#!/usr/bin/env python3
"""One-command local launcher for Math Book Store."""
from __future__ import annotations
import getpass
import os
import re
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
PYTHON = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
ENV_FILE = ROOT / ".env"
URL = "http://127.0.0.1:8017/"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    if sys.version_info < (3, 11):
        print("Can Python 3.11 tro len. Hay cai Python 3.11+ roi chay lai.")
        return 1

    if not PYTHON.exists():
        print("[1/4] Dang tao moi truong Python rieng...")
        run([sys.executable, "-m", "venv", str(VENV)])

    print("[2/4] Dang cai/cap nhat thu vien (can Internet trong lan dau)...")
    run([str(PYTHON), "-m", "pip", "install", "-r", str(ROOT / "server" / "requirements.txt")])

    from dotenv import dotenv_values, set_key
    config = dotenv_values(ENV_FILE) if ENV_FILE.exists() else {}
    if not config.get("MBS_ADMIN_USER") or not config.get("MBS_ADMIN_PASSWORD"):
        print("\n[3/4] Tao tai khoan quan tri lan dau")
        print("Mat khau toi thieu 12 ky tu. Thong tin duoc luu trong file .env tren may nay.")
        while True:
            username = input("Ten dang nhap quan tri: ").strip().lower()
            if len(username) >= 3 and len(username) <= 60 and re.fullmatch(r"[a-z0-9_]+", username):
                break
            print("Ten dang nhap can 3-60 ky tu, chi gom chu thuong, so va dau gach duoi.")
        while True:
            password = getpass.getpass("Mat khau quan tri: ")
            confirm = getpass.getpass("Nhap lai mat khau: ")
            if len(password) >= 12 and password == confirm:
                break
            print("Mat khau chua du 12 ky tu hoac khong trung nhau. Thu lai.")
        set_key(str(ENV_FILE), "MBS_ADMIN_USER", username)
        set_key(str(ENV_FILE), "MBS_ADMIN_PASSWORD", password)
        print("Da luu cau hinh tai khoan quan tri.")
    else:
        print("[3/4] Da tim thay cau hinh tai khoan quan tri.")

    print("[4/4] Dang khoi dong website...")
    env = os.environ.copy()
    env.update({k: v for k, v in dotenv_values(ENV_FILE).items() if v is not None})
    process = subprocess.Popen(
        [str(PYTHON), "-m", "uvicorn", "server.app:app", "--host", "127.0.0.1", "--port", "8017"],
        cwd=ROOT, env=env,
    )
    time.sleep(2)
    if process.poll() is not None:
        print("Website khong khoi dong duoc. Kiem tra thong bao loi o phia tren.")
        return int(process.returncode or 1)
    print("\nMath Book Store dang chay tai:", URL)
    print("Trang quan tri:", URL + "admin.html")
    print("Nhan Ctrl+C de dung website. Khong dong cua so nay khi dang su dung.")
    webbrowser.open(URL)
    try:
        return process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait()
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        print("\nKhong the cai dat/khoi dong. Hay kiem tra Internet va Python 3.11+.")
        raise SystemExit(error.returncode or 1)
