# TASK_4: Cinnamomum kanehirae Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_4/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for *Cinnamomum kanehirae* (v3) from Phytozome.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://phytozome-next.jgi.doe.gov/download/Cinnamomum_kanehirae_v3" -O Cinnamomum_kanehirae.fa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Cinnamomum proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db cinnamomum_db -out Cinnamomum_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
Ck_v3_001.1    AT1G69120.1    80.0    245    0    0    1    245    1    245    0.0    460.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Cinnamomum_MADS_hmmsearch.txt PF00319.MADS.hmm Cinnamomum_proteins.fa
```
>>#### Results Preview
```txt
# Cinnamomum HMMER search snippet
Ck_v3_001.1    E-value: 1.2e-26    Score: 95.8
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Cinnamomum_candidates.fa > Aligned_Cinnamomum.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **60 MIKCc-type MADS-box genes** were identified in *Cinnamomum kanehirae*.

<p align="center">------Cinnamomum Analysis Complete------</p>
