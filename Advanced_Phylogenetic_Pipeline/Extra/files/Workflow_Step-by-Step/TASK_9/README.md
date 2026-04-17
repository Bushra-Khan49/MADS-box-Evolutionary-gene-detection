# TASK_9 — *Helianthus annuus* (Phytozome v1.2)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the model Asteraceae species *Helianthus annuus* (Sunflower). As a representative of the most diverse eudicot family, it provides critical insights into the evolution of complex inflorescence structures.

---

## Why *Helianthus annuus*?

*Helianthus annuus* (Sunflower) is the primary model for the Asteraceae (Compositae) family. Its large and complex genome (Phytozome v1.2) has been shaped by multiple rounds of whole-genome duplication, contributing to the development of the pseudanthium (flower head). Studying the MADS-box gene family in this species allows us to analyze how these regulators have evolved to control the differentiation of specialized floret types (ray and disc) and the overall architecture of the Asteraceae inflorescence.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading Phytozome v1.2 proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates (evalue 1e-5, outfmt 7) |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation using Pfam HMM profiles (PF00319 + PF01486) |
| 4 | [4.MSA_search.md](./4.MSA_search.md) | Multiple Sequence Alignment (CLI + MEGA 12) |
| 5 | [5.Results&Interpretations.md](./5.Results&Interpretations.md) | Final candidate list and clade classification |

---

## Data Source

- **Database**: Phytozome (DOE JGI)
- **Assembly Version**: v1.2 (Hannuus_v1.0)
- **URL**: [https://phytozome-next.jgi.doe.gov](https://phytozome-next.jgi.doe.gov)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 142 | 128 |
| HMMER (PF00319 + PF01486) | 134 | 128 |

**Total confirmed MIKCc-type MADS-box genes: 128**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Helianthus annuus Analysis Complete------</p>
