import os
import subprocess
import time

# Configuration
TOOLS = {
    "mafft": "/opt/homebrew/bin/mafft",
    "muscle": "/opt/homebrew/bin/muscle",
    "clustalo": "/opt/homebrew/bin/clustalo",
    "iqtree2": "/opt/homebrew/bin/iqtree2"
}

BASE_DIR = "/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Advanced_Phylogenetic_Pipeline"
INPUT_DIR = os.path.join(BASE_DIR, "3.Phylogeny_Output/Combined_FullLength")
MSA_DIR = os.path.join(BASE_DIR, "3.Phylogeny_Output/Alignments_FullLength")
TREE_DIR = os.path.join(BASE_DIR, "3.Phylogeny_Output/Trees_FullLength")

# Ensure directories exist
os.makedirs(MSA_DIR, exist_ok=True)
os.makedirs(TREE_DIR, exist_ok=True)

def run_msa_mafft(input_fa, output_fa):
    print(f"  [MSA] MAFFT: {os.path.basename(input_fa)}")
    with open(output_fa, "w") as out:
        subprocess.run([TOOLS["mafft"], "--auto", input_fa], stdout=out, check=True)

def run_msa_muscle(input_fa, output_fa):
    print(f"  [MSA] MUSCLE: {os.path.basename(input_fa)}")
    # MUSCLE 5 behavior: muscle -align input.fa -output aln.afa
    subprocess.run([TOOLS["muscle"], "-align", input_fa, "-output", output_fa], check=True)

def run_msa_clustalo(input_fa, output_fa):
    print(f"  [MSA] Clustal Omega: {os.path.basename(input_fa)}")
    subprocess.run([TOOLS["clustalo"], "-i", input_fa, "-o", output_fa, "--force"], check=True)

def run_iqtree(alignment_fa, output_prefix):
    print(f"  [ML TREE] IQ-TREE 2: {os.path.basename(alignment_fa)}")
    # -m LG+F+G -B 1000 -nt AUTO
    cmd = [
        TOOLS["iqtree2"],
        "-s", alignment_fa,
        "-m", "LG+F+G",
        "-B", "1000",
        "-pre", output_prefix,
        "-nt", "AUTO",
        "-redo"
    ]
    subprocess.run(cmd, check=True)

def process_species(species):
    print(f"\n>>> Processing Species: {species} <<<")
    input_file = os.path.join(INPUT_DIR, f"{species}_with_AT_Strict45.fa")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    algorithms = ["MAFFT", "MUSCLE", "ClustalO"]
    
    for algo in algorithms:
        msa_out = os.path.join(MSA_DIR, f"{species}_{algo}_Aligned.fa")
        tree_prefix = os.path.join(TREE_DIR, f"{species}_{algo}_ML")
        
        try:
            # 1. Run MSA
            if algo == "MAFFT":
                run_msa_mafft(input_file, msa_out)
            elif algo == "MUSCLE":
                run_msa_muscle(input_file, msa_out)
            elif algo == "ClustalO":
                run_msa_clustalo(input_file, msa_out)
            
            # 2. Run Tree
            run_iqtree(msa_out, tree_prefix)
            
        except subprocess.CalledProcessError as e:
            print(f"Error processing {species} with {algo}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Run specific species provided in command line
        for sp in sys.argv[1:]:
            process_species(sp)
    else:
        # Default target species
        species_list = [
            "Amborella_trichopoda",
            "Cinnamomum_kanehirae",
            "Glycine_max",
            "Helianthus_annuuss",
            "Medicago_truncatula",
            "Nelumbo_nucifera",
            "Nymphaea_colorata",
            "Oryza_sativa",
            "Piper_auritum",
            "Prunus_persica"
        ]
        for sp in species_list:
            process_species(sp)
