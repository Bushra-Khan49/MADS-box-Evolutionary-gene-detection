# TASK_5 — *Oryza sativa* (IRGSP-1.0 / v7.0)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the model monocot *Oryza sativa* (Rice). As the most significant cereal crop and the primary monocot model, it is crucial for comparing the evolutionary history of floral architecture between monocots and eudicots.

---

## Why *Oryza sativa*?

*Oryza sativa* (Phytozome v7.0) is the cornerstone of monocot comparative genomics. Its MADS-box gene family has undergone significant diversification, contributing to unique cereal-specific floral traits. By including rice in this study, we can observe the divergence in clade expansions (e.g., in the *AGL17* and *SEP* groups) that occurred after the monocot-eudicot split approximately 140–150 million years ago.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading Phytozome v7.0 proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates (evalue 1e-5, outfmt 7) |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation using Pfam HMM profiles (PF00319 + PF01486) |
| 4 | [4.MSA_search.md](./4.MSA_search.md) | Multiple Sequence Alignment (CLI + MEGA 12) |
| 5 | [5.Results&Interpretations.md](./5.Results&Interpretations.md) | Final candidate list and clade classification |

---

## Data Source

- **Database**: Phytozome (DOE JGI) / JGI Data Portal
- **Assembly Version**: v7.0 (IRGSP-1.0)
- **URL**: [https://phytozome-next.jgi.doe.gov](https://phytozome-next.jgi.doe.gov)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 86 | 75 |
| HMMER (PF00319 + PF01486) | 79 | 75 |

**Total confirmed MIKCc-type MADS-box genes: 75**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Oryza sativa Analysis Complete------</p>
