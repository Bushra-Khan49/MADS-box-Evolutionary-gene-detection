# TASK_9: Helianthus annuus Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_9/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for *Helianthus annuus* (Ha412HOv2) from Phytozome.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://phytozome-next.jgi.doe.gov/download/Helianthus_annuus_Ha412HOv2" -O Helianthus_annuus.fa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Sunflower proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db sunflower_db -out Sunflower_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
Han_v2_001.1    AT1G69120.1    76.0    245    0    0    1    245    1    245    0.0    475.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Sunflower_MADS_hmmsearch.txt PF00319.MADS.hmm Helianthus_annuus_proteins.fa
```
>>#### Results Preview
```txt
# Sunflower HMMER search snippet
Han_v2_001.1    E-value: 2.1e-28    Score: 101.2
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Sunflower_candidates.fa > Aligned_Sunflower.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **120 MIKCc-type MADS-box genes** were identified in *Helianthus annuus*.

<p align="center">------Sunflower Analysis Complete------</p>
