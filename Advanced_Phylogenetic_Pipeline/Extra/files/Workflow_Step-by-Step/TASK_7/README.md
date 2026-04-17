# TASK_7 — *Medicago truncatula* (Phytozome v4)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the model legume *Medicago truncatula* (Barrel Medic). As a high-quality diploid reference, it provides a crucial comparative framework for understanding MADS-box gene evolution in the legumes.

---

## Why *Medicago truncatula*?

*Medicago truncatula* is the premier model species for genomic studies in temperate legumes. Unlike its polyploid relative, soybean, *M. truncatula* (Phytozome v4) has a relatively small and stable genome, making it ideal for identifying the core set of MADS-box genes essential for legume floral development and symbiosis. Including it in this study allows for a direct comparison of gene family expansion patterns within the Fabaceae.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading Phytozome v4 proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates (evalue 1e-5, outfmt 7) |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation using Pfam HMM profiles (PF00319 + PF01486) |
| 4 | [4.MSA_search.md](./4.MSA_search.md) | Multiple Sequence Alignment (CLI + MEGA 12) |
| 5 | [5.Results&Interpretations.md](./5.Results&Interpretations.md) | Final candidate list and clade classification |

---

## Data Source

- **Database**: Phytozome (DOE JGI)
- **Assembly Version**: v4 (Mtruncatula_198)
- **URL**: [https://phytozome-next.jgi.doe.gov](https://phytozome-next.jgi.doe.gov)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 84 | 72 |
| HMMER (PF00319 + PF01486) | 76 | 72 |

**Total confirmed MIKCc-type MADS-box genes: 72**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Medicago truncatula Analysis Complete------</p>
