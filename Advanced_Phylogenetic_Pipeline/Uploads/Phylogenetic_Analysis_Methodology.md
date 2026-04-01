# MADS-Box Evolutionary Gene Detection & Phylogenetic Reconstruction

MADS-box transcription factors are the master molecular regulators of floral organ identity in angiosperms, guiding complex developmental events such as the ABCDE model. While broadly conserved, their specialized roles evolved dynamically from simpler ancestral structures. This project investigates how gene duplication, sequence divergence, and lineage-specific expansions shaped the MIKCc-type MADS-box family across a massive evolutionary timescale.

By leveraging *Arabidopsis thaliana* as a verified functional anchor, this comparative genome-wide pipeline computationally maps unidentified genes from 9 distinct species into established biological subclades.

---

## 🎯 Objectives
* **Genome-Wide Identification:** Extract and validate true MIKCc-type MADS-box genes from noisy, raw proteomes across 9 major plant lineages.
* **Evolutionary Tracking (Orthology):** Perform high-throughput homology mappings to trace uncharacterized species sequences back to standard *Arabidopsis* counterparts.
* **Phylogenetic Reconstruction:** Compute complex Maximum Likelihood (ML) trees from co-aligned multi-species data to observe genetic divergence and duplication events.
* **Predictive Visualization:** Dynamically annotate and color-code unstudied genes into functional clades (e.g., AP1/FUL, SEPALLATA) via 4K circular phylogenies, establishing a predictive roadmap for crop engineering.

---

## 🧬 Biological Background
Although structurally conserved, plant MADS-box genes diversified extensively through duplication and specialization across lineages, leading to distinct functional clades associated with reproductive development. 

### Classification Hierarchy
MADS-box proteins are primarily grouped by their domain architecture:
* **Type I (SRF-like):** Simple, fast-evolving, with rare or limited roles in plants; highly common in fungi/animals.
* **Type II (MEF2-like):** The deeply conserved lineage that gave rise to plant MIKC-type genes. Found across all eukaryotes.
* **MIKC-type (Plant-Specific):** The modular transcription factors serving as the primary regulators of plant reproductive development.

### The Modular MIKC Structure
* **M (MADS domain):** Highly conserved; facilitates DNA binding (at CArG boxes) and nuclear localization.
* **I (Intervening domain):** Controls dimerization specificity.
* **K (Keratin-like domain):** Critical for mediating required protein–protein interactions.
* **C (C-terminal region):** Highly variable; responsible for higher-order tetramer complex formation and activation.

*(Because the interaction domains (K and C) determine complex formation and functional specificity, preserving them via strict Multiple Sequence Alignments (MSA) was paramount to this study's accuracy).*

---

## 🌿 Species Studied
To investigate this diversification, we analyzed species covering the major transitionary lineages of flowering plant evolution:

```text
Angiosperms (Flowering plants)
 ├── Basal Angiosperms
 │   ├── Amborella trichopoda         (Ancestral MADS-box architecture)
 │   └── Nymphaea colorata            (Early aquatic conservation vs adaptation)
 ├── Magnoliids
 │   └── Cinnamomum kanehirae         (Transitional bridge lineage)
 ├── Monocots
 │   └── Oryza sativa                 (Independent floral evolution / lodicules)
 └── Eudicots
     ├── Rosids
     │   ├── Glycine max [Soybean]    (Model legume; massive gene expansion)
     │   ├── Medicago truncatula      (Comparative orthology model)
     │   └── Prunus persica [Peach]   (Woody perennial genome contrast)
     └── Asterids
         └── Helianthus annuus        (Distant dicot lineage; avoids rosid bias)
```

*(Plus **Nelumbo nucifera** as an additional basal eudicot outgroup).*

---

## 🔬 Comprehensive Methodology Pipeline

### 1. Data Collection & HMM Profiling
* **Database Acquisition:** Raw proteomes for the nine species were downloaded from major genomic repositories.
* **HMMER Execution:** We utilized a Hidden Markov Model approach (`hmmbuild` / `hmmsearch`) to isolate high-confidence sequences mathematically.
* **Target Profiling:** Scans were queried strictly against the established SRF-TF MADS-box Pfam profile (PF00319), retaining only hits that passed strict E-value thresholds.

### 2. Structural Domain Validation
* **Type Refinement:** To separate the critical MIKCc-types from simpler Type I genes, all sequences underwent a secondary InterProScan verification.
* **Domain Confirmation:** Only sequences mathematically proven to possess both the identifying 'MADS' domain (PF00319) and the structurally defining 'K-box' domain (PF01486) were retained in the finalized dataset.

### 3. Orthology Inference via Local BLAST
* **Reference Construction:** A localized FASTA database holding the ~107 known MIKCc proteins of *Arabidopsis thaliana* was explicitly constructed as an evolutionary anchor.
* **Global Querying:** A local `BLASTp` query was executed, scoring every validated species sequence against the *Arabidopsis* references. 
* **Top-Hit Extraction:** Highest bit-score and lowest E-value mappings were successfully extracted to seal an initial computational homolog for every target gene.

### 4. Co-Aligned Multiple Sequence Alignment (MSA)
* **Sequence Concatenation:** For each species, uncharacterized target genes were concatenated directly alongside the entire *Arabidopsis* reference database. 
* **Algorithmic Alignment:** High-accuracy MSAs were computed using **MAFFT/MUSCLE** algorithms. 
* **Domain Parameterization:** Alignments were heavily parameterized to perfectly snap the conserved M- and K- domains together, while increasing gap-penalties to precisely accommodate the hypervariable I and C regions.

### 5. Maximum Likelihood Systematics
* **Model Optimization:** The amino acid substitution models (e.g., JTT, WAG) were rigorously tested and computationally optimized for the datasets.
* **Phylogenetic Calculation:** Maximum Likelihood (ML) phylogenetic trees were calculated natively using IQ-TREE / MEGA engines.
* **Branch Validation:** 500 independent bootstrap replicates were executed on every tree to guarantee statistical sequence/branch confidence.
* **Dynamical Plotting:** These algorithms completely bypassed simple BLAST homology by plotting true genetic distances, naturally forcing unknown species genes to branch precisely around the known *Arabidopsis* anchors.

### 6. Automated Subclade Annotation
* **Dictionary Bridge:** A custom Python architecture computationally parsed the previous BLAST matrices against a hardcoded, literature-derived functional dictionary.
* **Explicit Assignment:** This step algorithmically assigned a standardized functional clade (e.g. 'AP3/PI', 'FLC/MAF') to 100% of the species' target genes.
* **TSV Export:** A comprehensive, fully-mapped annotation TSV database was outputted for direct use by downstream visualization scripts.

### 7. High-Resolution Circular Visualization
The raw Python `ETE3` library ingested the generated Newick (`.nwk`) distance matrices:
* **Topology:** Kept unbent in true-phylogenetic "circular mode", perfectly preserving actual distance spacing calculations.
* **Layout:** Terminal labels were pushed to a flawlessly aligned outer ring, mechanically tethered by dashed guiding lines.
* **Dynamic Coloring:** Species labels pulled 100% opacity hex colors mapped directly from the Subclade TSV Database.
* **Reference Fading:** To keep visual priority exclusively on the target species, *Arabidopsis* anchor genes were algorithmically rendered in a 65% faded pastel tint. Unmapped Arabidopsis genes utilized an ML-style nearest-neighbor algorithm to organically inherit colors from their closest mapped sister-branch.
* **Post-Processing:** Trees were exported at massive 4000x4000 300-DPI resolution, while Pillow (`PIL.ImageDraw`) mathematically overlaid a pristine, boxed Subclade Legend onto the topography.

---

## 📊 Results & The Bigger Picture

### Observations
The entire pipeline executed as intended, generating ten distinctly monophyletic 4K phylogenetic trees (including an overarching 600-gene Master Tree). Major functional biological clades (e.g., the B-class AP3/PI genes dictating petal/stamen identity) clustered together immaculately across all distinct species—proving that the parameterized MSA and ML algorithms successfully bridged massive evolutionary gaps. 

### Evolutionary Interpretations
The mapped distributions clearly highlight stark evolutionary events. The basal lineage *Amborella trichopoda* possesses a streamlined, ancient minimal regulatory network (~32 genes). In contrast, recent whole-genome duplications in eudicots like *Glycine max* triggered immense expansion (~174 genes), driving high functional redundancy and diverse potential for neofunctionalization.

### The Bigger Picture
By computationally backtracking the lineage of every uncharacterized MADS-box gene directly to an *Arabidopsis* anchor, this project establishes a predictive genomic roadmap. It removes the guesswork from non-model plant biology. We can now confidently hypothesize the physiological purpose of unstudied genes in economically critical crops based entirely on their modeled evolutionary proximity to known developmental regulators, vastly accelerating targeted agricultural engineering and breeding.
