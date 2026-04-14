# TASK_1 — *Arabidopsis thaliana* (TAIR10)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the model angiosperm *Arabidopsis thaliana*. As the best-annotated flowering plant genome, *Arabidopsis thaliana* (TAIR10) serves as the reference framework for classifying MADS-box clades and identifying orthologous genes across all other species in this study.

---

## Why *Arabidopsis thaliana*?

*Arabidopsis thaliana* has experimentally validated ABCDE model genes (AP1, AP3, PI, AG, SEP) with well-characterized expression patterns and protein functions. TAIR10 is the most stable and extensively curated version of this genome, making it the standard coordinate system for comparative genomics in flowering plants.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading TAIR10 proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation & Intersection for Anchor Set |
| 4 | [4.Results_Interpretations.md](./4.Results_Interpretations.md) | Final candidate list (45 MIKCc genes) |
| 5 | [5.Evolutionary_Conclusion.md](./5.Evolutionary_Conclusion.md) | Conclusion on the Arabidopsis Anchor Set |

---

## Data Source

- **Database**: TAIR (The Arabidopsis Information Resource)
- **Assembly Version**: TAIR10
- **URL**: [https://www.arabidopsis.org](https://www.arabidopsis.org)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 79 | 45 |
| HMMER (PF00319 + PF01486) | 79 | 45 |

**Total confirmed MIKCc-type MADS-box genes: 45**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Arabidopsis thaliana Analysis Complete------</p>
