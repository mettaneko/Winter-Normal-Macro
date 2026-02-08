import sys
import subprocess
import os
import json
import re
import time
import urllib.request

UPDATE_SCRIPT = "update.py"
POSITION_SCRIPT = "Position.py"
MACRO_ORIGINAL = "Winter_Event.py"
MACRO_TEMP_RUN = "Winter_Event_Run.py"
SETTINGS_FILE = "settings.json"

DISCORD_CLIENT_ID = "1470090515755171911"
DEFAULT_EXIT_KEY = "z"

def run_wait(name):
    if os.path.exists(name):
        print(f"> {name}...")
        subprocess.Popen([sys.executable, name]).wait()

def ensure_pip():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("> PIP not found. Installing PIP...")
        try:
            get_pip_path = "get-pip.py"
            urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip_path)
            subprocess.check_call([sys.executable, get_pip_path], stdout=subprocess.DEVNULL)
            os.remove(get_pip_path)
            print("> PIP installed successfully.")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to install pip: {e}")
            input("Press Enter to exit...")
            sys.exit(1)

def install_deps():
    ensure_pip()

    required = ["keyboard", "pypresence", "requests"]
    to_install = []
    
    for lib in required:
        try:
            __import__(lib)
        except ImportError:
            to_install.append(lib)

    if to_install:
        print(f"> Installing libraries: {', '.join(to_install)}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *to_install, '--no-warn-script-location'], stdout=subprocess.DEVNULL)

def main():
    install_deps()
    import keyboard

    # 1. Update & Position
    run_wait(UPDATE_SCRIPT)
    run_wait(POSITION_SCRIPT)

    if not os.path.exists(MACRO_ORIGINAL):
        print(f"Error: {MACRO_ORIGINAL} missing.")
        return

    try:
        with open(MACRO_ORIGINAL, 'r', encoding='utf-8') as f:
            content = f.read()

        exit_key = DEFAULT_EXIT_KEY
        if os.path.exists(SETTINGS_FILE):
            print("> Patching settings...")
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            exit_key = settings.pop("EXIT_HOTKEY", DEFAULT_EXIT_KEY)

            for key, val in settings.items():
                pattern = rf"^{key}\s*=\s*.*"
                if re.search(pattern, content, flags=re.MULTILINE):
                    content = re.sub(pattern, f"{key} = {repr(val)}", content, flags=re.MULTILINE)

        BUTTON_LABEL = "Download Macro"
        BUTTON_URL = "https://github.com/mettaneko/Winter-Normal-Macro"

        print("> Injecting RPC...")
        rpc_code = f"""
import threading, time, sys, os
def _rpc():
    try:
        from pypresence import Presence
        # Подключаемся
        RPC = Presence("{DISCORD_CLIENT_ID}")
        RPC.connect()
        
        start = time.time()
        while True:
            try:
                RPC.update(
                    state="Farming...",             # Вторая строка статуса
                    details="AV Winter Event Mango",   # Первая строка (жирная)
                    start=start,                    # Время (00:01 elapsed)
                    large_image="logo",             # Имя картинки в Assets (должно быть загружено!)
                    large_text="v2.0",              # Текст при наведении на картинку
                    buttons=[
                        {{"label": "{BUTTON_LABEL}", "url": "{BUTTON_URL}"}}
                    ]
                )
            except Exception as e:
                pass
                
            time.sleep(15)
    except Exception as e:
        pass
rpc_thread = threading.Thread(target=_rpc, daemon=True)
rpc_thread.start()
"""

        content = rpc_code + "\n" + content

        with open(MACRO_TEMP_RUN, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n[MAIN] RUNNING. Press '{exit_key.upper()}' to FULLY STOP & EXIT.")
        proc = subprocess.Popen([sys.executable, MACRO_TEMP_RUN])

        while True:
            if proc.poll() is not None:
                print("\n> Macro closed.")
                break
            if keyboard.is_pressed(exit_key):
                print(f"\n> EXIT KEY pressed. Stopping...")
                proc.kill()
                break
            time.sleep(0.05)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(MACRO_TEMP_RUN):
            try:
                for _ in range(20): 
                    os.remove(MACRO_TEMP_RUN)
                    break
            except: pass
        time.sleep(0.5)

if __name__ == "__main__":
    main()
