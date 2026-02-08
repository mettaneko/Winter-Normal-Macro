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
    """Запустить и подождать завершения"""
    if os.path.exists(name):
        print(f"> {name}...")
        subprocess.Popen([sys.executable, name]).wait()

def main():
    # 1. Обновляем и позиционируем
    run_wait(UPDATE_SCRIPT)
    run_wait(POSITION_SCRIPT)

    # 2. Патчим
    if not os.path.exists(MACRO_ORIGINAL):
        print(f"Error: {MACRO_ORIGINAL} missing.")
        time.sleep(3)
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

        # Важный момент: добавляем в конец удаление временного файла ПОСЛЕ завершения работы макроса
        # Так как main.py закроется, он не сможет удалить файл сам. Пусть макрос удалит сам себя (файл).
        cleanup_code = f"\nimport os\ntry:\n    os.remove('{MACRO_TEMP_RUN}')\nexcept: pass"
        # content += cleanup_code  <-- РАСКОММЕНТИРОВАТЬ, если хотите, чтобы файл удалялся после закрытия макроса.
        # Но учтите: Windows может не дать удалить файл, который еще исполняется. Обычно временные файлы оставляют.

        with open(MACRO_TEMP_RUN, 'w', encoding='utf-8') as f:
            f.write(content)

        print("> Launching Macro & Exiting...")
        
        # 3. ЗАПУСК И ВЫХОД
        # CREATE_NEW_CONSOLE (0x00000010) - создает новое окно для макроса
        # DETACHED_PROCESS (0x00000008) - процесс отвязан от консоли (если нужно совсем скрытно)
        # Используем просто Popen, скрипт завершится, а процесс останется жить.
        subprocess.Popen([sys.executable, MACRO_TEMP_RUN], creationflags=subprocess.CREATE_NEW_CONSOLE)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
