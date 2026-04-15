import os, csv, re
import subprocess
from ete3 import Tree, TreeStyle, NodeStyle, TextFace, faces
from PIL import Image, ImageDraw, ImageFont

# Set offscreen rendering for headless environment
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# ─────────────────────────────────────────────────────────────
# Professional Color Palette (HSL Tailored)
# ─────────────────────────────────────────────────────────────
CLADE_COLORS = {
    "AP1/FUL/CAL":   "#E74C3C", # Red
    "SEP/AGL2-like": "#E67E22", # Orange
    "AGL17/ANR1":    "#82E0AA", # Light Green
    "SHP/STK/AG":    "#2980B9", # Blue
    "FLC/MAF":       "#8E44AD", # Purple
    "SOC1/AGL20":    "#E91E8C", # Pink
    "AGL15/AGL18":   "#1ABC9C", # Cyan
    "AGL22/AGL24":   "#F4D03F", # Yellow
    "AP3/PI":        "#27AE60", # Bright Green
    "AGL104/AGL66":  "#C0392B", # Dark Red
    "AGL12":         "#5D6D7E", # Slate
    "Unknown":       "#BDC3C7", # Grey
}

# Mapping Arabidopsis IDs to subclades
AT_TO_CLADE = {
    "AT1G69120": "AP1/FUL/CAL", "AT1G24260": "AP1/FUL/CAL", "AT5G60910": "AP1/FUL/CAL",
    "AT3G02310": "SEP/AGL2-like", "AT2G03710": "SEP/AGL2-like", "AT5G15800": "SEP/AGL2-like",
    "AT3G61120": "SEP/AGL2-like", "AT2G03060": "SEP/AGL2-like",
    "AT4G18960": "AGL17/ANR1", "AT3G57230": "AGL17/ANR1", "AT5G13790": "AGL17/ANR1", "AT2G14210": "AGL17/ANR1",
    "AT3G54340": "SHP/STK/AG", "AT2G42830": "SHP/STK/AG", "AT3G58780": "SHP/STK/AG", "AT4G09960": "SHP/STK/AG",
    "AT5G10140": "FLC/MAF", "AT1G77080": "FLC/MAF", "AT5G65050": "FLC/MAF", "AT5G65070": "FLC/MAF",
    "AT2G45660": "SOC1/AGL20", "AT5G62165": "SOC1/AGL20", "AT2G22540": "SOC1/AGL20", "AT4G37940": "SOC1/AGL20",
    "AT3G57390": "AGL15/AGL18", "AT1G22130": "AGL15/AGL18", "AT3G30260": "AGL15/AGL18",
    "AT4G24540": "AGL22/AGL24", "AT1G26310": "AGL22/AGL24",
    "AT5G23260": "AP3/PI", "AT5G20240": "AP3/PI", "AT3G54340": "AP3/PI",
}

# Paths
BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline"
TREE_DIR = os.path.join(BASE_DIR, "3.Phylogeny_Output/Trees_FullLength")
ANN_FILE = os.path.join(BASE_DIR, "Uploads/MIKCc_Subclade_Annotation_Table.tsv")
OUT_DIR  = os.path.join(BASE_DIR, "4.Visualization_Portfolio/Standardized_Trees")
os.makedirs(OUT_DIR, exist_ok=True)

def load_annotations():
    ann = {}
    if not os.path.exists(ANN_FILE):
        return ann
    with open(ANN_FILE) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            gid = row["Gene_ID"].strip()
            ann[gid] = row["Subclade"]
    return ann

def make_pastel(hex_str, factor=0.65):
    hex_str = hex_str.lstrip('#')
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def layout(node):
    if not node.is_leaf():
        node.name = ""

def draw_standard_premium(tree_file, output_image, title, species_ann):
    try:
        t = Tree(tree_file, format=1)
    except Exception as e:
        print(f"Error loading {tree_file}: {e}")
        return

    ts = TreeStyle()
    ts.mode = "c"
    ts.show_leaf_name = False
    ts.arc_start = -180
    ts.arc_span = 360
    ts.layout_fn = layout
    
    # Professional Margins for Legend
    ts.margin_top = 200
    ts.margin_bottom = 200
    ts.margin_left = 200
    ts.margin_right = 1100
    
    ts.draw_guiding_lines = True
    ts.guiding_lines_color = "#AAAAAA"
    ts.guiding_lines_type = 0

    title_face = TextFace(f" {title} ", fsize=24, bold=True)
    title_face.margin_bottom = 30
    ts.title.add_face(title_face, column=0)

    # 1. Assign Clades
    for leaf in t.get_leaves():
        raw = leaf.name
        clade = "Unknown"
        if raw.startswith("AT"):
            base = raw.split(".")[0].split("|")[0].strip()
            clade = AT_TO_CLADE.get(base, "Unknown")
        else:
            # Check target species annotation
            clade = species_ann.get(raw, "Unknown")
        leaf.add_features(my_clade=clade)

    # 2. Dynamic Nearest-Neighbor for Unknowns
    known_leaves = [lf for lf in t.get_leaves() if lf.my_clade != "Unknown"]
    for leaf in t.get_leaves():
        if leaf.my_clade == "Unknown" and known_leaves:
            best_dist = float('inf')
            best_clade = "Unknown"
            for kl in known_leaves:
                d = t.get_distance(leaf, kl)
                if d < best_dist:
                    best_dist = d
                    best_clade = kl.my_clade
            leaf.my_clade = best_clade

    # 3. Draw Leaves
    for leaf in t.get_leaves():
        clade = leaf.my_clade
        color = CLADE_COLORS.get(clade, "#BDC3C7")
        
        display_color = make_pastel(color) if leaf.name.startswith("AT") else color
        label = leaf.name

        nstyle = NodeStyle()
        nstyle["shape"] = "circle"
        nstyle["size"] = 0
        leaf.set_style(nstyle)
        
        face = TextFace(f" {label} ", fsize=10, bold=True)
        face.background.color = display_color
        leaf.add_face(face, column=0, position="aligned")

    # High-Res Render
    t.render(output_image, w=4000, units="px", dpi=300, tree_style=ts)
    
    # 4. Post-process Legend (PIL)
    try:
        img = Image.open(output_image)
        draw = ImageDraw.Draw(img)
        box_width, box_height = 850, 100 + (len(CLADE_COLORS)-1) * 70
        margin = 150
        x0, y0 = img.width - box_width - margin, margin
        x1, y1 = x0 + box_width, y0 + box_height
        
        draw.rectangle([x0, y0, x1, y1], fill="white", outline="black", width=6)
        
        try:
            f_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
            f_text = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 35)
        except:
            f_title = f_text = ImageFont.load_default()
            
        draw.text((x0 + 50, y0 + 35), "MIKCc Subclade Legend", fill="black", font=f_title)
        
        curr_y = y0 + 110
        for name, color in CLADE_COLORS.items():
            if name == "Unknown": continue
            draw.rectangle([x0 + 50, curr_y, x0 + 110, curr_y + 50], fill=color, outline="black", width=3)
            draw.text((x0 + 140, curr_y + 5), name, fill="black", font=f_text)
            curr_y += 70
            
        img.save(output_image)
    except Exception as e:
        print(f"Legend failed: {e}")

if __name__ == "__main__":
    import sys
    species = "Amborella_trichopoda"
    ann = load_annotations()
    
    # Re-render Amborella set
    algos = ["MAFFT", "MUSCLE", "ClustalO"]
    for algo in algos:
        tree = os.path.join(TREE_DIR, f"{species}_{algo}_ML.treefile")
        out = os.path.join(OUT_DIR, f"{species}_{algo}_Premium.png")
        draw_standard_premium(tree, out, f"{species.replace('_',' ')} — {algo} ML High-Res", ann)
