# TASK_5: Oryza sativa Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_5/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for *Oryza sativa* (IRGSP-1.0) from Phytozome or JGI.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://data.jgi.doe.gov/display/Osativa_323_v7.0" -O Oryza_sativa.fa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Rice proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db rice_db -out Rice_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
LOC_Os03g03100.1    AT1G69120.1    78.0    240    0    0    1    240    1    240    0.0    440.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Rice_MADS_hmmsearch.txt PF00319.MADS.hmm Oryza_proteins.fa
```
>>#### Results Preview
```txt
# Rice HMMER search snippet
LOC_Os03g03100.1    E-value: 4.5e-28    Score: 97.9
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Oryza_candidates.fa > Aligned_Oryza.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **75 MIKCc-type MADS-box genes** were identified in *Oryza sativa*.

<p align="center">------Rice Analysis Complete------</p>
