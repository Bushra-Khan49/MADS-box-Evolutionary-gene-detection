# Phase 0: Workflow Audit & Reconciliation Log

## 📝 Background
During the transition to Phase 2 (Systematic Phylogenetics), a numbering mismatch was identified between the directory structure and the historical git commit messages. This log documents the resolution of these inconsistencies.

## 🗂️ Task Numbering History
The following table reconciles the "Logical Task ID" (used in commit messages) with the actual **Physical Folder Name** and the species analyzed.

| Logical Task (Commits) | Physical Directory | Species Analyzed | Validation Result |
| :--- | :--- | :--- | :---: |
| Phase 0 | `TASK_0` | General Data Collection / HMMs | N/A |
| TASK 0 | `TASK_1` | *Arabidopsis thaliana* | 107 genes |
| TASK 1 | `TASK_2` | *Amborella trichopoda* | 36 genes |
| TASK 2 | `TASK_3` | *Nymphaea colorata* | 45 genes |
| TASK 3 | `TASK_4` | *Cinnamomum kanehirae* | 50 genes |
| TASK 4 | `TASK_5` | *Oryza sativa* (Rice) | 75 genes |
| TASK 5 | `TASK_6` | *Glycine max* (Soybean) | 228 genes |
| TASK 6 | `TASK_7` | *Medicago truncatula* | 72 genes |
| TASK 7 | `TASK_8` | *Prunus persica* (Peach) | 68 genes |
| TASK 8 | `TASK_9` | *Helianthus annuus* (Sunflower) | 128 genes |
| TASK 9 | `TASK_10` | *Nelumbo nucifera* (Sacred Lotus) | 48 genes |

> [!IMPORTANT]
> **Conclusion**: The current folder structure (`TASK_1` to `TASK_10`) is fixed and validated. The Master Index in `Workflow_Step-by-Step/README.md` has been updated to reflect these physical paths.

## 🚫 Excluded Species
The following species were investigated but excluded from the current pipeline:

1.  **Piper auritum**: Excluded due to lack of a complete reference genome and proteome + annotation set (only scattered UniProt entries available).
2.  **Magnolia grandiflora**: Excluded for similar reasons (nuclear genome unavailable).

## 🚀 Future Directives
- Use **Physical Directory IDs** (e.g., `TASK_10`) for all future scripts and documentation.
- All Phase 2 outputs will be stored in `Final_Phylogenetic_Analysis/` to avoid polluting individual task folders.
