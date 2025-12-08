# About Nephele WGSA2+

This Docker image contains the WGSA2+ (Whole Genome Shotgun Amplicon 2 Plus) pipeline for the Nephele microbiome analysis platform. WGSA2+ is a comprehensive metagenomics pipeline that processes paired-end shotgun sequencing data to produce de novo assemblies, taxonomic classifications, and functional annotations for microbial communities.

## Features

- **Quality Control**: Trimming, error correction, and quality filtering of raw reads
- **Decontamination**: Removal of host and contaminant sequences
- **De Novo Assembly**: Sample-level metagenomic assembly using MEGAHIT
- **Taxonomic Classification**: Multiple classification approaches:
  - Read-based classification (Kraken2)
  - Gene-based classification (optional)
  - Scaffold-based classification (optional)
  - MAG-based classification (optional)
- **Functional Annotation**: Gene prediction and annotation using:
  - eggNOG-mapper for orthology assignment
  - MinPath for pathway inference
  - KEGG or MetaCyc pathway databases
- **Antimicrobial Resistance**: Optional AMRFinderPlus analysis
- **Metagenome-Assembled Genomes (MAGs)**: Optional binning and MAG reconstruction
- **Transcriptomics Support**: De novo transcriptome assembly with Trinity (optional)
- **Visualization**: Interactive HTML visualizations including:
  - Krona taxonomic and functional charts
  - Alpha and beta diversity plots
  - PCoA and nMDS ordination plots
  - Heatmaps and rarefaction curves
- **MicrobiomeDB Export**: BIOM files formatted for direct upload to MicrobiomeDB

## Supported Databases

### Taxonomic Classification Databases

- **plusPFV**: PlusPFP database with Protozoa, Fungi, and Viruses - comprehensive reference for diverse microbiomes (default)
- **MGBCdb**: Microbial Genomes Bacterial Collection - specialized bacterial genome collection
- **UHGGdb**: Unified Human Gastrointestinal Genome database - optimized for human gut microbiome studies
- **EuPATHdb**: Eukaryotic Pathogen database - specialized for eukaryotic pathogens

### Functional Annotation Databases

- **eggNOG**: Evolutionary genealogy of genes: Non-supervised Orthologous Groups
- **KEGG**: Kyoto Encyclopedia of Genes and Genomes - metabolic pathways and enzyme functions
- **MetaCyc**: Alternative metabolic pathway database

### Decontamination Databases

Various host organism databases available for removing host sequences from metagenomic data.

## Pipeline Workflow

1. **Read Processing**: Quality trimming and error correction
2. **Decontamination**: Host sequence removal
3. **Assembly**: De novo metagenomic assembly per sample
4. **Gene Prediction**: ORF prediction from assembled contigs
5. **Taxonomic Annotation**: Classification at multiple levels (reads, genes, scaffolds, MAGs)
6. **Functional Annotation**: Orthology assignment and pathway inference
7. **Abundance Quantification**: Read mapping and TPM calculation
8. **Diversity Analysis**: Alpha and beta diversity metrics
9. **Visualization**: Interactive charts and publication-ready plots

## Output Organization

The pipeline produces organized outputs including:

- **TAXprofiles**: Dataset-wide taxonomic abundance matrices and visualizations
- **PWYprofiles**: Functional pathway profiles and gene abundance tables
- **asmb_files**: Assembly FASTA and BAM files for downstream analysis
- **Per-sample folders**: Individual sample results with detailed annotations
- **BIOM files**: Standardized format for integration with other tools

## Use Cases

- **Microbiome Profiling**: Comprehensive taxonomic and functional characterization
- **Human Gut Studies**: Optimized databases and workflows for human microbiome research
- **Environmental Metagenomics**: Flexible database options for diverse environments
- **Pathogen Detection**: Support for viral, fungal, and eukaryotic pathogen identification
- **Antimicrobial Resistance**: AMR gene detection and characterization
- **Comparative Analysis**: Multi-sample diversity and differential abundance analysis
- **Metatranscriptomics**: Combined genomic and transcriptomic analysis

## Key Publications

**MEGAHIT Assembly:**
Li, D., et al. (2015). MEGAHIT: an ultra-fast single-node solution for large and complex metagenomics assembly via succinct de Bruijn graph. Bioinformatics, 31(10):1674-1676.

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
