# About Nephele WGSA2+

This Docker image contains the WGSA2+ (Whole Genome Shotgun Assembly 2 Plus) pipeline for the Nephele microbiome analysis platform. WGSA2+ is a comprehensive metagenomics/metatranscriptomics pipeline that processes paired-end shotgun sequencing reads to produce taxonomic classifications, _de novo_ assemblies, and functional annotations for microbial communities.

## Features

- **Quality Control**: Trimming, error correction, and quality filtering of raw reads
- **Decontamination**: Removal of host and contaminant sequences from a selection of common host databases
- **De Novo Assembly** with optional **read normalization**: 
    - Sample-level short read assembly using metaSPAdes/Trinity (mgx/mtx mode). 
    - Option for coverage normalization (recommended for large samples), to reduce read redundancy, resource consumption especially during assembly, and thus run time and assembly mistakes
- **Taxonomic Classification**: Multiple classification approaches:
  - Read-based classification (default; Kraken2)
  - Gene-based classification (optional; Kraken2)
  - Scaffold-based classification (optional; Kraken2)
  - MAG-based classification (optional; CheckM)
- **Functional Annotation**: Gene prediction and annotation using:
  - gene orthology assignment (eggNOG-mapper2)
  - pathway inference based on gene annotations (MinPath)
  - user elected pathway databases (KEGG or MetaCyc)
- **Antimicrobial Resistance**: Optional Resistance Gene Identification (RGI)
- **Metagenome-Assembled Genomes (MAGs)**: Optional binning and MAG reconstruction
- **Visualization**: Interactive HTML visualizations including:
  - Krona taxonomic and functional charts
  - Alpha and beta diversity plots
  - PCoA and nMDS ordination plots
  - Heatmaps and rarefaction curves
- **MicrobiomeDB Export**: BIOM files formatted for direct upload to MicrobiomeDB

## Supported Databases

### Host Decontamination Databases

- **[Human and Mouse Decontamination DB](https://zenodo.org/records/17873172)**: genomes of Human and Mouse 
- **[Primates Decontamination DB](https://zenodo.org/records/17882674)**: genomes of common primates (+human)
- **[Rodent Decontamination DB](https://zenodo.org/records/17882258)**:genomes of mouse, hamster and other rodent species (+human)
- **[Nematode Decontamination DB](https://zenodo.org/records/17872145)**: genomes of ~15 nematode species (+human)
- **[Mosquito Decontamination DB](https://zenodo.org/records/17871419)**:genomes of 2 mosquito species (+human)
- **[Tick Decontamination DB](https://zenodo.org/uploads/17913269)**: genomes of 14 tick species (+human) 
- **[Bat Decontamination DB](https://zenodo.org/uploads/17913858)**: genomes of 9 bat species (+human)
- **[Marine Decontamination DB](https://zenodo.org/records/17873185)**: genomes of 18 common marine host organisms (+human)
- **[Plants Decontamination DB](https://ftp.ncbi.nlm.nih.gov/genomes/refseq/plant/)**: reference genomes of ~111 plant species from NCBI (no human) collected in 2023

### Taxonomic Classification Databases

- **[plusPFV](https://benlangmead.github.io/aws-indexes/k2)**: Standard RefSeq database with Protozoa, Fungi, and Viruses (PlusPF) from 10/15/2025
- **[MGBCdb](https://github.com/BenBeresfordJones/MGBC)**: Mouse Gastrointestinal Bacterial Catalogue from 11/16/2021
- **[UHGG2db](https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/human-gut/v2.0.2/)**: Unified Human Gastrointestinal Genome database v2
- **[EuPATHdb](https://benlangmead.github.io/aws-indexes/k2)**: Eukaryotic Pathogen database from 4/18/2023

### Functional Annotation Databases

- **[EggNOG v5.0](http://eggnog5.embl.de/#/app/home)**: Evolutionary genealogy of genes: Non-supervised Orthologous Groups
- **[KEGG](https://www.kegg.jp/kegg/)**: Kyoto Encyclopedia of Genes and Genomes - metabolic pathways and enzyme functions
- **[MetaCyc](https://metacyc.org/)**: curated database of experimentally elucidated metabolic pathways from all domains of life


## Pipeline Workflow

1. **Read Processing**: Quality trimming and error correction
2. **Host decontamination**: Host sequence removal
3. **Taxonomic annotation of clean reads**: Taxonomic classification of cleaned reads (TEDreads)
4. **Read normalization** (optional): normalize read coverage in preparation for assembly 
5. **Assembly**: De novo metagenomic or metatranscriptomics assembly per sample
6. **Gene Prediction**: Genomic features prediction from assembled contigs
7. **Functional Annotation**: Orthology assignment of gene annotations and pathway inference
8. **Abundance Quantification**: Read mapping and TPM calculation for genes and pathway abundance estimations
9. **Taxonomic annotation of assembled features** (optional): Classification of genes, scaffolds and/or MAGs
10. **Metagenome-predicted genomes** (optional): prediction of metagenome assembled genomes (MAGs) and quality control
11. **Antimicrobial gene mining** (optional): scanning predicted features for antimicrobial resistance genes
12. **Diversity Analysis**: Alpha and beta diversity metrics across full dataset
13. **Visualization**: Interactive charts and dataset summary plots

## Output Organization

The pipeline produces organized outputs including:

- **TEDreads**: per-sample reports and logs produced from host decontamination step
- **TAXprofiles**: Dataset-wide taxonomic abundance matrices and visualizations
  - **readsTAX_{taxDBname}**: taxonomic annotations of reads per sample for dataset
      - **merged_tables**: dataset-wide community metrics tables 
      - **DivPlots**: dataset-wide summary plots of taxonomic diversity metrics 
  - **geneTAX_{taxDBname}** (conditional): taxonomic annotations of genes for dataset
  - **scafTAX_{taxDBname}** (conditional): taxonomic annotations of scaffolds/transcripts for dataset
  - **magsTAX_checkM** (conditional): MAG-based information for dataset
- **PWYprofiles/{pwyDBname}**: Dataset-wide functional pathway profiles and gene abundance tables
    - **merged_tables/**: dataset-wide functional diversity metrics
    - **DiversityPlots/**: dataset-wide summary plots of functional diversity metrics
- **asmb{MGX,MTX}/{Samp}_asmb/**:Per-sample assembly results, assembly stats and assembled features processing, including
  - **taxonomic**:
    - **geneTAX_{taxDBname}/** (conditional): taxonomic annotations of genes (user electable)
    - **scafTAX_{taxDBname}/** (conditional): taxonomic annotations of scaffolds (user electable)
    - **magsTAX_checkM/** (conditional): produced MAGs within sample
  - **functional**:
    - **genes/**: gene prediction and details within sample
    - **annotations/**: gene annotations and details within samples
    - **pathways/**: pathways predicted based on genes & user-elected pwyDB
- **asmb_files**: Assembly FASTA and BAM files, shortcuts or external analyses (e.g. Nephele DiscoVir pipeline)
- **BIOM files**: Standardized format for integration with other tools


## Use Cases

- **Microbiome Profiling**: Comprehensive taxonomic and functional characterization of short read shotgun metagenomic and metatranscriptomic data
- **Human Gut Studies**: Optimized databases and workflows for human microbiome research
- **Environmental Metagenomics**: Flexible database options for diverse environments
- **Pathogen Detection**: Support for viral, fungal, and eukaryotic pathogen identification
- **Antimicrobial Resistance**: AMR gene detection and characterization
- **Comparative Analysis**: Multi-sample diversity and differential abundance analysis
- **Metatranscriptomics**: Combined genomic and transcriptomic analysis

## Key Publications

**metaSPAdes Assembly:**
Nurk, S., Meleshko, D., Korobeynikov, A., & Pevzner, P. A. (2017). metaSPAdes: a new versatile de novo metagenomic assembler. Genome Research, 27(5), 824–834. 

**Kraken2 Classification:**
Wood, D.E., et al. (2019). Improved metagenomic analysis with Kraken 2. Genome Biology, 20:257.

**eggNOG-mapper Annotation:**
Huerta-Cepas, J., et al. (2019). eggNOG 5.0: a hierarchical, functionally and phylogenetically annotated orthology resource based on 5090 organisms and 2502 viruses. Nucleic Acids Research, 47(D1):D309-D314.

**MinPath Pathway Inference:**
Ye, Y. and Doak, T.G. (2009). A parsimony approach to biological pathway reconstruction/inference for genomes and metagenomes. PLoS Computational Biology, 5(8):e1000465.

**AMRFinderPlus:**
Feldgarden, M., et al. (2021). AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence. Scientific Reports, 11:12728.

## Links

- [GitHub Repository](https://github.com/niaid/nephele_wgsa2)
- [Nephele Platform](https://nephele.niaid.nih.gov/)
- [Pipeline Documentation](https://github.com/niaid/nephele_wgsa2/blob/main/docs/PipelineOutputDetails_WGSA2plus.md)
- [MicrobiomeDB](https://microbiomedb.org/)
