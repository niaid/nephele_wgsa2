## Pipeline output details (version 0.1.9)

### Global Files

- `WGSA2plus_output_details.pdf`: Here, we detail the various pipeline outputs produced by WGSA2+.
- `logfile.txt`: A file log from the pipeline. If the pipeline halts in error, this is where the information will be logged for tracing the error.
- `for_analyze_with_microbiomedb.biom`: TAX community abundance matrix of the dataset, which can be [uploaded to MicrobiomeDB](https://nephele.niaid.nih.gov/user-guide/tutorials#microbiomeDb).
- `mapping_file.txt`: a copy of the mapping file submitted with the pipeline.


### Aggregated (Main) Results

#### TAXprofiles folder

**Contains dataset-wide taxonomic results**

Although listed first here, this folder is one of the last produced from the pipeline as it contains the dataset-wide taxonomic results (visualizations, summaries and community matrices) produced from each processed sample. 

Complete contents of this folder will depend on the options elected for the pipeline.

- `ReadsTAX_<DBname>` folder (default): Contains logs and reports from the taxonomic classification of TED reads [Step 3](#step-3). Sub-folders:
  - `bin` folder: files used by Krona for creating the `TAXplots` html chart. These are the text versions of the per-sample taxonomic reports from the TED reads, and they are visualized in the `TAXplots_ReadsTAX_<DBname>.html` report.
  - `bioms` folder: The files from the `bin` folder presented in a _json biom_ format. These can be manually uploaded to MicrobiomeDB or any other analytical platform, if needed.
  - `reports` folder: contains Kraken2 report files of the taxonomic classifications produced for each sample.
  - `TAXplots_ReadsTAX_<DBname>.html` file: interactive Krona chart of the TED read-based taxonomic profiles, collected in the `bin` folder.
  - `merged_tables` folder (**conditional of ≥ 2 samples**): a folder containing the collated taxonomic abundance matrix from the entire dataset. Creation of this folder is not performed for datasets with less than 2 samples. The TAX abundance matrix is reported in 6 tab-delimited text files and 1 biom file. The files are named based on content and format of certain profile information. **TAX-labels** designate files that contain the taxonomy in separate columns per rank, the **Lineage-labels** designate files representing the lineage of each taxonomy (all tax ranks) in 1 column (ranks separated by ';' within the column). **Counts-label** indicates files representing the abundance counts of each taxonomy for each sample (collated across dataset). The **biom file** represents counts for each sample and lineage column. This is the source file for the `for_analyze_with_microbiomedb.biom` file in the primary folder.
	- `DivPlots` folder (**conditional of ≥ 2 samples**): Diversity plots and exploratory statistics for the dataset (**note new location** is within `ReadsTAX` folder as it summarizes the data from the ReadTAX profiles). The plots include alpha diversity indices table and boxplot (`TAX_AlphaDiv.txt` and `TAX_AlphaDiv.pdf`), beta diversity PCoA and nMDS ordination plots (`TAX_BetaDiv_nMDS.pdf` & `TAX_BetaDiv_PCoA.pdf`, require ≥ 3 samples), TAX content heatmap (`TAX_Profile_Heatmap.pdf`), Rankabundance (`TAX_RankAbundanceCurve.pdf`) and Rarefaction Curves (`TAX_RareficationCurve.pdf`). In some cases (e.g. ordination plots), some exploratory statistics will fail due to the content of the dataset.

- `geneTAX_<DBname>` & `scaffTAX_<DBname>` folders **(based on user-elections)**: Conditional on the choice of classification DB, visual summary of the gene-based taxonomic annotaitons for each sample, are presented here. Note **MGBCdb does not produce visual summaries**. This folder contains a `bin` folder with text versions of the profiles from each sample and a `TAXplots_genetax.html` interactive krona plot summary file of the gene-based taxonomic profiles from each sample.
- `MAGs_TAX` folder **(based on user-elections)**: This folder is generated only if MAGs creation and taxonomic profiling is enabled, and is not an option in *Metatranscriptomics Mode*. It contains the TAX classification and abundances of the MAGs. It also contains a `bin` folder with text versions of the MAG-based taxonomic profiles and visualizations by KronaTools (`TAXplots_MAGx.html`). It will also contain a `MAG-based_Counts+TAX.biom` biom file summarizing the MAG-based taxonomic profiles of all samples.

Note: scaffold-based taxonomic annotations option will not produce visualizations, but annotations are reported within each sample's assembly folder.

### PWYprofiles folder

**Contains dataset-wide functional results**

Contains the dataset-wide functional analysis results from the pipeline, including pathway inferred profiles (PWY) and gene-based profiles. The folder will contain one folder, named based on the **metabolic pathway database** chosen at submission: `keggPWYs.MP` (default choice) or `metacycPWYs.MP` (alternative choice) folder. Either folder will have the same structure

- `PWYplots_[ko2gg or ec2cc].html`: an interactive krona html report with the functional profiles for each sample (KronaTools), based on inferred PWYs.
- `pwybin` folder: per-sample text reports of the PWYs identity & abundances files. The files are used to create the html report & biom files.
- `bioms` folder: the json biom versions of the `pwybin` files.
- `genebin` folder: per-sample text reports of identity and abundances of each unique gene found in the sample.
- `merged_tables` folder (**conditional of ≥ 2 samples**): Dataset-wide PWY abundance matrix tables representing the collated results based on each sample's functional annotation and abundance scoring. The PWY abundance matrix is represented in 6 tab-delimited text files and 1 biom file. The files are named based on content and format of certain profile information: **PWY-labels** designate files that contain the pathway information as separate columns per tiers, the **allTiers-labels** designate files representing the Tiers of each pathway in one ';'-delimited column. **Counts-label** indicates files representing the abundance counts of each pathway for each sample (collaged across dataset). The `biom file` represents counts for each sample and tiers column. The folder also contains a gene-based abundance matrix (`merged_geneTPMtable.txt`) produced from the collated gene abundance information in the `genebin` folder.
- `DivPlotsMP` (**conditional of ≥ 2 samples**): Simple exploratory plots of PWY functional dataset-wide profiles. Visualizations include a community PCoA and nMDS functional composition ordination plots (`PWY_BetaDiv_nMDS.pdf` & `PWY_BetaDiv_PCoA.pdf`; (>=3 samples)) produced from the inferred PWY matrix in `merged_tables.MP` as well as a pathway abundance heatmap plot (`PWY_Profile_Heatmap.pdf` (>=2 samples)).

### `asmb_files` folder

**Contains the per-sample final assembly `fasta` and `bam` files

for convenient uploads in downstream processing pipelines such as Nephele's DiscoVir pipeline.

At the end of WGSA2+ processing, the pipeline will copy the `fasta` and `bam` files from each assembly into the `asmb_files/` folder. This is done to conveniently use these results in downstream pipelines like Nephele's DiscoVir pipeline. The `{sampName}_assembly.{fasta,bam}` files are also linked to their original locations in each sample's assembly folder (`{asmbMetaSpades OR asmbTrinity}/{sampName}_asmb/`)

## Detailed Results

**Contains per-sample results & analyses**

### `TEDreads`/`TEDreads_mtx` folder

Output of Steps 1 & 2. These log files track the stats of samples through the trimming, filtering (T), error correction (E) and decontamination (D) Steps (TED Steps). When using **Metatranscriptomics Mode**, this folder will be called `TEDreads_mtx` and contain additional logs from sortMeRNA. If you chose the **Output TEDread FASTQ files** user option, we recommend downloading & storing the TEDreads to this folder. For each sample you will see the following files:

- `<SampName>_fastplog.[html,txt]`: log file with filtering, trimming and error-correction stats, in HTML and TXT format
- `<SampName>_kr2_decontam[REPORT,LOG].txt`: files reporting abundance and classification details of the host reads removed from the dataset.
- `<SampName>_sortmerna.log` (if **Metatranscriptomics Mode** elected): standard error log file provided by SortMeRNA, which may help in debugging.
- `<SampName>_sortmerna_aligned.log` (if **Metatranscriptomics Mode** elected): this log file is produced at the end of SortMeRNA and provides additional information about the command and parameters used. It also describes the number and proportion of reads that were identified as rRNA under the "Results" section (see "Total reads passing E-value threshold"). Samples having fewer than 100 reads after SortMeRNA are considered not suitable for proceeding in the assembly pipeline.


### `asmbMetaSpades`/`asmbTrinity` folder

**Contain per-sample assembly-related results**

Although discussed last in this text, this folder is the dataset's most detailed per-sample results. For metagenomics datasets, this will be `asmbMetaSpades`, while in **Metatranscriptomics Mode**, you will find `asmbTrinity`. Each sample with sufficient reads for assembly will have its own sub-folder here (`<SampleName>_asmb`), the content of which will be consistent across samples, but will depend on the **user options** elected (e.g. _Run AMRFinder_, _Produce MAGs_, etc). The aggregated results of the pipeline (see above) will be produced from select files and information from here (for each sample).

Organized into sub-folders based on the chronological order of the workflow steps, the `asmbMetaSpades` or `asmbTrinity` folder contains the following:

#### Assembly-related Files

##### within `<SampName>_asmb` folder

  - `contigs.FASTA` & `{sampName}_assembly.FASTA`: FASTA files of the produced assembly from sample. The assembly represented in independent contigs (contiguous consensus sequences) are stored in `contigs.FASTA`, while the scaffolded assembly (the same contigs, oriented, arranged and connected with gaps (Ns in the sequence), based on PE information from the TED reads) are in `{sampName}_assembly.FASTA`.  It is the scaffold assembly that is used for all subsequent assembly-based analyses.
  - For **Metatranscriptomics Mode**, we provide only `{sampName}_assembly.FASTA`, which represents the assembled transcripts from Trinity. This file is used for all subsequent assembly-based analyses in this mode, when selected.
  - `{sampName}_assembly_scaffCoverage.txt` file: per-scaffold stats and abundance scores such as average read count, % scaffold covered by reads, number covered bases, GC content, etc. The file also contains RPM abundance values (reads per million) for each scaffold (it is this value that is used to assess taxonomic abundance in the elective scaffold-based taxonomic profiles). As noted above, in **Metatranscriptomics Mode**, these statistics will relate to assembled transcripts and not scaffolds, but are otherwise consistent.
  - `{sampName}_assembly_stats.txt` file: assembly-wide stats such as size of assembly, N50 and L50 stats, number of scaffolds created, etc. File also contains TEDread mapping stats and alignment de-replication stats. As noted above, in **Metatranscriptomics Mode**, these statistics will relate to assembled transcripts and not scaffolds.
  - `{sampName}_assembly.bam` & `.bam.bai`: assembly alignment and index of alignment files (.bam file is big)
  - `spades.log` or `{SampName}_trinity.log`: log file of the assembly software SPAdes, or Trinity in **Metatranscriptomics Mode**.
  - `scaffTAX_<DBname>` folder **(user-elective)**: This folder contains the taxonomic assignments of each scaffold (if elected) within the sample, the raw Kraken2 report, the produced human- & Krona-readable `<SampName>_4krona` file, and a taxonomy-supplemented scaffold coverage file `{sampName}_assembly_scaffCovr+tax.txt`. _Note_: The database used for taxonomic classification of the scaffolds is the same as the one elected for main taxonomic classification of WGSA2+ (TED read TAX classification). In **Metatranscriptomics Mode**, this folder will have the same name and contents, but will be performed on assembled transcripts instead of scaffolds.

Note: To save on output size, the `{sampName}_assembly.fasta` & `{sampName}_assembly.bam` files within this folder are aliases to the files in the `asmb_files/` folder.

#### Gene-related Files 

##### within `<SampName>_asmb/genes` folder

This folder contains files with information about predicted features (likely genes) within each assembly. These files have the prefix `PREDgenes`:

  - `PREDgenes.{faa, fna, gff, gtf}` text files: contain information about the predicted features/genes from the sample, described as amino acid sequences (.faa), nucleotide sequences (.fna), or scaffold names and coordinates (.gff & .gtf) files.
  - `PREDgenes_ABUNtab.txt` text file: **provides feature abundance values** with information about feature length, coverage and estimated abundances in RPK (reads per kilobases) and TPM (transcripts per million) score for each feature (instance of gene; iTPM). This value is the same for both Metagenomics and Metatranscriptomics.
  - `PREDgenes_stats.txt`: overall stats of predicted features including information about annotation yields, etc.
  - `genesTAX_<DBname>` folder **(user-elective)**: Taxonomic association of each predicted feature (gene) within the sample. If elected, the Kraken2 report is provided (`taxREPORT.txt`), along with produced human- & Krona-readable `<sampName>_4krona.txt` file (used to produce Krona charts in `TAXprofiles/geneTAX` folder). Additionally, the PREDgenes_ABUNtab.txt file is re-provided and amended with gene-based taxonomic affiliation (`PREDgenes_ABUNtab+tax.txt` file).
  - `AMRs` folder **(user-elective)**: A folder containing results from the AMR-finding algorithm, if elected during submission. Files `AMRs{.faa & _info.txt}` contain the amino-acid sequences and characterizing information (element name, symbol, type, coverage and other stats) for each predicted AMR. 

_Note_: The `$SampName_asmb/genes/PREDgenes.faa` file can be manually provided to the [GhostKoala online annotation & pathway mapping tool](https://www.kegg.jp/ghostkoala/) for sample-specific metabolic and taxonomic annotation outside of the WMSA pipeline.

#### annotation-related files 
##### within `<SampName>_asmb/genes/annotations`
    
Folder containing information about successfully annotated features - features recognized as homologues of known genes.

 - `annots.emapper.{annotations, hits, seed_orthologs}.txt` files: raw outputs of EggNOG-mapper2, from which various annotation types are extracted for analysis. These files also provide detailed (too much) and interweaved information about each annotated gene.
 - `annots.{ko, ec, KEGGmap, COG}.txt` files: extracted annotations for each annotation type (KO, EC, KEGGmap and COG annotation respectively) from the e-mapper raw output files.
 - `annots.{ko,ec}.{fna,faa}` files: conveniently extracted NT and AA sequences from the annotated genes
 - `ANNOTgenes_ABUNDtab.{ko,ec}.txt`: a subset of the `PREDgenes_ABUNtab.txt` text file from `$SampName_asmb/genes`, containing only the predicted features with successfully assigned KO or EC annotations (_Note_: the provided gene information (length, cov, RPK and iTPM) is again, per instance of the gene in the sample => multiple features with the same annotation exist). 
 - `geneTPMtab.{ko,ec}.txt`: files summarizing **gene abundances for each unique gene** with KO or EC annotation types. _Note_: It is this file that is collected from each sample in the `PWYprofiles/<DBname>PWY.MP/genebin` folder, and used to produce the gene-based community matrix in the `PWYprofiles/<DBname>PWY.MP/merged_tables` folder.


#### pathway-related information 
##### within `<SampName>_asmb/genes/pathways`

This folder contains inferred pathways information (from MinPATH) based on the predicted genes (`annots.{ko,ec}.txt`) and calculated abundance scores (iTPM values from `ANNOTgenes_ABUNDtab.{ko,ec}.txt` file) for each sample. Depending on the user-elected `<DBname>`, the file names will have `<prefix>` of `ko2gg` (for KO annotations mapped to KEGGdb) or `ec2mc` (for EC annotations mapped to MetaCycDB).

 - `<prefix>.{report,details,log}.txt` files: raw output from MinPath pathway prediction tool. See: [How to read MinPath output](https://omics.informatics.indiana.edu/MinPath/output-readme.txt) and the [MinPATH publication](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000465) for more information about how to read files.
 - `<prefix>_4krona.txt` file: Information from the `report` file is used to create this file, describing each complete pathway and corresponding calculated abundance score (from iTPM values). The `_4krona.txt` file from each assembled sample is copied in `PWYprofiles/<DBname>PWYs.MP/pwybin` and is used to produce functional profile plots and matrices in the `PWYprofiles/<DBname>PWYs.MP/` folder.
 - `missing_pathways.txt`: a raw output from the MinPATH tool, which would provide information about expected but missing pathways (in most cases, this file will be empty). 


#### MAGs-related information 
##### within `$SampName_asmb/MAGs` optional folder

This folder contains output from metagenome assembled genomes (MAGs) if the **MAGs and MAG TAX Annotations** option was elected at submission. It contains binned scaffolds forming draft genomes and their quality assessments. The number of files will vary based on the community composition, organismal abundance and sequence representation. This folder will not be available in **Metatranscriptomics Mode** as it is a disabled option.

  - MAGs FASTA files (draft genomes):

    - `mag.{count}.fa`: FASTA file containing scaffolds assumed to be representing the same organism or lineage
    - `mag.{lowDepth, tooShort, unbinned}.fa`: FASTA files containing scaffolds that do not meet the binning tool's (MetaBat2) criteria for binning (see [Metabat2 publication](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6662567/)). These files are also likely to contain scaffolds affiliated with unicellular eukaryotic organisms (if such are present in the sample).

  - `magsQA` folder: Output of CheckM's bin quality assessment tool. In this folder are: `bins/`, `QCplots/`, `storage/` folders as well as `checkm.log` and `lineage.ms` files. More information can be found on [CheckM's website](https://github.com/Ecogenomics/CheckM/wiki). Of note are:

    - `magsQA/bins/`: AA and NT sequences for the predicted genes from that bin, along with gene coordinates, annotations (.gff) and other files
    - `magsQA/QCplots`: plots describing QC stats for each bin; [more info here](https://github.com/Ecogenomics/CheckM/wiki#plots).

    The WGSA2+ pipeline extracts the more descriptive information from CheckM's output to create the following reports:
    
    - `mags_SUMMARY.txt`: taxonomic, abundance, coverage and other information and stats about each MAG. This file is also used to create the MAGs-based TAX profiles reported in `TAXprofiles/MAGs_TAX` folder.
    - `mags_coverage.txt`: per scaffold coverage and read mapping stats for each MAG
    - `mags_profiles.txt`: coverage & abundance assessment stats for each MAG; [more info here](https://github.com/Ecogenomics/CheckM/wiki/Utility-Commands#profile)
    - `mags_qa.txt`: quality assessment stats for each MAG
    - `mags_tax.txt`: more detailed taxonomic information about each MAG


## Contact Us

For feedback, questions, problems or concerns with WGSA2+, please contact us at [nephelesupport@nih.gov](mailto:nephelesupport@nih.gov), with specific mention of the WGSA2+ pipeline in the subject line. Thank you!

