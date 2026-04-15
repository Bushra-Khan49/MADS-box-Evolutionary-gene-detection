import os
import sys
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

# Set offscreen rendering for headless environment
os.environ["QT_QPA_PLATFORM"] = "offscreen"

def render_tree(tree_file, output_image, title):
    if not os.path.exists(tree_file):
        print(f"Error: Tree file {tree_file} not found.")
        return
    
    try:
        # Load the tree (Newick format 1 includes support values)
        t = Tree(tree_file, format=1)
    except Exception as e:
        print(f"Error loading tree: {e}")
        return
        
    ts = TreeStyle()
    ts.mode = "c" # Circular mode
    ts.arc_start = -180
    ts.arc_span = 360
    ts.show_leaf_name = False 
    ts.title.add_face(TextFace(title, fsize=20), column=0)
    
    # Legend
    ts.legend.add_face(TextFace("Legend:", fsize=12), column=0)
    ts.legend.add_face(TextFace(" Blue: Target Species (Amborella)", fgcolor="blue", fsize=10), column=0)
    ts.legend.add_face(TextFace(" Red: Arabidopsis Anchors (Strict 45)", fgcolor="red", fsize=10), column=0)
    
    for n in t.iter_leaves():
        nstyle = NodeStyle()
        if "AT" in n.name:
            # Arabidopsis Anchor
            nstyle["fgcolor"] = "red"
            nstyle["size"] = 10
            face = TextFace(n.name, fgcolor="red", fsize=12)
            face.opacity = 0.6 
        else:
            # Target Species
            nstyle["fgcolor"] = "blue"
            nstyle["size"] = 15
            face = TextFace(n.name, fgcolor="blue", fsize=14, bold=True)
            face.opacity = 1.0
        
        n.set_style(nstyle)
        n.add_face(face, column=0, position="branch-right")
    
    # Clean up internal nodes
    for n in t.traverse():
        if not n.is_leaf():
            nstyle = NodeStyle()
            nstyle["size"] = 0
            n.set_style(nstyle)
            
    # Render
    t.render(output_image, w=2000, units="px", tree_style=ts)
    print(f"Tree rendered successfully to {output_image}")

if __name__ == "__main__":
    species = "Amborella_trichopoda"
    tree_dir = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/3.Phylogeny_Output/Trees_FullLength"
    img_dir = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/4.Visualization_Portfolio/Standardized_Trees"
    
    os.makedirs(img_dir, exist_ok=True)
    
    algorithms = ["MAFFT", "MUSCLE", "ClustalO"]
    for algo in algorithms:
        tree_path = os.path.join(tree_dir, f"{species}_{algo}_ML.treefile")
        output_path = os.path.join(img_dir, f"{species}_{algo}_Check.png")
        render_tree(tree_path, output_path, f"{species} ({algo} ML Tree)")
