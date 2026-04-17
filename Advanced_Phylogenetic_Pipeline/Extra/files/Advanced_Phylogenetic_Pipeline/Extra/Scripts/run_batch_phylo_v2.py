import os, csv, re
import subprocess
import time
from ete3 import Tree, TreeStyle, NodeStyle, TextFace
from PIL import Image, ImageDraw, ImageFont

# Set offscreen rendering for headless environment
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Configuration
TOOLS = {
    "mafft": "/opt/homebrew/bin/mafft",
    "muscle": "/opt/homebrew/bin/muscle",
    "clustalo": "/opt/homebrew/bin/clustalo",
    "iqtree2": "/opt/homebrew/bin/iqtree2"
}

BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline"
INPUT_DIR = os.path.join(BASE_DIR, "3.Phylogeny_Output/Combined_FullLength")
MSA_DIR = os.path.join(BASE_DIR, "3.Phylogeny_Output/Alignments_FullLength")
TREE_DIR = os.path.join(BASE_DIR, "3.Phylogeny_Output/Trees_FullLength")
IMG_DIR = os.path.join(BASE_DIR, "4.Visualization_Portfolio/Standardized_Trees")
ANN_FILE = os.path.join(BASE_DIR, "Uploads/MIKCc_Subclade_Annotation_Table.tsv")

# Subclade Palette
CLADE_COLORS = {
    "AP1/FUL/CAL": "#E74C3C", "SEP/AGL2-like": "#E67E22", "AGL17/ANR1": "#82E0AA",
    "SHP/STK/AG": "#2980B9", "FLC/MAF": "#8E44AD", "SOC1/AGL20": "#E91E8C",
    "AGL15/AGL18": "#1ABC9C", "AGL22/AGL24": "#F4D03F", "AP3/PI": "#27AE60",
    "AGL104/AGL66": "#C0392B", "AGL12": "#5D6D7E", "Unknown": "#BDC3C7"
}

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

# Ensure directories
for d in [MSA_DIR, TREE_DIR, IMG_DIR]: os.makedirs(d, exist_ok=True)

def load_annotations():
    ann = {}
    if os.path.exists(ANN_FILE):
        with open(ANN_FILE) as f:
            for row in csv.DictReader(f, delimiter="\t"): ann[row["Gene_ID"].strip()] = row["Subclade"]
    return ann

def make_pastel(hex_str, factor=0.65):
    hex_str = hex_str.lstrip('#')
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    r = int(r + (255 - r) * factor); g = int(g + (255 - g) * factor); b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def render_premium(tree_file, output_image, species_name, algo_name, species_ann):
    try: t = Tree(tree_file, format=1)
    except: return
    ts = TreeStyle()
    ts.mode = "c"; ts.show_leaf_name = False; ts.arc_start = -180; ts.arc_span = 360
    ts.margin_top = 200; ts.margin_bottom = 200; ts.margin_left = 200; ts.margin_right = 200
    ts.draw_guiding_lines = True; ts.guiding_lines_color = "#AAAAAA"
    
    # 0. Center Title with Standard Format
    title_str = f"{species_name.replace('_',' ')} - {algo_name} | Maximum Likelihood (ML)"
    title_face = TextFace(f" {title_str} ", fsize=28, bold=True)
    title_face.hz_align = 1 # Center
    title_face.margin_bottom = 40
    ts.title.add_face(title_face, column=1) # column 1 often helps centering in circular layout
    
    for leaf in t.get_leaves():
        raw = leaf.name; clade = "Unknown"
        if raw.startswith("AT"):
            base = raw.split(".")[0].split("|")[0].strip()
            clade = AT_TO_CLADE.get(base, "Unknown")
        else: clade = species_ann.get(raw, "Unknown")
        leaf.add_features(my_clade=clade)

    known_leaves = [lf for lf in t.get_leaves() if lf.my_clade != "Unknown"]
    for leaf in t.get_leaves():
        if leaf.my_clade == "Unknown" and known_leaves:
            best_dist = float('inf'); best_clade = "Unknown"
            for kl in known_leaves:
                d = t.get_distance(leaf, kl)
                if d < best_dist: best_dist = d; best_clade = kl.my_clade
            leaf.my_clade = best_clade

    for leaf in t.get_leaves():
        color = CLADE_COLORS.get(leaf.my_clade, "#BDC3C7")
        display_color = make_pastel(color) if leaf.name.startswith("AT") else color
        nstyle = NodeStyle(); nstyle["shape"] = "circle"; nstyle["size"] = 0; leaf.set_style(nstyle)
        face = TextFace(f" {leaf.name} ", fsize=10, bold=True); face.background.color = display_color
        leaf.add_face(face, column=0, position="aligned")

    t.render(output_image, w=4000, units="px", dpi=300, tree_style=ts)
    
    try:
        img = Image.open(output_image); draw = ImageDraw.Draw(img)
        box_width, box_height = 850, 100 + (len(CLADE_COLORS)-1) * 70
        margin = 150
        # Bottom Right Position
        x0, y0 = img.width - box_width - margin, img.height - box_height - margin
        x1, y1 = x0 + box_width, y0 + box_height
        
        draw.rectangle([x0, y0, x1, y1], fill="white", outline="black", width=6)
        try: f_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45); f_text = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 35)
        except: f_title = f_text = ImageFont.load_default()
        draw.text((x0 + 50, y0 + 35), "MIKCc Subclade Legend", fill="black", font=f_title)
        curr_y = y0 + 110
        for name, color in CLADE_COLORS.items():
            if name == "Unknown": continue
            draw.rectangle([x0 + 50, curr_y, x0 + 110, curr_y + 50], fill=color, outline="black", width=3)
            draw.text((x0 + 140, curr_y + 5), name, fill="black", font=f_text); curr_y += 70
        img.save(output_image)
    except: pass

def run_msa_mafft(input_fa, output_fa):
    with open(output_fa, "w") as out: subprocess.run([TOOLS["mafft"], "--auto", input_fa], stdout=out, check=True)

def run_msa_muscle(input_fa, output_fa):
    subprocess.run([TOOLS["muscle"], "-align", input_fa, "-output", output_fa], check=True)

def run_msa_clustalo(input_fa, output_fa):
    subprocess.run([TOOLS["clustalo"], "-i", input_fa, "-o", output_fa, "--force"], check=True)

def run_iqtree(alignment_fa, output_prefix):
    subprocess.run([TOOLS["iqtree2"], "-s", alignment_fa, "-m", "LG+F+G", "-B", "1000", "-pre", output_prefix, "-nt", "AUTO", "-redo"], check=True)

def process_species(species, ann):
    print(f"\n>>> {species} <<<")
    input_file = os.path.join(INPUT_DIR, f"{species}_with_AT_Strict45.fa")
    if not os.path.exists(input_file): return
    for algo in ["MAFFT", "MUSCLE", "ClustalO"]:
        msa_out = os.path.join(MSA_DIR, f"{species}_{algo}_Aligned.fa")
        tree_prefix = os.path.join(TREE_DIR, f"{species}_{algo}_ML")
        tree_file = tree_prefix + ".treefile"
        img_out = os.path.join(IMG_DIR, f"{species}_{algo}_Premium.png")
        try:
            if algo == "MAFFT": run_msa_mafft(input_file, msa_out)
            elif algo == "MUSCLE": run_msa_muscle(input_file, msa_out)
            elif algo == "ClustalO": run_msa_clustalo(input_file, msa_out)
            run_iqtree(msa_out, tree_prefix)
            render_premium(tree_file, img_out, species, algo, ann)
        except Exception as e: print(f"Error {species} {algo}: {e}")

if __name__ == "__main__":
    import sys
    ann = load_annotations()
    targets = sys.argv[1:] if len(sys.argv) > 1 else [
        "Cinnamomum_kanehirae", "Glycine_max", "Helianthus_annuuss",
        "Medicago_truncatula", "Nelumbo_nucifera", "Nymphaea_colorata",
        "Oryza_sativa", "Piper_auritum", "Prunus_persica"
    ]
    for sp in targets: process_species(sp, ann)
