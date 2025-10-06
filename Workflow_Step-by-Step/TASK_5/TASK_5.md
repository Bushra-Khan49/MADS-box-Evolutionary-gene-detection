# Reciprocal Best Hits (RBH) Workflow for MADS-box Orthologs in Prunus persica

This repository documents a bioinformatics workflow to identify putative orthologs of Arabidopsis thaliana (A. thaliana) MADS-box transcription factor proteins in Prunus persica (peach) using the Reciprocal Best Hits (RBH) approach with BLAST. The workflow uses forward and reverse BLAST searches to ensure reciprocity, filtering for high-confidence orthologs.

The original workflow was executed in a terminal session on macOS (using Conda environment `(base)`). It processes protein sequences from A. thaliana MADS-box genes against the Prunus persica v2.1 proteome.

## Workflow Overview
1. **Build BLAST database** from Prunus persica proteins.
2. **Forward BLAST**: Search A. thaliana MADS-box proteins against Prunus DB.
3. **Process hits**: Remove duplicates, extract pairs, and unique subjects.
4. **Extract and label sequences**: Pull Prunus hit sequences and label with A. thaliana IDs.
5. **Reverse BLAST**: Search labeled hits back against Prunus DB.
6. **Select best hits**: Identify reciprocal best hits (RBH) based on e-value and bitscore.
7. **Final extraction and labeling**: Generate labeled FASTA for orthologs.

**Key Results**:
- Initial forward BLAST: ~293k hits (after dedup).
- Unique subjects: 1,258 Prunus proteins.
- Reverse BLAST: 3,360 hits across 74 unique queries.
- Final RBH: 74 ortholog pairs.

This workflow assumes the working directory contains the input files (see below).

## Prerequisites
- **Tools**:
  - BLAST+ (e.g., `makeblastdb`, `blastp`): Install via [NCBI BLAST](https://blast.ncbi.nlm.nih.gov/doc/blast-help/).
  - `seqtk`: For FASTA subsetting ([GitHub](https://github.com/lh3/seqtk)).
  - Standard Unix tools: `awk`, `cut`, `sort`, `uniq`, `wc`, `head`.
- **Environment**: Tested in Conda `(base)` on macOS.
- **Input Files** (place in working directory):
  - `AT_ALL_MADSbox_PROTEINseq.fa`: A. thaliana MADS-box protein FASTA (39,647 bytes).
  - `Ppersica_298_v2.1.protein.fa`: Prunus persica v2.1 proteome FASTA (37,319,736 bytes).
  - (Optional) HMM files: `PF00319.MADS.hmm`, `PF01486.K_domain.hmm` (not used in this workflow).

**Working Directory**: `/Users/bushrakhan/Desktop/NIPGR-data/TASK_5/3` (adjust as needed).

