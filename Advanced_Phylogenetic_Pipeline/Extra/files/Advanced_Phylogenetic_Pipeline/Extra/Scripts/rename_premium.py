import os

BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
WORKFLOW_DIR = os.path.join(BASE_DIR, "Workflow_Step-by-Step")

def rename_trees():
    for i in range(1, 11):
        task_id = f"TASK_{i}"
        target_dir = os.path.join(WORKFLOW_DIR, task_id, "uploads", "2.Tree_Visualizations")
        
        if os.path.exists(target_dir):
            print(f"Checking {task_id}...")
            for f in os.listdir(target_dir):
                if f.endswith("_Premium.png"):
                    old_path = os.path.join(target_dir, f)
                    new_filename = f.replace("_Premium.png", "_ML.png")
                    new_path = os.path.join(target_dir, new_filename)
                    
                    try:
                        os.rename(old_path, new_path)
                        print(f"  Renamed: {f} -> {new_filename}")
                    except Exception as e:
                        print(f"  Error renaming {f}: {e}")

if __name__ == "__main__":
    rename_trees()
