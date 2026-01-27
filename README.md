# MADS-box-Evolutionary-gene-detection

# Genome-wide Identification and Evolutionary Analysis of MADS-box Genes in Land Plants

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
### Classification
- **Type I (SRF-like)** → rare in plants, common in fungi/animals  
- **Type II (MEF2-like)** → vertebrates  
- **MIKC-type (plant-specific)** → Major focus, modular TFs  
  - **M**: MADS domain → DNA binding, nuclear localization  
  - **I**: Intervening domain → dimerization specificity  
  - **K**: Keratin-like domain → protein–protein interactions  
  - **C**: Variable C-terminal region → complex/tetramer formation  

### Evolutionary Roles
- **Ferns** → broad developmental roles, no floral orthologues  
- **Gymnosperms** → early BC/D-like system for cone specification  
- **Basal Angiosperms** → expansion, co-option of B genes → petals  
- **Monocots** → lodicule specification, high gene duplication  
- **Eudicots** → conserved ABCDE model, broader roles  

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

## Species Studied

(To investigate the evolutionary diversification of MADS-box genes across flowering plants, we selected species representing major angiosperm lineages. Amborella trichopoda and Nymphaea colorata represent basal angiosperms, providing insight into ancestral gene architectures. Cinnamomum kanehirae (magnoliid) bridges early and derived angiosperms, while Oryza sativa represents monocots. Multiple eudicot species spanning rosids (Glycine max, Medicago truncatula, Prunus persica) and asterids (Helianthus annuus) were included to capture lineage-specific duplication, divergence, and functional specialization. Arabidopsis thaliana was used as a reference model for gene annotation and clade classification.)

- *Medicago truncatula*  
- *Glycine max*  
- *Helianthus annuus*  
- *Nelumbo nucifera*  
- *Magnolia grandiflora*  
- *Piper auritum*  
- *Cinnamomum kanehirae*  
- *Amborella trichopoda*  
- *Nymphaea colorata*  

### Phylogenetic distribution of angiosperm species selected for comparative analysis of MADS-box genes. Species were chosen to represent key evolutionary transitions from basal angiosperms to derived eudicots ###

Angiosperms (Flowering plants)
│
├── Basal Angiosperms
│   ├── Amborella trichopoda
│   │   └─ Represents ancestral angiosperm MADS-box architecture
│   │
│   └── Nymphaea colorata
│       └─ Early aquatic angiosperm; tests conservation vs adaptation
│
├── Magnoliids
│   └── Cinnamomum kanehirae
│       └─ Transitional lineage between basal angiosperms and eudicots
│
├── Monocots
│   └── Oryza sativa
│       └─ Independent flower evolution; tests lineage-specific divergence
│
└── Eudicots
    ├── Rosids
    │   ├── Glycine max
    │   │   └─ Legume model; gene family expansion & duplication
    │   │
    │   ├── Medicago truncatula
    │   │   └─ Model legume; comparative orthology
    │   │
    │   └── Prunus persica
    │       └─ Woody perennial; structural genome contrast
    │
    └── Asterids
        └── Helianthus annuus
            └─ Distant dicot lineage; avoids rosid-only bias

          
---

## Expected Outcomes
- A **catalog of MADS-box genes** across nine plant species  
- **Phylogenetic insights** into duplication and diversification events  
- Contribution to understanding the **evolution of floral organ identity genes**  

---

## References
- Rodríguez-Pelayo et al., 2022  
- Thangavel & Nayar, 2018  
- Theissen et al. (Review on MADS-box genes)  
