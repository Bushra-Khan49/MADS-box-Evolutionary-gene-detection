import os
import shutil

# Paths
BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
WORKFLOW_DIR = os.path.join(BASE_DIR, "Workflow_Step-by-Step")
MEGA_SRC_DIR = os.path.join(BASE_DIR, "Advanced_Phylogenetic_Pipeline/3.Phylogeny_Output")

# Species to Correct TASK Mapping
SPECIES_TO_TASK = {
    "Arabidopsis": "TASK_1",
    "Amborella": "TASK_2",
    "Nymphaea": "TASK_3",
    "Cinnamomum": "TASK_4",
    "Oryza": "TASK_5",
    "Rice": "TASK_5",
    "Glycine": "TASK_6",
    "Medicago": "TASK_7",
    "Prunus": "TASK_8",
    "Helianthus": "TASK_9",
    "Nelumbo": "TASK_10"
}

def realign_and_consolidate():
    # 1. Realignment Audit & Execution
    tasks = [f"TASK_{i}" for i in range(1, 11)]
    
    for task_id in tasks:
        task_path = os.path.join(WORKFLOW_DIR, task_id, "uploads")
        if not os.path.exists(task_path): continue
        
        for subfolder in ["1.Phylogenetic_Trees", "2.Tree_Visualizations", "3.Sequence_Alignments", "4.Technical_Metadata"]:
            sub_path = os.path.join(task_path, subfolder)
            if not os.path.exists(sub_path): continue
            
            for filename in os.listdir(sub_path):
                # Identify species keyword
                detected_species = None
                for species_key in SPECIES_TO_TASK.keys():
                    if filename.lower().startswith(species_key.lower()):
                        detected_species = species_key
                        break
                
                if detected_species:
                    correct_task = SPECIES_TO_TASK[detected_species]
                    if correct_task != task_id:
                        # Move to correct task
                        src = os.path.join(sub_path, filename)
                        dest_dir = os.path.join(WORKFLOW_DIR, correct_task, "uploads", subfolder)
                        os.makedirs(dest_dir, exist_ok=True)
                        dest = os.path.join(dest_dir, filename)
                        
                        print(f"Moving {filename}: {task_id} -> {correct_task}")
                        shutil.move(src, dest)

    # 2. MEGA File Distribution
    if os.path.exists(MEGA_SRC_DIR):
        for filename in os.listdir(MEGA_SRC_DIR):
            if filename.endswith(".meg") or filename.endswith(".mtsx"):
                detected_species = None
                for species_key in SPECIES_TO_TASK.keys():
                    if filename.lower().startswith(species_key.lower()):
                        detected_species = species_key
                        break
                
                if detected_species:
                    correct_task = SPECIES_TO_TASK[detected_species]
                    dest_dir = os.path.join(WORKFLOW_DIR, correct_task, "uploads", "1.Phylogenetic_Trees")
                    os.makedirs(dest_dir, exist_ok=True)
                    dest = os.path.join(dest_dir, filename)
                    
                    src = os.path.join(MEGA_SRC_DIR, filename)
                    print(f"Distributing MEGA File {filename} to {correct_task}")
                    shutil.copy2(src, dest)

if __name__ == "__main__":
    realign_and_consolidate()
