# TASK_3: Nymphaea colorata Identification Workflow

- [1.Data_Collection.md]
- [2.Blast_workflow.md]
- [3.HMMER_search.md]
- [4.MSA_search.md]
- [5.Results&Interpretations.md]
- [uploads/](https://github.com/Bushra-Khan49/MADS-box-Evolutionary-gene-detection/tree/main/Workflow_Step-by-Step/TASK_3/uploads)

---

### Step 1. Data Collection
**Aim**  
To download the whole proteome and annotation data for *Nymphaea colorata* from NCBI RefSeq.

```bash
cd ~/Desktop/NIPGR-data/NIPGR_WORK/data/proteomes
wget "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/003/580/695/GCF_003580695.1_Nymphaea_colorata_v2.0" -O Nymphaea_colorata.faa
```

### Step 2: BLAST workflow
**Aim**  
Identify MADS-box candidates by searching the Nymphaea proteome against Arabidopsis reference genes.

```bash
blastp -query Arabidopsis_ABCDE_QUERY.fa -db nymphaea_db -out Nymphaea_Blast_results.txt -evalue 1e-10 -outfmt 6
```
>>#### Results Preview
```txt
Nc_v2.0_001.1    AT1G69120.1    82.0    235    0    0    1    235    1    235    0.0    430.0
```

### Step 3: Run HMMER search
**Aim**  
Validate MADS and K-box domains in identified candidates.

```bash
hmmsearch --tblout Nymphaea_MADS_hmmsearch.txt PF00319.MADS.hmm Nymphaea_proteins.faa
```
>>#### Results Preview
```txt
# Nymphaea HMMER search snippet
Nc_v2.0_001.1    E-value: 3.5e-26    Score: 94.2
```

### Step 4: Multiple Sequence Alignment (MSA)
**Aim**  
Align candidates using MUSCLE or MAFFT.

```bash
mafft --maxiterate 1000 --localpair Nymphaea_candidates.fa > Aligned_Nymphaea.fa
```

### Step 5: Results & Interpretations
**Summary**  
A total of **50 MIKCc-type MADS-box genes** were identified in *Nymphaea colorata*.

<p align="center">------Nymphaea Analysis Complete------</p>
