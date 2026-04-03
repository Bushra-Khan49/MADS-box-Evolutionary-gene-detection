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

Following the completion of the Step 4 Multiple Sequence Alignments (MSA), the following phylogenetic investigations will be executed to rigorously analyze gene diversification.

### 1. Robust MSA Protocols & Comparative Alignment
- **Why & How**: To ensure alignment robustness and eliminate potential algorithm-specific biases in gap placement, we integrate **MUSCLE** and **Clustal Omega** alongside **MAFFT**. This multi-tool approach validates that the resulting residue correspondences are consistent across different mathematical scoring models before tree construction begins.

### 2. Multi-Algorithm Tree Construction & Validation
- **Why & How**: For every alignment, three distinct phylogenetic inference models are computed to cross-validate the evolutionary topology:
  1. **Maximum Likelihood (ML)**: To identify the most statistically probable tree under chosen substitution models (e.g., JTT+G+I).
  2. **Neighbour Joining (NJ)**: To provide a distance-based perspective on sequence divergence.
  3. **Bayesian Inference (Bayes)**: To estimate posterior probabilities of clades, offering a robust confidence measure for deeper nodes.

### 3. Species-Specific Phylogenetic Mapping (Ortho-Clade Resolution)
- **Why & How**: Using **ML + MAFFT**, we generate dual trees per species to resolve orthological relationships:
  - **Tree A (Internal Structure)**: Target Proteome + Target K-box candidates to evaluate domestic duplication patterns.
  - **Tree B (Comparative Reference)**: Target Proteome + Target K-box + *Arabidopsis* (AT) reference to map candidates to known ABCDE clades.

### 4. Domain-Level Evolutionary Tracking & Selection Analysis
- **Why & How**: Domain-specific trees are constructed to isolate selective pressures acting on functional motifs rather than full-length proteins. This allows us to determine if the **MADS domain** (DNA binding) or the **K-box domain** (protein interaction) is the primary driver of sequence divergence in specific lineages.

### 5. Clade Specialization & Divergence Checks
- **Why & How**: We perform a final inspection for specific clades exhibiting the **"one separate and rest together"** pattern. This topological signature is a key indicator of potential lineage-specific neofunctionalization or ancestral divergence, where one orthologue has significantly diverged from the conserved cluster.

---
<p align="center">Standardized by NIPGR-data Pipeline Automation</p>
