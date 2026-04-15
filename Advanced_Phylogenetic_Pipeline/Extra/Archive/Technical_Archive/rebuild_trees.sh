for f in Advanced_Phylogenetic_Pipeline/3.Phylogeny_Output/Alignments_FullLength/*.fa; do
    species=$(basename "$f" _MAFFT_Aligned.fa)
    echo "Constructing ML Tree for $species (LG + 1000 BS)..."
    /opt/homebrew/bin/iqtree2 -s "$f" -m LG -B 1000 -pre "Advanced_Phylogenetic_Pipeline/3.Phylogeny_Output/Trees_FullLength/${species}_ML" -nt AUTO -redo
done
echo "--- ALL TREES COMPLETE ---"
