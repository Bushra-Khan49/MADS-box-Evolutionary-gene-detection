# TASK_3 — *Nymphaea colorata* (NCBI RefSeq GCF_003580695.1)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in *Nymphaea colorata*, a representative of the Nymphaeales — one of the three lineages of the ANA grade (basal angiosperms). Together with *Amborella trichopoda*, it provides critical context for understanding the early evolution of floral organ identity genes.

---

## Why *Nymphaea colorata*?

The Nymphaeales represent an independent early-diverging lineage that separated from other angiosperms shortly after the origin of flowering plants. Studying *Nymphaea colorata* allows us to determine whether MADS-box gene duplications and subfunctionalization predated or occurred after the separation of these basal lineages, offering a second evolutionary anchor alongside *Amborella*. The NCBI RefSeq assembly (GCF_003580695.1) is the most complete and current reference available for this species.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading NCBI RefSeq proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates (evalue 1e-5, outfmt 7) |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation using Pfam HMM profiles (PF00319 + PF01486) |
| 4 | [4.MSA_search.md](./4.MSA_search.md) | Multiple Sequence Alignment (CLI + MEGA 12) |
| 5 | [5.Results&Interpretations.md](./5.Results&Interpretations.md) | Final candidate list and clade classification |

---

## Data Source

- **Database**: NCBI RefSeq / UniProt
- **Assembly**: GCF_003580695.1 (v2.0)
- **URL**: [https://www.ncbi.nlm.nih.gov/refseq/](https://www.ncbi.nlm.nih.gov/refseq/)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 52 | 45 |
| HMMER (PF00319 + PF01486) | 48 | 45 |

**Total confirmed MIKCc-type MADS-box genes: 45**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Nymphaea colorata Analysis Complete------</p>
