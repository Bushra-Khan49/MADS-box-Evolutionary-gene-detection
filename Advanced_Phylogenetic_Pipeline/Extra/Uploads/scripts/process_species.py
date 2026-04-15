import os
import sys
import subprocess
import re
import csv

def run_cmd(cmd, shell=True):
    # print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\nStderr: {result.stderr}", file=sys.stderr)
    return result.stdout

def parse_domtblout(file_path):
    ids = set()
    if not os.path.exists(file_path):
        return ids
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("#"): continue
            parts = line.split()
            if parts: ids.add(parts[0])
    return ids

def extract_sequences(fasta_in, id_list, fasta_out):
    id_set = set(id_list)
    with open(fasta_in, 'r') as fin, open(fasta_out, 'w') as fout:
        keep = False
        for line in fin:
            if line.startswith(">"):
                # Extracts the identifier before the first space
                header = line.split()[0][1:]
                keep = header in id_set
            if keep:
                fout.write(line)

def generate_summary(all_candidates, blast_file, at_mapping, out_csv):
    blast_results = {}
    if os.path.exists(blast_file):
        with open(blast_file, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if not parts or len(parts) < 6: continue
                qseqid, sseqid, evalue, bitscore, pident, length = parts
                if qseqid not in blast_results:
                    clean_at_id = sseqid.split('|')[0].strip()
                    symbol = at_mapping.get(clean_at_id, "N/A")
                    blast_results[qseqid] = [clean_at_id, symbol, evalue, bitscore, pident, length]
                
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Species_Gene_ID", "Homologous_Arabidopsis_Symbol", "Top_Arabidopsis_Hit", "E-value", "Bit-score", "%_Identity", "Alignment_Length"])
        for qid in sorted(list(all_candidates)):
            if qid in blast_results:
                writer.writerow([qid] + blast_results[qid])
            else:
                writer.writerow([qid, "No Match", "N/A", "N/A", "N/A", "N/A", "N/A"])

def load_at_mapping(at_ref_fasta):
    mapping = {}
    if not os.path.exists(at_ref_fasta): return mapping
    with open(at_ref_fasta, 'r') as f:
        for line in f:
            if line.startswith(">"):
                match = re.search(r'>(AT\w+G\d+\.\d+)\s*\|\s*Symbols:\s*([^|]+)', line)
                if match:
                    mapping[match.group(1)] = match.group(2).strip()
    return mapping

def process_species(working_dir, species_name, proteome_path, at_ref_path, at_mapping, remove_isoforms=True):
    print(f"--- Processing {species_name} ---")
    spec_work_dir = os.path.join(working_dir, "NIPGR_WORK", species_name)
    os.makedirs(spec_work_dir, exist_ok=True)
    
    mads_out = os.path.join(spec_work_dir, f"{species_name}_MADS.domtblout")
    kbox_out = os.path.join(spec_work_dir, f"{species_name}_Kbox.domtblout")
    ap2_out = os.path.join(spec_work_dir, f"{species_name}_AP2.domtblout")
    
    mads_ids = parse_domtblout(mads_out)
    kbox_ids = parse_domtblout(kbox_out)
    ap2_ids = parse_domtblout(ap2_out)
    
    mikcc_ids = mads_ids.intersection(kbox_ids) - ap2_ids
    print(f"Initial MIKCc candidates (MADS+K-box and NOT AP2): {len(mikcc_ids)}")
    
    if remove_isoforms:
        gene_to_isoform = {}
        for cid in sorted(list(mikcc_ids)):
            # More robust gene ID extraction depending on species
            # If standard rice format LOC_Os... .1
            if "." in cid:
                gene_id = cid.rsplit('.', 1)[0]
            else:
                gene_id = cid
                
            if gene_id not in gene_to_isoform:
                gene_to_isoform[gene_id] = cid
            elif ".1" in cid:
                gene_to_isoform[gene_id] = cid
        final_ids = sorted(gene_to_isoform.values())
    else:
        final_ids = sorted(list(mikcc_ids))
        
    print(f"Final candidates: {len(final_ids)}")
    
    id_file = os.path.join(spec_work_dir, f"{species_name}_MIKCc_final_ids.txt")
    with open(id_file, 'w') as f:
        for fid in final_ids: f.write(fid + "\n")
        
    candidate_fasta = os.path.join(spec_work_dir, f"{species_name}_candidates.fa")
    extract_sequences(proteome_path, final_ids, candidate_fasta)
    
    if len(final_ids) > 0:
        blast_out = os.path.join(spec_work_dir, f"{species_name}_vs_AT.blastp.out")
        run_cmd(f"blastp -query {candidate_fasta} -db {at_ref_path} -out {blast_out} -evalue 1e-5 -outfmt '6 qseqid sseqid evalue bitscore pident length'")
        generate_summary(final_ids, blast_out, at_mapping, os.path.join(spec_work_dir, f"{species_name}_Annotation_Summary.csv"))
    else:
        print(f"Skipping BLAST for {species_name} - no candidates found.")

if __name__ == "__main__":
    base_dir = "/Users/bushrakhan/Desktop/NIPGR-data"
    at_ref = os.path.join(base_dir, "AT_ALL_MADSbox_PROTEINseq.txt")
    mapping = load_at_mapping(at_ref)
    
    species_data = [
        ("Amborella_trichopoda", "NIPGR-Plants/Amborella_trichopoda/Atrichopoda_291_v1.0.protein_primaryTranscriptOnly.fa", False),
        ("Cinnamomum_kanehirae", "NIPGR-Plants/Cinnamomum_kanehirae/Ckanehirae_531_v3.protein_primaryTranscriptOnly.fa", False),
        ("Glycine_max", "NIPGR-Plants/Glycine_max/Gmax_508_Wm82.a4.v1.protein_primaryTranscriptOnly.fa", False),
        ("Helianthus_annuuss", "NIPGR-Plants/Helianthus_annuuss/Hannuus_494_r1.2.protein_primaryTranscriptOnly.fa", False),
        ("Medicago_truncatula", "NIPGR-Plants/Medicago_truncatula/Mtruncatula_285_Mt4.0v1.protein_primaryTranscriptOnly.fa", False),
        ("Nelumbo_nucifera", "NIPGR-Plants/Nelumbo_nucifera/protein.faa", False),
        ("Nymphaea_colorata", "NIPGR-Plants/Nymphaea_colorata/Ncolorata_566_v1.2.protein_primaryTranscriptOnly.fa", False),
        ("Oryza_sativa", "NIPGR-Plants/Oryza_sativa/Osativa_323_v7.0.protein_primaryTranscriptOnly.fa", False),
        ("Prunus_persica", "NIPGR-Plants/Prunus_persica/Ppersica_298_v2.1.protein_primaryTranscriptOnly.fa", False)
    ]
    
    for s_name, p_path, rm_iso in species_data:
        full_p_path = os.path.join(base_dir, p_path)
        if os.path.exists(full_p_path):
            process_species(base_dir, s_name, full_p_path, at_ref, mapping, rm_iso)
        else:
            print(f"Proteome not found for {s_name}: {full_p_path}")
