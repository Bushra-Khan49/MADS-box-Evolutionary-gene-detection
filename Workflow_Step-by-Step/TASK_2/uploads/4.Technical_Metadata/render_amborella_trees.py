import os
from ete3 import Tree, TreeStyle, NodeStyle, AttrFace, TextFace

# --- Configure paths ---
TASK_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_2/uploads"
OUTPUT_DIR = os.path.join(TASK_DIR, "Colored_Tree_Images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define standard color palette for MIKCc subclades
CLADE_COLORS = {
    "SEP": "#FF0000", "AP1": "#FF4500", "FUL": "#FF8C00", "AP3": "#1E90FF",
    "PI": "#00BFFF", "AG": "#008000", "STK": "#32CD32", "SOC1": "#8B008B",
    "SVP": "#9932CC", "ANR1": "#FFD700", "FLC": "#DAA520", "Bs": "#4B0082"
}

def get_subclade(name):
    for clade in CLADE_COLORS:
        if clade in name: return clade
    return "Unknown"

def render_circular_tree(nwk_file, output_name, title):
    if not os.path.exists(nwk_file):
        print(f"Skipping {nwk_file}")
        return
        
    t = Tree(nwk_file)
    ts = TreeStyle()
    ts.mode = "c"
    ts.show_leaf_name = False # We'll add custom faces
    ts.title.add_face(TextFace(title, fsize=20), column=0)
    
    for leaf in t.iter_leaves():
        subclade = get_subclade(leaf.name)
        color = CLADE_COLORS.get(subclade, "#808080")
        
        nstyle = NodeStyle()
        nstyle["fgcolor"] = color
        nstyle["size"] = 8
        leaf.set_style(nstyle)
        
        # Add a custom text face for the leaf name
        leaf.add_face(TextFace(leaf.name, fsize=10, fgcolor=color), column=0, position="branch-right")

    # Add Legend using TextFace
    ts.legend.add_face(TextFace("Subclade Legend", fsize=15), column=0)
    for clade, color in CLADE_COLORS.items():
        ts.legend.add_face(TextFace(f"■ {clade}", fgcolor=color, fsize=12), column=0)
    
    render_path = os.path.join(OUTPUT_DIR, output_name)
    t.render(render_path, tree_style=ts, w=3000, units="px")
    print(f"Rendered: {render_path}")

# --- Execution ---
render_circular_tree(os.path.join(TASK_DIR, "Atrichopoda_ML_Full.treefile"), "Amborella_Full_Proteome_circular.png", "Amborella trichopoda - Full MIKCc Tree")
render_circular_tree(os.path.join(TASK_DIR, "Amborella_MADS_Domain_ML.treefile"), "Amborella_MADS_Domain_circular.png", "Amborella trichopoda - MADS Domain Tree")
render_circular_tree(os.path.join(TASK_DIR, "Amborella_Kbox_Domain_ML.treefile"), "Amborella_Kbox_Domain_circular.png", "Amborella trichopoda - K-box Domain Tree")
