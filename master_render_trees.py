import os
import sys
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

# Set QT_QPA_PLATFORM for offscreen rendering
os.environ["QT_QPA_PLATFORM"] = "offscreen"

def render_tree(tree_path, output_image):
    if not os.path.exists(tree_path):
        print(f"Skipping: {tree_path} (not found)")
        return
    
    try:
        t = Tree(tree_path, format=1)
    except:
        print(f"Error parsing: {tree_path}")
        return

    ts = TreeStyle()
    ts.shape_heading_filter = False
    ts.show_leaf_name = False  # We add custom TextFaces
    ts.mode = "c"
    ts.arc_start = -180
    ts.arc_span = 360
    ts.legend_position = 4

    for node in t.iter_leaves():
        nstyle = NodeStyle()
        if "AT" in node.name:
            # Arabidopsis Anchor: Red, 50% opacity
            nstyle["fgcolor"] = "red"
            nstyle["size"] = 5
            face = TextFace(node.name, fgcolor="red", fsize=10)
            face.opacity = 0.5
        else:
            # Target Species: Blue, 100% opacity
            nstyle["fgcolor"] = "blue"
            nstyle["size"] = 8
            face = TextFace(node.name, fgcolor="blue", fsize=10)
            face.opacity = 1.0
        
        node.set_style(nstyle)
        node.add_face(face, column=0, position="branch-right")

    t.render(output_image, w=1600, units="px", tree_style=ts)
    print(f"Rendered: {output_image}")

base_dir = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step"
output_dir = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Colored_Tree_Images"
os.makedirs(output_dir, exist_ok=True)

tasks = [
    ("TASK_1", "Rice_Full_Proteome", "Rice_ClustalO_ML.treefile"),
    ("TASK_1", "Rice_MADS_Domain", "Rice_MADS_Domain_ML.treefile"),
    ("TASK_1", "Rice_Kbox_Domain", "Rice_Kbox_Domain_ML.treefile"),
    
    ("TASK_2", "Amborella_Full_Proteome", "Atrichopoda_ML_Full.treefile"),
    ("TASK_2", "Amborella_MADS_Domain", "Amborella_MADS_Domain_ML.treefile"),
    ("TASK_2", "Amborella_Kbox_Domain", "Amborella_Kbox_Domain_ML.treefile"),
    
    ("TASK_3", "Nymphaea_Full_Proteome", "Nymphaea_Full_ML.treefile"),
    ("TASK_3", "Nymphaea_MADS_Domain", "Nymphaea_MADS_ML.treefile"),
    ("TASK_3", "Nymphaea_Kbox_Domain", "Nymphaea_Kbox_ML.treefile"),
    
    ("TASK_4", "Cinnamomum_Full_Proteome", "Cinnamomum_Full_ML.treefile"),
    ("TASK_4", "Cinnamomum_MADS_Domain", "Cinnamomum_MADS_ML.treefile"),
    ("TASK_4", "Cinnamomum_Kbox_Domain", "Cinnamomum_Kbox_ML.treefile"),
    
    ("TASK_5", "Glycine_Full_Proteome", "Glycine_Full_ML.treefile"),
    ("TASK_5", "Glycine_MADS_Domain", "Glycine_MADS_ML.treefile"),
    ("TASK_5", "Glycine_Kbox_Domain", "Glycine_Kbox_ML.treefile"),
    
    ("TASK_6", "Medicago_Full_Proteome", "Medicago_Full_ML.treefile"),
    ("TASK_6", "Medicago_MADS_Domain", "Medicago_MADS_ML.treefile"),
    ("TASK_6", "Medicago_Kbox_Domain", "Medicago_Kbox_ML.treefile"),
    
    ("TASK_7", "Prunus_Full_Proteome", "Prunus_Full_ML.treefile"),
    ("TASK_7", "Prunus_MADS_Domain", "Prunus_MADS_ML.treefile"),
    ("TASK_7", "Prunus_Kbox_Domain", "Prunus_Kbox_ML.treefile"),
    
    ("TASK_8", "Helianthus_Full_Proteome", "Helianthus_Full_ML.treefile"),
    ("TASK_8", "Helianthus_MADS_Domain", "Helianthus_MADS_ML.treefile"),
    ("TASK_8", "Helianthus_Kbox_Domain", "Helianthus_Kbox_ML.treefile"),
    
    ("TASK_9", "Nelumbo_Full_Proteome", "Nelumbo_Full_ML.treefile"),
    ("TASK_9", "Nelumbo_MADS_Domain", "Nelumbo_MADS_ML.treefile"),
    ("TASK_9", "Nelumbo_Kbox_Domain", "Nelumbo_Kbox_ML.treefile"),
]

for task_folder, name, tf in tasks:
    tree_path = os.path.join(base_dir, task_folder, "uploads", tf)
    output_image = os.path.join(output_dir, f"{name}_circular.png")
    render_tree(tree_path, output_image)
    # Also copy to Task folder
    task_out = os.path.join(base_dir, task_folder, f"{name}_circular.png")
    if os.path.exists(output_image):
        import shutil
        shutil.copy2(output_image, task_out)

