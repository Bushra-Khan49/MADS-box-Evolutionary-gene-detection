import os, time, sys
sys.path.append("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/Scripts")
from run_batch_phylo_v2 import render_premium, load_annotations

TREE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/3.Phylogeny_Output/Trees_FullLength"
IMG_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline/4.Visualization_Portfolio/Standardized_Trees"

def continuous_render():
    ann = load_annotations()
    print("Starting continuous background rendering...")
    while True:
        tree_files = [f for f in os.listdir(TREE_DIR) if f.endswith(".treefile")]
        for tf in tree_files:
            # Expected name format: Species_Algorithm_ML.treefile
            parts = tf.replace(".treefile", "").split("_")
            if len(parts) < 3: continue
            
            algo = parts[-2]
            species = "_".join(parts[:-2])
            img_out = os.path.join(IMG_DIR, f"{species}_{algo}_Premium.png")
            
            # If image doesn't exist or is older than the tree, render it
            tree_path = os.path.join(TREE_DIR, tf)
            if not os.path.exists(img_out) or os.path.getmtime(tree_path) > os.path.getmtime(img_out):
                print(f"Rendering {species} ({algo})...")
                render_premium(tree_path, img_out, species, algo, ann)
        
        time.sleep(60) # Check every minute

if __name__ == "__main__":
    continuous_render()
