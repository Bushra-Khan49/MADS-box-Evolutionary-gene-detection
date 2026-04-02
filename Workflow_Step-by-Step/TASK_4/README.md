# TASK_4 — *Cinnamomum kanehirae* (Phytozome v3)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the Magnoliid *Cinnamomum kanehirae* (Taiwan incense cedar). Magnoliids occupy a critical phylogenetic position between the basal angiosperms (*Amborella*, *Nymphaea*) and the core angiosperm lineages (monocots and eudicots), making them essential for tracking the early expansion of MADS-box gene families.

---

## Why *Cinnamomum kanehirae*?

The Magnoliids represent one of the three major angiosperm lineages alongside monocots and eudicots. *Cinnamomum kanehirae* (Phytozome v3) provides a high-quality chromosome-level reference for the Laureales order within the Magnoliids. Studying gene family size and clade composition in this species helps establish which MIKCc duplications and subfunctionalization events occurred before or after the monocot-eudicot split.

---

## Workflow Files

| Step | File | Description |
|------|------|-------------|
| 1 | [1.Data_Collection.md](./1.Data_Collection.md) | Downloading Phytozome v3 proteome, genome, and annotations |
| 2 | [2.Blast_workflow.md](./2.Blast_workflow.md) | BLASTP search for MADS-box candidates (evalue 1e-5, outfmt 7) |
| 3 | [3.HMMER_search.md](./3.HMMER_search.md) | Domain validation using Pfam HMM profiles (PF00319 + PF01486) |
| 4 | [4.MSA_search.md](./4.MSA_search.md) | Multiple Sequence Alignment (CLI + MEGA 12) |
| 5 | [5.Results&Interpretations.md](./5.Results&Interpretations.md) | Final candidate list and clade classification |

---

## Data Source

- **Database**: Phytozome (DOE JGI)
- **Assembly Version**: v3
- **URL**: [https://phytozome-next.jgi.doe.gov](https://phytozome-next.jgi.doe.gov)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 58 | 50 |
| HMMER (PF00319 + PF01486) | 53 | 50 |

**Total confirmed MIKCc-type MADS-box genes: 50**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Cinnamomum kanehirae Analysis Complete------</p>
