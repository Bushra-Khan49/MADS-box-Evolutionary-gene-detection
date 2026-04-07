import os, re
import ete3
from PIL import Image, ImageDraw, ImageFont

RESULTS_DIR = os.path.abspath("Results_v4")
GALLERY_DIR = os.path.abspath("Results_v4/Gallery")

SPECIES_LIST = [
    "Amborella_trichopoda", "Cinnamomum_kanehirae", "Glycine_max",
    "Helianthus_annuuss", "Medicago_truncatula", "Nelumbo_nucifera",
    "Nymphaea_colorata", "Oryza_sativa", "Prunus_persica"
]

CLADE_COLORS = {
    "AP1/FUL/CAL":   "#E74C3C", "SEP/AGL2-like": "#E67E22", "AGL17/ANR1":    "#82E0AA",
    "SHP/STK/AG":    "#2980B9", "FLC/MAF":       "#8E44AD", "SOC1/AGL20":    "#E91E8C",
    "AGL15/AGL18":   "#1ABC9C", "AGL22/AGL24":   "#F4D03F", "AP3/PI":        "#27AE60",
    "AGL104/AGL66":  "#C0392B", "AGL12":         "#5D6D7E", "Unknown":       "#BDC3C7",
}

AT_TO_CLADE = {
    "AT1G69120": "AP1/FUL/CAL", "AT1G24260": "AP1/FUL/CAL", "AT5G61850": "AP1/FUL/CAL",
    "AT4G36590": "AP1/FUL/CAL", "AT2G45650": "AP1/FUL/CAL", "AT5G20240": "AP1/FUL/CAL",
    "AT5G60910": "AP1/FUL/CAL", "AT3G02310": "SEP/AGL2-like", "AT1G24500": "SEP/AGL2-like", "AT2G03710": "SEP/AGL2-like",
    "AT1G67060": "SEP/AGL2-like", "AT4G22950": "SEP/AGL2-like", "AT3G61120": "SEP/AGL2-like",
    "AT2G03060": "SEP/AGL2-like", "AT5G15800": "SEP/AGL2-like", "AT4G18960": "AGL17/ANR1", "AT3G61890": "AGL17/ANR1", "AT3G57230": "AGL17/ANR1",
    "AT5G13790": "AGL17/ANR1", "AT2G14210": "AGL17/ANR1", "AT3G54340": "SHP/STK/AG", "AT2G42830": "SHP/STK/AG", "AT3G58780": "SHP/STK/AG",
    "AT4G09960": "SHP/STK/AG", "AT5G10140": "FLC/MAF", "AT3G05390": "FLC/MAF", "AT1G77080": "FLC/MAF",
    "AT3G65060": "FLC/MAF", "AT5G65070": "FLC/MAF", "AT5G65060": "FLC/MAF",
    "AT5G48670": "FLC/MAF", "AT5G65050": "FLC/MAF", "AT2G45660": "SOC1/AGL20", "AT5G62165": "SOC1/AGL20", "AT1G77760": "SOC1/AGL20",
    "AT2G22540": "SOC1/AGL20", "AT4G37940": "SOC1/AGL20", "AT1G18750": "SOC1/AGL20", "AT3G57390": "AGL15/AGL18", "AT3G22380": "AGL15/AGL18", "AT1G22130": "AGL15/AGL18",
    "AT3G30260": "AGL15/AGL18", "AT4G24540": "AGL22/AGL24", "AT1G26310": "AGL22/AGL24", "AT1G79840": "AP3/PI", "AT2G40080": "AP3/PI", "AT5G23260": "AP3/PI",
    "AT1G48150": "AGL104/AGL66", "AT4G16900": "AGL104/AGL66", "AT1G77990": "AGL104/AGL66",
    "AT1G60920": "AGL104/AGL66", "AT1G77980": "AGL104/AGL66", "AT1G71692": "AGL12"
}

def make_pastel(hex_str, factor=0.5):
    """Blends a hex color toward white to simulate reduced opacity.
    factor=0.5 → 50% opacity look; factor=0 → original color."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        return '#' + hex_str
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f'#{r:02x}{g:02x}{b:02x}'

def sanitize_newick(newick_str):
    return re.sub(r'\)[^,;\(\)]+:', r'):', newick_str)

def layout(node):
    if not node.is_leaf():
        node.name = ""

def draw_tree(species, filepath, out_img):
    try:
        with open(filepath, "r") as f:
            newick_content = f.read().strip()
        clean_newick = sanitize_newick(newick_content)
        tree = ete3.Tree(clean_newick, format=1)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return

    ts = ete3.TreeStyle()
    ts.mode = "c"
    ts.force_topology = False
    ts.show_leaf_name = False
    ts.arc_start = -180
    ts.arc_span = 360
    ts.layout_fn = layout
    ts.draw_guiding_lines = True
    ts.guiding_lines_color = "#000000"
    ts.guiding_lines_type = 0

    title = ete3.TextFace(f" {species.replace('_',' ')} — Focus-Opacity Circular Tree", fsize=20, bold=True)
    title.margin_bottom = 20
    ts.title.add_face(title, column=0)

    # Topological Clade Extrapolation
    for leaf in tree.get_leaves():
        raw = leaf.name
        clade = "Unknown"
        if raw.upper().startswith("AT"):
            base = raw.split(".")[0] if "." in raw else raw
            if base in AT_TO_CLADE:
                clade = AT_TO_CLADE[base]
        leaf.add_features(my_clade=clade)

    # Nearest Neighbor extrapolation for unmapped leaves
    known_leaves = [lf for lf in tree.get_leaves() if lf.my_clade != "Unknown"]
    for leaf in tree.get_leaves():
        if leaf.my_clade == "Unknown" and known_leaves:
            best_dist = float('inf')
            best_c = "Unknown"
            for kl in known_leaves:
                d = tree.get_distance(leaf, kl)
                if d < best_dist:
                    best_dist = d
                    best_c = kl.my_clade
            leaf.my_clade = best_c

    # Node rendering with Focus-Opacity rules:
    # Target species → full clade color (100% opacity)
    # AT anchors     → pastel/faded version of same clade color (50% opacity simulation)
    for leaf in tree.get_leaves():
        raw = leaf.name
        clade = leaf.my_clade
        full_color = CLADE_COLORS.get(clade, "#BDC3C7")
        
        is_at = raw.upper().startswith("AT")
        # Simulate opacity by blending with white:
        # AT anchors get 50% blend → visibly faded background
        # Target species get 0% blend → full vivid color
        display_color = make_pastel(full_color, factor=0.55) if is_at else full_color
        
        nstyle = ete3.NodeStyle()
        nstyle["shape"] = "circle"
        nstyle["size"] = 0
        nstyle["vt_line_width"] = 1
        nstyle["hz_line_width"] = 1
        leaf.set_style(nstyle)
        
        face = ete3.TextFace(f" {raw} ", fsize=7, bold=(not is_at))
        face.margin_top = 1
        face.margin_bottom = 1
        face.margin_left = 2
        face.background.color = display_color
        
        leaf.add_face(face, column=0, position="aligned")

    # High-Res render to give enough padding for the Legend safely!
    tree.render(out_img, w=4000, units="px", dpi=300, tree_style=ts)

    # Pillow legend — placed in BOTTOM-RIGHT corner to fully avoid title overlap
    try:
        img = Image.open(out_img)
        draw = ImageDraw.Draw(img)

        # Compact legend sizing
        row_h = 45
        box_width = 680
        n_items = len([k for k in CLADE_COLORS if k != "Unknown"])
        box_height = 70 + n_items * row_h
        margin = 80

        # Bottom-right positioning — clear of tree body
        x0 = img.width - box_width - margin
        y0 = img.height - box_height - margin
        x1 = x0 + box_width
        y1 = y0 + box_height

        # Semi-transparent white box (drawn as solid white with border)
        draw.rectangle([x0 - 5, y0 - 5, x1 + 5, y1 + 5], fill="#F8F8F8", outline="#333333", width=4)

        try:
            font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            font_text  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
        except:
            font_title = ImageFont.load_default()
            font_text  = ImageFont.load_default()

        draw.text((x0 + 30, y0 + 15), "MIKCc Subclade Legend", fill="#111111", font=font_title)

        curr_y = y0 + 62
        for c_name, hex_color in CLADE_COLORS.items():
            if c_name == "Unknown": continue
            # Color swatch
            draw.rectangle([x0 + 30, curr_y, x0 + 68, curr_y + 30], fill=hex_color, outline="black", width=2)
            # Label
            draw.text((x0 + 88, curr_y + 4), c_name, fill="#111111", font=font_text)
            curr_y += row_h

        img.save(out_img)
        print(f"  -> Successfully generated Colored & Legend-Safe Focus Tree: {out_img}")
    except Exception as e:
        print(f"  -> Warning: Failed to apply Pillow legend to {out_img}: {e}")

if __name__ == "__main__":
    os.makedirs(GALLERY_DIR, exist_ok=True)
    for sp in SPECIES_LIST:
        print(f"Rendering {sp}...")
        sp_dir = os.path.join(RESULTS_DIR, sp)
        if not os.path.isdir(sp_dir): continue
        out_d = os.path.join(GALLERY_DIR, sp)
        os.makedirs(out_d, exist_ok=True)
        for tf in os.listdir(sp_dir):
            if tf.endswith(".treefile"):
                fp = os.path.join(sp_dir, tf)
                op = os.path.join(out_d, tf.replace(".treefile", ".png"))
                draw_tree(sp, fp, op)
    print("Gallery completely processed.")
