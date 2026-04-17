import os, subprocess, sys, csv, re
from ete3 import Tree, TreeStyle, NodeStyle, TextFace, faces
from PIL import Image, ImageDraw, ImageFont

# ── Configuration ─────────────────────────────────────────────────────────────
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

WORK_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/Uploads"
AT_REF   = "/Users/bushrakhan/Desktop/NIPGR-data/TASK_4/Brapa_vs_Athaliana/ATH_MADS.domains.fa"
OUT_DIR  = os.path.join(WORK_DIR, "Colored_Tree_Images")
ANN_FILE = os.path.join(WORK_DIR, "MIKCc_Subclade_Annotation_Table.tsv")
IQTREE_BIN = os.path.join(WORK_DIR, "scripts/iqtree2")

MUSCLE_BIN = "/opt/homebrew/bin/muscle"
CLUSTALO_BIN = "/opt/homebrew/bin/clustalo"

SPECIES_LIST = [
    "Amborella_trichopoda", "Cinnamomum_kanehirae", "Glycine_max",
    "Helianthus_annuuss",   "Medicago_truncatula",  "Nelumbo_nucifera",
    "Nymphaea_colorata",    "Oryza_sativa",         "Prunus_persica"
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
    "AT5G60910": "AP1/FUL/CAL", "AT3G02310": "SEP/AGL2-like", "AT1G24500": "SEP/AGL2-like",
    "AT2G03710": "SEP/AGL2-like", "AT1G67060": "SEP/AGL2-like", "AT4G22950": "SEP/AGL2-like",
    "AT3G61120": "SEP/AGL2-like", "AT2G03060": "SEP/AGL2-like", "AT5G15800": "SEP/AGL2-like",
    "AT4G18960": "AGL17/ANR1", "AT3G61890": "AGL17/ANR1", "AT3G57230": "AGL17/ANR1",
    "AT5G13790": "AGL17/ANR1", "AT2G14210": "AGL17/ANR1", "AT3G54340": "SHP/STK/AG",
    "AT2G42830": "SHP/STK/AG", "AT3G58780": "SHP/STK/AG", "AT4G09960": "SHP/STK/AG",
    "AT5G10140": "FLC/MAF", "AT3G05390": "FLC/MAF", "AT1G77080": "FLC/MAF",
    "AT3G65060": "FLC/MAF", "AT5G65070": "FLC/MAF", "AT5G48670": "FLC/MAF",
    "AT5G65050": "FLC/MAF", "AT2G45660": "SOC1/AGL20", "AT5G62165": "SOC1/AGL20",
    "AT2G22540": "SOC1/AGL20", "AT4G37940": "SOC1/AGL20", "AT1G18750": "SOC1/AGL20",
    "AT3G57390": "AGL15/AGL18", "AT3G22380": "AGL15/AGL18", "AT1G22130": "AGL15/AGL18",
    "AT3G30260": "AGL15/AGL18", "AT4G24540": "AGL22/AGL24", "AT1G26310": "AGL22/AGL24",
    "AT1G79840": "AP3/PI", "AT2G40080": "AP3/PI", "AT5G23260": "AP3/PI",
    "AT1G48150": "AGL104/AGL66", "AT4G16900": "AGL104/AGL66", "AT1G60920": "AGL104/AGL66",
    "AT1G77980": "AGL104/AGL66", "AT1G71692": "AGL12"
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_annotations():
    ann = {}
    if not os.path.exists(ANN_FILE): return ann
    with open(ANN_FILE) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            gid = row["Gene_ID"].strip()
            ann[gid] = ann[re.sub(r'[.\-\s]', '_', gid)] = {
                "subclade": row["Subclade"], "species":  row["Species"],
            }
    return ann

def make_pastel(hex_str, factor=0.65):
    hex_str = hex_str.lstrip('#')
    r, g, b = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    r = int(r + (255 - r) * factor); g = int(g + (255 - g) * factor); b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def layout_fn(node):
    if not node.is_leaf(): node.name = ""

def run_cmd(cmd, cwd=None):
    print(f"  Executing: {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd, capture_output=True)

# ── Rendering ─────────────────────────────────────────────────────────────────
def render_tree(species, nwk_path, species_ann, algo, mode="c"):
    try:
        with open(nwk_path, 'r') as f:
            t = Tree(re.sub(r'\[stddev=[^\]]+\]', '', f.read()), format=1)
    except: return

    ts = TreeStyle()
    ts.mode, ts.show_leaf_name, ts.force_topology = mode, False, False
    if mode == "c": ts.arc_start, ts.arc_span = -180, 360
    ts.layout_fn = layout_fn
    
    # ── Margins to prevent overlap with Title/Legend (reduces tree radius) ─────
    ts.margin_top = 600
    ts.margin_bottom = 600
    ts.margin_left = 600
    ts.margin_right = 600

    ts.draw_guiding_lines, ts.guiding_lines_color = True, "#333333"

    for leaf in t.get_leaves():
        clade = "Unknown"
        if leaf.name.startswith("AT") or "|PACid" in leaf.name:
            base = leaf.name.split("|")[0].split(".")[0]
            clade = AT_TO_CLADE.get(base, "Unknown")
        else:
            clade = species_ann.get(leaf.name, {}).get("subclade", "Unknown")
        leaf.add_features(my_clade=clade)

    known_leaves = [lf for lf in t.get_leaves() if lf.my_clade != "Unknown"]
    for leaf in t.get_leaves():
        if leaf.my_clade == "Unknown" and (leaf.name.startswith("AT") or "|PACid" in leaf.name) and known_leaves:
            best_kl = min(known_leaves, key=lambda kl: t.get_distance(leaf, kl))
            leaf.my_clade = best_kl.my_clade

    for leaf in t.get_leaves():
        color = CLADE_COLORS.get(leaf.my_clade, "#BDC3C7")
        disp_color = make_pastel(color) if (leaf.name.startswith("AT") or "|PACid" in leaf.name) else color
        nstyle = NodeStyle()
        nstyle["size"] = 0
        leaf.set_style(nstyle)
        face = TextFace(f" {leaf.name} ", fsize=8, bold=True)
        face.background.color = disp_color
        leaf.add_face(face, column=0, position="aligned")

    mode_str = "Circular" if mode == "c" else "Standard"
    display_sp = species.replace('_',' ')
    filename = f"{display_sp} - {algo} - ML ({mode_str}).png"
    out = os.path.join(OUT_DIR, filename)
    t.render(out, w=4000, units="px", dpi=300, tree_style=ts)

    try:
        img = Image.open(out); draw = ImageDraw.Draw(img)
        try:
            f_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 100)
            f_l_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 60)
            f_text = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 50)
        except: f_title = f_l_title = f_text = ImageFont.load_default()

        full_t = f"{display_sp} — {algo} | Maximum Likelihood (ML)"
        bbox = f_title.getbbox(full_t); tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        draw.text(((img.width - tw) // 2, 80), full_t, fill="black", font=f_title)

        items = [c for c in CLADE_COLORS.items() if c[0] != "Unknown"]
        row_h, box_w, box_h = 70, 900, 100 + (len(items) * 70)
        lx0, ly0 = img.width - box_w - 100, img.height - box_h - 100
        draw.rectangle([lx0, ly0, lx0+box_w, ly0+box_h], fill="white", outline="black", width=6)
        draw.text((lx0 + 40, ly0 + 30), "MIKCc Subclade Legend", fill="black", font=f_l_title)
        cy = ly0 + 110
        for name, col in items:
            draw.rectangle([lx0 + 40, cy, lx0 + 100, cy + 40], fill=col, outline="black", width=2)
            draw.text((lx0 + 130, cy - 5), name, fill="black", font=f_text); cy += 70
        img.save(out)
        print(f"    Done: {filename}")
    except Exception as e: print(f"    Error post-processing: {e}")

# ── Main ──────────────────────────────────────────────────────────────────────
print("Starting Extra ML Tree Generation (MUSCLE & ClustalO)...")
all_ann = load_annotations()

for sp in SPECIES_LIST:
    print(f"\n>>> Processing {sp}")
    spec_dir = os.path.join(WORK_DIR, sp)
    cand_fa = os.path.join(spec_dir, f"{sp}_candidates.fa")
    if not os.path.exists(cand_fa): continue

    combined = os.path.join(spec_dir, f"{sp}_combined.fa")
    with open(combined, 'w') as f:
        with open(cand_fa) as fc: f.write(fc.read())
        with open(AT_REF) as fr: f.write(fr.read())

    for algo in ["MUSCLE", "ClustalO"]:
        print(f"  -- {algo}")
        aln = os.path.join(spec_dir, f"{sp}_{algo}.fa")
        if algo == "MUSCLE": 
            # MUSCLE v5 uses -align and -output. Super5 is better for >500 seqs but -align is fine here.
            run_cmd(f"{MUSCLE_BIN} -align {combined} -output {aln}")
        else: 
            run_cmd(f"{CLUSTALO_BIN} -i {combined} -o {aln} --force")

        iq_out = os.path.join(spec_dir, f"{sp}_{algo}_ML")
        # -bb 1000 is required by IQ-TREE 2 UFBoot for proper validation
        run_cmd(f"{IQTREE_BIN} -s {aln} -m LG+G -bb 1000 -T 4 --redo --prefix {iq_out}")
        
        nwk = f"{iq_out}.treefile"
        if os.path.exists(nwk):
            sp_ann = {g: i for g, i in all_ann.items() if i["species"] == sp}
            render_tree(sp, nwk, sp_ann, algo, mode="c")
            render_tree(sp, nwk, sp_ann, algo, mode="r")

print("\n✅ All extra trees generated and rendered.")
