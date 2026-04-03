from Bio import SeqIO
import os

def merge(in_files, out_file):
    seen = set()
    uniq = []
    for f in in_files:
        for r in SeqIO.parse(f, "fasta"):
            if r.id not in seen:
                seen.add(r.id)
                uniq.append(r)
    SeqIO.write(uniq, out_file, "fasta")
    print(f"Merged {out_file}")

os.chdir("/Users/bushrakhan/Desktop/NIPGR-data/MADS-box-Evolutionary-gene-detection/Workflow_Step-by-Step/TASK_7/uploads/")
merge(["Prunus_persica_cleaned.fa", "AT_Full_Anchors.fa"], "Prunus_with_AT_Full.fa")
merge(["Prunus_MADS_Domains.fa", "AT_MADS_Anchors.fa"], "Prunus_with_AT_MADS.fa")
merge(["Prunus_Kbox_Domains.fa", "AT_Kbox_Anchors.fa"], "Prunus_with_AT_Kbox.fa")
