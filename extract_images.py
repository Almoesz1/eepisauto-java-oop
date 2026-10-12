import json
import re
import os
import base64
import io
from PIL import Image

fpath = r"C:\Users\musto\.gemini\antigravity\brain\8057df29-e5b1-42be-9daf-f109f1bece7c\.system_generated\logs\transcript_full.jsonl"
if not os.path.exists(fpath):
    fpath = r"C:\Users\musto\.gemini\antigravity\brain\8057df29-e5b1-42be-9daf-f109f1bece7c\.system_generated\logs\transcript.jsonl"

out_dir = r"d:\PraktikumOOP\EepisAutoGUI\ppt_assets"
os.makedirs(out_dir, exist_ok=True)

with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

print("Read lines:", len(lines))
# search backwards for user prompt containing <!DOCTYPE html>
html_content = ""
for line in reversed(lines):
    if "DOCTYPE html" in line:
        try:
            data = json.loads(line)
            html_content = data.get("content", "")
            break
        except Exception:
            pass

print("HTML content found length:", len(html_content))

# Extract all images with their alt attribute
# Pattern: src='data:image/webp;base64,...' alt="..."
pattern = re.compile(r"src=['\"]data:image/webp;base64,([^'\"]+)['\"][^>]*alt=['\"]([^'\"]+)['\"]", re.DOTALL)
matches = pattern.findall(html_content)

if not matches:
    # try alt before src
    pattern2 = re.compile(r"alt=['\"]([^'\"]+)['\"][^>]*src=['\"]data:image/webp;base64,([^'\"]+)['\"]", re.DOTALL)
    m2 = pattern2.findall(html_content)
    matches = [(src, alt) for alt, src in m2]

print("Matches found:", len(matches))

for i, (b64, alt) in enumerate(matches):
    try:
        raw = base64.b64decode(b64)
        im = Image.open(io.BytesIO(raw))
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', alt).lower()
        out_file = os.path.join(out_dir, f"{i+1}_{clean_name}.png")
        im.save(out_file, "PNG")
        print(f"Saved [{i+1}] {alt} -> {out_file} (Size: {im.size})")
    except Exception as e:
        print(f"Error {i+1}: {e}")
