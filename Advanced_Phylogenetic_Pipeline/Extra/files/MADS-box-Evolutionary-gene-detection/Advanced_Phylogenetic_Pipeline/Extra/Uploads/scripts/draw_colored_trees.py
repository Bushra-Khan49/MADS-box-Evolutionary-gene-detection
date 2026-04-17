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

WORK_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/Uploads"
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

# ── Draw colored circular or rectangular phylogenetic tree ─────────────────────
def draw_tree(species, nwk_path, species_ann, mode="c"):
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
    ts.mode = mode  # 'c' for Circular, 'r' for Rectangular
    ts.force_topology = False
    ts.show_leaf_name = False
    if mode == "c":
        ts.arc_start = -180
        ts.arc_span = 360
    ts.layout_fn = layout
    
    # ── Perfected Centered Expansion (Maximized and Balanced) ──────────────────
    ts.margin_top = 200
    ts.margin_bottom = 200
    ts.margin_left = 200
    ts.margin_right = 200

    # Draw solid black lines connecting branch tips to the perfectly aligned names
    ts.draw_guiding_lines = True
    ts.guiding_lines_color = "#333333"
    ts.guiding_lines_type = 0 # solid

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
        if raw and (raw.startswith("AT") or "|PACid" in raw):
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
        if leaf.my_clade == "Unknown" and (leaf.name.startswith("AT") or "|PACid" in leaf.name) and known_leaves:
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
        if raw.startswith("AT") or "|PACid" in raw:
            display_color = make_pastel(color, factor=0.65) # 65% faded
        else:
            display_color = color
            
        label = raw

        # Create colored node style
        nstyle = NodeStyle()
        nstyle["shape"] = "circle"
        nstyle["size"] = 0
        nstyle["vt_line_width"] = 1
        nstyle["hz_line_width"] = 1
        leaf.set_style(nstyle)
        
        face = TextFace(f" {label} ", fsize=8, bold=True)
        face.margin_top = 1
        face.margin_bottom = 1
        face.margin_left = 2
        face.background.color = display_color
        
        leaf.add_face(face, column=0, position="aligned")

    # Output naming
    mode_str = "Circular" if mode == "c" else "Standard"
    display_species = species.replace('_',' ') if species != "MASTER_MIKCc_FULL" else "Master MIKCc Full"
    filename = f"{display_species} - MAFFT - ML ({mode_str}).png"
    out = os.path.join(OUT_DIR, filename)

    # Huge resolution rendering
    t.render(out, w=4000, units="px", dpi=300, tree_style=ts)
    
    # ── Post-process with Pillow ──
    try:
        img = Image.open(out)
        # Expand canvas for title if needed, or just draw on top
        draw = ImageDraw.Draw(img)
        
        # 1. Load Fonts
        try:
            font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 100)
            font_legend_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 60)
            font_text = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 50)
        except:
            font_title = ImageFont.load_default()
            font_legend_title = ImageFont.load_default()
            font_text = ImageFont.load_default()

        # 2. Draw Large Centered Title
        full_title = f"{display_species} — MAFFT | Maximum Likelihood (ML)"
        # Using getbbox to get (left, top, right, bottom)
        bbox = font_title.getbbox(full_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((img.width - tw) // 2, 80), full_title, fill="black", font=font_title)

        # 3. Draw Legend in Bottom-Right
        legend_items = [c for c in CLADE_COLORS.items() if c[0] != "Unknown"]
        row_h = 70
        box_w = 450
        box_h = 100 + (len(legend_items) * row_h)
        
        lx0 = img.width - box_w - 60
        ly0 = img.height - box_h - 60
        lx1 = lx0 + box_w
        ly1 = ly0 + box_h
        
        # Draw semi-transparent white box or solid white
        draw.rectangle([lx0, ly0, lx1, ly1], fill="white", outline="black", width=6)
        draw.text((lx0 + 40, ly0 + 30), "MIKCc Subclade Legend", fill="black", font=font_legend_title)
        
        curr_y = ly0 + 110
        for c_name, hex_color in legend_items:
            # Swatch
            draw.rectangle([lx0 + 20, curr_y, lx0 + 60, curr_y + 40], fill=hex_color, outline="black", width=2)
            # Label
            draw.text((lx0 + 80, curr_y - 5), c_name, fill="black", font=font_text)
            curr_y += row_h
            
        img.save(out)
        print(f"  Successfully rendered: {filename}")
    except Exception as img_e:
        print(f"  Warning: Post-processing failed: {img_e}")

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
    # Draw only Circular trees as requested
    draw_tree(sp, nwk, sp_ann, mode="c")

print(f"\n✅ All images regenerated in: {OUT_DIR}")

print(f"\n✅ All circular images saved to: {OUT_DIR}")
