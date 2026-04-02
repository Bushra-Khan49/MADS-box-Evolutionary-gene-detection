# TASK_8: Prunus persica Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_8/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for *Prunus persica* (v2.0+) from Phytozome.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://phytozome-next.jgi.doe.gov/download/Prunus_persica_v2.1" -O Prunus_persica.fa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Peach proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db peach_db -out Peach_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
Prupe.1G123400.1    AT1G69120.1    79.0    243    0    0    1    243    1    243    0.0    0.0    472.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Peach_MADS_hmmsearch.txt PF00319.MADS.hmm Prunus_persica_proteins.fa
```
>>#### Results Preview
```txt
# Peach HMMER search snippet
Prupe.1G123400.1    E-value: 1.5e-26    Score: 96.2
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Peach_candidates.fa > Aligned_Peach.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **85 MIKCc-type MADS-box genes** were identified in *Prunus persica*.

<p align="center">------Peach Analysis Complete------</p>
