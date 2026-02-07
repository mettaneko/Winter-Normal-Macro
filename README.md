

---

# Winter-Normal-Macro
An Anime Vanguards macro for the **Winter Normal** LTM mode.
This is a **personal** project so if something breaks you might have to fix/tweak it yourself!

---

## Overview
This folder contains **updated Python files** for the Winter event so new QoL changes and fixes can be released quickly.  
Make sure you also copy the **new images** from the `resources` folder.

For the rest of the required files, download the base package here:  
https://mega.nz/file/CphzFRiR#s5_-7hDLLsRpXCn5DjvZ6p9ZT-V0tVR8_sHXh21uiZM

After downloading, **replace the old files** in that package with the updated ones from this repo.

**Important:**  
Inside the `Tools` folder, open `avMethods.py` and **remove**:

```python
print(restart_match())
```

---

## Common Fixes
Mega downloads can occasionally corrupt files, which breaks either **Python** or **Tesseract**.

### Tesseract issues
If Tesseract stops working or the macro can’t detect text:

- Re‑download the files and unzip again, **or**
- Install a clean version of Tesseract from:  
  https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0  
- Clear the old Tesseract folder before installing
- Optionally add the **Tesseract directory** (not the exe) to your system PATH

### Python issues
If Python fails to run or packages are missing:

- Install a clean Python **3.13.11**
- Install the required packages listed here:  
  https://pastebin.com/mS2xFd3m

---

## Recent Updates

### Added best loss detection
Detecting loss now will restart the program, with the new auto_start feature it will completely let you restart if you lose at any point! Also made the stop key work

### Added full nimbus support
```python
USE_NIMBUS = True # Use the nimbus cloud instead of newsman (more consistent + better)
```
### Click‑to‑Move (CTM) support
For direction 1 and 2
Roblox’s built‑in pathing is now supported.  
Useful for **low‑end devices**, **lag**, or **high ping**.

Use CTM like this:

```python
directions('1', CTM=True)
# or
directions('1', 'rabbit', CTM=True)
```

### Caloric Stone unit selection
You can now choose **any unit** to place with Caloric Stone.

```python
USE_WD = True          # Use World Destroyer
USE_DIO = False        # Use built‑in DIO logic instead
USE_AINZ_UNIT = ""     # Name of the unit to place
```

### Monarch + Auto‑Upgrade logic
```python
MONARCH_AINZ_PLACEMENT = False   # Gets monarch for the unit placed with Caloric Stone
MAX_UPG_AINZ_PLACEMENT = False   # True = spam Z for auto-upgrade
                                 # False = upgrade until a specific move is detected
```

### Custom move detection
```python
AINZ_PLACEMENT_MOVE_PNG = "Winter\\YOUR_MOVE.png"
# Take a screenshot of the move, name it YOUR_MOVE.png,
# and the macro will upgrade until it finds that image.
```

---
