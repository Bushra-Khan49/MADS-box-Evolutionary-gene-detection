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
