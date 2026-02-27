
# WGSA2plus Pipeline (Updated Feb 2026)

## Introduction
The Nephele team at NIAID has implemented a command line-free Whole Metagenome Sequencing Assembly-based pipeline called WGSA2, into our cloud-based microbiome analysis platform. Initially built to process metagenomics datasets, the pipeline was recently expanded for metatranscriptomics datasets, leading to WGSA2plus (or WGSA2+). In a command-line free experience built to reduce the need for individual computational resources and expertise, WGSA2+ facilitates the processing of these shotgun datasets derived from complex single-cell microbial communities and diverse habitats, including both host-associated and environmental samples. It generates visualizations and summarized output based on functional and taxonomic annotation, as well as per sample assemblies, draft genomes and antimicrobial resistance gene identification. The pipeline can be customized with extensive host and functional databases. Overall, WGSA2+ fills a computational void in metagenomics, enhances accessibility and comprehension of the data, and paves the way for deeper exploration of the microbiome.

Note: The WGSA2+ pipeline can handle phylogenically diverse communities of single-cell microbial organisms including prokaryotes, viruses and unicellular eukaryotes (e.g. protozoa, single cell fungus, some diatoms). Currently, WGSA2+ is not optimized for identifying complex eukaryotic genes.

## Recent Updates
### Oct 2025 updates: addition of Metatranscriptomics mode
#### Since Oct 2025 our WGSA2 pipeline has been expanded to support _metatranscriptomics_ data analysis. The new expanded version WGSA2plus pipeline has an additional `Pipeline Mode` parameter, which allows users to customize the pipeline processing between different types of data:
- **Metagenomics mode (MGX)**: the default mode of the WGSA2 pipeline optimized for short read shotgun paried end metagenomic data
- **Metatranscriptomics mode (MTX)**: optimized for bulk RNAseq data processing, this mode utilizes tools specific for handling metatranscriptomics data appropriately

### Jan 2026 updates: enhanced processing, organization and tools
#### Since Jan 2026, our WGSA2plus pipeline has been extended with the following features:
- addition of **read coverage normalization** step aimed at improved assembly and processing of large and high coverage MGX and MTX samples
- **optimization of the RNA removal step** by replacement of sortMeRNA tool with ribodetector
- improved of **Antimicrobial Resistance Gene (AMRs, ARGs) finding** capacity for MGX/MTX datasets, by replacing AMRfinder tool with RGI tool
- for more advanced users, the addition of **adjustable confidence values used in annotation of host and taxonomic identification**, is implemented. 

Check out the [Workflow](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2#workflow) section for a deeper dive into these updates!



## Abbreviations and definitions used in text
* MTX: metatranscriptomics
* MGX: metagenomics
* PE: paired end
* TEDreads: reads that have been trimmed & filtered (T), error-corrected (E) and decontaminated (D)
* iTPM: designates the abundance score for each instance of a gene/transcript
* geneTPM: designates the abundance score for each unique annotation
* AMR: antimicrobial resistance
* ARG: antimicrobial resistance gene
* MAGs: metagenome-assembled genomes
* contigs: contiguous consensus sequences produced from assembly of short reads
* scaffolds: contigs oriented, arranged and connected, based on pairing information the short reads. Gaps between contigs of the same scaffold are presented with Ns. 


## Prerequisites for WGSA2+ submission
### Sequencing Data: require FASTQ files
The input sequences must be paired-end (PE), metagenomic or metatranscriptomic whole-genome shotgun reads (not merged) in **FASTQ format** (see our [FAQ on PE vs SE reads](https://nephele.niaid.nih.gov/faqs#:~:text=or%20paired%2Dend%3F-,Paired%2Dend%3A,-Paired%2Dend%20sequencing)). Due to the scaffold-based approach of the assemblies, single-end (SE) reads are not acceptable for WGSA2+ pipeline.  

### File Formats and Size Limitations
* WGSA2+ can accept only **FASTQ files** in both gzipped (`*.fastq.gz`) or unzipped format (`*.fastq`). Other sequencing formats are not currently accepted (e.g. `*.bam`, `*.fasta`, `*.bcl`, etc).  
* Due to the huge computational and time resource requirements of WGSA2+, the entire submitted **dataset size must not exceed 150GB zipped**. If your dataset exceeds this size, please split it into smaller submission batches. 
* In addition, the user must **enable the read coverage normalization** mode for a job, **if a single sample** within the dataset (combined FWD (R1) and REV (R2) files) **exceeds 8Gb zipped size**.  
* File names of the fastq files, should not contain any special characters.

### Pre-Processing of the data: require QC pipeline
**Datasets submitted to WGSA2+ must firstly be run through [Nephele's QC pipeline](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/short-read-qc)!!** The QC pipeline performs basic quality checks, trimming and filtering of the dataset, averts PE mismatch and other issues that can cause failure of WGSA2+ (and pipelines). In addition, the produced QC pipeline reports helps the user understand their dataset better in terms of read quality, read duplication rates, sample sizes, adaptor content and potential issues for each sample in datast.

### Mapping File
A mapping file containing metadata is required during import datasets in Nephele. This is a tab-delimited file linking sample names (column **SampleID**), to the sample's respective RWD and REV FASTQ files (**ForwardFastqFile** and **ReverseFastqFile**), and simple's basic metadata (a grouping column **TreatmentGroup**). In WGSA2+, the TreatmentGroup column provides information for statistics and visualization steps. The [mapping file template can be downloaded here](https://nephele.niaid.nih.gov/user-guide/demo-datasets#wgs). The mapping file can be a `.xlsx` or `.txt` file.


## User Options During Submission

### *NEW* Pipeline Mode (Elective)
WGSA2+ now allows users to switch between two pipeline modes, form processing metagenomic data (bulk DNA-based data for **Metagenomics Mode**) to metatranscriptomic (bulk RNAseq data for  **Metatranscriptomics Mode**). The pipeline switches processing tools optimized for the specific data type chosen. The default running more of the pipeline is MGX.

### Run Additional Trim and Filter (Elective)
After running QC pipeline, the WGSA2+ workflow can be used to apply additional (to its default baseline) trimming and filtering steps for the dataset. These steps ensure dataset meets the threshold quality requirements for downstream processing and assembly. The additional trimming and filtering steps include the ability to set higher thresholds for the average read quality, 5' and 3' end trimming, and/or minimum read length.

### Host Decontamination DB (Options)
Decontamination of MGX/MTX datasets is a required step for WGSA2 in order to reduce dataset size produced of to biologically uninformative sequences (e.g. host data, vector data, known uninformative simple and complex repetitive sequence data). The custom decontamination databases of choice for WGSA2 are tailored to target a specific host group or related host genomes. Please [contact our Nephele team](https://tinyl.co/4IUL), if you are unsure what is the best decontamination database to use for your dataset. Alternatively, you can start with the default host decontamination dataset (Human and Mouse DB)

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
     * Description: genomes of 14 tick species (+human) 
     * [Content information and download](https://zenodo.org/uploads/17913269)
     * [Content report](==🔴add file for link download==)

7. **Bat Decontamination DB (NEW!)**
     * Description: genomes of 9 bat species (+human)
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

### *New* Host detection confidence threshold (Optional)
The default confidence threshold for host read identification and removal by the Kraken2 tool is set to 0.05.This value can range from 0 to 1. User can now choose to increase or decrease this value based on their familiarity and expectations of their dataset. For unexperienced users, leaving this option to default is advised. 

### TAX Classification database (Options)
For taxonomic annotations of the organisms in each dataset, users can choose from the following group or habitat specific databases:


1. **[RefSeq](https://www.ncbi.nlm.nih.gov/refseq/about/)** (Reference Sequences database plus Fungi and Protozoa)
   - date of creation: Oct 2025
   - [Source](https://benlangmead.github.io/aws-indexes/k2)
   - The Reference Genomic Sequence database is comprised of ~170,400 curated reference genomes from bacterial, archaeal, viral kingdoms of life.  This database is also extended with high quality single-cell eukaryotic protozoan and fungal genomes. This database, is recommended for global overview of any microbial community. 
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

### *NEW* TAX classification confidence threshold (Optional)
The default confidence threshold for read classification to a specific known organism by the Kraken2 tool is set to 0.15. This value can range from 0 to 1. User can now choose to increase or decrease this value based on the taxonomic sensitivity vs taxonomic noise tolerance of their choice. For unexperienced users, leaving this option to default is advised, at it is optimized to reduce spurious taxonomic assignments (taxonomic noise) while still retaining taxonomic sensitivity. 

### *New* Read coverage normalization and threshold (Optional)
For datasets with known high coverage or highly duplicated reads and large sample sizes (>8Gb zipped combined PE files), this option is HIGHLY advised. Samples of this nature are excessively computationally and time demanding and can cause pipeline failure due to resource limitations. Thus, this read coverage normalization step applied immediately before assembly is advised. The normalization step produces smaller but more accurate assemblies to the cost of minor community sensitivity loss. Normalized reads are never outputted by the pipeline as they are used _only_ for assembly. Post assembly, the reads used for mapping to the assembly the cleaned un-normalized TED reads, providing the most accurate abundance scores possible for scaffolds and genes for each sample. Default read coverage threshold for MGX and MTX reads is 40. User may choose to adjust that by assessing risk of pipeline failure due to resource limitations vs assembly size and community resolution. 

### Metabolic pathways database (Options)
Post assembly, the functional capacity of a community is assessed by mapping the gene annotations from each sample against a database of known functional pathways. WGSA2+ provides the user with 2 choices of functional pathway databases:
- the KEGG DB (as of Jun 2024), which uses KO gene annotations [default], or 
- the MetaCyc DB (as of Jun 2024), which utilizes the EC annotations.   

The database of user choice depends on their familiarity with either database.

### Identify Antimicrobial Resistance Genes (ARGs) (Elective)
For users that are interested in the Antimicrobial Resistance Peptides (AMRs) within their samples, we have provided an elective option to run RGI (Resistance Gene Identifier), which uses the [CARD database](https://card.mcmaster.ca/) [as of v4.0.1] to identify homologues of known ARGs. Note: As of Jan 2026, WGSA2 no longer uses [AMRFinderPlus](https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/) for identifing ARGs

### Output Downloadable TEDread FASTQ Files (Elective)
The first steps of the pipeline are to pass each sample through trimming and filtering (T), error-correction (E), and host- and rRNA- decontamination (D) steps, producing a clean set of reads (TED reads) used for all downstream processing. Since the size of these can equate the size of the uploaded dataset, and thus if user needs them, they can choose to have them provided as a separate download post pipeline completion, by selecting the option **Downloadable TED read fastq files**. These files are a separate download, external to the main results output of the pipeline. The download link for them would be provided on the results page. 


### Produce Gene-Based or Scaffold-Based Taxonomic Profiles (Electives)
As a default setting, WGSA2+ generates taxonomic profiles based on the cleaned TEDreads for each sample (Workflow section Step 3). Through extensive testing, we have found these **readTAX-based profiles [default] are the most taxonomically accurate and sensitive (while also computationally lenient) option of the pipeline**. The readTAX-based profiles are always produced. However, in addition to those, users may choose to also explore taxonomic composition, based on assembled scaffolds and/or predicted genes for each sample, by choosing **Scaffold-based TAX annotations** or **Gene-based TAX annotations** options. While these alternative approaches may have **lower accuracy in community profiling**, they are valuable in linking scaffolds/transcripts/genes to specific organisms of interest. Note: utilization of alternative/multiple TAX profiling methods is NOT necessary for reliable taxonomic profiling of a community, and would generally corroborate with the default readTAX-based profiles. Therefore, Gene and Scaffold-based profiles are not part of the default pipeline output.

### Produce MAGs (Elective; MGX mode only)
This option enables the generation of draft genomes and their quality assessment to metagenome-assembled genomes (MAGs). It is optimized for prokaryote-rich communities. Note: this option is **highly resource and time-consuming**, resulting in increased processing and compute time usage. It is **advisable to use subsets of selected samples** when utilizing this option. Despite the reduced resolution at the community level, the MAG-based taxonomic profiles generated by this WGSA2+ option are **highly biologically accurate** and can provide detailed strain-level information of the most abundant prokaryotic organisms in the community.



****************************************************

## WGSA2+ pipeline Workflow

==🔴[insert the main workflow diagram here]==

## Steps 1 & 2: Trimming, Error-Correction and Decontamination (TED)
The WGSA2+ pipeline begins by pre-processing reads, getting them ready for assembly, and accurate taxonomic annotation. This includes 3 main steps (process acronym TED) and 2 optional steps (RN):
* **(T) trimming and filtering** of reads ([fastp](https://bit.ly/4ro9yos)). This step is not the same as [QC pipeline](https://bit.ly/3ZQnj3C) and therefore **should not be considered its substitute**. By default, this step ensures that the reads are of sufficient minimum quality, pairing and read length for assembly. User may choose to increase these thresholds and to more stringent requirements (see [Run Additional Trim and Filter user option](https://tinyl.co/4IVP) section).
* **(E) error-correction** (fastp). PE reads are compared and sequencing errors are corrected within the overlapping regions. This process is specifically designed to improve assembly accuracy, efficiency and success.
* **(D) decontamination** ([Kraken 2](https://tinyl.co/4IVS)). The dataset undergoes a thorough cleaning process to remove host DNA and non-informative elements such as homopolymeric or simple sequence repeats. This is achieved by utilizing a user-selected database containing curated collections of potential host organism genomes (see [user options **Host Decontamination DB** and **Host confidence threshold**](https://tinyl.co/4IVT)). The decontamination process is crucial for reducing the dataset size and increasing taxonomic accuracy by removing non-informative host, junk and repeat sequences. Contamination levels and identification of host organisms are reported per sample in the form of `$SampleName_contamREPORT`.

Logs with information gathered during the TED processing are stored in folder `TEDreads_mgx` (for **Metagenomic Mode**) and `TEDreads_mtx` (for **Metatranscriptomics Mode**). Additional/optional cleaning steps applied on the TEDreads: 
* **(R) rRNA removal** ([RiboDetector](https://github.com/hzi-bifo/RiboDetector)). In **MTX mode** and after the mandatory TED steps reads are additionally scanned and cleaned of rRNA reads (e.g. 16S rRNA 5.8S rRNA and more). Logs for this process are stored in `TEDreads_mtx/$SampleName_rna_aliLOG.txt` files and they contain information about number of processed sequences, number of non-rRNA (outputted) sequences and number of detected rRNA sequences. If fewer than 100 reads remain after rRNA removal, the pipeline will show a specific error and fail. If your data derives from 16S or other rRNA amplicon data, pipelines like DADA2 or QIIME are more appropriate for your samples.
* **(N) read coverage normalization** ([bbnorm as part of the bbTools suite](https://tinyl.co/4IVn)). Assembly is a highly computational resource and time demanding process that can cause pipeline failures for large samples. For datasets with samples of expected high coverage, high duplication levels (see QC report) or large sample sizes (>8Gb zipped combined PE files), normalization of the reads is HIGHLY advised. The _in silico_ read coverage normalization step applied _after_ all other pre-processing steps (above) and immediately before assembly. Normalized reads are used _only_ for assembly, producing smaller but more accurate assemblies to the cost of minor community sensitivity loss. Normalization can be applied in **both MGX and MTX modes**  Normalized reads are never outputted by the pipeline as they are used only for assembly. Post assembly, it is the TEDreads (and TEDR reads in MTX mode) are used for abundance scoring (see assembly and read mapping section), retaining the accuracy of the abundance measures. Default read coverage threshold for MGX and MTX reads is 50.

## Step 3: read-based TAX Profiling (readTAX)
By default, WGSA2+ includes the generation of **read-based taxonomic profiles based on the TED reads per sample**, utilizing the [Kraken2 tool](https://tinyl.co/4IVS).  WGSA2+ offers users the flexibility to choose the classification databases that best suit their datasets (see [user options for **TAX Classification DB** and **TAX confidence threshold**](https://tinyl.co/4IVz)). The resulting taxonomic profiles are visualized per sample using the interactive plots of [Krona](https://tinyl.co/4IW3), as well as a dataset-wide heat plot produced from the sample-consolidated community matrix table (`TAXprofiles/readsTAX_$DBname/merged_tables/merged_Counts+TAX.txt`; see Step 9). While WGSA2+ also provides basic statistics and visualizations based on this community matrix (see steps 10-11), this table serves as a foundation for customized community analysis by the user. 

## Steps 4: _de novo_ Assembly
In this step, the pipeline uses [metaSPAdes](https://pmc.ncbi.nlm.nih.gov/articles/PMC3342519/) assembler (**MGX mode**) or  [Trinity](https://www.nature.com/articles/nbt.1883) (**MTX mode**), to perform de novo assembly of the TED reads per sample. In cases when normalization of the read coverage was required/elected, the normalized TED reads are used. The final assemblies of whatever assembler chosen would be within `asmbMGX/$SampleName_asmb` or `asmbMTX/$SampleName_asmb/` folders. Trinity produces assembled transcripts in terms of contigs outputted in `$SampleName_contig.fasta`. In **Metagenomics mode** the metaSPAdes assembler can go a step further and used PE information between the assembled reads to output `$SampleNames_scaffolds.fasta`. The final assemblies form either tool become the sample's `$SampleNames_asmbFinal.fasta`. Quality metrics and other information on the properties and quality of the assembly for each sample can be found in `$SampleName_asmbStats.txt` file.

## Step 5: Read Mapping to Assembly
Next, [Bowtie2](https://bit.ly/4r2OxQH) is used to align each sample's TED reads (always non-normalized, but rRNA-clean in MTX mode) to the final assembly (a process called 'mapping'). The alignment is also QC'd and cleaned (de-replicated, mate pairs are fixed, etc) by [SAMtools](https://bit.ly/3ZiaoHC) to ensure each pair of reads is mapped to its single best location within the assembly.

## Step 6: Abundance Scoring for Assembly 
Finally, the correctly aligned reads are enumerated to production of abundance scores per contig/transcript/scaffold (sometimes called Node) in each sample. Normalized for Node length, the read depth, coverage and RPM (reads per million) and other statistics are calculated (e.g. GC content, plus/minus strand alignments). This information is collected in `$SampleName_asmbCovr.txt` file and are used for downstream abundance assessments. 

## Step 6A: Scaffold-based taxonomic profiles [Add-on]
User may elect to taxonomically annotate the assembled scaffolds (or transcripts in MTX mode) for each sample. These can be useful in identifying scaffolds that belong to organisms of interests and/or when managing MAGs (see step 12). WGSA2+ will utilize the same classification database for scaffold profiling, as elected for the read-based taxonomic profiling (main). The pipeline will bind the taxonomic annotations of each scaffold/transcript to the corresponding abundance scores to produce per-sample scaffold-based TAX profiles (dubbed **scaffTAX**). These can be found under `$SampleName_asmb/taxonomic/scaffTAX_$DBname/` along with some statistics of taxonomic annotation success. Across all samples those are also summarized in `TAXprofiles/scafTAX_$DBname/TAXplots_scafTAX_$DBname.html`. However, **scafTAX profiles are _not_ an accurate community composition metric**, so they are not part of the main output of the pipeline (see step 10). 

## Steps 7: Gene Prediction & gene abundance scoring (iTPMs)
WGSA2+ utilizes [Prodigal](https://tinyl.co/4IX4) for genetic feature predictions (genes or transcripts) in both MGX mode and in MTX mode, as both prokaryotic and single-cell eukaryotic organisms possess primarily contiguous genetic features. Output is recorded in `$SampleName_asmb/functional/genes/` folder and files are prefixed `PREDgenes` in pipeline output. 

Gene abundance scores are computed by enumerating the number of reads correctly aligned to the predicted gene coordinates of the scaffold ([VERSE tool](https://www.biorxiv.org/content/10.1101/053306v1)) (used: default settings "featureCounts", -z 0). RPM (reads per million) and TPM (transcripts per million) values are calculated and the TPM value is used as the abundance scores of each gene/transcript. Since the TPM value is calculated _per instance_ of predicted feature, the abundance value (TPM) is dubbed **iTPM (instance TPM)** for this pipeline's context. This per-instance abundance information is provided in `SampleName_asmb/functional/genes/PREDgenes_ABUNtab.txt`

## Step 8: Gene Annotation and annotation-based abundance scores (geneTPMs)
[EggNOG-mapper2](https://tinyl.co/4IX5) is used for annotation of the predicted features, using the extensive [EggNOG-v5 database](https://tinyl.co/4IX6). Functional annotations extracted from this tool's output are in terms of 1) KEGG ontology gene groups (KO), 2) Enzyme Commission number (EC) and 3) clusters of Orthologus groups (COG; extracted but unused in pipeline). Output is recorded in `$SampleName_asmb/functional/annotations` folder. Since each sample contains multiple forms and copies of any given functional group (KO or EC) (e.g. different gene copies or from different organisms), abundances are also summarized per unique functional annotation across all samples (dubbed **geneTPM** within WGSA2). This per-annotation geneTPM abundance matrix is also provided as `PWYprofiels/$DBname.MP/merged_tables/merged_geneTPMtable.txt` table.


## Step 8A: Gene-based taxonomic profiles (geneTAX) [Add-on]
By default, WGSA2+ will produce TEDread-based taxonomic profiling with Kraken2. User may elect to additionally produce taxonomic annotations for the predicted genes, within each sample. These can be useful in identifying genes belonging to specific organism or lineage of interest. WGSA2+ will utilize the same classification database for gene profiling, as elected for the read-based taxonomic profiling. The pipeline will bind the taxonomic annotations of each gene to the corresponding abundance scores for the feature, to produce per-sample gene-based TAX profiles (dubbed **geneTAX**). These can be found under `$SampleName_asmb/taxonomic/geneTAX_$DBname/` along with some statistics of taxonomic annotation success. Across all samples those are also summarized in `TAXprofiles/geneTAX_$DBname/TAXplots_geneTAX_$DBname.html`. Although these profiles would generally align with the readTAX-based profiles, currently the **geneTAX profiles are _not_ collated into a community matrix** or visualized as part of the main output of the pipeline (see steps 10 and 11). 

## Step 8B: Antimicrobial Resistance Gene Identification (ARG ID) [Add-on]
User may elect to scan the predicted genes for antimicrobial resistance (AMR) functionality. This the pipeline does using [RGI tool and the accompanying CARD database](https://card.mcmaster.ca/). The outputs would be stored in each sample's `$SampName_asmb/functional/RGI/` folder. Abundances for each ARG are extracted from the iTPM value of each ARG gene.

## Step 9: Pathway Inference
Based on the user's chosen option for functional database (KEGG or MetaCyc (dubbed mmcc)), the corresponding functional annotation (KO or EC) is used to predict functional profiles (KOs are mapped to KEGG and ECs are mapped to MetaCyc). This mapping is accomplished by parsimony approach for reconstructing the minimal set of pathways described by a query of genes (tool used is  [MinPath](hthttps://tinyl.co/4ImJ)). The abundance of each pathway is then calculated by averaging the iTPM values of each gene instance within the inferred pathway. To achieve this, the script [genes.to.kronaTable.py](https://tinyl.co/4ImK) is employed. The resulting functional profiles, representing metabolic pathway profiles, are summarized for each sample in `PWYprofiles/${DBname}PWYs.MP/PWYplots_${map}.html`.

## Steps 10: Dataset Collations & Abundance Matrix Summaries (Conditional of n >2)
These steps **produce the main pipeline outputs of WGSA2plus: the TAX and PWY dataset-wide community matrices**. Production of these is **conditional to datasets containing multiple samples** (n >2). For each profile type (**TAX**, GENE, RGI or **PWY**) of each sample, the profiles (identity and abundance of each feature) are collated into 1 common abundance matrix (per profile type) representing each unique feature's identity and abundance for each sample. These main outputs can be used by user for custom statistical community analysis.Produced main outputs of this step and for the the pipeline are stored in the following paths/files:
* `TAX profiles/readsTAX_$DBname/merged_tables/merged_Counts+TAX.txt` (** **main output** **)
* `PWYprofiles/$pwyDBname.MP/merged_tables/merged_Counts+PWY.txt` (** **main output** **)
* `PWYprofiles/$pwyDBname.MP/merged_tables/merged_geneTPMtable.txt`
* `PWYprofiles/$pwyDBname.MP/merged_tables/merged_argsTPMtable.txt` (if step 8B elected)

Within the above output paths, other versions and formats of the same main output matrixes are also provided. For example, the read-based TAX and PWY profile matrices (main outputs) are further formatted into `.biom` files that include the submitted metadata. These files can be conveniently uploaded into external pipelines such as [MicrobiomeDB](https://microbiomedb.org/mbio/app) or used for other user-specific purposes. Thus, it is a good rule of thumb to add more metadata columns in the mapping file upon submission to the pipeline, which can be outputted in the produced biom files. 

## Step 11: Community Visualizations and Summaries (Conditional of n >3)
Basic community composition visualizations (e.g. alpha and beta diversity plots, abundance profile heatmaps etc.) are produced based on the main community outputs (TAX and PWY abundance matrices) of the pipeline. Those plots can be found in `TAX profiles/readsTAX_$DBname/DivPlots/` and `PWYprofiles/$pwyDBname.MP/DivPlots/`

## Step 12: Creation and Evaluation of MAGs [Add-on] (Conditional of MGX mode)
Users have the option to select the MAGs creation (metagenome-assembled genomes or draft genomes) as an extra feature in WGSA2plus. **This feature is only availbale in MGX mode** and it aims to reconstruct the genomes of the most abundant organisms within each community/sample.  MAGs can be used for various research explorations. The pipeline employs [MetaBat2](https://pmc.ncbi.nlm.nih.gov/articles/PMC6662567/) to bin scaffolds with sufficient length (>1500bp) and other features (e.g. connectivity, GC content and read coverage) into draft genomes. Quality assessments of these draft genomes is then performed by [CheckM](https://pubmed.ncbi.nlm.nih.gov/25977477/). The assessment includes taxonomic affiliation, genome size, abundance estimations, completeness, contamination levels, number of genes, and more. The most complete and pure (contamination-free) draft genomes are considered higher quality MAGs (metagenome-assembled genomes), although **the pipeline will output all produced draft genomes** (even low qualty ones). The MAG-based taxonomic profiles are visualized per sample (KronaTools)[https://github.com/marbl/Krona/wiki] and outputted per sample in `$SampleName_asmb/fatxonomic/MAGs/magsQA/` and globally in `TAXprofiles/magsTAX_checkM/`. While MAG-based profiles align closely with TEDread-based profiles (see [WGSA2 benchmarking section](https://nephele.niaid.nih.gov/user-guide/pipeline-descriptions/wgsa2#profiling)), they are be biased towards most abundant and/or smaller genomes and restrict the utility of the pipeline. Thus, **MAG-based profiles are _not_ part of the main output of WGSA2**.

Considerations for using this add-on:
* **Only availbale in MGX mode**
* **Primarily useful for prokaryotic communities**. Eukaryotic draft genomes are not reliably produced, can act as contaminants and are not successfully annotated. 
* **Biased towards most abundant and smaller genomes**
* **Adds major resource and compute time demands to WGSA2+ job**. Thus, this feature is useful only for few samples of interest, that have been pre-explored by the user. 

****************************************************


## Pipeline Output Details
Please refer to ==🔴[fix [this file to OutputDetails_WGSA2plus_Feb2026.pdf]]== for the complete and detailed list of the pipeline output and details. File will also be part of the main output downloaded from the pipeline. Here, we detail only the outputs of the main result aggregate folders.

### Dataset-wide (Main) Results

#### `TAXprofiles` folder

**Contains dataset-wide taxonomic results**

Although listed first here, this folder is one of the last produced by the pipeline as it contains the dataset-wide taxonomic results (visualizations, summaries and community matrices) produced from each processed sample. Exact contents of this folder will depend on the tax-classification options selected for the pipeline (e.g. read, gene, scaffold, MAG taxonomy), and the database options ($DBname). For convenience files and folders that are the main outputs of interest to researchers, will be highlighted in this text. 

- `readsTAX_$DBname` folder (default): Contains logs and reports from the default taxonomic classification of the pipeline, based on the TED reads ([see TEDreads section below](#tedreadstedreads_mtx-folder)). Sub-folders:
  - bin/ folder: these are the text versions of the per-sample taxonomic reports from the TED reads, used for taxonomic profile visualization presented in the `TAXplots_ReadsTAX_$DBname.html` reportr.
  - bioms/ folder: The files from the `bin` folder presented in a _BIOM V1 (JSON)_ format. These can be manually uploaded to MicrobiomeDB or any other analytical platform, if needed.
  - reports/ folder: contains taxonomic classifications reports produced by Kraken2 for each sample.
  - `TAXplots_readsTAX_$DBname.html` file: interactive Krona chart of the TED read-based taxonomic profiles, collected in the `bin` folder.
  - `merged_tables/` folder (**conditional for dataset with ≥ 2 samples**): a folder containing the collated taxonomic abundance matrix from the entire dataset. 
    - The  full matrix is represented in 2 files - tab-delimited text file (`merged_Counts+TAX.txt`) and 2 lineage based files(`merged_Counts+Lineage{.txt,.biom}`. The .biom file is JSON format and is the source file for the `for_analyze_with_microbiomedb.biom` file in the primary folder). RData and log files are outputted from R for troubleshooting.   
  - `DivPlots/` folder (**conditional for dataset with ≥ 2 samples**): Diversity plots and basic exploratory statistics for the dataset, summarizing and providing basic visualization for the data from the merged_tables/ folder. Provided are alpha diversity tab-delimited text file alongside a boxplot (`TAX_AlphaDiv.txt` and `TAX_AlphaDiv.pdf`), beta diversity PCoA and nMDS ordination plots (`TAX_BetaDiv_nMDS.pdf` & `TAX_BetaDiv_PCoA.pdf`), taxonomic profile heatmaps of most abundant taxa (`TAX_Profile_Heatmap.pdf`) as well as other basic community measures. Please note that some exploratory statistics and visualizations require ≥ 3 samples in dataset to produce. 
- `geneTAX_$DBname/` folder: **(based on user selections)**: a visual summary of the gene-based taxonomic annotations for each sample. Each folder would contain a bin/ with text versions of the per-sample profiles and a `TAXplots_<gene>TAX.html` interactive krona plot summary file of the assembled-feature-based taxonomic profiles. (Note **Some database do not produce visual summaries for genes**)
- `magsTAX_checkM/` folder **(conditional and optional)**: Generated only if "MAGs & MAG TAX annotations" is selected, and is **Metagenomics Mode** *ONLY*. It contains the TAX classification and abundances of the MAGs produced by CheckM. It also contains a bin/ folder with text versions of the MAG-based taxonomic profiles and visualizations by KronaTools (`TAXplots_MAGx.html`) as well as a `MAG-based_Counts+TAX.biom` biom file summarizing the MAG-based taxonomic profiles of all samples.
- scaffTAX_$DBname/ folder: the scaffold-based taxonomic annotations option will not produce dataset-wide visualizations. Annotations are reported only within each sample's assembly folder.

#### `PWYprofiles` folder

**Contains dataset-wide functional results**

Contains the dataset-wide functional analysis results from the pipeline, including pathway inferred profiles (PWY) and gene-based profiles. This folder contains `keggPWYs.MP/` folder **or** `mtccPWYs.MP/` folder (default vs alternative user choice of **metabolic pathway database**). Either folder will have the same structure:

- `PWYplots_$mapping.html`: an interactive krona html report with the functional profiles for each sample (KronaTools), based on inferred PWYs. Gene mapping is either designated `ko2gg` (KO annotations to KEGG pathways) or `ec2mc` (EC annotations to metaCyc pathways) and is part of the file name.
- pwybin/ folder: per-sample text reports of the PWYs identity & abundances files, used to create the html report & biom files.
- bioms/ folder: the json biom versions of the `pwybin` files.
- genebin/ folder: per-sample text reports of identity and abundances of each unique gene found in the sample.
- `merged_tables/` folder (**conditional for datasets with ≥ 2 samples**): a folder containing the collated pathway annotations and abundance matrix from the entire dataset. The file content is analogous to the taxonomic one.
  - the  full matrix is represented in 2 files - tab-delimited text file (`merged_Counts+PWY.txt`) and 2 lineage based files (`merged_Counts+allTiers{.txt,.biom}`. RData and log files are outputted from R for troubleshooting. 
  - If AMR gene prediction was elected, this folder will also contain a `merged_argsTPMtable.txt` with collated information from all samples about the presence and abundance of AMR genes identified in each sample. 
- `DivPlots/` (**conditional on ≥ 2 samples**): exploratory plots of PWY functional dataset-wide profiles. Visualizations include a community PCoA and nMDS functional composition ordination plots (`PWY_BetaDiv_nMDS.pdf` & `PWY_BetaDiv_PCoA.pdf`; (≥3 samples)) produced from the inferred PWY matrix in `merged_tables/` as well as a pathway abundance heatmap plot (`PWY_Profile_Heatmap.pdf` (≥2 samples)).



## External results
### `TEDreads_fqs` folder (optional and external)
**Contains the trimmed, filtered, error-corrected, host-decontaminated (TED), rna-cleaned fastq files**

Due to the size of these TED files, they are omitted from the main output of the pipeline. User needs to elect **Output TEDread FASTQ files** to produce the `TEDreads_fqs/` folder containing those files, available as a separate download. If chosen to download, we recommend storing this folder within their original home, the `TEDreads_$mode/` folder. Note: the normalized reads are _not_ contained in the TEDreads_fqs/ folder, as they were used only for assembly.

### `asmb_files` folder
**Contains the per-sample final assembly files (`.fasta` and `.bam` bam index and depth files) needed for external processing**

For easy access to main assembly files from each sample, the pipeline moves the `fasta` and `bam` files from each assembly into the `asmb_files/` folder. These can then easily accessed when submitting to external pipelines such as Nephele's DiscoVir or for custom downstream processing. The `$SampleName_asmbFinal.{fasta,bam,bam.bai,depths.txt}` files are linked to their original location in the per-sample assembly folders (at `{asmbMGX/asmbMTX}/$SampleName_asmb/` [see below for details](#asmbmetaspadesasmbtrinity-folder))




************************************



## Accuracy of WGSA2+ Profiling

We assessed the accuracy and strategies of WGSA2+ taxonomic assignments by evaluating results against known microbial communities from the [2nd CAMI Toy Human Microbiome Project Dataset](https://cami-challenge.org/) ([Sczyrba et al. 2017](https://pubmed.ncbi.nlm.nih.gov/28967888/)). The plots bellow represent results from the comparison of the taxonomic and functional profiles of 3 CAMI samples (S1-GI, S6-Oral & S28-Skin) against each other, as produced by the various strategies of WGSA2+, bioBakery or as expected by sample design. To produce these comparisons, the community abundance matrices from each pipeline and strategy were merged based on TAXid, rarified to same readDepths (sample with lowest read depth) and ASVs filtered at relative abundance >0.5%.

##### Taxonomic assessments 
We chose tool Kraken2 as our main taxonomic classifier because it relies on a comprehensive database of k-mers derived from entire genomes, enabling taxonomy assignment for both coding and non-coding reads. This allowed a taxonomic sensitivity to diverse genomic sequences along with a computational efficiency preferable to alternative tools. The heatmap of the profile compositions bellow also demonstrated an imporoved taxonomic and abundance accuracy at read level (readTAX) compared to gene or scaffold levels.

##### Assembelers 
In literature and extensive testing MetaSpades showed improved assembly metrics  (greater number of longer contigs), scaffolding capacity and assembly quality metrics (greater number assigned reads and identified), than other metagenomic data assembler tools. Thus it was chosen as the tool for metagenomics mode. 
For metatranscriptomics data, Trinity showed the preferable assembly statistics (greater number of longer transcripts) and quality metrics (e.g. increased number of identified genes) compared to metaSPAdes and rnaSPAdes, so was chosen as the prefered assember for this mode.

##### Normalization
Our tests indicate that assemblies produced from normalized reads substaintially reduce computational and resource demands of the pipeline. Despite producing smaller assemblies and less genes and pathways, the quality scores of the assemblies (e.g. number of aligning reads to features, ambiguous or miss-paired reads, taxonomic recognition, etc) were comparable and in cases improvements to the non-normalized tests.

##### Gene prediction
Prodigal was the gene identifier of choice for both **Metagenomics and Metatranscriptomics modes** as it showed not only suitable for predicting contiguous genetic features (characteristic for prokaryotes and simple single-cell eukaryotes), but also performed comparably to transcriptomics-specific tools for prokaryotic samples during our extensive testing.

##### Diverstiy
The Alpha Diversity box plots represent the average Shannon diversity and produced Species Richness from the 3 samples. This plot best presents the overall accuracy of the strategies used by WGSA2+ TAX assignments. To produce these plots, the community abundance matrices from each strategy were merged based on TAXid, rarified to lowest available read depth and filtered to relative abundance of 0.5%.

1 A heatmap of the top 35 species from 3 CAMI sample profiles, produced by the WGSA2+ TED-read-based TAX profiles (Kraken2 at confidence level 0.05), the bioBakery pipeline (MetaPhlAn3), and as Expected by sample design):## ![](wgsa2_heatmap-DdXeU_H3.png)

2 Alpha Diversity box plots, represent the average Species Richness, Chao1, Shannon & InvSimpson Diversity across 3 CAMI samples. The plot demonstrates the overall expected accuracy of the strategies used by WGSA2+ for TAX assignments and compares them to the expected profiles and the bioBakery produced TAX profiles:## ![](wgsa2_AlphaDivAll-775sh3cR.png)

3 Beta Diversity PCoA ordination plot based on Bray-Curtis dissimilarity matrix, produced from 3 CAMI samples from WGSA2+ TAX profiles based on different strategies (read, gene & scaffold-based TAX profiles), bioBakery produced profiles and as expected by design:## ![](wgsa2_BetaDivAll-DAXc9-YX.png)
4 A table for number of predicted EC annotations and unique pathways, produced from WGSA2+ vs bioBakery:## ![](wgsa2_PWYcomparisonsTAB-95G4Do8c.png)

⠀If you wish to test the WGSA2+ pipeline, you can find and download a small example dataset (3 CAMI samples, subset to read depth of 1 million reads) and corresponding mapping file specific for the WGSA2+ pipeline, from Nephele's [Demo Datasets](https://nephele.niaid.nih.gov/user-guide/demo-datasets#wgs) page.


## Feedback
The Nephele team is working hard to improve and extend this pipeline to provide users with a better experience and more analyses. Please kindly provide us with feedback and keep an eye on Nephele updates.



## Software, Scripts, Tools Utilized by the Pipeline
Tool versions used by the pipeline are recorded in the log file.
* [fastp](https://github.com/OpenGene/fastp)  
* [kraken2](https://github.com/DerrickWood/kraken2)  
* [spades](https://pmc.ncbi.nlm.nih.gov/articles/PMC3342519/)  
* [bowtie2](https://bowtie-bio.sourceforge.net/bowtie2/index.shtml)  
* [bbtools](https://jgi.doe.gov/data-and-tools/software-tools/bbtools/)  
* [samtools](https://www.htslib.org/)  
* [MetaBAT2](https://bitbucket.org/berkeleylab/metabat/src/master/)  
* [Prodigal](https://github.com/hyattpd/Prodigal)  
* [eggNOG-mapper2](https://github.com/eggnogdb/eggnog-mapper)  
* [verse](https://kim.bio.upenn.edu/software/verse.shtml)  
* [RGI and CARD database](https://card.mcmaster.ca/)  
* [KronaTools](https://github.com/marbl/Krona/wiki)  
* [MinPath](https://github.com/mgtools/MinPath)  
* [R statistical computing](https://www.r-project.org/)  
* [kreport2krona.py](https://github.com/jenniferlu717/KrakenTools)  
* [CheckM](https://ecogenomics.github.io/CheckM/)  
* [biom-format](https://biom-format.org/)  
* [RiboDetector](https://github.com/hzi-bifo/RiboDetector)
* [Trinity](https://github.com/trinityrnaseq/trinityrnaseq/wiki)  


## References
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
