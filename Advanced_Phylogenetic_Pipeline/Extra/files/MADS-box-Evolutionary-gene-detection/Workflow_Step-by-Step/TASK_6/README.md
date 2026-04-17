# TASK_6 — *Glycine max* (Phytozome v2.1)

## Overview

This task covers the genome-wide identification of MIKCc-type MADS-box genes in the paleopolyploid legume *Glycine max* (Soybean). Soybean's complex history of whole-genome duplications makes it a crucial target for understanding gene family expansion and redundancy in the Fabaceae.

---

## Why *Glycine max*?

*Glycine max* (Soybean) is a key legume crop with a genome that has undergone two rounds of whole-genome duplication (WGD) approximately 59 and 13 million years ago. This polyploid nature has led to a significant expansion of the MADS-box gene family. By studying *G. max* (Phytozome v2.1), we can analyze how multiple copies of floral organ identity genes contribute to the characteristic development of the papilionaceous flower and its evolutionary success.

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
- **Assembly Version**: v2.1 (Gmax_275)
- **URL**: [https://phytozome-next.jgi.doe.gov](https://phytozome-next.jgi.doe.gov)

---

## Final Results Summary

| Method | Initial Hits | Validated |
|--------|-------------|-----------|
| BLASTP (1e-5) | 254 | 228 |
| HMMER (PF00319 + PF01486) | 236 | 228 |

**Total confirmed MIKCc-type MADS-box genes: 228**

---

## Raw Data

All raw outputs (BLAST results, HMMER tables, FASTA files) are stored in the [`uploads/`](./uploads/) folder.

<p align="center">------Glycine max Analysis Complete------</p>
