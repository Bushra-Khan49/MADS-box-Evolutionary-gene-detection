# TASK_8 — *Prunus persica* (Phytozome v2.1)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the model Rosaceae species *Prunus persica* (Peach). As a high-quality diploid reference, it provides a crucial comparative framework for understanding the evolution of floral and fruit traits in the Rosales.

---

## Why *Prunus persica*?

*Prunus persica* is the cornerstone of Rosaceae comparative genomics. Its relatively small diploid genome (Phytozome v2.1) is well-annotated and stable, having avoided recent whole-genome polyploidization events seen in other family members. This makes it a perfect model for identifying the core set of MADS-box genes responsible for floral organ identity and fruit development in the Rosales. By including it in this study, we can track the evolutionary conservation and divergence of these regulators across the eudicots.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading Phytozome v2.1 proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates (evalue 1e-5, outfmt 7) |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation using Pfam HMM profiles (PF00319 + PF01486) |
| 4 | [4.MSA_search.md](./4.MSA_search.md) | Multiple Sequence Alignment (CLI + MEGA 12) |
| 5 | [5.Results&Interpretations.md](./5.Results&Interpretations.md) | Final candidate list and clade classification |

---

## Data Source

- **Database**: Phytozome (DOE JGI)
- **Assembly Version**: v2.1 (Ppersica_298)
- **URL**: [https://phytozome-next.jgi.doe.gov](https://phytozome-next.jgi.doe.gov)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 76 | 68 |
| HMMER (PF00319 + PF01486) | 71 | 68 |

**Total confirmed MIKCc-type MADS-box genes: 68**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Prunus persica Analysis Complete------</p>
