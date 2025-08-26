

## Data collection index

- [BLAST workflow](1.Blast_workflow.md)
- 
# Step 1. Data Collection

**Aim**  
To download Whole Genome, Whole Proteome, CDS, and annotations data for Model and selected species.

---

### Tasks
- Make a list of all the files that are required.  
  **Examples:**
  1. Whole proteome file of ABCDE _Arabidopsis_ genes  
  2. Whole proteome file of _Oryza sativa_ (rice)  
  3. Pfam domain files for all MADS-box domains  
     - PF00319 (MADS)  
     - PF00847 (AP2)  
     - PF01486 (K-domain)  

- Search different databases for each file.  
  1. Since most species have their separate database, it's recommended to collect whole genome/proteome data files from their specific database.  
  2. Check for last updated date and choose the most recent ones.  
  3. Make sure for Whole proteome data you choose the files which have the **complete proteome** present.  
  4. Choose specific data type files as per requirements (analysis, annotation/gene, info, unclassified, orthology, etc.).  
  5. Check file availability, file size, and file version according to your requirements.  
  6. Download all files in correct required file formats (see below).  

---

### Databases Used

- **Phytozome (DOE JGI)** → most plant species in this study were downloaded from here  
  - [https://phytozome-next.jgi.doe.gov](https://phytozome-next.jgi.doe.gov)  

- **TAIR (Arabidopsis)** → Arabidopsis reference proteome and ABCDE floral genes  
  - [https://www.arabidopsis.org](https://www.arabidopsis.org)  

- **JGI Data Portal** → _Oryza sativa_ (rice) genome and proteome data  
  - [https://data.jgi.doe.gov](https://data.jgi.doe.gov)  

- **NCBI RefSeq/GenBank** → for species not available in Phytozome  
  - [https://www.ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov)  

- **Pfam** → protein domain HMM profiles (PF00319, PF00847, PF01486)  
  - [https://pfam.xfam.org](https://pfam.xfam.org)  

---

### File Formats

**a) Genome (DNA sequence)**  
- FASTA (`.fa` / `.fna` / `.fasta`) → nucleotide sequences of the genome  
- Example: `Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz`  
- Sometimes split into chromosome FASTAs  

**b) Proteome (Protein sequence)**  
- FASTA (`.fa` / `.faa` / `.pep` / `.fasta`) → amino acid sequences of predicted proteins  
- Example: `Arabidopsis_thaliana.TAIR10.pep.all.fa.gz`  

**c) CDS (Coding Sequences only)**  
- FASTA (`.cds.fa` / `.cds.fna`) → contains only the coding sequences (no UTRs)  
- Example: `Arabidopsis_thaliana.TAIR10.cds.all.fa.gz`  

**d) Transcriptome / cDNA**  
- FASTA (`.cdna.fa` / `.mrna.fa`) → mRNA/cDNA including UTRs  

**e) Annotations (Gene Models)**  
- GFF3 (`.gff3`) → General Feature Format  
- GTF (`.gtf`) → Gene Transfer Format (RNA-seq tools like STAR/featureCounts)  
- Example: `Arabidopsis_thaliana.TAIR10.51.gff3.gz`  

**f) Protein Domains (Pfam HMM profiles)**  
- HMM (`.hmm`) → Hidden Markov Model profiles  
- Example: `PF00319.hmm`  

**g) Other Metadata (optional but useful)**  
- TSV/CSV with gene descriptions, orthogroups, gene families  
- README / version info → indicates database release  

---

### Download Guide (Summary)

- Whole Genome → `.fa`  
- Whole Proteome → `.fa` / `.faa`  
- CDS → `.cds.fa`  
- Annotations → `.gff3` (preferred) and `.gtf` (for RNA-seq)  
- Pfam domains → `.hmm` (PF00319, PF01486, PF00847)  

---

