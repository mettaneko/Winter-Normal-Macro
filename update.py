import os
import sys
import zipfile
import io
import time

try: import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'], stdout=subprocess.DEVNULL)
    os.execl(sys.executable, sys.executable, *sys.argv)

LOADER_REPO = "https://github.com/mettaneko/Winter-Normal-Macro/archive/refs/heads/main.zip"
MACRO_REPO = "https://github.com/loxersoun2369189-wq/Winter-Normal-Macro/archive/refs/heads/main.zip"

LOADER_FILES = {"main.py", "update.py"}

MACRO_IGNORE = {
    "README.md", "README.txt", "settings.json", 
    "main.py", "update.py", "Winter_Event_Run.py", "get-pip.py", ".gitignore"
}
IGNORE_PREFIXES = ("Python/", "__pycache__/", ".git/") 

def download_and_extract(url, target_files=None, ignore_files=None, is_loader=False):
    root = os.path.dirname(os.path.abspath(__file__))
    updated = False
    
    try:
        r = requests.get(url)
        r.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            repo_root = z.namelist()[0].split('/')[0]
            
            for m in z.infolist():
                if m.is_dir() or not m.filename.startswith(repo_root): continue
                
                rel_path = m.filename[len(repo_root)+1:]
                filename = os.path.basename(rel_path)
                
                if not rel_path: continue

                if any(rel_path.startswith(prefix) for prefix in IGNORE_PREFIXES):
                    continue

                if target_files and filename not in target_files: continue
                if ignore_files and filename in ignore_files: continue
                
                dest = os.path.join(root, rel_path)
                
                if is_loader and filename == "main.py" and os.path.exists(dest):
                    if os.path.getsize(dest) != m.file_size:
                        try:
                            old = dest + ".old"
                            if os.path.exists(old): os.remove(old)
                            os.rename(dest, old)
                            updated = True
                            print(f"  [UPD] {filename} (Self-update)")
                        except OSError: continue
                    else: continue

                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, 'wb') as f:
                    f.write(z.read(m.filename))
                    
    except Exception as e:
        print(f"Download error ({url}): {e}")
        return False
        
    return updated

def update():
    print("> Checking Loader updates...")
    if download_and_extract(LOADER_REPO, target_files=LOADER_FILES, is_loader=True):
        print("\n[INFO] LOADER UPDATED. RESTARTING...")
        time.sleep(2)
        os.execl(sys.executable, sys.executable, "main.py")

    print("> Checking Macro updates...")
    download_and_extract(MACRO_REPO, ignore_files=MACRO_IGNORE)
    
    print("> Update check complete.")

if __name__ == "__main__":
    update()
