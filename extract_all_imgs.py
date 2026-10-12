import json, re, os, base64, io
from PIL import Image

path = r"C:\Users\musto\.gemini\antigravity\brain\8057df29-e5b1-42be-9daf-f109f1bece7c\.system_generated\logs\transcript_full.jsonl"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()
content = json.loads(lines[80]).get("content", "")

out_dir = r"d:\PraktikumOOP\EepisAutoGUI\ppt_assets"
os.makedirs(out_dir, exist_ok=True)

# Find all <img> tags
img_pattern = re.compile(r"<img\s+([^>]+)>", re.DOTALL)
tags = img_pattern.findall(content)
print("Total img tags found:", len(tags))

for i, tag in enumerate(tags):
    src_match = re.search(r"src=['\"]data:image/webp;base64,([^'\"]+)['\"]", tag)
    alt_match = re.search(r"alt=['\"]([^'\"]*)['\"]", tag)
    if src_match:
        b64 = src_match.group(1)
        alt = alt_match.group(1) if alt_match else f"image_{i+1}"
        raw = base64.b64decode(b64)
        im = Image.open(io.BytesIO(raw))
        clean_alt = re.sub(r'[^a-zA-Z0-9_-]', '_', alt).lower()
        out_file = os.path.join(out_dir, f"{i+1}_{clean_alt}.png")
        im.save(out_file, "PNG")
        print(f"[{i+1}] '{alt}' saved to {out_file} (Size: {im.size})")
