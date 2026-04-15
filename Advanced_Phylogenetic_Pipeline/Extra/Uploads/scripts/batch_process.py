#!/usr/bin/env python3
import os
import subprocess

# Configuration: Species -> Protein Sequence File (Remaining 4)
SPECIES_MAP = {
    "Nymphaea_colorata": "NIPGR-Plants/Nymphaea_colorata/Ncolorata_566_v1.2.protein_primaryTranscriptOnly.fa",
    "Oryza_sativa": "NIPGR-Plants/Oryza_sativa/Osativa_323_v7.0.protein_primaryTranscriptOnly.fa",
    "Piper_auritum": "NIPGR-Plants/Piper_auritum/MUNP-translated-protein.fa",
    "Prunus_persica": "NIPGR-Plants/Prunus_persica/Ppersica_298_v2.1.protein_primaryTranscriptOnly.fa"
}

WORKDIR = "NIPGR_WORK"
HMM_MADS = "PF00319.MADS.hmm"
HMM_KBOX = "PF01486.K_domain.hmm"
AT_DB = "AT_MADS_db"

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)

    for species, fasta in SPECIES_MAP.items():
        print(f"\n--- Processing {species} ---")
        spec_dir = os.path.join(WORKDIR, species)
        if not os.path.exists(spec_dir):
            os.makedirs(spec_dir)

        # 1. HMM Search
        mads_tbl = os.path.join(spec_dir, f"{species}_MADS.domtblout")
        kbox_tbl = os.path.join(spec_dir, f"{species}_Kbox.domtblout")
        
        run_cmd(f"hmmsearch --domtblout {mads_tbl} {HMM_MADS} {fasta} > {spec_dir}/hmm_mads.log")
        run_cmd(f"hmmsearch --domtblout {kbox_tbl} {HMM_KBOX} {fasta} > {spec_dir}/hmm_kbox.log")

        # 2. Filter dual domain
        hits_fa = os.path.join(spec_dir, f"{species}_candidates.fa")
        run_cmd(f"python3 scripts/filter_dual_domains.py {mads_tbl} {kbox_tbl} {fasta} {hits_fa}")

        # 3. BLASTp
        blast_out = os.path.join(spec_dir, f"{species}_vs_AT.blastp.out")
        run_cmd(f"blastp -query {hits_fa} -db {AT_DB} -out {blast_out} -outfmt 6 -evalue 1e-5")

        # 4. Top Hits
        top_hits = os.path.join(spec_dir, f"{species}_TopHits_AT.txt")
        run_cmd(f"python3 scripts/get_top_hits.py {blast_out} {top_hits}")

        # 5. Alignment
        aligned_fa = os.path.join(spec_dir, f"{species}_candidates.aligned.fa")
        if os.path.exists(hits_fa) and os.path.getsize(hits_fa) > 0:
            run_cmd(f"mafft --auto {hits_fa} > {aligned_fa}")
            
            # 6. Domain Extraction
            mads_domains = os.path.join(spec_dir, f"{species}_MADS_domains.fa")
            kbox_domains = os.path.join(spec_dir, f"{species}_Kbox_domains.fa")
            run_cmd(f"python3 scripts/extract_domains_native.py {aligned_fa} {mads_tbl} {mads_domains}")
            run_cmd(f"python3 scripts/extract_domains_native.py {aligned_fa} {kbox_tbl} {kbox_domains}")
        else:
            print(f"No candidates found for {species}")

if __name__ == "__main__":
    main()
