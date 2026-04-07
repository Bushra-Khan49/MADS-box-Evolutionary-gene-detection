import os
from ete3 import Tree, TreeStyle, TextFace, NodeStyle

# Configuration
WORKSPACE = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Simultaneous_Phylogenetic_Analysis"
TREE_DIRS = [
    os.path.join(WORKSPACE, "Results_v2/Trees/NJ"),
    os.path.join(WORKSPACE, "Results_v2/Trees/Bayes")
]
IMAGE_DIR = os.path.join(WORKSPACE, "Results_v2/Images")
ANNOTATION_FILE = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/Uploads/MIKCc_Subclade_Annotation_Table.tsv"

os.makedirs(IMAGE_DIR, exist_ok=True)

# Load Annotations
clade_colors = {
    "AP1/SQUA": "#E1C699", "SEP": "#C7E9B4", "AG": "#FDAE61", "STK": "#FDAE61",
    "SOC1/TM3": "#ABD9E9", "FLC": "#2C7BB6", "SVP/StMADS11": "#D7191C",
    "PI": "#FFFFBF", "AP3": "#FFFFBF", "Bs": "#FB9A99", "M-type": "#999999"
}
gene_to_clade = {}
if os.path.exists(ANNOTATION_FILE):
    with open(ANNOTATION_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                gene_to_clade[parts[0]] = parts[1]

def render_tree(tree_path, output_path, title):
    try:
        with open(tree_path, 'r') as f:
            nwk = f.read().strip()
            # Handle IQ-TREE double supports (e.g., 99/100) by taking the final one
            # ETE3 sometimes chokes on the slash
            import re
            nwk = re.sub(r'(\d+\.?\d*)/(\d+\.?\d*)', r'\2', nwk)
            
        t = Tree(nwk, format=0)
        ts = TreeStyle()
        ts.mode = "c"
        ts.show_leaf_name = True
        ts.show_branch_support = True
        ts.title.add_face(TextFace(title, fsize=20), column=0)
        
        for leaf in t.iter_leaves():
            is_at = leaf.name.startswith("AT")
            clade = gene_to_clade.get(leaf.name, "Unclassified")
            base_color = clade_colors.get(clade, "#D3D3D3")
            
            # Implementation of Focus-Opacity logic
            if is_at:
                # Faded Gray for Arabidopsis reference
                final_color = "#DCDCDC" # Gainsboro (Light Gray)
                font_color = "#A9A9A9"  # Dark Gray (faded appearance)
                node_size = 5
            else:
                # Full Intensity for Target Species (Os, Amb, Nym, etc.)
                final_color = base_color
                font_color = "#000000"  # Solid Black for prominence
                node_size = 12
            
            nstyle = NodeStyle()
            nstyle["fgcolor"] = final_color
            nstyle["size"] = node_size
            leaf.set_style(nstyle)
            
            # Apply label style
            leaf.add_face(TextFace(leaf.name, fsize=14, fgcolor=font_color), column=0)
            leaf.name = "" # Clear name to avoid double labeling
            
        t.render(output_path, tree_style=ts, units="px", w=1600)
        return True
    except Exception as e:
        print(f"Error rendering {tree_path}: {e}")
        return False

if __name__ == "__main__":
    print("Starting gallery rendering...")
    for tdir in TREE_DIRS:
        for f in os.listdir(tdir):
            if f.endswith(".treefile"):
                tree_path = os.path.join(tdir, f)
                img_name = f.replace(".treefile", ".png")
                output_path = os.path.join(IMAGE_DIR, img_name)
                
                if os.path.exists(output_path): continue
                
                print(f"Rendering: {f}")
                render_tree(tree_path, output_path, f.replace("_", " "))
    print("Gallery rendering complete.")
