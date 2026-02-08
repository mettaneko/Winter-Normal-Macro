import sys
import subprocess
import os
import json
import re
import time

UPDATE_SCRIPT = "update.py"
POSITION_SCRIPT = "Position.py"
MACRO_ORIGINAL = "Winter_Event.py"
MACRO_TEMP_RUN = "Winter_Event_Run.py"
SETTINGS_FILE = "settings.json"

def run_wait(name):
    if os.path.exists(name):
        print(f"> Running {name}...")
        subprocess.Popen([sys.executable, name]).wait()

def main():
    run_wait(UPDATE_SCRIPT)
    run_wait(POSITION_SCRIPT)
    if not os.path.exists(MACRO_ORIGINAL):
        print(f"Error: {MACRO_ORIGINAL} missing.")
        return

    try:
        with open(MACRO_ORIGINAL, 'r', encoding='utf-8') as f:
            content = f.read()

        if os.path.exists(SETTINGS_FILE):
            print("> Patching settings...")
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            for key, val in settings.items():
                pattern = rf"^{key}\s*=\s*.*"
                if re.search(pattern, content, flags=re.MULTILINE):
                    content = re.sub(pattern, f"{key} = {repr(val)}", content, flags=re.MULTILINE)

        with open(MACRO_TEMP_RUN, 'w', encoding='utf-8') as f:
            f.write(content)

        print("> Switching to Macro...")
        os.execl(sys.executable, sys.executable, MACRO_TEMP_RUN)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
