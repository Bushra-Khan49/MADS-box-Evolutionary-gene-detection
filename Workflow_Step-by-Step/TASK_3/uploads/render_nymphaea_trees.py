import os
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

def render_tree(tree_file, output_img, title):
    if not os.path.exists(tree_file):
        print(f"Skipping {tree_file}")
        return

    t = Tree(tree_file)
    ts = TreeStyle()
    ts.mode = "c"  # Circular
    ts.arc_start = -180
    ts.arc_span = 360
    ts.show_leaf_name = False # Custom face
    ts.title.add_face(TextFace(title, fsize=20), column=0)

    # Standard MIKCc subclade palette
    clade_colors = {
        "SEP": "#FF0000", "AP1": "#FF4500", "FUL": "#FF8C00", "AP3": "#1E90FF",
        "PI": "#00BFFF", "AG": "#008000", "STK": "#32CD32", "SOC1": "#8B008B",
        "SVP": "#9932CC", "ANR1": "#FFD700", "FLC": "#DAA520", "Bs": "#4B0082"
    }

    for leaf in t.iter_leaves():
        color = "#808080"  # Default Gray
        for clade, hex_color in clade_colors.items():
            if clade in leaf.name.upper():
                color = hex_color
                break
        
        nstyle = NodeStyle()
        nstyle["fgcolor"] = color
        nstyle["size"] = 6
        leaf.set_style(nstyle)
        
        # Add labels with matching color
        leaf.add_face(TextFace(leaf.name, fsize=10, fgcolor=color), column=0, position="branch-right")

    # Legend
    ts.legend.add_face(TextFace("Subclade Legend:", fsize=15, bold=True), column=0)
    for clade, color in clade_colors.items():
        ts.legend.add_face(TextFace(f" ■ {clade} ", fgcolor=color, fsize=12), column=0)

    t.render(output_img, w=2500, units="px", tree_style=ts)
    print(f"Rendered {output_img}")

os.chdir("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_3/uploads/")
os.makedirs("Colored_Tree_Images", exist_ok=True)
render_tree("Nymphaea_Full_ML.treefile", "Colored_Tree_Images/Nymphaea_Full_Proteome_circular.png", "Nymphaea colorata - Full Proteome ML Tree")
render_tree("Nymphaea_MADS_ML.treefile", "Colored_Tree_Images/Nymphaea_MADS_Domain_circular.png", "Nymphaea colorata - MADS Domain ML Tree")
render_tree("Nymphaea_Kbox_ML.treefile", "Colored_Tree_Images/Nymphaea_Kbox_Domain_circular.png", "Nymphaea colorata - K-box Domain ML Tree")
