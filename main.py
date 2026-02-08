import sys
import subprocess
import os
import json
import re
import time
from collections import OrderedDict

UPDATE_SCRIPT = "update.py"
POSITION_SCRIPT = "Position.py"
MACRO_ORIGINAL = "Winter_Event.py"
MACRO_TEMP_RUN = "Winter_Event_Run.py"
WEBHOOK_FILE = "webhook.py"
SETTINGS_FILE = "settings.json"

DISCORD_CLIENT_ID = "1470090515755171911" 

DEFAULT_SETTINGS = OrderedDict([
    ("WEBHOOK_URL", "paste_ur_url"),
    ("ENABLE_DISCORD_RPC", True),
    ("EXIT_HOTKEY", "z"),            
    ("AUTO_START", False),
    ("USE_NIMBUS", True),
    ("USE_WD", True),
    ("USE_DIO", False),
    ("USE_AINZ_UNIT", ""),
    ("MONARCH_AINZ_PLACEMENT", False),
    ("MAX_UPG_AINZ_PLACEMENT", False),
    ("AINZ_SPELLS", False),
])
# ---------------------------------------------------------

def sync_settings():
    """Читает settings.json, добавляет недостающее из DEFAULT, сохраняет обратно."""
    current = {}
    
    # 1. Читаем текущий файл
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                current = json.load(f)
        except:
            print("> [WARN] Settings file corrupted. Recreating.")
            current = {}

    new_settings = DEFAULT_SETTINGS.copy()
    changed = False
    
    for key, default_val in DEFAULT_SETTINGS.items():
        if key in current:
            new_settings[key] = current[key]
        else:
            changed = True
    for key, val in current.items():
        if key not in new_settings:
            new_settings[key] = val

    if changed or not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_settings, f, indent=4, ensure_ascii=False)
        print("> Settings updated.")
        
    return new_settings

def run_wait(name):
    if os.path.exists(name):
        print(f"> {name}...")
        subprocess.Popen([sys.executable, name]).wait()

def install_deps():
    try: import keyboard; import pypresence
    except ImportError: 
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'keyboard', 'pypresence'], stdout=subprocess.DEVNULL)

def patch_file(filepath, settings):
    """Патчит файл (например, webhook.py)"""
    if not os.path.exists(filepath): return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    patched = False
    for key, val in settings.items():
        pattern = rf"^{key}\s*=\s*.*"
        if re.search(pattern, content, flags=re.MULTILINE):
            content = re.sub(pattern, f"{key} = {repr(val)}", content, flags=re.MULTILINE)
            patched = True
            
    if patched:
        print(f"> Patched {os.path.basename(filepath)}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    install_deps()
    import keyboard

    settings = sync_settings()
    
    exit_key = settings.get("EXIT_HOTKEY", "end") 
    
    run_wait(UPDATE_SCRIPT)
    run_wait(POSITION_SCRIPT)

    if not os.path.exists(MACRO_ORIGINAL):
        print(f"Error: {MACRO_ORIGINAL} missing.")
        return

    try:
        if os.path.exists(WEBHOOK_FILE):
             patch_file(WEBHOOK_FILE, settings)
             
        with open(MACRO_ORIGINAL, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for key, val in settings.items():
            pattern = rf"^{key}\s*=\s*.*"
            if re.search(pattern, content, flags=re.MULTILINE):
                content = re.sub(pattern, f"{key} = {repr(val)}", content, flags=re.MULTILINE)

        if settings.get("ENABLE_DISCORD_RPC", True):
            rpc_code = f"""
import threading, time, sys
def _rpc():
    try:
        from pypresence import Presence
        RPC = Presence("{DISCORD_CLIENT_ID}")
        RPC.connect()
        start = time.time()
        while True:
            try:
                RPC.update(state="Farming...", details="AV Winter Event Mango", start=start, large_image="logo")
            except: pass
            time.sleep(15)
    except: pass
threading.Thread(target=_rpc, daemon=True).start()
"""
            content = rpc_code + "\n" + content
        else:
            print("> Discord RPC is disabled.")

        with open(MACRO_TEMP_RUN, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n[MAIN] RUNNING. Press '{exit_key.upper()}' to EXIT.")
        proc = subprocess.Popen([sys.executable, MACRO_TEMP_RUN])

        while True:
            if proc.poll() is not None:
                print("\n> Macro closed.")
                break
            if keyboard.is_pressed(exit_key):
                print(f"\n> EXIT.")
                proc.kill()
                break
            time.sleep(0.05)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(MACRO_TEMP_RUN):
            try: os.remove(MACRO_TEMP_RUN)
            except: pass
        time.sleep(0.5)

if __name__ == "__main__":
    main()
