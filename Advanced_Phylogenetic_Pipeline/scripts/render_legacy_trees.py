#!/usr/bin/env python3
"""
Finalized renderer for legacy trees.
Includes:
1. Exact filenames in titles.
2. Fully functional legend with subclade swatches.
3. Support for anchored AT IDs.
"""
import os, csv, re
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from ete3 import Tree, TreeStyle, NodeStyle, TextFace, faces
from PIL import Image, ImageDraw, ImageFont

# ─────────────────────────────────────────────────────────────
CLADE_COLORS = {
    "AP1/FUL/CAL":   "#E74C3C",
    "SEP/AGL2-like": "#E67E22",
    "AGL17/ANR1":    "#82E0AA",
    "SHP/STK/AG":    "#2980B9",
    "FLC/MAF":       "#8E44AD",
    "SOC1/AGL20":    "#E91E8C",
    "AGL15/AGL18":   "#1ABC9C",
    "AGL22/AGL24":   "#F4D03F",
    "AP3/PI":        "#27AE60",
    "AGL104/AGL66":  "#C0392B",
    "AGL12":         "#5D6D7E",
    "Unknown":       "#BDC3C7",
}

ROOT_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
ADV_DIR  = os.path.join(ROOT_DIR, "Advanced_Phylogenetic_Pipeline")
ANN_FILE = os.path.join(ADV_DIR, "4.Visualization_Portfolio/Annotation_Tables/MIKCc_Subclade_Annotation_Table.tsv")
LEGACY_DIR = os.path.join(ADV_DIR, "Archive/Legacy_Analysis_Folders/Simultaneous_Phylogenetic_Analysis/Results")
TREE_DIR = os.path.join(LEGACY_DIR, "Trees_Anchored")
OUT_DIR  = os.path.join(LEGACY_DIR, "Images")
os.makedirs(OUT_DIR, exist_ok=True)

# Arabidopsis MIKCc gene → Subclade mapping (hardcoded fallback)
AT_TO_CLADE = {
    "AT1G69120": "AP1/FUL/CAL", "AT1G24260": "AP1/FUL/CAL", "AT5G61850": "AP1/FUL/CAL",
    "AT4G36590": "AP1/FUL/CAL", "AT2G45650": "AP1/FUL/CAL", "AT5G20240": "AP1/FUL/CAL",
    "AT5G60910": "AP1/FUL/CAL", "AT3G02310": "SEP/AGL2-like", "AT1G24500": "SEP/AGL2-like",
    "AT2G03710": "SEP/AGL2-like", "AT1G67060": "SEP/AGL2-like", "AT4G22950": "SEP/AGL2-like",
    "AT3G61120": "SEP/AGL2-like", "AT2G03060": "SEP/AGL2-like", "AT5G15800": "SEP/AGL2-like",
    "AT4G18960": "AGL17/ANR1", "AT3G61890": "AGL17/ANR1", "AT3G57230": "AGL17/ANR1",
    "AT5G13790": "AGL17/ANR1", "AT2G14210": "AGL17/ANR1", "AT3G54340": "SHP/STK/AG",
    "AT2G42830": "SHP/STK/AG", "AT3G58780": "SHP/STK/AG", "AT4G09960": "SHP/STK/AG",
    "AT5G10140": "FLC/MAF", "AT3G05390": "FLC/MAF", "AT1G77080": "FLC/MAF",
    "AT3G65060": "FLC/MAF", "AT5G65070": "FLC/MAF", "AT5G65060": "FLC/MAF",
    "AT5G48670": "FLC/MAF", "AT5G65050": "FLC/MAF", "AT2G45660": "SOC1/AGL20",
    "AT5G62165": "SOC1/AGL20", "AT1G77760": "SOC1/AGL20", "AT2G22540": "SOC1/AGL20",
    "AT4G37940": "SOC1/AGL20", "AT1G18750": "SOC1/AGL20", "AT3G57390": "AGL15/AGL18",
    "AT3G22380": "AGL15/AGL18", "AT1G22130": "AGL15/AGL18", "AT3G30260": "AGL15/AGL18",
    "AT4G24540": "AGL22/AGL24", "AT1G26310": "AGL22/AGL24", "AT1G79840": "AP3/PI",
    "AT2G40080": "AP3/PI", "AT5G23260": "AP3/PI", "AT1G48150": "AGL104/AGL66",
    "AT4G16900": "AGL104/AGL66", "AT1G77990": "AGL104/AGL66", "AT1G60920": "AGL104/AGL66",
    "AT1G77980": "AGL104/AGL66", "AT1G71692": "AGL12"
}

def load_annotations():
    ann = {}
    if not os.path.exists(ANN_FILE):
        return {}
    with open(ANN_FILE) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            gid = row["Gene_ID"].strip()
            key = re.sub(r'[.\-\s]', '_', gid)
            ann[key] = ann[gid] = {
                "subclade": row.get("Subclade", "Unknown"),
                "species":  row.get("Species", ""),
            }
    return ann

def make_pastel(hex_str, factor=0.7):
    hex_str = hex_str.lstrip('#')
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def draw_tree(nwk_path, out_name, all_ann):
    try:
        t = Tree(nwk_path, format=1)
    except:
        try: t = Tree(nwk_path)
        except Exception as e:
            print(f"Error loading {nwk_path}: {e}")
            return

    ts = TreeStyle()
    ts.mode = "c"
    ts.show_leaf_name = False
    ts.margin_top = 200
    ts.margin_bottom = 200
    ts.margin_left = 200
    ts.margin_right = 1100
    ts.draw_guiding_lines = True
    
    # EXACT FILENAME IN TITLE
    title_text = os.path.basename(nwk_path).replace(".treefile","").replace(".nwk","")
    title = TextFace(f" {title_text}", fsize=22, bold=True)
    ts.title.add_face(title, column=0)

    for leaf in t.get_leaves():
        raw = leaf.name
        key = re.sub(r'[.\-\s]', '_', raw) if raw else ""
        info = all_ann.get(raw) or all_ann.get(key)
        
        clade = "Unknown"
        if raw and "AT" in raw:
            at_match = re.search(r'AT[1-5]G\d{5}', raw.upper())
            if at_match:
                base = at_match.group(0)
                clade = AT_TO_CLADE.get(base, "Unknown")
        else:
            clade = info["subclade"] if info else "Unknown"
        
        leaf.add_features(my_clade=clade)

    for leaf in t.get_leaves():
        raw = leaf.name
        clade = leaf.my_clade
        color = CLADE_COLORS.get(clade, "#BDC3C7")
        # Fade the AT anchors slightly to highlight the target species
        display_color = make_pastel(color, 0.75) if "AT" in raw.upper() else color

        nstyle = NodeStyle()
        nstyle["size"] = 0
        leaf.set_style(nstyle)
        
        face = TextFace(f" {raw} ", fsize=8, bold=True)
        face.background.color = display_color
        leaf.add_face(face, column=0, position="aligned")

    out_path = os.path.join(OUT_DIR, f"{out_name}.png")
    t.render(out_path, w=4000, units="px", dpi=300, tree_style=ts)
    
    # ── ADVANCED LEGEND DRAWING (PIL) ──
    try:
        img = Image.open(out_path)
        draw = ImageDraw.Draw(img)
        
        # Legend Box Dimensions
        box_w, box_h = 800, 850
        x0 = img.width - box_w - 100
        y0 = 100
        
        # Background
        draw.rectangle([x0, y0, x0 + box_w, y0 + box_h], fill="white", outline="black", width=5)
        
        # Font Configuration
        try:
            f_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
            f_text = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 35)
        except:
            f_title = f_text = ImageFont.load_default()
            
        draw.text((x0 + 40, y0 + 30), "Subclade Legend", fill="black", font=f_title)
        
        curr_y = y0 + 120
        for name, color in CLADE_COLORS.items():
            if name == "Unknown": continue
            # Swatch
            draw.rectangle([x0 + 40, curr_y, x0 + 100, curr_y + 40], fill=color, outline="black", width=2)
            # Label
            draw.text((x0 + 130, curr_y), name, fill="black", font=f_text)
            curr_y += 65
            
        img.save(out_path)
    except Exception as e:
        print(f"  Warning: Legend drawing failed: {e}")
        
    print(f"  Saved image: {out_path}")

print("Loading annotations...")
all_annotations = load_annotations()

for root, dirs, files in os.walk(TREE_DIR):
    for f in files:
        if f.endswith(".treefile") or f.endswith(".nwk"):
            full_path = os.path.join(root, f)
            print(f"Rendering {f}...")
            draw_tree(full_path, f.replace(".treefile","").replace(".nwk",""), all_annotations)
