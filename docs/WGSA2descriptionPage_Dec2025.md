
see Bear for updated version


# WGSA2+ Pipeline (Updated Oct 2025)
###### Introducing WGSA2+! Our WGSA2 pipeline has expanded to support bulk RNAseq data and metatranscriptomics analysis. Under pipeline parameters you will find `Pipeline Mode` options, to process your data under `Metatranscriptomics Mode` or the default `Metagenomics Mode`. Check out the [Workflow](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2#workflow) section for a deeper dive into these updates!
# Introduction
The Nephele team at NIAID has implemented a command line-free Whole Metagenome Sequencing Assembly-based pipeline called WGSA2, into our cloud-based microbiome analysis platform. Initially built to process metagenomics datasets, the pipeline was recently expanded for metatranscriptomics datasets, leading to WGSA2+. In a command-line free experience built to reduce the need for individual computational resources and expertise, WGSA2+ facilitates the processing of these shotgun datasets derived from complex microbial communities and diverse habitats, including both host-associated and environmental samples. It generates visualizations and summarized output based on functional and taxonomic annotation, as well as assembly binning for metagenomics. The pipeline can be customized with extensive host and functional databases. Overall, WGSA2+ fills a computational void in metagenomics, enhances accessibility and comprehension of the data, and paves the way for deeper exploration of the microbiome.
Please visit our online WGSA2+ workflow tutorial at [WGSA2 workflow - a tutorial](https://www.protocols.io/view/wgsa2-workflow-a-tutorial-n92ldm98xl5b/v1).
# Prerequisites for WGSA2+ Submission
## Sequencing Data
The input sequences must be paired-end (PE), whole metagenome or metatranscriptome shotgun reads (not merged) in FASTQ format (see our FAQ on PE vs SE reads). Due to the scaffold-based approach of the assemblies, single-end (SE) reads are not acceptable for WGSA2+ pipeline.  

## File Formats and Dataset Size Limitations
* WGSA2+ can accept both gzipped (*.fastq.gz) and unzipped FASTQ files (*.bam, *.fasta or other file formats not accepted)
* File names should not contain special characters  
* Due to the huge resource and time requirements of WGSA2+, which grows with dataset size, the entire sumitted dataset **must not exceed 150GB gzipped**. If your dataset exceeds this size, please consider splitting it into separate submissions.  
* In addition to the restrictions above, a single sample in **Metatranscriptomics Mode** cannot be more than 25GB. This is the sum of both forward and reverse reads. If you have a sample exceeding this limit, we suggest subsampling it prior to uploading. In the future, we hope to have a solution that will accomodate larger file sizes in Metatranscriptomics Mode.  

## QC and Pre-Processing
Datasets submitted to WGSA2+ must firstly be run through [Nephele's QC pipeline](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/short-read-qc). This pipeline performs basic quality checks, trimming and filtering of the dataset, averts PE mismatch and other issues that can cause failure of WGSA2+ (or other time & resource consuming pipelines). This also helps with troubleshooting potential errors with WGSA2+ or other pipelines. Finally the produced QC reports helps the user better understand the quality, quantity, size and issues of their samples, sequences and dataset.
## Mapping File
A mapping file containing metadata is required during import of FASTQ files to Nephele, prior to starting a WGSA2+ job. This is a tab-delimited file containing information about submitted samples (sample names), the names of their respective FASTQ files, and simple grouping column (called **TreatmentGroup**). In WGSA2+, the TreatmentGroup column provides information for statistics and visualization steps. The template can be downloaded [here](https://nephele.niaid.nih.gov/user-guide/demo-datasets#wgs). The mapping file can be an *.xlsx file or a simple *.txt file.
## Biological Considerations
* Phylogenic composition and community complexity: The WGSA2+ pipeline can handle phylogenically diverse communities of single-cell microbial organisms including prokaryotes, viruses and unicellular eukaryotes (e.g. protozoa, single cell fungus, some diatoms). However, currently, WGSA2+ is not optimized for identifying complex eukaryotic genes.
## Abbreviations in Text
* TEDreads: reads that have been trimmd & filtered (T), error-corrected (E) and decontaminated (D)
* iTPM: designates the abundance score for each instance of a gene/transcript/annotation
* geneTPM: designates the abundance score for each unique gene / annotation label
* AMR: antimicrobial resistance
* MAGs: metagenome-assembled genomes


# User Options During Submission
## Run Additional Trim and Filter (Elective)
The WGSA2+ workflow incorporates a default procedure for baseline trimming and filtering of datasets, ensuring that the dataset meets the basic quality requirements for assembly. Although these settings are sufficient for reliable analysis, users have the option to customize/increase the read trimming and filtration criteria in preparation for assembly processing. This includes the ability to set thresholds for the average quality of reads, trimming the 5' and 3' ends, and/or specify a customized minimum read length.

## *NEW* Pipeline Mode (Elective)
WGSA2+ was recently updated to allow users to select between two pipeline modes. In addition to shotgun metagenomics from DNA, Nephele now supports data from RNA of complex communities, too! Use **Metagenomics Mode** to continue using our DNAseq approaches, or choose **Metatranscriptomics Mode** when you are processing bulk RNAseq.

## Host Decontamination DB (Options)
Given the nature of library preparation and shotgun sequencing, it is necessary to perform decontamination of metagenomic datasets, which allows fore removal of reads that contain any host genomes or biologically uninformative repeat sequences. For this purpose, we have created custom decontamination databases, each tailored to target specific group of host genomes. A detailed description of the content of each custom database is provided below. If you have any uncertainty regarding the appropriate database selection or if you would like to provide feedback and recommendations for such databases for future updates of WGSA2+, please don't hesitate to contact the [Nephele team](https://nephele.niaid.nih.gov/about/project-team).  

1. **Human and Mouse Decontamination DB (Default)**
     * Description: genomes of Human and Mouse 
     * [Content information and download](https://zenodo.org/records/17873172)
     * [Detailed content report](==🔴add file for link download==)
  
2. **Primates Decontamination DB**
     * Description: genomes of common primates (+human)
     * [Content information and download](https://zenodo.org/records/17882674)
     * [Content report](==🔴add file for link download==)
  
3. **Rodent Decontamination DB**
     * Description: genomes of mouse, hamster and other rodent species (+human)
     * [Content information and download](https://zenodo.org/records/17882258)
     * [Content report](==🔴add file for link download==)

4. **Nematode Decontamination DB**
     * Description: genomes of ~15 nematode species (+human)
     * [Content information and download](https://zenodo.org/records/17872145)
     * [Content report](==🔴add file for link download==)
  
5. **Mosquito Decontamination DB**
     * Description: genomes of 2 mosquito species (+human)
     * [Content information and download](https://zenodo.org/records/17871419)
     * [Content report](==🔴add file for link download==)

6. **Tick Decontamination DB (NEW!)**
     * Description: genomes of ~33 tick species (+human) 
     * [Content information and download](https://zenodo.org/uploads/17913269)
     * [Content report](==🔴add file for link download==)

7. **Bat Decontamination DB (NEW!)**
     * Description: genomes of 33 bat species (+human)
     * [Content information and download](https://zenodo.org/uploads/17913858)
     * [Content report](==🔴add file for link download==)
  
8. **Marine Decontamination DB**
     * Description: genomes of 18 common marine host organisms (+human)
     * [Content information and download](https://zenodo.org/records/17873185)
     * [detailed content report](==🔴add file for link download==)

9. **Plants Decontamination DB**
     * Description: reference genomes of ~111 plant species from NCBI (no human) collected in 2023
     * [Content information and download](https://ftp.ncbi.nlm.nih.gov/genomes/refseq/plant/)
     * [Content report](==🔴add file for link download==)


## TAX Classification DB (Options)

1. **[RefSeq](https://www.ncbi.nlm.nih.gov/refseq/about/)** (Reference Sequences database plus Fungi and Protozoa)
   - date of creation: Oct 2025
   - [Source](https://benlangmead.github.io/aws-indexes/k2)
   - The Reference Genomic Sequence database is comprised of ~170,400 curated reference genomes from bacterial, archaeal, viral kingdoms of life.  This database is also extended with high quality single-cell eukaryotic protozoan and fungal genomes. This database, is recomended for global overview of any microbial community. 
   - Find RefSeq DB content report, [here](==🔴add file for link download==) 
   

2. **[MGBC](https://github.com/BenBeresfordJones/MGBC)** (Mouse Gastrointestinal Bacterial Catalogue)
   - date of creation: Nov 2021
   - [Source](https://github.com/BenBeresfordJones/MGBC)
   - The Mouse Gastrointestinal Bacterial Catalogue comprises of 26,640 high-quality, non-redundant genomes from mouse microbiota obtained by MAGs cultures and isolates. It provides improved bacterial taxonomic assignments of metagenomic samples of mouse gut origin. 
   - Find MGBC DB content report, [here](==🔴add file for link download==).

3. **[UHGG2](https://www.ebi.ac.uk/about/news/updates-from-data-resources/uhgg-v20-released-mgnify/)** (Human Gastrointestinal Genome Catalogue) **(NEW!!)** 
   - date of creation: Nov 2022
   - [Source](https://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/human-gut/v2.0.2/)
   - Unified Human Gastrointestinal Genome catalogue comprises of 289,232 prokaryotic genomes clustered into 4,744 representative species, collected from both RefSeq and GTDB. UHGG provides improved bacterial taxonomic assignments for microbiomes of human gut origin. 
   - Find UHGG DB content report [here](==🔴add file for link download==)

4. **[EuPathDB](https://www.sanger.ac.uk/collaboration/eupathdb/)** (Eukaryotic Pathogen Database)
    - date of creation: April 2023 
    - [Source](https://benlangmead.github.io/aws-indexes/k2)
    - Eukaryotic Pathogen Database is a resource for detecting eukaryotic pathogens.
    - Find EuPathDB ontent report [here](==🔴add file for link download==)


# Output Downloadable TEDread FASTQ Files (Elective)
The first steps of the pipeline are to pass the reads of each sample through its own QA steps, customized for the processes ahead -  trimming and filtering (T), error-correction (E), and host- and rRNA-decontamination (D). These TED reads (TEDreads) are produced for each sample and are used downstream in the pipeline. Since the size of these can be quite large (comparable to the input size of the dataset), they are provided as a separate file to download, after pipeline completion. These files are an optional download not part of the main results output of the pipeline. 

## Run AMR Finding (Elective)
For users that are interested in the Antimicrobial Resistance Peptides (AMRs) content of their samples, we have provided an elective option to run [AMRFinderPlus](https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/) on the assembled genes for each sample. Since this additional step is resource and time consuming, it is omitted from the default workflow of the pipeline. Please be aware that by selecting this option, additional compute time will be required for the completion of the pipeline.
## Metabolic Pathways Database (Options)
Functional capacity of a community is assessed by mapping the gene annotations from each sample against a database of known functional pathways. WGSA2+ provides the user with 2 choices of functional pathway databases - the KEGG DB (as of Sept 2022), which uses KO annotations [default], or the MetaCyc DB (as of Sept 2022), which utilizes the EC annotations of the dataset. There is no wrong choice.
## Produce Gene-Based or Scaffold-Based Taxonomic Profiles (Electives)
As a default setting, WGSA2+ utilizes the Kraken2 tool (refer to Workflow section Step 3) to generate taxonomic profiles based on TEDreads for each sample. Through extensive testing, we have found these Kraken2 profiles to be highly accurate, taxonomically sensitive, and computationally lenient. Additionally, users have the option to generate taxonomic characterizations on the predicted genes (or scaffolds) within each sample, which also allows for the evaluation of community profiles. While these alternative approaches may have lower sensitivity in detecting taxonomic presence and abundance, they are valuable for identifying genes (or genomic regions) associated with specific organisms of interest. Please note that utilizing alternative or multiple TAX profiling strategies is necessary, for reliable taxonomic characterization of a dataset and would generally produce concordant results. Therefore, Gene and Scaffold-based profiles are not part of the default pipeline output.
## Produce MAGs (Elective)
This option enables the generation of metagenome-assembled genomes (MAGs) and is optimized for communities with known and prokaryote-rich organisms, catering to users interested in the more abundant organisms within their samples. It's important to note that this option of the WGSA2+ pipeline is highly resource and time-consuming, which may result in increased job-time. It is advisable to use subsets of selected samples when utilizing this option. Despite the reduced resolution at the community level, the MAG-based taxonomic profiles generated by this WGSA2+ option are highly accurate and can provide detailed strain-level information.
This option is available in **Metagenomics Mode** ONLY.
# Workflow
==🔴[insert the main workflow plot here]==
## Steps 1 & 2: Trimming, Error-Correction and Decontamination (TED)
The WGSA2+ pipeline begins by processing reads in preparation for assembly, which includes 3 steps (process acronym is chosen as TED):
* (T) trimming and filtering of reads ([fastp](https://academic.oup.com/bioinformatics/article/34/17/i884/5093234?login=false)). This step is not as thorough as the recommended pre-processing performed by our [QC pipeline](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/short-read-qc) and therefore should not be considered its replacement. By default, this step verifies that the reads have met the required minimal QA standards. However, if the user desires to apply more stringent quality thresholds after running the QA pipeline, this step allows for such customization through elective trimming and filtering options (see [user options](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2#options) section).
* (E) error-correction (fastp). PE sequences are merged and sequencing errors are corrected within the PE overlapping regions. This process is specifically designed to improve assembly efficiency and success.
* (D) decontamination ([Kraken 2](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2014-15-3-r46)). The dataset undergoes a thorough cleaning process to remove host DNA and non-informative elements such as homopolymeric or simple sequence repeats. This is achieved by utilizing a user-selected database containing curated collections of potential host organism genomes (see [user options](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2#options) section). The decontamination process is crucial for reducing the dataset size to include only biologically relevant data. By removing non-informative host, junk and repeat sequences, the assembly quality is significantly improved for each sample. Contamination levels and identification of host organisms are reported per sample in the form of {sampleName}_decontamREPORT.
* (D mtx) Removal of rRNA ([SortMeRNA](https://academic.oup.com/bioinformatics/article/28/24/3211/246053)). After host decontamination, and if the user selects **Metatranscriptomics Mode**, reads will be additionally filtered for rRNA reads. This produces a folder called TEDreads_mtx (instead of TEDreads) that will contain reads additionally filtered for rRNAs. The sortMeRNA alignment report, which describes the proportion of reads that were identified as rRNA can be found in TEDreads_mtx/{SampleName}_sortmerna_aligned.log. This is a useful file to review the efficiency of rRNA removal techniques during library preparation. If fewer than 100 reads remain after rRNA filtering, the pipeline will fail. In this case, it may be possible that your data derives from 16S rRNA amplicon data, and DADA2 or QIIME may be more appropriate for your samples.
RNA reads can be composed of up to 90% ribosomal RNA (rRNA) if not depleted during library preparation to enrich for messenger RNA. Still, bench-based rRNA deppletion methods can still have limited efficiency. Therefore, we use sortMeRNA to deplete rRNA computationally. The pipeline currently uses the default rRNA database (v 4.3.4, dated July 21, 2021, downloaded December 2023). It contains the SILVA bacterial 16S database clustered at 90%, 5S and 5.8S seeds, as well as fungal and archaeal rRNA clustered at 95%. This database has a benchmark accuracy of 99.899%, per SortMeRNA. The TEDreads_mtx/{sampleName}_sortmerna_aligned.logfile reports the number and proportion of reads identified as rRNA and removed.
## Step 3: TAX Profiling
By default, WGSA2+ includes the generation of taxonomic profiles per sample based on the TED reads, utilizing the [Kraken 2](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2014-15-3-r46) tool. Our tests have demonstrated that Kraken 2 is a computationally efficient method that provides moderate accuracy and taxonomic sensitivity compared to other common profiling methods (e.g., gene-based or alternative tools). Kraken relies on a comprehensive database of k-mers derived from entire genomes, enabling accurate taxonomy assignment for both coding and non-coding reads. WGSA2+ offers users the flexibility to choose the classification databases that best suit their datasets (see [user options](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2#options) section). The resulting taxonomic profiles are visualized using the [Krona tool](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-385) on a per-sample basis, and they are also consolidated into a summary community matrix table (see Step 9). This table serves as a foundation for customized project-specific community analysis by the user, while WGSA2+ additionally provides basic statistics and visualizations in steps 10-11.
## Steps 4 & 5: De Novo Assembly, Read Mapping and Abundance Scoring
In this step, the pipeline uses [metaSPAdes](https://pmc.ncbi.nlm.nih.gov/articles/PMC3342519/) assembler, to perform de novo assembly of the TED reads. The process is performed for each sample independently.
If **Metatranscriptomics Mode** is selected, de novo assembly of rRNA-filtered TED reads into transcripts is performed with [Trinity](https://www.nature.com/articles/nbt.1883) for each sample independently. In literature and extensive testing, Trinity showed improved assembly statistics (greater number of longer transcripts) as well as an increased number of identified genes compared to metaSPAdes or rnaSPAdes among metatranscriptomics datasets.
Next, [Bowtie2](https://pmc.ncbi.nlm.nih.gov/articles/PMC3322381/) and [SAMtools](https://academic.oup.com/bioinformatics/article/25/16/2078/204688?login=false) are used to align each sample's TED reads to the sample's assembly (a process called 'mapping'). The alignment is also QC'd and cleaned (de-replicated, mate pairs are fixed, etc) to ensure each pair of reads maps best and only once to the produced assembly. Then, the aligned reads are evaluated (GC content, plus/minus strand alignments), enumerated and abundance scores produced per scaffold per sample (scaffold length, depths, coverage, RPM (reads per million), etc. statistics are collected). This information is used for downstream abundance assessments.
Note: this is one of the most time & resource consuming stages of the pipeline and depending on sample size may take longer than a few hours per sample. Parallelization is used to achieve assembly of multiple samples simultaneously (however patience is still required). Pipeline failures in this processing stage suggests problematic sample depths or read quality.
## Steps 6 & 7: Gene Prediction & Annotation
WGSA2+ utilizes [Prodigal](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-119) for performing genetic feature predictions, and [EggNOG-mapper2](https://academic.oup.com/mbe/article/38/12/5825/6379734?login=false) against the extensive EggNOG-v5 database for annotation of the predicted features. Gene annotations produced are based on KO, EC and COG annotation terms.
Prodigal was also maintained as the gene identifier of choice for **Metatranscriptomics Mode** as it performed comparably to other transcriptomics-specific tools for prokaryotic samples during our extensive testing.
Gene abundance scores are computed by enumerating the number of reads aligned to the gene coordinates of the scaffold ([VERSE tool](https://www.biorxiv.org/content/10.1101/053306v1)) (used: default settings "featureCounts", -z 0). RPM and TPM (transcripts per million) values are calculated based per transcript instance in each scaffold per sample and produce the abundance scores of each gene (iTPM).
**NEW** Since each sample contains multiple organisms that may contain multiple copies of any given gene transcript, gene abundances are also summarized per unique gene annotation in each sample (geneTPM). A geneTPM abundance matrix is now provided with WGSA2+.
## Step 8: Pathway Inference
Based on the user's chosen option for functional database (KEGG or MetaCyc), the functional profiles for each sample is generated by mapping the the corresponding gene annotation terms (KO or EC) to their corresponding database of pathways. This mapping is accomplished by [MinPath](https://pmc.ncbi.nlm.nih.gov/articles/PMC2714467/), which is a parsimony approach for reconstructing the minimal set of pathways described by a query of genes. The abundance of each pathway is then calculated by averaging the iTPM values (from each instance of gene) from each gene within each inferred pathway. To achieve this, the script [genes.to.kronaTable.py](https://metagenomics-workshop.readthedocs.io/en/latest/annotation/summarize.html) is employed. The resulting functional profiles, representing metabolic pathway profiles, are summarized for each sample in an HTML file using KronaTools.
## Steps 9: Dataset Collations & Abundance Matrix Summaries
These steps are conditional to datasets containing multiple samples (best if >3 samples). Firstly, the community profiles from each sample are collated to create 1 abundance matrix per profile type, which represents the dataset. These profile types producing community matrices are:
* Per Taxonomic composition for each sample (unique species composition)  
* Per Genetic composition for each sample (unique gene composition)  
* Per Functional composition for each sample (inferred pathway composition)  
The Taxonomic and Functional profile matrices are further formatted into biom files that include metadata. These `*.biom` files can be conveniently uploaded into [MicrobiomeDB](https://microbiomedb.org/mbio/app) or customized for other user-specific purposes.
## Step 10: Community Visualizations and Summaries
The created abundance matrices are imported in R to produce simple community characterizing visualization plots (e.g. alpha and beta diversity plots, abundance profile heatmaps etc.).
## Workflow: Add-ons
In addition to the main workflow of WGSA2+, the user has a few additional options for consideration. Those include:
* Creation and evaluation of MAGs
* Production of gene or scaffold taxonomic assignments (depending on research interest)
* AMR gene finding


# Creation and Evaluation of MAGs
Users have the option to select the MAGs (metagenome-assembled genomes) feature in WGSA2+, which enables the generation of individual genomes from metagenomic assemblies. The WGSA2+ pipeline employs [MetaBat2](https://pmc.ncbi.nlm.nih.gov/articles/PMC6662567/) to bin scaffolds with a length greater than 1500bp, based on scaffold features like connectivity, GC content and read coverage. This process aims to reconstruct the most representative genomes of each community. Quality assessments of the resulting MAGs are performed using [CheckM](https://pubmed.ncbi.nlm.nih.gov/25977477/). The assessment includes taxonomic affiliation, MAG size, abundance estimations, completeness, contamination levels, number of genes, and more. Additionally, a biom file is generated, consolidating the MAGs data from all the samples.
Please note that the MAGs option within WGSA2+ is primarily recommended for prokaryotic-dominated communities, as the classification of eukaryotic draft genomes (bins) may not be as accurate. Taxonomic profiles are once again produced, summarized, and visualized per sample using KronaTools. While MAG-based profiles align closely with TEDread-based profiles, they may be less sensitive in capturing less abundant organisms (for more details, refer to [WGSA2 benchmarking section](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2#profiling)).
When **Metatranscriptomics Mode** is selected, the option to assemble MAGs will not be available.
## Production of Gene or Scaffold-Based Taxonomic Profiles
By default, WGSA2+ will produce TEDread-based taxonomic profiling with Kraken2. User may elect to additionally produce taxonomic characterization of the predicted features or scaffolds, within each sample, and community profiles based on those classifications. These can be useful in identifying genes (or genomic regions) within specific taxonomies of interest. WGSA2+ will utilize the same classification database for gene or scaffold profiling, as elected for the TEDread-based taxonomic profiling.
## AMR Gene Finding
User may elect to run the antimicrobial resistance gene tool [AMRFinderPlus](https://github.com/ncbi/amr/wiki/Running-AMRFinderPlus) using the predicted features from each sample. This option is time consuming and not provided in the default output.
# Pipeline Output Details
Please refer to ==🔴[fix [this file]]== for the complete and detailed list of the pipeline output and details. File will also be part of the main output downloaded from the pipeline. Here, we detail only the outputs of the main result aggregate folders.

##### **TAXprofiles** Folder
**Contains dataset-wide taxonomic results**
Although listed first here, this folder is one of the last produced from the pipeline as it contains the dataset-wide taxonomic results (visualizations, summaries and community matrices) produced from each processed sample.
Complete contents of this folder will depend on the options selected for the pipeline.  
* **readsTAX_{DBname}** folder (default): Contains logs and reports from the taxonomic classification of TED reads. Sub-folders:  

  * `bin` folder: files used by Krona for creating the `TAXplots` HTML chart. These are the text versions of the per-sample taxonomic reports from the TED reads, and they are visualized in the `TAXplots_ReadsTAX_{DBname}.html` report.    
  * `bioms` folder: The files from the bin folder presented in a JSON BIOM format. These can be manually uploaded to MicrobiomeDB or any other analytical platform, if needed.  
  * `reports` folder: contains Kraken2 report files with detailed taxonomic classifications produced for each sample  
  * TAXplots_readsTAX_{DBname}.html file: interactive Krona chart of the TED read-based taxonomic profiles, collected in the bin folder.    
  * `merged_tables` folder (**conditional of ≥ 2 samples**): a folder containing the collated taxonomic abundance matrix from the entire dataset. The TAX abundance matrix is reported in 6 tab-delimited text files and 1 BIOM file. The files are named based on content and format of certain profile information: TAX*labels designate files that contain the taxonomy in separate columns per rank, the Lineage* labels designate files representing the lineage of each taxonomy (all tax ranks) in 1 column (ranks separated by ; within the column). Counts* label indicates files representing the abundance counts of each taxonomy for each sample (collated across dataset). The *.biom file represents counts for each sample and lineage column. This is the source file for the for_analyze_with_microbiomedb.biom in the main folder.  
  * `DivPlots` folder (**conditional of ≥ 2 samples**): Diversity plots and exploratory statistics for the dataset within the ReadsTAX folder. The files include an alpha diversity indices table, as well as a boxplot (TAX_AlphaDiv.txt and TAX_AlphaDiv.pdf), beta diversity PCoA and nMDS ordination plots (TAX_BetaDiv_nMDS.pdf and TAX_BetaDiv_PCoA.pdf, requires >=3 samples), TAX content heatmap (TAX_Profile_Heatmap.pdf), Rank Abundance Curve plot (TAX_RankAbundanceCurve.pdf) and Rarefaction Curves (TAX_RarefactionCurve.pdf). In some cases (e.g. ordination plots), some exploratory statistics will fail due to the content of the dataset.  
* **geneTAX_<DBname>** folder (**based on user selections**): Conditional on the choice of classification DB, visual summary of the gene-based taxonomic annotations for each sample, are presented here. **Note: MGBCdb does not produce visual summaries**. This folder contains a `bin` folder with text versions of the profiles from each sample and a `TAXplots_genetax.html` interactive krona plot summary file of the gene-based taxonomic profiles from each sample.
* **MAGs_TAX** folder (**based on user selections**): This folder is generated only if "MAGs & MAG TAX annotation" is chosen, and is available in Metagenomics Mode **ONLY**. It contains the TAX classification and abundances of the MAGs. It also contains a `bin` folder with text versions of the MAG-based taxonomic profiles and visualizations by KronaTools (`TAXplots_MAGx.html`). It will also contain a `MAG-based_Counts+TAX.biom` file summarizing the MAG-based taxonomic profiles of all samples.  
  **NOTE**: Scaffold-based taxonomic annotations option will not produce visualizations, but annotations are reported within each sample's assembly folder.

##### **PWYprofiles** Folder
  **Contains dataset-wide functional results**
Contains dataset-wide the functional analysis results from the pipeline, including pathway inferred profiles (PWY) and gene-based profiles. The folder will contain one folder, named based on the **metabolic pathway database** chosen at submission: keggPWYs.MP (default choice) or metacycPWYs.MP (alternative choice). Either folder will have the same structure:
* **PWYplots_{ko2gg, ec2cc}.html**: an interactive krona html report with the functional profiles for each sample (KronaTools), based on inferred PWYs    
* **pwybin** folder: per-sample text reports of the PWYs identity & abundances files. the files are used to create the html report & biom files  
* **bioms** folder: the JSON BIOM versions of the `pwybin` files.  
* **genebin** folder: per-sample text reports of identity and abundances of each unique gene found in the sample.
* **merged_tables** folder (**conditional of ≥ 2 samples**): Dataset-wide PWY abundance summary abundance matrix tables representing the collated results each sample functional annotation and abundance scoring. The PWY abundance matrix is reported in 6 tab-delimited text files and 1 BIOM file. The files are named based on content and format of certain profile information: PWY labels designate files that contain the pathway information as separate columns per tiers, the allTiers labels designate files representing the Tiers of each pathway in 1 ;-delimited column. Counts label indicates files representing the abundance counts of each pathway for each sample (collated across dataset). The biom file represents counts for each sample and tiers column. The folder also contains a gene-based abundance matrix (merged_geneTPMtable.txt) produced from the collated gene abundance information in the genebin folder.  
* **DivPlotsMP** (**conditional of ≥ 2 samples**): Simple exploratory plots of PWY functional dataset-wide profiles. Visualizations include a community PCoA and nMDS functional composition ordination plots (PWY_BetaDiv_nMDS.pdf and PWY_BetaDiv_PCoA.pdf; (>=3 samples)) produced from the inferred PWY matrix in merged_tables.MP as well as a pathway abundance heatmap plot (PWY_Profile_Heatmap.pdf (>=2 samples)).
##### **asmb_files** Folder
  For user's convenience, WGSA2+ now creates a folder for storing the final assembly files from each sample (the `{sampleName}_assembly.bam` and `*.fasta` files). This new main output folder is a convenient way to transfer your data to downstream pipelines such as [DiscoVir](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/discovir). The assembly files in this folder are also found in their original per-sample assembly folder location (`asmbMetaSpades/{sampleName}_asmb/ `(for metagenomics mode) OR `asmbTrinity/{sampleName}_asmb/` (for **Metatranscriptomics Mode**)).


# Accuracy of WGSA2+ Profiling
We sought to assess and benchmark the accuracy of the WGSA2+ taxonomic assignments by evaluating results when running the pipeline with known microbial community. For this, we used the [2nd CAMI Toy Human Microbiome Project Dataset](https://cami-challenge.org/) ([Sczyrba et al. 2017](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2)). The plots bellow represent results from the comparison of the taxonomic and functional profiles of 3 CAMI samples (S1-GI, S6-Oral & S28-Skin) against each other, as produced by the various strategies of WGSA2+, bioBakery or as expected by sample design. To produce these comparisons, the community abundance matrices from each pipeline and strategy were merged based on TAXid, rarified to same readDepths (sample with lowest read depth) and ASVs filtered at relative abundance >0.5%.
The Alpha Diversity box plots represent the average Shannon diversity and produced Species Richness from the 3 samples. This plot best presents the overall accuracy of the strategies used by WGSA2+ TAX assignments. To produce these plots, the community abundance matrices from each strategy were merged based on TAXid, rarified to sample with lowest read depth and filtered to relative abundance of 0.5%.
1 A heatmap of the top 35 species from 3 CAMI sample profiles, produced by the WGSA2+ TED-read-based TAX profiles (Kraken2 at confidence level 0.05), the bioBakery pipeline (MetaPhlAn3), and as Expected by sample design):## ![](wgsa2_heatmap-DdXeU_H3.png)
2 Alpha Diversity box plots, represent the average Species Richness, Chao1, Shannon & InvSimpson Diversity across 3 CAMI samples. The plot demonstrates the overall expected accuracy of the strategies used by WGSA2+ for TAX assignments and compares them to the expected profiles and the bioBakery produced TAX profiles:## ![](wgsa2_AlphaDivAll-775sh3cR.png)
3 Beta Diversity PCoA ordination plot based on Bray-Curtis dissimilarity matrix, produced from 3 CAMI samples from WGSA2+ TAX profiles based on different strategies (read, gene & scaffold-based TAX profiles), bioBakery produced profiles and as expected by design:## ![](wgsa2_BetaDivAll-DAXc9-YX.png)
4 A table for number of predicted EC annotations and unique pathways, produced from WGSA2+ vs bioBakery:## ![](wgsa2_PWYcomparisonsTAB-95G4Do8c.png)

⠀If you wish to test the WGSA2+ pipeline, you can find and download a small example dataset (3 CAMI samples, subset to read depth of 1 million reads) and corresponding mapping file specific for the WGSA2+ pipeline, from Nephele's [Demo Datasets](https://nephele.niaid.nih.gov/user-guide/demo-datasets#wgs) page.
# Feedback
The Nephele team is working hard to improve and extend this pipeline to provide users with a better experience and more analyses. Please kindly provide us with feedback and keep an eye on Nephele updates.
# Software, Scripts, Tools Utilized by the Pipeline
Tool versions used by the pipeline are recorded in the log file.
* [fastp](https://github.com/OpenGene/fastp)  
* [kraken2](https://github.com/DerrickWood/kraken2)  
* [spades](https://pmc.ncbi.nlm.nih.gov/articles/PMC3342519/)  
* [bowtie2](https://bowtie-bio.sourceforge.net/bowtie2/index.shtml)  
* [bbtools](https://jgi.doe.gov/data-and-tools/software-tools/bbtools/)  
* [samtools](https://www.htslib.org/)  
* [MetaBAT 2](https://bitbucket.org/berkeleylab/metabat/src/master/)  
* [Prodigal](https://github.com/hyattpd/Prodigal)  
* [eggNOG-mapper2](https://github.com/eggnogdb/eggnog-mapper)  
* [verse](https://kim.bio.upenn.edu/software/verse.shtml)  
* [AMRFinderPlus](https://github.com/ncbi/amr)  
* [KronaTools](https://github.com/marbl/Krona/wiki)  
* [MinPath](https://github.com/mgtools/MinPath)  
* [R statistical computing](https://www.r-project.org/)  
* [kreport2krona.py](https://github.com/jenniferlu717/KrakenTools)  
* [CheckM](https://ecogenomics.github.io/CheckM/)  
* [biom-format](https://biom-format.org/)  
* [SortMeRNA](https://sortmerna.readthedocs.io/en/latest/index.html)  
* [Trinity](https://github.com/trinityrnaseq/trinityrnaseq/wiki)  


⠀References
* Angelova AG, et al. (2023). WGSA2 workflow - a tutorial. [https://dx.doi.org/10.17504/protocols.io.n92ldm98xl5b/v1](https://dx.doi.org/10.17504/protocols.io.n92ldm98xl5b/v1)
* Joint Genome Institute. [BBtools](https://jgi.doe.gov/data-and-tools/software-tools/bbtools/). 2014
* Shifu Chen, Yanqing Zhou, Yaru Chen, Jia Gu, fastp: an ultra-fast all-in-one FASTQ preprocessor, Bioinformatics, Volume 34, Issue 17, 01 September 2018, Pages i884-i890, [https://doi.org/10.1093/bioinformatics/bty560](https://doi.org/10.1093/bioinformatics/bty560)
* Bankevich et al. SPAdes: A New Genome Assembly Algorithm and Its Applications to Single-Cell Sequencing. [J Comput Biol](https://pmc.ncbi.nlm.nih.gov/articles/PMC3342519/). 2012 May; 19(5): 455-477.doi: [10.1089/cmb.2012.0021](https://www.liebertpub.com/doi/10.1089/cmb.2012.0021)
* Langmead, B., Trapnell, C., Pop, M. et al. Ultrafast and memory-efficient alignment of short DNA sequences to the human genome. Genome Biol, (2009). [https://doi.org/10.1186/gb-2009-10-3-r25](https://doi.org/10.1186/gb-2009-10-3-r25)
* Li H, Handsaker B, Wysoker A, Fennell T, Ruan J, Homer N, Marth G, Abecasis G, Durbin R; 1000 Genome Project Data Processing Subgroup. The Sequence Alignment/Map format and SAMtools. Bioinformatics. 2009 Aug 15;25(16):2078-9. doi: 10.1093/bioinformatics/btp352. Epub 2009 Jun 8. PMID: 19505943; PMCID: PMC2723002.
* Kang, Dongwan D et al. MetaBAT 2: an adaptive binning algorithm for robust and efficient genome reconstruction from metagenome assemblies, PeerJ. 2019, doi:10.7717/peerj.7359
* Cantalapiedra Carlos P., Hernandez-Plaza Ana, Letunic Ivica, Bork Peer, Huerta-Cepas Jaime. eggNOG-mapper v2: functional annotation, orthology assignments, and domain prediction at the metagenomic scale. biorxiv. (2021) doi: [https://doi.org/10.1101/2021.06.03.446934](https://doi.org/10.1101/2021.06.03.446934)
* Hyatt, Doug et al., Prodigal: prokaryotic gene recognition and translation initiation site identification., BMC bioinformatics vol. 11 119. 8 Mar. 2010, doi:10.1186/1471-2105-11-119
* Parks, Donovan H et al., CheckM: assessing the quality of microbial genomes recovered from isolates, single cells, and metagenomes., Genome research vol. 25,7 (2015): 1043-55. doi:10.1101/gr.18607214
* Ondov, B.D., Bergman, N.H. Phillippy, A.M. Interactive metagenomic visualization in a Web browser. BMC Bioinformatics, 385 (2011). [https://doi.org/10.1186/1471-2105-12-385](https://doi.org/10.1186/1471-2105-12-385)
* Ye Y, Doak TG (2009) A Parsimony Approach to Biological Pathway Reconstruction/Inference for Genomes and Metagenomes. PLOS Computational Biology 5(8): e1000465. [https://doi.org/10.1371/journal.pcbi.1000465](https://doi.org/10.1371/journal.pcbi.1000465)
* [Caspi et al 2020](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2), The MetaCyc database of metabolic pathways and enzymes - a 2019 update, Nucleic Acids Research 48(D1):D445-D453
* Zhu, Q., Fisher, S.A., Shallcross, J., Kim, J. (Preprint). VERSE: a versatile and efficient RNA-Seq read counting tool. bioRxiv 053306. doi: [http://dx.doi.org/10.1101/053306](http://dx.doi.org/10.1101/053306)
* Kopylova E, Noé L, Touzet H. SortMeRNA: fast and accurate filtering of ribosomal RNAs in metatranscriptomic data. Bioinformatics. 2012 Dec 15;28(24):3211-7. doi: [http://doi.org/10.1093/bioinformatics/bts611](http://doi.org/10.1093/bioinformatics/bts611).
* Grabherr MG, Haas BJ, Yassour M, et al. Full-length transcriptome assembly from RNA-Seq data without a reference genome. Nat Biotechnol. 2011 May 15;29(7):644-52. doi: [http://doi.org/10.1038/nbt.1883](http://doi.org/10.1038/nbt.1883).
* H. Li, [Seqtk](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2): a fast and lightweight tool for processing FASTA or FASTQ sequences, 2013.
* Carlos P. Cantalapiedra, Ana Hernandez-Plaza, Ivica Letunic, Peer Bork, and Jaime Huerta-Cepas., eggNOG-mapper v2: functional annotation, orthology assignments, and domain prediction at the metagenomic scale. 2021, Molecular Biology and Evolution, [https://doi.org/10.1093/molbev/msab293](https://doi.org/10.1093/molbev/msab293)
* Minoru Kanehisa, Yoko Sato, Masayuki Kawashima, Miho Furumichi, Mao Tanabe, KEGG as a reference resource for gene and protein annotation, Nucleic Acids Research, 2016, [https://doi.org/10.1093/nar/gkv1070](https://doi.org/10.1093/nar/gkv1070)
* Wood, D.E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2. Genome Biol, 2019. [https://doi.org/10.1186/s13059-019-1891-0](https://doi.org/10.1186/s13059-019-1891-0)
* R Core Team (2021). R: A language and environment for statistical computing. R Foundation for Statistical Computing, Vienna, Austria. [URL](https://www.r-project.org/)


## Acknowledgments
This pipeline is made possible, public and free due to the efforts of scientists from [BCBB Bioinformatics and Computational Biosciences](https://www.niaid.nih.gov/research/bioinformatics-computational-biosciences-branch) from OCICB/OSMO/OD/NIAID/NIH and the [Nephele team](https://nephele.niaid.nih.gov/about/project-team).
# Contact Us
For feedback, questions, problems or concerns with WGSA2+, please contact us at [nephelesupport@nih.gov](mailto:nephelesupport@nih.gov), with specific mention of the WGSA2+ pipeline in subject. Thank you.
