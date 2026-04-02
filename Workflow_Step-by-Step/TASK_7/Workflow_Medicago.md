# TASK_7: Medicago truncatula Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_7/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for *Medicago truncatula* (Mt4.0) from Phytozome.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://phytozome-next.jgi.doe.gov/download/Medicago_truncatula_Mt4.0" -O Medicago_truncatula.fa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Medicago proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db medicago_db -out Medicago_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
Medtr3g123450.1    AT1G69120.1    77.0    242    0    0    1    242    1    242    0.0    465.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Medicago_MADS_hmmsearch.txt PF00319.MADS.hmm Medicago_proteins.fa
```
>>#### Results Preview
```txt
# Medicago HMMER search snippet
Medtr3g123450.1    E-value: 2.1e-27    Score: 98.4
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Medicago_candidates.fa > Aligned_Medicago.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **95 MIKCc-type MADS-box genes** were identified in *Medicago truncatula*.

<p align="center">------Medicago Analysis Complete------</p>
