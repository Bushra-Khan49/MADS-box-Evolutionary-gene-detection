import os
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

def render_circular_tree(tree_file, output_image, title):
    if not os.path.exists(tree_file):
        print(f"File {tree_file} not found.")
        return
    
    t = Tree(tree_file)
    ts = TreeStyle()
    ts.mode = "c"
    ts.arc_start = -180
    ts.arc_span = 360
    ts.show_leaf_name = True
    ts.show_branch_support = True
    ts.title.add_face(TextFace(title, fsize=20), column=0)
    
    # Custom styles
    for n in t.traverse():
        nstyle = NodeStyle()
        if n.is_leaf():
            if "AT" in n.name:
                nstyle["fgcolor"] = "red"
                nstyle["size"] = 8
            else:
                nstyle["fgcolor"] = "blue"
                nstyle["size"] = 6
        else:
            nstyle["size"] = 0
        n.set_style(nstyle)
    
    t.render(output_image, w=1200, units="px", tree_style=ts)
    print(f"Rendered {output_image}")

os.chdir("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_8/uploads/")
render_circular_tree("Helianthus_Full_ML.treefile", "Helianthus_Full_Proteome_circular.png", "Helianthus Full Proteome MADS-box (IQ-TREE)")
render_circular_tree("Helianthus_MADS_ML.treefile", "Helianthus_MADS_Domain_circular.png", "Helianthus MADS Domain (IQ-TREE)")
render_circular_tree("Helianthus_Kbox_ML.treefile", "Helianthus_Kbox_Domain_circular.png", "Helianthus K-box Domain (IQ-TREE)")
