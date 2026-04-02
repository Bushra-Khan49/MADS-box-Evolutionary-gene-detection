"""
Generate colored annotated circular phylogenetic tree images using ETE3.
Reads Newick files and colors leaves by MIKCc subclade to match the reference slides.
"""
import os, csv, re
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from ete3 import Tree, TreeStyle, NodeStyle, TextFace, faces

# ── Colors matching your Google Slides ────────────────────────────────────────
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

# ============================================================
# Arabidopsis MIKCc gene → Subclade mapping
# ============================================================
AT_TO_CLADE = {
    # AP1/FUL/CAL Clade (A-class, floral meristem/organ identity) - RED
    "AT1G69120": "AP1/FUL/CAL", "AT1G24260": "AP1/FUL/CAL", "AT5G61850": "AP1/FUL/CAL",
    "AT4G36590": "AP1/FUL/CAL", "AT2G45650": "AP1/FUL/CAL", "AT5G20240": "AP1/FUL/CAL",
    "AT5G60910": "AP1/FUL/CAL", 

    # SEP/AGL2/AGL4/AGL6/AGL9/AGL13 Clade (E-class, SEPALLATA) - ORANGE
    "AT3G02310": "SEP/AGL2-like", "AT1G24500": "SEP/AGL2-like", "AT2G03710": "SEP/AGL2-like",
    "AT1G67060": "SEP/AGL2-like", "AT4G22950": "SEP/AGL2-like", "AT3G61120": "SEP/AGL2-like",
    "AT2G03060": "SEP/AGL2-like", "AT5G15800": "SEP/AGL2-like",

    # AGL17/ANR1 Clade (root/flowering time) - LIGHT GREEN
    "AT4G18960": "AGL17/ANR1", "AT3G61890": "AGL17/ANR1", "AT3G57230": "AGL17/ANR1",
    "AT5G13790": "AGL17/ANR1", "AT2G14210": "AGL17/ANR1",

    # SHP/STK/AG Clade (C/D-class, carpel/ovule identity) - BLUE
    "AT3G54340": "SHP/STK/AG", "AT2G42830": "SHP/STK/AG", "AT3G58780": "SHP/STK/AG",
    "AT4G09960": "SHP/STK/AG",

    # FLC/MAF/FLM Clade (Flowering repression/vernalization) - PURPLE
    "AT5G10140": "FLC/MAF", "AT3G05390": "FLC/MAF", "AT1G77080": "FLC/MAF",
    "AT3G65060": "FLC/MAF", "AT5G65070": "FLC/MAF", "AT5G65060": "FLC/MAF",
    "AT5G48670": "FLC/MAF", "AT5G65050": "FLC/MAF",

    # SOC1/AGL20 Clade (Flowering time integration) - PINK
    "AT2G45660": "SOC1/AGL20", "AT5G62165": "SOC1/AGL20", "AT1G77760": "SOC1/AGL20",
    "AT2G22540": "SOC1/AGL20", "AT4G37940": "SOC1/AGL20", "AT1G18750": "SOC1/AGL20",

    # AGL15/AGL18 Clade (Embryogenesis/flower regulation) - CYAN
    "AT3G57390": "AGL15/AGL18", "AT3G22380": "AGL15/AGL18", "AT1G22130": "AGL15/AGL18",
    "AT3G30260": "AGL15/AGL18",

    # AGL22/AGL24 Clade (SVP-like, flowering control) - YELLOW
    "AT4G24540": "AGL22/AGL24", "AT1G26310": "AGL22/AGL24",

    # AP3/PI/TT16 Clade (B-class, petal/stamen identity) - BRIGHT GREEN
    "AT1G79840": "AP3/PI", "AT2G40080": "AP3/PI", "AT5G23260": "AP3/PI",

    # AGL104/AGL66/AGL67 Clade (pollen-expressed) - MAGENTA
    "AT1G48150": "AGL104/AGL66", "AT4G16900": "AGL104/AGL66", "AT1G77990": "AGL104/AGL66",
    "AT1G60920": "AGL104/AGL66", "AT1G77980": "AGL104/AGL66",
    
    # AGL12
    "AT1G71692": "AGL12"
}

WORK_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK"
NWK_DIR  = os.path.join(WORK_DIR, "Newick_Trees")
ANN_FILE = os.path.join(WORK_DIR, "MIKCc_Subclade_Annotation_Table.tsv")
OUT_DIR  = os.path.join(WORK_DIR, "Colored_Tree_Images")
os.makedirs(OUT_DIR, exist_ok=True)

SPECIES = [
    "Amborella_trichopoda", "Cinnamomum_kanehirae", "Glycine_max",
    "Helianthus_annuuss",   "Medicago_truncatula",  "Nelumbo_nucifera",
    "Nymphaea_colorata",    "Oryza_sativa",         "Prunus_persica",
    "MASTER_MIKCc_FULL"
]

# ── Load annotations ──────────────────────────────────────────────────────────
def load_annotations():
    ann = {}
    with open(ANN_FILE) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            gid = row["Gene_ID"].strip()
            key = re.sub(r'[.\-\s]', '_', gid)
            ann[key] = ann[gid] = {
                "at_name":  row["AT_Gene_Name"],
                "subclade": row["Subclade"],
                "species":  row["Species"],
            }
    return ann


def layout(node):
    # Hide internal node labels
    if not node.is_leaf():
        node.name = ""

def make_pastel(hex_str, factor=0.6):
    """Fades a hex color by blending it with white (fakes 50% transparency without alpha bugs)"""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6: return "#" + hex_str
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

# ── Draw colored circular phylogenetic tree ───────────────────────────────────
def draw_tree(species, nwk_path, species_ann):
    try:
        with open(nwk_path, 'r') as f:
            nwk_str = f.read()
        # Remove MEGA's [stddev=...] tags which break ETE3
        clean_nwk = re.sub(r'\[stddev=[^\]]+\]', '', nwk_str)
        t = Tree(clean_nwk, format=1)
    except Exception as e:
        print(f"Error loading {nwk_path}: {e}")
        return

    n = len(t.get_leaves())
    if n == 0:
        print(f"  No leaves found in {nwk_path}")
        return

    ts = TreeStyle()
    ts.mode = "c"  # Circular tree
    ts.force_topology = False  # DO NOT bend the tree! True phylogenetic branch lengths
    ts.show_leaf_name = False
    ts.arc_start = -180
    ts.arc_span = 360
    ts.layout_fn = layout
    
    # Draw solid black lines connecting branch tips to the perfectly aligned circular names
    ts.draw_guiding_lines = True
    ts.guiding_lines_color = "#000000"
    ts.guiding_lines_type = 0 # solid

    # Add Title
    title = TextFace(f" {species.replace('_',' ')} — Circular MIKCc Subclade Tree", fsize=20, bold=True)
    title.margin_bottom = 20
    ts.title.add_face(title, column=0)

    from PIL import Image, ImageDraw, ImageFont

    # 1. First pass: Assign known clades
    for leaf in t.get_leaves():
        raw = leaf.name
        key = re.sub(r'[.\-\s]', '_', raw) if raw else ""
        info = species_ann.get(raw) or species_ann.get(key)
        
        # Substring fallback for concatenated MASTER tree strings
        if not info and raw:
            for ann_key, ann_val in species_ann.items():
                if len(ann_key) > 5 and re.sub(r'[.\-\s]', '_', ann_key) in key:
                    info = ann_val
                    break

        clade = "Unknown"
        if raw and raw.startswith("AT"):
            base = raw.split("|")[0] if "|" in raw else raw.split(".")[0]
            if base in AT_TO_CLADE:
                clade = AT_TO_CLADE[base]
            else:
                base = base.split(".")[0]
                clade = AT_TO_CLADE.get(base, "Unknown")
        else:
            clade = info["subclade"] if info else "Unknown"
            
        leaf.add_features(my_clade=clade)

    # 1.5. Dynamic Pass: Color unmapped AT genes based on nearest mapped neighbor
    known_leaves = [lf for lf in t.get_leaves() if lf.my_clade != "Unknown"]
    for leaf in t.get_leaves():
        if leaf.my_clade == "Unknown" and leaf.name.startswith("AT") and known_leaves:
            # Find closest reference
            best_dist = float('inf')
            best_c = "Unknown"
            for kl in known_leaves:
                d = t.get_distance(leaf, kl)
                if d < best_dist:
                    best_dist = d
                    best_c = kl.my_clade
            leaf.my_clade = best_c

    # 2. Second pass: Draw
    for leaf in t.get_leaves():
        raw = leaf.name
        clade = leaf.my_clade
        color = CLADE_COLORS.get(clade, "#BDC3C7")
        
        # Fake transparency for exactly AT genes
        if raw.startswith("AT"):
            display_color = make_pastel(color, factor=0.65) # 65% faded
        else:
            display_color = color
            
        # DO NOT change the label name, keep it exactly as it appeared in the raw tree
        label = raw

        # Create colored node style
        nstyle = NodeStyle()
        nstyle["shape"] = "circle"
        nstyle["size"] = 0
        nstyle["vt_line_width"] = 1
        nstyle["hz_line_width"] = 1
        leaf.set_style(nstyle)
        
        # Add label with colored background
        # position "aligned" pushes all names to a perfect, even outer circle
        face = TextFace(f" {label} ", fsize=7, bold=True)
        face.margin_top = 1
        face.margin_bottom = 1
        face.margin_left = 2
        face.background.color = display_color
        
        leaf.add_face(face, column=0, position="aligned")

    out = os.path.join(OUT_DIR, f"{species}_circular_colored_tree.png")
    # Huge resolution rendering (4000w pixels) for crystal clear zoom
    t.render(out, w=4000, units="px", dpi=300, tree_style=ts)
    
    # ── Post-process to add a perfectly bordered, aligned Legend using Pillow ──
    try:
        img = Image.open(out)
        draw = ImageDraw.Draw(img)
        
        # Legend sizing and positioning (Top Right Corner)
        box_width = 800
        box_height = 100 + (len(CLADE_COLORS) - 1) * 60
        margin = 100
        x0 = img.width - box_width - margin
        y0 = margin
        x1 = x0 + box_width
        y1 = y0 + box_height
        
        # Draw boxed background
        draw.rectangle([x0, y0, x1, y1], fill="white", outline="black", width=5)
        
        # Draw Title
        # Using default font scaled up via ImageFont (or just draw text directly)
        try:
            # Attempt to use a larger default font if available or system font
            font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            font_text = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        except:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()
            
        draw.text((x0 + 40, y0 + 30), "Subclade Legend", fill="black", font=font_title)
        
        # Draw Color Swatches and Text
        curr_y = y0 + 100
        for c_name, hex_color in CLADE_COLORS.items():
            if c_name == "Unknown": continue
            
            # Swatch box
            draw.rectangle([x0 + 40, curr_y, x0 + 90, curr_y + 40], fill=hex_color, outline="black", width=2)
            
            # Label
            draw.text((x0 + 120, curr_y + 5), c_name, fill="black", font=font_text)
            curr_y += 60
            
        img.save(out)
    except Exception as img_e:
        print(f"  Warning: Pillow legend drawing failed: {img_e}")

    print(f"  Tree saved: {out}")

# ── Main ──────────────────────────────────────────────────────────────────────
print("Loading annotations...")
all_ann = load_annotations()

for sp in SPECIES:
    print(f"\n── {sp}")
    nwk = os.path.join(NWK_DIR, f"{sp}.nwk")
    if not os.path.exists(nwk):
        print(f"  Newick not found: {nwk}")
        continue
    
    # For Master tree, use all annotations
    if sp == "MASTER_MIKCc_FULL":
        sp_ann = all_ann
    else:
        sp_ann = {g: i for g, i in all_ann.items() if i["species"] == sp}
        
    print(f"  Annotated genes: {len(sp_ann)}")
    draw_tree(sp, nwk, sp_ann)

print(f"\n✅ All circular images saved to: {OUT_DIR}")
