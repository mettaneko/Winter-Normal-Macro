import os
import sys
import zipfile
import io
import time

# Auto-install requests silently
try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'], stdout=subprocess.DEVNULL)
    os.execl(sys.executable, sys.executable, *sys.argv)

REPO = "https://github.com/loxersoun2369189-wq/Winter-Normal-Macro"
ZIP_URL = f"{REPO}/archive/refs/heads/main.zip"

IGNORED = {"README.md", "README.txt", os.path.basename(__file__), "settings.json"}

def update():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print("Checking for updates...")

    try:
        r = requests.get(ZIP_URL)
        r.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            repo_root = z.namelist()[0].split('/')[0]
            
            for m in z.infolist():
                if m.is_dir() or not m.filename.startswith(repo_root): continue
                
                rel_path = m.filename[len(repo_root)+1:]
                if not rel_path or os.path.basename(rel_path) in IGNORED: continue

                path = os.path.join(root_dir, rel_path)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                
                with open(path, 'wb') as f:
                    f.write(z.read(m.filename))
        
        print("Update complete.")
        
    except Exception as e:
        print(f"Update failed: {e}")
        time.sleep(2)

if __name__ == "__main__":
    update()
