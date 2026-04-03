import os
from Bio import SeqIO

def extract_domains(domtblout, fasta, output_mads, output_kbox):
    mads_coords = {}
    kbox_coords = {}
    
    # Parse domtblout for MADS (PF00319) and K-box (PF01486)
    with open(domtblout, "r") as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.split()
            target = parts[0]
            domain = parts[3]
            start = int(parts[17])
            end = int(parts[18])
            score = float(parts[13])
            
            if domain == "MADS":
                if target not in mads_coords or score > mads_coords[target][2]:
                    mads_coords[target] = (start, end, score)
            elif domain == "K-box":
                if target not in kbox_coords or score > kbox_coords[target][2]:
                    kbox_coords[target] = (start, end, score)
    
    # Extract sequences
    mads_seqs = []
    kbox_seqs = []
    for record in SeqIO.parse(fasta, "fasta"):
        if record.id in mads_coords:
            s, e, _ = mads_coords[record.id]
            sub = record[s-1:e]
            sub.id = f"{record.id}_MADS"
            sub.description = ""
            mads_seqs.append(sub)
        if record.id in kbox_coords:
            s, e, _ = kbox_coords[record.id]
            sub = record[s-1:e]
            sub.id = f"{record.id}_Kbox"
            sub.description = ""
            kbox_seqs.append(sub)
            
    SeqIO.write(mads_seqs, output_mads, "fasta")
    SeqIO.write(kbox_seqs, output_kbox, "fasta")
    print(f"Extracted {len(mads_seqs)} MADS and {len(kbox_seqs)} K-box domains.")

# For Amborella, I'll combine the domtblout results if they are in separate files
# NIPGR_WORK has Amborella_trichopoda_MADS.domtblout and Amborella_trichopoda_Kbox.domtblout

def extract_from_separate():
    fasta = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/Amborella_trichopoda/Amborella_trichopoda_candidates.fa"
    mads_tbl = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/Amborella_trichopoda/Amborella_trichopoda_MADS.domtblout"
    kbox_tbl = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/Amborella_trichopoda/Amborella_trichopoda_Kbox.domtblout"
    
    mads_seqs = []
    kbox_seqs = []
    
    # MADS
    with open(mads_tbl, "r") as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.split()
            target, start, end = parts[0], int(parts[17]), int(parts[18])
            for record in SeqIO.parse(fasta, "fasta"):
                if record.id == target:
                    sub = record[start-1:end]
                    sub.id = f"{record.id}_MADS"
                    sub.description = ""
                    mads_seqs.append(sub)
                    break
    
    # Kbox
    with open(kbox_tbl, "r") as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.split()
            target, start, end = parts[0], int(parts[17]), int(parts[18])
            for record in SeqIO.parse(fasta, "fasta"):
                if record.id == target:
                    sub = record[start-1:end]
                    sub.id = f"{record.id}_Kbox"
                    sub.description = ""
                    kbox_seqs.append(sub)
                    break
                    
    SeqIO.write(mads_seqs, "Amborella_MADS_Domains.fa", "fasta")
    SeqIO.write(kbox_seqs, "Amborella_Kbox_Domains.fa", "fasta")
    print(f"Done: {len(mads_seqs)} MADS, {len(kbox_seqs)} Kbox.")

extract_from_separate()
