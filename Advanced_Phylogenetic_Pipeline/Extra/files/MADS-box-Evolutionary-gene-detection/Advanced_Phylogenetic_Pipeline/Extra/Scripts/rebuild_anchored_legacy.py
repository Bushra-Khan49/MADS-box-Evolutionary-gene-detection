#!/usr/bin/env python3
import os, subprocess, shutil, csv, re
from Bio import SeqIO

# --- Paths ---
ROOT_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
ADV_DIR  = os.path.join(ROOT_DIR, "Advanced_Phylogenetic_Pipeline")
LEGACY_DIR = os.path.join(ADV_DIR, "Archive/Legacy_Analysis_Folders/Simultaneous_Phylogenetic_Analysis/Results")
ANCHOR_FILE = os.path.join(ADV_DIR, "0.Data_Resources/Arabidopsis_Master_Anchors.fa")
TREES_DIR = os.path.join(LEGACY_DIR, "Trees_Anchored") # New anchored trees
IMAGES_DIR = os.path.join(LEGACY_DIR, "Images") # Final images destination

os.makedirs(TREES_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# 1. --- Rebuild Anchored Alignments and Trees ---
def rebuild_anchored_results():
    species_list = [
        "Amborella_trichopoda", "Cinnamomum_kanehirae", "Glycine_max",
        "Helianthus_annuuss", "Medicago_truncatula", "Nelumbo_nucifera",
        "Nymphaea_colorata", "Oryza_sativa", "Prunus_persica", "Piper_auritum"
    ]
    algorithms = ["MAFFT", "MUSCLE", "ClustalO"]
    
    for species in species_list:
        print(f"\nProcessing {species}...")
        # Get species-only sequences from existing legacy alignments (extract without gaps)
        # We try to find any existing legacy alignment for that species
        species_seqs = []
        for alg in ["MAFFT", "MUSCLE", "ClustalO"]:
            legacy_fa = os.path.join(LEGACY_DIR, "Alignments", f"{species}_{alg}.fa")
            if os.path.exists(legacy_fa):
                for rec in SeqIO.parse(legacy_fa, "fasta"):
                    if not rec.id.startswith("AT"):
                        rec.seq = rec.seq.replace("-", "")
                        species_seqs.append(rec)
                break # Found the candidates
        
        if not species_seqs:
            print(f"  Warning: No legacy sequences found for {species}")
            continue

        # Merge with anchors
        combined_fa = os.path.join(TREES_DIR, f"{species}_combined.fa")
        anchors = list(SeqIO.parse(ANCHOR_FILE, "fasta"))
        # De-gap anchors just in case
        for r in anchors: r.seq = r.seq.replace("-", "")
        
        SeqIO.write(species_seqs + anchors, combined_fa, "fasta")
        
        # Run Alignments and Trees
        for alg in algorithms:
            print(f"  -> Running {alg} + IQ-TREE for anchored {species}...")
            out_fa = os.path.join(TREES_DIR, f"{species}_{alg}_Anchored.fa")
            
            # Align
            if alg == "MAFFT":
                with open(out_fa, "w") as f_out:
                    subprocess.run(["/opt/homebrew/bin/mafft", "--auto", combined_fa], stdout=f_out, stderr=subprocess.DEVNULL)
            elif alg == "MUSCLE":
                subprocess.run(["/opt/homebrew/bin/muscle", "-align", combined_fa, "-output", out_fa], stderr=subprocess.DEVNULL)
            elif alg == "ClustalO":
                subprocess.run(["/opt/homebrew/bin/clustalo", "-i", combined_fa, "-o", out_fa, "--force"], stderr=subprocess.DEVNULL)
            
            # Tree (Fast NJ-ML mode for batch)
            prefix = os.path.join(TREES_DIR, f"{species}_{alg}_NJ")
            subprocess.run(["/opt/homebrew/bin/iqtree2", "-s", out_fa, "-m", "LG", "-fast", "-pre", prefix, "-redo"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 2. --- Visualization Helper (Fixed Legend & Title) ---
# (I will execute this as a second part of the script)

if __name__ == "__main__":
    rebuild_anchored_results()
