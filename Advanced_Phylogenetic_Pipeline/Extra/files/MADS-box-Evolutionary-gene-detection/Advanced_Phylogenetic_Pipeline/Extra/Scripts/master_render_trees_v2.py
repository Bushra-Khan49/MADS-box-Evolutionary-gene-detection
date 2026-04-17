import os
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

os.environ["QT_QPA_PLATFORM"] = "offscreen"

def render_v2(tree_file, output_image, title):
    if not os.path.exists(tree_file):
        return
    
    try:
        t = Tree(tree_file, format=1)
    except:
        return
        
    ts = TreeStyle()
    ts.mode = "c"
    ts.arc_start = -180
    ts.arc_span = 360
    ts.show_leaf_name = False # We use custom faces
    ts.title.add_face(TextFace(title, fsize=15), column=0)
    
    for n in t.iter_leaves():
        nstyle = NodeStyle()
        if "AT" in n.name:
            nstyle["fgcolor"] = "red"
            nstyle["size"] = 5
            face = TextFace(n.name, fgcolor="red", fsize=10)
            face.opacity = 0.5
        else:
            nstyle["fgcolor"] = "blue"
            nstyle["size"] = 8
            face = TextFace(n.name, fgcolor="blue", fsize=12)
            face.opacity = 1.0
        
        n.set_style(nstyle)
        n.add_face(face, column=0, position="branch-right")
    
    for n in t.traverse():
        if not n.is_leaf():
            nstyle = NodeStyle()
            nstyle["size"] = 0
            n.set_style(nstyle)
            
    t.render(output_image, w=1600, units="px", tree_style=ts)

tasks = [
  ("TASK_1", "Rice", "Rice_ClustalO_ML.treefile", "Rice_MADS_Domain_ML.treefile", "Rice_Kbox_Domain_ML.treefile"),
  ("TASK_2", "Amborella", "Atrichopoda_ML_Full.treefile", "Amborella_MADS_Domain_ML.treefile", "Amborella_Kbox_Domain_ML.treefile"),
  ("TASK_3", "Nymphaea", "Nymphaea_Full_ML.treefile", "Nymphaea_MADS_ML.treefile", "Nymphaea_Kbox_ML.treefile"),
  ("TASK_4", "Cinnamomum", "Cinnamomum_Full_ML.treefile", "Cinnamomum_MADS_ML.treefile", "Cinnamomum_Kbox_ML.treefile"),
  ("TASK_5", "Glycine", "Glycine_Full_ML.treefile", "Glycine_MADS_ML.treefile", "Glycine_Kbox_ML.treefile"),
  ("TASK_6", "Medicago", "Medicago_Full_ML.treefile", "Medicago_MADS_ML.treefile", "Medicago_Kbox_ML.treefile"),
  ("TASK_7", "Prunus", "Prunus_Full_ML.treefile", "Prunus_MADS_ML.treefile", "Prunus_Kbox_ML.treefile"),
  ("TASK_8", "Helianthus", "Helianthus_Full_ML.treefile", "Helianthus_MADS_ML.treefile", "Helianthus_Kbox_ML.treefile"),
  ("TASK_9", "Nelumbo", "Nelumbo_Full_ML.treefile", "Nelumbo_MADS_ML.treefile", "Nelumbo_Kbox_ML.treefile"),
]

base = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step"
img_base = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Colored_Tree_Images"
os.makedirs(img_base, exist_ok=True)

for task, species, f_tree, m_tree, k_tree in tasks:
    up = os.path.join(base, task, "uploads")
    # Full
    render_v2(os.path.join(up, f_tree), os.path.join(img_base, f"{species}_Full_Proteome_circular.png"), f"{species} Full Proteome")
    # MADS
    render_v2(os.path.join(up, m_tree), os.path.join(img_base, f"{species}_MADS_Domain_circular.png"), f"{species} MADS Domain")
    # Kbox
    render_v2(os.path.join(up, k_tree), os.path.join(img_base, f"{species}_Kbox_Domain_circular.png"), f"{species} K-box Domain")

