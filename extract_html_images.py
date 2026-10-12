import re
import os
import base64
import io
from PIL import Image
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def extract_images_from_transcript():
    transcript_path = r"C:\Users\musto\.gemini\antigravity\brain\8057df29-e5b1-42be-9daf-f109f1bece7c\.system_generated\logs\transcript.jsonl"
    out_dir = r"d:\PraktikumOOP\EepisAutoGUI\ppt_assets"
    os.makedirs(out_dir, exist_ok=True)
    
    saved_images = {}
    if os.path.exists(transcript_path):
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Cari semua alt dan src base64
        # pattern: alt="([^"]+)" ... src='data:image/webp;base64,([^']+)'
        # atau src='data:image/webp;base64,([^']+)' ... alt="([^"]+)"
        img_tags = re.findall(r"<img\s+src=[\x27\"]data:image/webp;base64,([^\x27\"]+)[\x27\"]\s+alt=[\x27\"]([^\x27\"]+)[\x27\"]", content)
        if not img_tags:
            # format kebalikannya
            img_tags = [(src, alt) for alt, src in re.findall(r"<img\s+alt=[\x27\"]([^\x27\"]+)[\x27\"]\s+src=[\x27\"]data:image/webp;base64,([^\x27\"]+)[\x27\"]", content)]
        
        for idx, (b64data, alt_name) in enumerate(img_tags):
            try:
                raw_bytes = base64.b64decode(b64data)
                img = Image.open(io.BytesIO(raw_bytes))
                clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', alt_name).lower()
                img_file = os.path.join(out_dir, f"{idx+1}_{clean_name}.png")
                img.save(img_file, "PNG")
                saved_images[alt_name.strip()] = img_file
                print(f"Extracted: {alt_name} -> {img_file}")
            except Exception as e:
                print(f"Error extracting image {alt_name}: {e}")
                
    return saved_images

print("Starting extraction...")
imgs = extract_images_from_transcript()
print("Images extracted:", len(imgs))
