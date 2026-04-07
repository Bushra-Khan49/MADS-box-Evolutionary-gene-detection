# MADS-box Evolutionary Pipeline: Workflow Step-by-Step

This directory contains the complete species-specific identification and evolutionary analysis pipeline for MADS-box genes across 11 plant lineages.

---

## 📂 Task Index (Phase 1: Identification)

All tasks follow a standardized 5-step analytical protocol: 
1. **Data Collection** | 2. **BLAST Search** | 3. **HMMER Profiling** | 4. **MSA Alignment** | 5. **Results**

- **[Phase 0: Data Preparation](TASK_0)** - Study design, genome sources, and HMM profile collection.
- **[TASK 1: Arabidopsis thaliana](TASK_1)** - Reference model (TAIR10) for ABCDE floral identity.
- **[TASK 2: Amborella trichopoda](TASK_2)** - Basal Angiosperm (Ancestral model).
- **[TASK 3: Nymphaea colorata](TASK_3)** - Basal Angiosperm (Water Lily).
- **[TASK 4: Cinnamomum kanehirae](TASK_4)** - Magnoliid transitional lineage (Stout Camphor).
- **[TASK 5: Oryza sativa](TASK_5)** - Monocot lineage (Rice - high diversity).
- **[TASK 6: Glycine max](TASK_6)** - Legume model (Soybean - massive expansion).
- **[TASK 7: Medicago truncatula](TASK_7)** - Legume model (Barrel Medic).
- **[TASK 8: Prunus persica](TASK_8)** - Rosid lineage (Peach).
- **[TASK 9: Helianthus annuus](TASK_9)** - Asterid lineage (Sunflower).
- **[TASK 10: Nelumbo nucifera](TASK_10)** - Basal eudicot lineage (Sacred Lotus).
- **[TASK 11: Piper auritum](Advanced_Phylogenetic_Pipeline/Uploads/Piper_auritum)** - Magnoliid transitional lineage (Hoja Santa).

---
---

## 📂 Task Index (Phase 2: Phylogenetics & Pattern Analysis)

Following the completion of the Phase 1 identifications, the following systematic phylogenetic investigations are executed to rigorously analyze gene diversification using **IQ-TREE 2** and high-resolution visualization tools.

### 1. Multi-Algorithm Tree Construction & Validation
- **Methodology**: For the master alignment, distinct phylogenetic inference models are computed to cross-validate the evolutionary topology:
  1. **Maximum Likelihood (ML)**: Statistical probability under JTT+G+I models (Completed in Advanced Pipeline).
  2. **Neighbour Joining (NJ)**: Distance-based phylogeny to validate core divergence patterns.
  3. **Bayesian-like Inference**: Using SH-aLRT and aBayes supports to estimate node confidence.

### 2. Species-Specific Phylogenetic Mapping (Ortho-Clade Resolution)
- **Goal**: Generate dual trees per species to resolve orthological relationships against the *Arabidopsis* (AT) reference to map candidates to known ABCDE clades.

### 3. Domain-Level Evolutionary Tracking
- **Goal**: Construct domain-specific trees (MADS vs K-box) to isolate selective pressures acting on functional motifs rather than full-length proteins.

---
<p align="center">Standardized by NIPGR-data Pipeline Automation</p>
