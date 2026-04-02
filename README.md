# MADS-box-Evolutionary-gene-detection

> [!NOTE]
> **Advanced 9-Species ML Pipeline:** For our complete computational protocol linking genome-wide identification, Maximum Likelihood orthology mappings, and custom ETE3 high-resolution visualization logic, please see the [Advanced_Phylogenetic_Pipeline](./Advanced_Phylogenetic_Pipeline) directory.


# Genome-wide Identification and Evolutionary Analysis of MADS-box Genes in Land Plants

```bash

MADS-box transcription factors are central regulators of floral organ identity in angiosperms, yet their specialized roles likely evolved from simpler ancestral developmental regulators.
This study investigates how gene duplication, sequence divergence, and domain specialization expanded the MADS-box family to generate the ABCDE floral identity system.
A comparative genome-wide analysis was conducted across representative angiosperm lineages—including basal angiosperms, magnoliids, monocots, and diverse eudicots—with Arabidopsis thaliana serving as a functional reference.
Gene repertoires were examined to identify patterns of conservation, expansion, and clade-specific diversification. Phylogenetic and domain-level comparisons reveal progressive increases in gene number and functional partitioning in more derived lineages.
Together, these findings provide an evolutionary framework linking molecular diversification of MADS-box genes to the emergence and complexity of flowers.

```

## Introduction
MADS-box genes are transcription factors defined by a conserved **MADS domain (~58 aa)** that binds CArG-box DNA motifs.  
The acronym **MADS** comes from:
- **MCM1** (yeast)
- **AGAMOUS (AG)** in *Arabidopsis thaliana*
- **DEFICIENS (DEF)** in *Antirrhinum majus*
- **Serum Response Factor (SRF)** in humans  

These genes are central to **plant development and floral organ identity (ABCDE model)**.

---

## Objectives
- Identify, classify, and trace the **evolutionary history of MADS-box families** (MADS, K-box, AP2) from lower plants to higher plants.  
- Pinpoint **gene duplication and amino acid changes** driving floral organ identity specialization.  
- Understand how **general regulators in lower plants** evolved into **specialized floral organ regulators in angiosperms**.

---

## Biological Background
Although structurally conserved, plant MADS-box genes diversified extensively through duplication and specialization across lineages, leading to distinct functional clades associated with reproductive development. This evolutionary expansion forms the basis for cross-species comparison.

### Classification
MADS-box proteins are grouped by domain architecture and evolutionary origin:

- **Type I (SRF-like)** → simple, fast-evolving, rare and limited roles in plants, common in fungi/animals  
- **Type II (MEF2-like)** → conserved lineage that gave rise to plant MIKC-type genes. Vertebrates (present across eukaryotes)
- **MIKC-type (plant-specific)** → Major regulators of reproductive development, modular TFs  
  - **M**: MADS domain → DNA binding, nuclear localization  
  - **I**: Intervening domain → dimerization specificity  
  - **K**: Keratin-like domain → protein–protein interactions  
  - **C**: Variable C-terminal region → complex/tetramer formation  
(Because interaction domains (K and C) determine complex formation and functional specificity, both full-length and domain-based phylogenies were analyzed in this study.)


### Evolutionary Roles
The function of MADS-box genes progressively specialized across plant evolution:

- **Ferns** → broad developmental roles, no floral orthologues  
- **Gymnosperms** → early BC/D-like system for cone specification  
- **Basal Angiosperms** → expansion, co-option of B genes → petals  
- **Monocots** → lodicule specification, high gene duplication  
- **Eudicots** → conserved ABCDE model, broader roles  

Floral organ identity and the ABCDE regulatory network are features unique to angiosperms, making flowering plants the most appropriate system for comparative analysis of MADS-box gene evolution. Earlier lineages such as ferns and gymnosperms lack true flowers and the complete set of floral MADS-box clades, which limits direct functional comparison. Sampling species across basal angiosperms, magnoliids, monocots, and diverse eudicot groups allows both ancestral and derived gene architectures to be represented while maintaining biological consistency among floral gene families. This evolutionary framework provides the foundation for a systematic genome-wide comparison to investigate gene diversification, duplication, and functional specialization across lineages.

---

## Workflow
- 1. **Data Collection** → Proteome & CDS datasets from Ensembl, Phytozome, NCBI  
- 2. **Reference Genes** → Arabidopsis ABCDE floral identity genes (from TAIR)  
- 3. **Database Building** → Linux-based proteome/CDS database setup  
- 4. **Orthology Inference** → BLASTp + reciprocal BLAST; OrthoFinder/OrthoMCL  
- 5. **HMM Search** → Pfam profiles: MADS (PF00319), K-box (PF01486), AP2 (PF00847)  
- 6. **MSA & Phylogenetics** → MAFFT & clade classification (SQUA, DEF, AG, etc.)  
- 7. **Gene Expression Analysis** → Integration of RNA-seq datasets for MADS/K-box/AP2 genes to study tissue/stage-specific expression and differential expression  
- 8. **Synteny & Collinearity** → Duplication/expansion analysis across species  
- 9. **Functional Divergence** → Neofunctionalization and adaptive changes  
- 10. **Integration & Interpretation** → Linking gene evolution, duplication, and expression to floral development pathways  

---

## Species Studied & Tasks

To investigate the evolutionary diversification of MADS-box genes across flowering plants, we selected species representing major angiosperm lineages. Tasks are organized in evolutionary and analytical sequence from ancestral to derived lineages.

- **TASK_0**: *Arabidopsis thaliana* (Reference Model)
- **TASK_1**: *Oryza sativa* (Rice - Monocot)
- **TASK_2**: *Amborella trichopoda* (Basal Angiosperm)
- **TASK_3**: *Nymphaea colorata* (Water Lily - Early Angiosperm)
- **TASK_4**: *Brassica rapa* (Field Mustard - Eudicot)
- **TASK_5**: *Glycine max* (Soybean - Legume)
- **TASK_6**: *Medicago truncatula* (Barrel Medic - Legume)
- **TASK_7**: *Helianthus annuus* (Sunflower - Asterid)
- **TASK_8**: *Prunus persica* (Peach - Rosid)
- **TASK_9**: *Piper auritum* (Hoja Santa - Magnoliid)
- **TASK_10**: *Cinnamomum kanehirae* (Stout Camphor Tree - Magnoliid)

#### Phylogenetic distribution of angiosperm species selected for comparative analysis.

```bash

Angiosperms (Flowering plants)
│
├── Basal Angiosperms (TASK_2, TASK_3)
│   ├── Amborella trichopoda 
│   └── Nymphaea colorata
│
├── Magnoliids (TASK_9, TASK_10)
│   ├── Piper auritum
│   └── Cinnamomum kanehirae
│
├── Monocots (TASK_1)
│   └── Oryza sativa
│
└── Eudicots (TASK_0, TASK_4, TASK_5, TASK_6, TASK_7, TASK_8)
    ├── Rosids (ATH, GMAX, MTRUN, PPERS)
    └── Asterids (HANNU)
```

---
## Expected Outcomes
- A **catalog of MADS-box genes** across all selected angiosperm genomes. 
- **Phylogenetic insights and clade classification** revealing gene duplication, expansion, and lineage-specific diversification.
- Comparative insights into the evolution of **floral organ identity networks and genes** across major plant lineages.
- Detection of **conserved and novel domain architectures** associated with functional specialization.

---

## References

### Foundational MADS-box Research
- **Becker, A., & Theissen, G. (2003).** The modular evolution of MADS-box genes. *Molecular Phylogenetics and Evolution*, 29(3), 483-502.
- **Parenicová, L., et al. (2003).** Genome-wide analysis of Arabidopsis MADS-box gene family. *Plant Physiology*, 132(3), 1387-1397.
- **Gramzow, L., & Theissen, G. (2010).** A comprehensive analysis of MADS-box genes in monocots. *Gene*, 461(1-2), 28-40.
- **Smaczniak, C., et al. (2012).** MADS-box transcription factor complexes. *Current Opinion in Plant Biology*, 15(5), 620-631.
- **Theissen, G., et al. (2016).** MADS-box genes and the evolution of flowers. *Journal of Experimental Botany*, 67(1), 35-49.
- **Rodríguez-Pelayo et al. (2022).** Genomic insights into MADS-box gene evolution.
- **Thangavel & Nayar (2018).** Computational identification of plant transcription factors.

### NIPGR Laboratory Contributions (Prabhakaran Lab)
- **Soundararajan, P., et al. (2018).** Anti-carcinogenic glucosinolates in cruciferous vegetables and their antagonistic effects on prevention of cancers. *Molecules*, 23(11), 2983. (Top-cited lab research).
- **Soundararajan, P., et al. (2015).** Blue LED light enhances growth, phytochemical contents, and antioxidant enzyme activities of Rehmannia glutinosa cultured in vitro. *HEB*, 56, 105-113.
- **Soundararajan, P., et al. (2019).** Mechanisms of silicon-mediated amelioration of salt stress in plants. *Plants*, 8(9), 307.
- **Soundararajan, P., et al. (2016).** Silicon Mitigates Salinity Stress by Regulating the Physiology, Antioxidant Enzyme Activities, and Protein Expression in Capsicum annuum 'Bugwang'. *BMRI*, 2016.
- **Soundararajan, P., et al. (2014).** Influence of silicon supplementation on the growth and tolerance to high temperature in Salvia splendens. *HEB*, 55, 271-279.
- **Soundararajan, P., et al. (2014).** Physiological and Proteomic Analysis in Chloroplasts of Solanum lycopersicum L. under Silicon Efficiency and Salinity Stress. *IJMS*, 15(12), 21820-21842.
- **Soundararajan, P., et al. (2025).** Pangenome-wide identification and characterization of WOX gene family among *Brassica Triangle of U's* genomes. *Plant Gene*, 42, 100497.
- **Soundararajan, P., et al. (2025).** Transcriptome-wide identification and expression analysis of expansin genes in *Adhatoda vasica*. *Plant Physiology Reports*.
- **Agarwal, Y., et al. (2022).** Paradigm and Framework of WUS-CLV Feedback Loop in Stem Cell Niche for SAM Maintenance and Cell Identity Transition. *Agronomy*, 12(12), 3132.
