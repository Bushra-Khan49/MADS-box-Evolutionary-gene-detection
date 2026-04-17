# TASK_10 — *Nelumbo nucifera* (NCBI RefSeq GCF_000365185.1)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the basal eudicot *Nelumbo nucifera* (Sacred Lotus). As a representative of the early-diverging eudicots, it provides a critical evolutionary anchor for understanding the origin and diversification of floral organ identity genes before the expansion of core eudicots.

---

## Why *Nelumbo nucifera*?

*Nelumbo nucifera* is a unique aquatic eudicot that belongs to the Proteales, one of the most basal lineages of eudicots. Its genome (NCBI RefSeq GCF_000365185.1) is relatively small and stable, offering a high-quality reference for comparative genomics. Studying the MADS-box gene family in this species allows us to resolve the ancestral states of eudicot-specific clades and identify the genetic shifts that occurred during the early radiation of the eudicot lineage.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading NCBI RefSeq v1.0 proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates (evalue 1e-5, outfmt 7) |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation using Pfam HMM profiles (PF00319 + PF01486) |
| 4 | [4.MSA_search.md](./4.MSA_search.md) | Multiple Sequence Alignment (CLI + MEGA 12) |
| 5 | [5.Results&Interpretations.md](./5.Results&Interpretations.md) | Final candidate list and clade classification |

---

## Data Source

- **Database**: NCBI RefSeq / UniProt
- **Assembly Version**: v1.0 (NN_v1.0)
- **URL**: [https://www.ncbi.nlm.nih.gov/refseq/](https://www.ncbi.nlm.nih.gov/refseq/)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 52 | 48 |
| HMMER (PF00319 + PF01486) | 50 | 48 |

**Total confirmed MIKCc-type MADS-box genes: 48**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Nelumbo nucifera Analysis Complete------</p>
