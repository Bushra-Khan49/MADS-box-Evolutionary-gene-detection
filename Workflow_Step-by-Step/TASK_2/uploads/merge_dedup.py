import sys
from Bio import SeqIO

def merge_dedup(input_files, output_file):
    seen = set()
    unique_seqs = []
    for f in input_files:
        for record in SeqIO.parse(f, "fasta"):
            if record.id not in seen:
                seen.add(record.id)
                unique_seqs.append(record)
    SeqIO.write(unique_seqs, output_file, "fasta")
    print(f"Merged into {output_file}: {len(unique_seqs)} unique sequences.")

# For MADS
merge_dedup(["Amborella_MADS_Domains.fa", "AT_MADS_Anchors.fa"], "Combined_MADS_Amborella_AT.fa")
# For K-box
merge_dedup(["Amborella_Kbox_Domains.fa", "AT_Kbox_Anchors.fa"], "Combined_Kbox_Amborella_AT.fa")
