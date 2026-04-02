# TASK_2: Amborella trichopoda Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_2/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for the basal angiosperm *Amborella trichopoda* (v1.0) from Phytozome.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://phytozome-next.jgi.doe.gov/download/Amborella_trichopoda_v1.0" -O Amborella_trichopoda.fa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Amborella proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db amborella_db -out Amborella_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
AmTr_v1.0_001.1    AT1G69120.1    85.0    240    0    0    1    240    1    240    0.0    450.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Amborella_MADS_hmmsearch.txt PF00319.MADS.hmm Amborella_proteins.fa
```
>>#### Results Preview
```txt
# Amborella HMMER search snippet
AmTr_v1.0_001.1    E-value: 2.1e-25    Score: 92.4
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Amborella_candidates.fa > Aligned_Amborella.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **36 MIKCc-type MADS-box genes** were identified in *Amborella trichopoda*.

<p align="center">------Amborella Analysis Complete------</p>
