# TASK_10: Nelumbo nucifera Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_10/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for *Nelumbo nucifera* from NCBI RefSeq.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/365/185/GCF_000365185.1_Lotus_v1.1" -O Nelumbo_nucifera.faa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Lotus proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db lotus_db -out Lotus_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
Nn_v1.1_001.1    AT1G69120.1    81.0    240    0    0    1    240    1    240    0.0    455.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Lotus_MADS_hmmsearch.txt PF00319.MADS.hmm Nelumbo_nucifera_proteins.faa
```
>>#### Results Preview
```txt
# Lotus HMMER search snippet
Nn_v1.1_001.1    E-value: 1.8e-26    Score: 95.1
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Lotus_candidates.fa > Aligned_Lotus.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **65 MIKCc-type MADS-box genes** were identified in *Nelumbo nucifera*.

<p align="center">------Lotus Analysis Complete------</p>
