import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
LEGACY_DIR = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/Archive/Legacy_Analysis_Folders/Unified_Phylogenetic_Tree_Collection/Simultaneous_Analysis")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" # Most likely location for Arial Bold on Mac

def update_titles():
    if not os.path.exists(LEGACY_DIR):
        print(f"Error: {LEGACY_DIR} not found.")
        return

    for root, dirs, files in os.walk(LEGACY_DIR):
        for f in files:
            if not f.endswith(".png"): continue
            
            # Extract info from filename (e.g., Amborella_trichopoda_ClustalO_NJ.png)
            parts = f.replace(".png", "").split("_")
            if len(parts) < 3: continue # Skip if naming doesn't match
            
            # Heuristic to find Species vs Algo vs Method
            # Species is usually the first few parts
            method = parts[-1] 
            algo_raw = parts[-2]
            species_raw = " ".join(parts[:-2])
            
            # Mapping
            method_map = {
                "NJ": "tree (NJ)",
                "Bayes": "tree (Bayesian)",
                "ML": "tree (Maximum Likelihood)"
            }
            algo_map = {
                "ClustalO": "Clustal Omega",
                "MAFFT": "MAFFT",
                "MUSCLE": "MUSCLE"
            }
            
            method_text = method_map.get(method, f"tree ({method})")
            algo_text = algo_map.get(algo_raw, algo_raw)
            species_text = species_raw.replace("_", " ")
            
            title_text = f"{species_text} - {algo_text} | {method_text}"
            
            # Image Processing
            img_path = os.path.join(root, f)
            try:
                img = Image.open(img_path)
                draw = ImageDraw.Draw(img)
                
                # 1. Wipe old title (top ~250 pixels)
                draw.rectangle([0, 0, img.width, 250], fill="white")
                
                # 2. Draw new title
                try:
                    font = ImageFont.truetype(FONT_PATH, 120)
                except:
                    font = ImageFont.load_default()
                
                # Calculate text position (Centered)
                bbox = draw.textbbox((0, 0), title_text, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                x = (img.width - w) // 2
                y = 80 # Vertical margin
                
                draw.text((x, y), title_text, fill="black", font=font)
                
                img.save(img_path)
                print(f"Updated: {f} -> {title_text}")
            except Exception as e:
                print(f"Failed to update {f}: {e}")

if __name__ == "__main__":
    update_titles()
