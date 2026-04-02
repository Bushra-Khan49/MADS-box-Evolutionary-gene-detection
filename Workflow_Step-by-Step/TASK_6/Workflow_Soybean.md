# TASK_6: Glycine max Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_6/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for *Glycine max* (Wm82.v4.a1.v1) from Phytozome.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://phytozome-next.jgi.doe.gov/download/Glycine_max_v4.a1.v1" -O Glycine_max.fa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Soybean proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db soybean_db -out Soybean_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
Glyma.06G123400.1    AT1G69120.1    75.0    245    0    0    1    245    1    245    0.0    480.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Soybean_MADS_hmmsearch.txt PF00319.MADS.hmm Glycine_max_proteins.fa
```
>>#### Results Preview
```txt
# Soybean HMMER search snippet
Glyma.06G123400.1    E-value: 8.4e-29    Score: 102.5
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Soybean_candidates.fa > Aligned_Soybean.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **150 MIKCc-type MADS-box genes** were identified in *Glycine max*.

<p align="center">------Soybean Analysis Complete------</p>
