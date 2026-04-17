import os
from Bio import SeqIO

def extract_best_domains(fasta_path, mads_tbl, kbox_tbl):
    fasta_dict = SeqIO.to_dict(SeqIO.parse(fasta_path, "fasta"))
    
    def get_best_hits(tbl):
        best_hits = {} 
        if not os.path.exists(tbl): return {}
        with open(tbl, "r") as f:
            for line in f:
                if line.startswith("#"): continue
                parts = line.split()
                target, score, start, end = parts[0], float(parts[13]), int(parts[17]), int(parts[18])
                if target not in best_hits or score > best_hits[target][2]:
                    best_hits[target] = (start, end, score)
        return best_hits

    mads_hits = get_best_hits(mads_tbl)
    kbox_hits = get_best_hits(kbox_tbl)
    
    mads_seqs = []
    for tid, (s, e, _) in mads_hits.items():
        if tid in fasta_dict:
            rec = fasta_dict[tid][s-1:e]
            rec.id = f"{tid}_MADS"
            rec.description = ""
            mads_seqs.append(rec)
            
    kbox_seqs = []
    for tid, (s, e, _) in kbox_hits.items():
        if tid in fasta_dict:
            rec = fasta_dict[tid][s-1:e]
            rec.id = f"{tid}_Kbox"
            rec.description = ""
            kbox_seqs.append(rec)
            
    SeqIO.write(mads_seqs, "Nymphaea_MADS_Domains.fa", "fasta")
    SeqIO.write(kbox_seqs, "Nymphaea_Kbox_Domains.fa", "fasta")
    print(f"Extracted {len(mads_seqs)} MADS and {len(kbox_seqs)} K-box unique best-hits.")

fasta = "Nymphaea_colorata_cleaned.fa"
mads_tbl = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/Nymphaea_colorata/Nymphaea_colorata_MADS.domtblout"
kbox_tbl = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/Nymphaea_colorata/Nymphaea_colorata_Kbox.domtblout"

extract_best_domains(fasta, mads_tbl, kbox_tbl)
