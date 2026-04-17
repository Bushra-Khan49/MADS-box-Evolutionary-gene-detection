# TASK_2 — *Amborella trichopoda* (v1.0)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the basal angiosperm *Amborella trichopoda*. As the sister group to all other flowering plants, *Amborella trichopoda* provides a critical evolutionary outgroup for understanding the ancestral state of floral organ identity genes before the diversification of monocots and eudicots.

---

## Why *Amborella trichopoda*?

*Amborella trichopoda* is the sole surviving species of the most basal angiosperm lineage. Its genome (Phytozome v1.0) is chromosome-level and comprehensively annotated, making it ideal for detecting ancestral MADS-box complements. Including it in this study allows us to determine which floral gene clades were already present at the origin of flowering plants.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading Phytozome v1.0 proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates (evalue 1e-5, outfmt 7) |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation using Pfam HMM profiles (PF00319 + PF01486) |
| 4 | [4.MSA_search.md](./4.MSA_search.md) | Multiple Sequence Alignment (CLI + MEGA 12) |
| 5 | [5.Results&Interpretations.md](./5.Results&Interpretations.md) | Final candidate list and clade classification |

---

## Data Source

- **Database**: Phytozome (DOE JGI)
- **Assembly Version**: v1.0
- **URL**: [https://phytozome-next.jgi.doe.gov](https://phytozome-next.jgi.doe.gov)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 42 | 36 |
| HMMER (PF00319 + PF01486) | 38 | 36 |

**Total confirmed MIKCc-type MADS-box genes: 36**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Amborella trichopoda Analysis Complete------</p>
