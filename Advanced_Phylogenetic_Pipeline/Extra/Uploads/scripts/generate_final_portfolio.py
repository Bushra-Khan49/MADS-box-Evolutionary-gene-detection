import os
import subprocess
import re
from ete3 import Tree, TreeStyle, NodeStyle, TextFace
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
TOOLS = {
    "mafft": "/opt/homebrew/bin/mafft",
    "muscle": "/opt/homebrew/bin/muscle",
    "clustalo": "/opt/homebrew/bin/clustalo",
    "iqtree2": "/opt/homebrew/bin/iqtree2"
}

BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
WORKFLOW_DIR = os.path.join(BASE_DIR, "Workflow_Step-by-Step")
OUTPUT_BASE = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/Uploads/Final_Portfolio_Refined")
ANN_FILE = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/Uploads/MIKCc_Subclade_Annotation_Table.tsv")

# Species Mapping: (Common Name, Task Path)
SPECIES_MAP = {
    "Amborella_trichopoda": os.path.join(WORKFLOW_DIR, "TASK_2/uploads/Atrichopoda_combined_with_AT.fa"),
    "Nymphaea_colorata":    os.path.join(WORKFLOW_DIR, "TASK_3/uploads/Nymphaea_with_AT_Full.fa"),
    "Cinnamomum_kanehirae": os.path.join(WORKFLOW_DIR, "TASK_4/uploads/Cinnamomum_with_AT_Full.fa"),
    "Glycine_max":         os.path.join(WORKFLOW_DIR, "TASK_5/uploads/Glycine_with_AT_Full.fa"),
    "Medicago_truncatula": os.path.join(WORKFLOW_DIR, "TASK_6/uploads/Medicago_with_AT_Full.fa"),
    "Prunus_persica":      os.path.join(WORKFLOW_DIR, "TASK_7/uploads/Prunus_with_AT_Full.fa"),
    "Helianthus_annuus":   os.path.join(WORKFLOW_DIR, "TASK_8/uploads/Helianthus_with_AT_Full.fa"),
    "Nelumbo_nucifera":    os.path.join(WORKFLOW_DIR, "TASK_9/uploads/Nelumbo_with_AT_Full.fa"),
}

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

AT_TO_CLADE = {
    "AT1G69120": "AP1/FUL/CAL", "AT1G24260": "AP1/FUL/CAL", "AT5G61850": "AP1/FUL/CAL",
    "AT4G36590": "AP1/FUL/CAL", "AT2G45650": "AP1/FUL/CAL", "AT5G20240": "AP1/FUL/CAL",
    "AT5G60910": "AP1/FUL/CAL", 
    "AT3G02310": "SEP/AGL2-like", "AT1G24500": "SEP/AGL2-like", "AT2G03710": "SEP/AGL2-like",
    "AT1G67060": "SEP/AGL2-like", "AT4G22950": "SEP/AGL2-like", "AT3G61120": "SEP/AGL2-like",
    "AT2G03060": "SEP/AGL2-like", "AT5G15800": "SEP/AGL2-like",
    "AT4G18960": "AGL17/ANR1", "AT3G61890": "AGL17/ANR1", "AT3G57230": "AGL17/ANR1",
    "AT5G13790": "AGL17/ANR1", "AT2G14210": "AGL17/ANR1",
    "AT3G54340": "SHP/STK/AG", "AT2G42830": "SHP/STK/AG", "AT3G58780": "SHP/STK/AG",
    "AT4G09960": "SHP/STK/AG",
    "AT5G10140": "FLC/MAF", "AT3G05390": "FLC/MAF", "AT1G77080": "FLC/MAF",
    "AT3G65060": "FLC/MAF", "AT5G65070": "FLC/MAF", "AT5G65060": "FLC/MAF",
    "AT5G48670": "FLC/MAF", "AT5G65050": "FLC/MAF",
    "AT2G45660": "SOC1/AGL20", "AT5G62165": "SOC1/AGL20", "AT1G77760": "SOC1/AGL20",
    "AT2G22540": "SOC1/AGL20", "AT4G37940": "SOC1/AGL20", "AT1G18750": "SOC1/AGL20",
    "AT3G57390": "AGL15/AGL18", "AT3G22380": "AGL15/AGL18", "AT1G22130": "AGL15/AGL18",
    "AT3G30260": "AGL15/AGL18",
    "AT4G24540": "AGL22/AGL24", "AT1G26310": "AGL22/AGL24",
    "AT1G79840": "AP3/PI", "AT2G40080": "AP3/PI", "AT5G23260": "AP3/PI",
    "AT1G48150": "AGL104/AGL66", "AT4G16900": "AGL104/AGL66", "AT1G77990": "AGL104/AGL66",
    "AT1G60920": "AGL104/AGL66", "AT1G77980": "AGL104/AGL66",
    "AT1G71692": "AGL12"
}

# --- Utility Functions ---

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

def load_annotations():
    ann = {}
    if not os.path.exists(ANN_FILE): return ann
    import csv
    with open(ANN_FILE) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            gid = row["Gene_ID"].strip()
            ann[gid] = row["Subclade"]
    return ann

def make_pastel(hex_str, factor=0.6):
    hex_str = hex_str.lstrip('#')
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def render_tree(species_name, algo, nwk_path, out_img, ann):
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    try:
        t = Tree(nwk_path, format=1)
    except:
        print(f"Failed to load tree: {nwk_path}")
        return

    ts = TreeStyle()
    ts.mode = 'c'
    ts.show_leaf_name = False
    ts.margin_top = ts.margin_bottom = ts.margin_left = ts.margin_right = 200
    ts.draw_guiding_lines = True
    ts.guiding_lines_color = "#333333"

    for leaf in t.get_leaves():
        raw = leaf.name
        clade = "Unknown"
        if raw.startswith("AT"):
            base = raw.split(".")[0]
            clade = AT_TO_CLADE.get(base, "Unknown")
        else:
            clade = ann.get(raw, "Unknown")
        
        color = CLADE_COLORS.get(clade, "#BDC3C7")
        if raw.startswith("AT"):
            display_color = make_pastel(color, factor=0.65)
        else:
            display_color = color
        
        nstyle = NodeStyle()
        nstyle["size"] = 0
        leaf.set_style(nstyle)
        
        face = TextFace(f" {raw} ", fsize=8, bold=True)
        face.background.color = display_color
        leaf.add_face(face, column=0, position="aligned")

    t.render(out_img, w=4000, units="px", dpi=300, tree_style=ts)
    
    # Post-process with Pillow
    img = Image.open(out_img)
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 100)
        font_legend = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 60)
        font_text = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 50)
    except:
        font_title = font_legend = font_text = ImageFont.load_default()

    full_title = f"{species_name.replace('_',' ')} — {algo} | Maximum Likelihood (ML)"
    bbox = font_title.getbbox(full_title)
    tw = bbox[2] - bbox[0]
    draw.text(((img.width - tw) // 2, 80), full_title, fill="black", font=font_title)

    # Legend
    legend_items = [c for c in CLADE_COLORS.items() if c[0] != "Unknown"]
    row_h, box_w = 70, 450
    box_h = 100 + (len(legend_items) * row_h)
    lx0, ly0 = img.width - box_w - 60, img.height - box_h - 60
    draw.rectangle([lx0, ly0, lx0+box_w, ly0+box_h], fill="white", outline="black", width=6)
    draw.text((lx0 + 40, ly0 + 30), "MIKCc Subclade Legend", fill="black", font=font_legend)
    curr_y = ly0 + 110
    for name, col in legend_items:
        draw.rectangle([lx0 + 20, curr_y, lx0 + 60, curr_y + 40], fill=col, outline="black", width=2)
        draw.text((lx0 + 80, curr_y - 5), name, fill="black", font=font_text)
        curr_y += row_h
    img.save(out_img)

# --- Main Execution ---

annotations = load_annotations()

for species, input_fa in SPECIES_MAP.items():
    if not os.path.exists(input_fa):
        print(f"Skipping {species}, input not found: {input_fa}")
        continue
    
    print(f"\nProcessing {species}...")
    for algo in ["MAFFT", "MUSCLE", "ClustalO"]:
        print(f"  Alignment: {algo}")
        aln_out = os.path.join(OUTPUT_BASE, f"Alignments/{species}_{algo}.fa")
        
        if algo == "MAFFT":
            subprocess.run(f"{TOOLS['mafft']} --auto {input_fa} > {aln_out}", shell=True)
        elif algo == "MUSCLE":
            run_cmd([TOOLS['muscle'], "-in", input_fa, "-out", aln_out])
        elif algo == "ClustalO":
            run_cmd([TOOLS['clustalo'], "-i", input_fa, "-o", aln_out, "--force"])
        
        if not os.path.exists(aln_out): continue
        
        print(f"  Tree: IQ-TREE 2")
        tree_prefix = os.path.join(OUTPUT_BASE, f"Trees/{species}_{algo}")
        run_cmd([TOOLS['iqtree2'], "-s", aln_out, "-m", "LG+G", "-B", "1000", "-T", "AUTO", "--prefix", tree_prefix, "-redo"])
        
        nwk = tree_prefix + ".treefile"
        if os.path.exists(nwk):
            print(f"  Rendering...")
            img_out = os.path.join(OUTPUT_BASE, f"Images/{species}_{algo}_ML_Circular.png")
            render_tree(species, algo, nwk, img_out, annotations)

print("\nDONE!")
