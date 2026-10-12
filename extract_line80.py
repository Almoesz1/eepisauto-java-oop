import json
import re
import os
import base64
import io
from PIL import Image

path = r"C:\Users\musto\.gemini\antigravity\brain\8057df29-e5b1-42be-9daf-f109f1bece7c\.system_generated\logs\transcript_full.jsonl"
out_dir = r"d:\PraktikumOOP\EepisAutoGUI\ppt_assets"
os.makedirs(out_dir, exist_ok=True)

with open(path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

print("Inspecting line 80...")
obj = json.loads(lines[80])
content = obj.get("content", "")
print("Content length of line 80:", len(content))

# regex for base64 webp
# <img src='data:image/webp;base64,...' alt="..."
pattern = re.compile(r"src=['\"]data:image/webp;base64,([^'\"]+)['\"][^>]*alt=['\"]([^'\"]+)['\"]")
matches = pattern.findall(content)
print("Matches found:", len(matches))

for i, (b64, alt) in enumerate(matches):
    try:
        raw = base64.b64decode(b64)
        im = Image.open(io.BytesIO(raw))
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', alt).lower()
        out_file = os.path.join(out_dir, f"{i+1}_{clean_name}.png")
        im.save(out_file, "PNG")
        print(f"Saved: {alt} -> {out_file} (Size: {im.size})")
    except Exception as e:
        print(f"Error {i+1}: {e}")
