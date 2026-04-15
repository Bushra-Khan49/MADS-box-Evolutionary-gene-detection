import os, shutil

BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
WORKFLOW_DIR = os.path.join(BASE_DIR, "Workflow_Step-by-Step")

# Define Categories
CAT_TREES = "1.Phylogenetic_Trees"
CAT_VISUALS = "2.Tree_Visualizations"
CAT_ALIGNMENTS = "3.Sequence_Alignments"
CAT_METADATA = "4.Technical_Metadata"

TREE_EXTS = [".treefile", ".contree", ".bionj", ".splits.nex", ".mldist", ".log", ".iqtree", ".ckp.gz"]
ALN_EXTS = [".fa", ".fasta", ".meg", ".mtsx", ".phy"]
VISUAL_EXTS = [".png", ".jpg", ".jpeg", ".pdf"]
META_EXTS = [".py", ".txt", ".zip", ".domtblout", ".html", ".out", ".csv"]

def get_target_dir(filename, base_uploads):
    ext = os.path.splitext(filename)[1].lower()
    if ext in TREE_EXTS: return os.path.join(base_uploads, CAT_TREES)
    if ext in VISUAL_EXTS: return os.path.join(base_uploads, CAT_VISUALS)
    if ext in ALN_EXTS: return os.path.join(base_uploads, CAT_ALIGNMENTS)
    return os.path.join(base_uploads, CAT_METADATA)

def classify_task(task_id):
    uploads_dir = os.path.join(WORKFLOW_DIR, task_id, "uploads")
    if not os.path.exists(uploads_dir): return
    
    print(f"Processing {task_id}...")
    
    # Create target dirs
    for d in [CAT_TREES, CAT_VISUALS, CAT_ALIGNMENTS, CAT_METADATA]:
        os.makedirs(os.path.join(uploads_dir, d), exist_ok=True)
    
    # We want to process EVERY file in the uploads directory recursively
    # but move them into the new 1-4 structure at the uploads/ level
    for root, dirs, files in os.walk(uploads_dir):
        # Skip the target dirs we just created to avoid infinite recursion or moving them into themselves
        if any(cat in root for cat in [CAT_TREES, CAT_VISUALS, CAT_ALIGNMENTS, CAT_METADATA]):
            continue
            
        for f in files:
            src_path = os.path.join(root, f)
            dest_cat_dir = get_target_dir(f, uploads_dir)
            dest_path = os.path.join(dest_cat_dir, f)
            
            # If destination already exists, don't overwrite unless it's the exact same file
            try:
                if os.path.exists(dest_path): os.remove(src_path)
                else: shutil.move(src_path, dest_path)
            except: pass

    # Cleanup empty subfolders (like 'ML')
    for d in os.listdir(uploads_dir):
        dp = os.path.join(uploads_dir, d)
        if os.path.isdir(dp) and d not in [CAT_TREES, CAT_VISUALS, CAT_ALIGNMENTS, CAT_METADATA]:
            try: shutil.rmtree(dp)
            except: pass

if __name__ == "__main__":
    for i in range(1, 11):
        classify_task(f"TASK_{i}")
    print("Done.")
