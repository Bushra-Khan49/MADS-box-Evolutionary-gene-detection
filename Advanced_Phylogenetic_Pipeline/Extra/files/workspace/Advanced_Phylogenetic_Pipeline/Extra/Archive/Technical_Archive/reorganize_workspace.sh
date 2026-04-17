#!/bin/bash
# Reorganization Script to synchronize workspace with 5-phase structure
BASE_DIR="/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection"
TARGET_DIR="$BASE_DIR/Advanced_Phylogenetic_Pipeline"

cd "$BASE_DIR"

# 1. Create structure
mkdir -p "$TARGET_DIR/0.Data_Resources/HMM_Models"
mkdir -p "$TARGET_DIR/0.Data_Resources/Project_Files"
mkdir -p "$TARGET_DIR/1.Orthology_Results/BLAST_Hits"
mkdir -p "$TARGET_DIR/1.Orthology_Results/Self_BLAST_Redundancy"
mkdir -p "$TARGET_DIR/2.Identification_Results/HMMER_Tables"
mkdir -p "$TARGET_DIR/2.Identification_Results/Intersection_Candidates"
mkdir -p "$TARGET_DIR/2.Identification_Results/Multiple_Sequence_Alignments"
mkdir -p "$TARGET_DIR/3.Phylogeny_Output/Newick_Trees"
mkdir -p "$TARGET_DIR/3.Phylogeny_Output/IQ-TREE_Logs"
mkdir -p "$TARGET_DIR/4.Visualization_Portfolio/Colored_Trees"
mkdir -p "$TARGET_DIR/4.Visualization_Portfolio/Subclade_Charts"
mkdir -p "$TARGET_DIR/4.Visualization_Portfolio/Annotation_Tables"
mkdir -p "$TARGET_DIR/Scripts"
mkdir -p "$TARGET_DIR/Archive/Legacy_Documentation"
mkdir -p "$TARGET_DIR/Archive/Legacy_Root_Uploads"
mkdir -p "$TARGET_DIR/Archive/Legacy_Analysis_Folders"
mkdir -p "$TARGET_DIR/Archive/Legacy_System_Folders"
mkdir -p "$TARGET_DIR/Archive/Species_Data_Archives"

# 2. Migration from Root Uploads
# Phase 1
mv Uploads/*/*_TopHits_AT.txt "$TARGET_DIR/1.Orthology_Results/BLAST_Hits/" 2>/dev/null
# Phase 2
mv Uploads/*/*.domtblout "$TARGET_DIR/2.Identification_Results/HMMER_Tables/" 2>/dev/null
mv Uploads/*/*_domains.fa "$TARGET_DIR/2.Identification_Results/HMMER_Tables/" 2>/dev/null
mv Uploads/*/*_aligned.fa "$TARGET_DIR/2.Identification_Results/Multiple_Sequence_Alignments/" 2>/dev/null
mv Uploads/*/*_candidates.fa "$TARGET_DIR/2.Identification_Results/Multiple_Sequence_Alignments/" 2>/dev/null
mv Uploads/*/Combined_*.fa "$TARGET_DIR/2.Identification_Results/Multiple_Sequence_Alignments/" 2>/dev/null
# Phase 3
mv Uploads/Newick_Trees/*.nwk "$TARGET_DIR/3.Phylogeny_Output/Newick_Trees/" 2>/dev/null
mv Uploads/MASTER_MIKCc_FULL_ALIGNMENT.* "$TARGET_DIR/3.Phylogeny_Output/" 2>/dev/null
mv Uploads/Master_MIKCc_All_Species_* "$TARGET_DIR/3.Phylogeny_Output/" 2>/dev/null
# Phase 4
mv Uploads/*/*.png "$TARGET_DIR/4.Visualization_Portfolio/Colored_Trees/" 2>/dev/null
mv Uploads/MIKCc_Subclade_Annotation_Table.tsv "$TARGET_DIR/4.Visualization_Portfolio/Annotation_Tables/" 2>/dev/null
mv Uploads/*/*_Annotation_Summary.csv "$TARGET_DIR/4.Visualization_Portfolio/Annotation_Tables/" 2>/dev/null

# 3. Migration of root resources
mv HMM_Models/* "$TARGET_DIR/0.Data_Resources/HMM_Models/" 2>/dev/null
mv Project_Resources/* "$TARGET_DIR/0.Data_Resources/Project_Files/" 2>/dev/null
mv *.py "$TARGET_DIR/Scripts/" 2>/dev/null

# 4. Archiving
mv Uploads/* "$TARGET_DIR/Archive/Legacy_Root_Uploads/" 2>/dev/null
mv Simultaneous_Phylogenetic_Analysis "$TARGET_DIR/Archive/Legacy_Analysis_Folders/" 2>/dev/null
mv Unified_Phylogenetic_Tree_Collection "$TARGET_DIR/Archive/Legacy_Analysis_Folders/" 2>/dev/null
mv bin scratch scripts "$TARGET_DIR/Archive/Legacy_System_Folders/" 2>/dev/null

# Restore README
mv "$TARGET_DIR/Archive/Legacy_System_Folders/README.md" "$BASE_DIR/" 2>/dev/null
mv "$TARGET_DIR/Archive/Legacy_System_Folders/Inferences_and_Conclusions.md" "$BASE_DIR/" 2>/dev/null
mv "$TARGET_DIR/Scripts/Workflow_Step-by-Step" "$BASE_DIR/" 2>/dev/null

echo "Reorganization Complete"
