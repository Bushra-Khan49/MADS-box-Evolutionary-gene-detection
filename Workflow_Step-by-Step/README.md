# MADS-box Evolutionary Pipeline: Workflow Step-by-Step

This directory contains the complete species-specific identification and evolutionary analysis pipeline for MADS-box genes across 11 plant lineages.

---

## 📂 Task Index (Phase 1: Identification)

All tasks follow a standardized 5-step analytical protocol: 
1. **Data Collection** | 2. **BLAST Search** | 3. **HMMER Profiling** | 4. **MSA Alignment** | 5. **Results**

- **[TASK 0: Arabidopsis thaliana](TASK_0)** - Reference model for MADS-box identity (ABCDE).
- **[TASK 1: Oryza sativa](TASK_1)** - Monocot lineage (Rice).
- **[TASK 2: Amborella trichopoda](TASK_2)** - Basal Angiosperm (Ancestral model).
- **[TASK 3: Nymphaea colorata](TASK_3)** - Basal Angiosperm (Water Lily).
- **[TASK 4: Brassica rapa](TASK_4)** - Eudicot (Field Mustard).
- **[TASK 5: Glycine max](TASK_5)** - Legume model (Soybean - massive expansion).
- **[TASK 6: Medicago truncatula](TASK_6)** - Legume model (Barrel Medic).
- **[TASK 7: Helianthus annuus](TASK_7)** - Asterid lineage (Sunflower).
- **[TASK 8: Prunus persica](TASK_8)** - Rosid lineage (Peach).
- **[TASK 9: Piper auritum](TASK_9)** - Magnoliid transitional lineage (Hoja Santa).
- **[TASK 10: Cinnamomum kanehirae](TASK_10)** - Magnoliid transitional lineage (Stout Camphor).

---
---

##  📂 Task Index (Phase 2: Phylogenetics & Pattern Analysis)

Following the completion of the Step 4 Multiple Sequence Alignments (MSA), the following phylogenetic investigations will be executed:

### 1. Comparative MSA Protocols
- Integration of **MUSCLE** and **Clustal Omega** algorithms alongside **MAFFT** to ensure alignment robustness.

### 2. Multi-Algorithm Tree Construction
For every alignment, three distinct phylogenetic inference models will be computed:
1. **Maximum Likelihood (ML)**
2. **Neighbour Joining (NJ)**
3. **Bayesian Inference (Bayes)**

### 3. Species-Specific Phylogenetic Mapping
Using **ML + MAFFT**, we will generate two trees per species:
- **Tree A**: Target Proteome + Target K-box.
- **Tree B**: Target Proteome + Target K-box + *Arabidopsis* (AT) reference.

### 4. Domain-Level Evolutionary Tracking
Domain-specific trees will be constructed to isolate selective pressures on functional motifs:
- **MADS Domain Tree**: Target Genome (GOI) + *Arabidopsis* (AT).
- **K-box Domain Tree**: Target Genome (GOI) + *Arabidopsis* (AT).

### 5. Clade Specialization Check
- Identification of specific clades exhibiting the **"one separate and rest together"** pattern, indicating potential lineage-specific neofunctionalization or ancestral divergence.

---
<p align="center">Standardized by NIPGR-data Pipeline Automation</p>
