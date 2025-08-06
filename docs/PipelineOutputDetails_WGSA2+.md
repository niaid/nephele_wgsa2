

## Pipeline output details

- `WGSA2plus_output_details.pdf`: contains these pipeline output details.
- `logfile.txt`: A file log from the pipeline. If the pipeline halts in error, this is where the information will be logged for tracing the error.
- `for_analyze_with_microbiomedb.biom`: TAX community abundance matrix of the dataset, which can be [uploaded to MicrobiomeDB](https://nephele.niaid.nih.gov/user_guide_microbiomedb_tutorial/).
- `_corrected.txt`: a copy of the mapping file submitted with the pipeline. The "corrected" label is not about the metadata.




### TEDreads/TEDreads_mtx folder

Output of Steps 1 & 2. These log files track the stats of samples through the trimming, filtering (T), error correction (E) and decontamination (D) Steps (TED Steps). When using **denovo Metatranscriptomics**, this folder will be called `TEDreads_mtx` and contain additional information regarding sortMeRNA results. If you chose the **Output TEDread fastq files** user option, we recommend downloading the TEDreads to this folder.

- `<SampleName>_fastpog.html`: log file with filtering, trimming and error-correction stats
- `<SampleName>_kr2_decontamREPORT.txt`: a log file reporting abundance and classification of the host reads (removed from the dataset).
- Metatranscriptomics Mode only:
  - `<SampleName>_sortmerna.log`: log file provided by SortMeRNA
  - `<SampleName>_sortmerna_aligned.log`: this log file provides additional information about the parameters used
     - Check out this file if you want to know how much rRNA was removed from your sample(s).


### TAXprofiles folder (dataset-wide taxonomic results)

Although listed first here, this folder is one of the last produced from the pipeline as it contains the dataset-wide taxonomic results (visualizations, summaries and community matrices) produced from each processed sample. 

Complete contents of this folder will depend on the options elected for the pipeline.

- `ReadsTAX_$DBname` folder (default):* Contains logs and reports from the taxonomic classification of TED reads [Step 3](#step-3). Sub-folders:
  - `bin` folder: files used by Krona for creating the `TAXplots` html chart. These are the text versions of the per-sample taxonomic reports from the TED reads, and they are visualized in the `TAXplots_ReadsTAX_$DBname.html` report.
  - `bioms` folder: The files from the _bin folders_ are translated to biom (json format) files for each sample. These can be manually uploaded to MicrobiomeDB or any other analytical platform, if needed.
  - `reports` folder: contains raw Kraken2 report files of the taxonomic classifications produced for each sample
  - `TAXplots_ReadsTAX.html` file: interactive Krona chart of the TED read-based taxonomic profiles
  - `merged_tables` folder (conditional of ≥ 2 samples): the summarized/collated TAX profiling results - a dataset-wide TAX abundance matrix containing each sample's profiles. Creation of this folder is not performed for datasets with less than 2 samples. The TAX abundance matrix in this folder is represented in various ways (Counts with Lineage included, Counts with Ranks included, Counts only, TAX only Lineage only, and a biom file of the community matrix). The biom file contained here is the same as `for_analyze_with_microbiomedb.biom` in main folder.
	- `DivPlots` (conditional of ≥ 2 samples): Diversity plots and exploratory statistics for the dataset (**note new location** is within `ReadsTAX` folder as it summarizes the data from the ReadTAX profiles). The plots include alpha diversity indices and boxplot (`TAX_AlphaDiv.txt` and `TAX_AlphaDiv.pdf`), beta diversity PCoA and nMDS ordination plots (`TAX_BetaDiv_nMDS.pdf` & `TAX_BetaDiv_PCoA.pdf`, require >=3 samples), TAX content heatmap (`TAX_Profile_Heatmap.pdf`), Rankabundance (`TAX_RankAbundanceCurve.pdf`) and rarefication curves (`TAX_RareficationCurve.pdf`). In some cases (e.g. ordination plots), some exploratory statistics will fail due to the content of the dataset. Expected files:
  -  (alpha diversity indices per-sample)

- `geneTAX_$DBname` & `scaffTAX_$DBname` folders *(user-elective):* Output of the gene or scaffold -based taxonomic profiles elected by user. It contains a `bin` folder with text versions of the profiles and *in some cases (depending on database used)* profile visualizations by KronaTools.
  - `TAXplots_genetax.html`: an html interactive report of the gene-based taxonomic profiles for each sample
- `MAGs_TAX` folder *(user-elective)*: This folder is generated only if MAGs creation and taxonomic profiling is enabled. It contains the TAX classification and abundances of the MAGs. It also contains a `bin` folder with text versions of the MAG-based taxonomic profiles and visualizations by KronaTools (`TAXplots_MAGx.html`). It will also contain a `MAG-based_Counts+TAX.biom` biom file summarizing the MAG-based taxonomic profiles of all samples.



### PWYprofiles folder (dataset-wide functional results)

Contains the dataset-wide functional results from the pipeline, including pathway (PWY) inferred profiles and gene-based profiles. The folder will contain one of 2 possible options from the pipeline, depending on **metabolic pathway database** chosen at submission: `keggPWY` (default choice) or `metacycPWY` (alternative choice) folder. Either folder will have the same structure

- `$DBnamePWY` contains the following sub-folders and files (Since the PWYs for WMSA are inferred with MinPATH tool, the resulting sub-folders are amended with .MP suffix):
  - `PWYplots_$DBname` html report with an interactive chart of the functional profiles for each sample (KronaTools)
  - `pwybin.MP` folder: per-sample text report of the `PWYplots` chart.
  - `bioms` folder: per-sample `_json.biom` files of the text-based PWY profiles per sample.
  - **NEW** `genebin` folder: containing per sample text file of abundances for each unique gene found in the sample.
  - `merged_tables.MP` folder (conditional of ≥ 2 samples in dataset): Dataset-wide PWY abundance summary abundance matrix tables representing the collated results each sample functional annotation and abundance scoring. The abundance matrix is represented in various ways (PWY abundances (aka "counts") + Tiers included, Tiers only, Counts only, Counts+Tier ranks, a biom file, etc). **NEW** as from WGSA v2.2 update, the folder also contains a gene-based abundance matrix (`merged_geneTPMtable.txt`) containing the per-sample gene abundances from the `genebin` folder.
	- `DivPlotsMP` (conditional of ≥ 2 samples): Simple exploratory plots of PWY functional dataset-wide profiles. Visualizations include a community PCoA and nMDS functional composition ordination plots (`PWY_BetaDiv_nMDS.pdf` & `PWY_BetaDiv_PCoA.pdf`; (>=3 samples)) produced from the inferred PWY matrix in `merged_tables.MP` as well as a pathway abundance heatmap plot (`PWY_Profile_Heatmap.pdf` (>=2 samples)).




### asmbMetaSpades/asmbTrinity folder (per sample detailed results)

Although discussed last in this text, this folder is the dataset's most detailed per-sample results. Each sample will have its own sub-folder, named <SampleName>_asmb. Content of each <SampleName>_asmb may vary depending on options chosen for the WGSA2+ pipeline (e.g. _Run AMRFinder_, _Produce MAGs_, etc), but the main structure and content of each sample's folders is the same. The summary files represented in the `TAXprofiles` or `PWYprofiles` folders are produced from files and information extracted from each sample's assembly contained in this folder.

- `$SampName_asmb` folder (one for each sample in dataset): 

Organized in chronological order of creation within the workflow of the pipeline, these folders (for each sample), contains the following:

#### assembly-related files & folders 
##### `$SampName_asmb/` folders

  - `contigs.fasta` & `final.assembly.fasta`: FASTA files of the produced assembly. The assembly represented in independent contigs (contiguous consensus sequences) are stored in `contigs.fasta`, while the scaffolded assembly (the same contigs, oriented, arranged and connected with gaps (Ns in the sequence), based on PE information from the TED reads) are in `final.assembly.fasta`.  It is the scaffolded assembly that is used for all subsequent assembly-based analyses.
  - For **denovo Metatranscriptomics**, we provide only `final.assembly.fasta`, which represents the assembled transcripts/contigs identified by Trinity. This file is used for all subsequent assembly-based analyses in this mode, when selected.
  - `final.assembly_scaffCoverage.txt` file: per-scaffold stats and abundance scores such as average read count, % scaffold covered by reads, number covered bases, GC content, etc. The file also contains RPM abundance values (reads per million) for each scaffold (it is this value that is used to assess taxonomic abundance in the elective scaffold-based taxonomic profiles). As noted above, in **Metatranscriptomics Mode**, these statistics will relate to assembled transcripts and not scaffolds.
  - `final.assembly_stats.txt` file: assembly-wide stats such as size of assembly, N50 an L50 stats, number of scaffolds created, etc. File also contains TED read mapping stats and alignment de-replication stats. As noted above, in **Metatranscriptomics Mode**, these statistics will relate to assembled transcripts and not scaffolds.
  - `final.assembly.bam` & `.bam.bai`: assembly alignment and index of alignment files (.bam file is big)
  - `spades.log` or `$SampName_trinity.log`: log file of the assembly software SPAdes (also captured by the main WGSA logfile.txt), or Trinity in **Metatranscriptomics Mode**.
  - `scaffTAX_$DBname` folder **(user-elective)**: This folder contains the taxonomic assignments of each scaffold (if elected) within the sample, the raw Kraken2 report, the produced human & Krona-readable `$SampName_4krona` file, and a taxonomy-supplemented scaffold coverage file `final.assembly_scaffCovr+tax.txt`. _Note_: The database used for taxonomic classification of the scaffolds is the same as the one elected for main taxonomic classification of WMSA (TED read TAX classification). In **Metatranscriptomics Mode**, this folder will have the same name and contents, but will be performed on assembled transcripts instead of scaffolds.


#### gene-related files 
##### within `$SampName_asmb/genes` folder

This folder contains files with information about predicted features (likely coding sequences (CDS) or "genes" for short). These files have the prefix `PREDgenes`:

  - `PREDgenes.{faa, fna, gff, gtf}` text files: contain information about the predicted features from the sample, described as amino acid sequences (.faa), nucleotide sequences (.fna), or scaffold names and coordinates {.gff & .gtf} files.
  - `PREDgenes_ABUNtab.txt` text file: **provides feature abundance values** with information about feature length, coverage and estimated abundances in RPK (reads per kilobases) and TPM (transcripts per million) score for each feature (instance of gene; iTPM).
  - `PREDgenes_stats.txt`: overall stats of predicted features including information about annotation yields, etc.
  - `genesTAX_$DBname` folder **(user-elective)**: Taxonomic association of each predicted feature (gene) within the sample. If elected, the raw Kraken2 report is provided (`taxREPORT.txt`), along with produced human & Krona-readable `$sampName_4krona.txt` file (used to produce Krona charts in `TAXprofiles/geneTAX` folder). Additionally, the PREDgenes_ABUNtab.txt file is re-provided amended with gene-based taxonomic affiliation (`PREDgenes_ABUNtab+tax.txt` file).
  - `AMRs` foler **(user-elective)**: A folder containing results from AMRFinding algorithm, if elected during submission. Files `AMRs{.faa & _info.txt}` contain the amino-acid sequences and characterizing information (element name, symbol, type, coverage and other stats) for each predicted AMR. 

_Note_: The `$SampName_asmb/genes/PREDgenes.faa` file can be manually provided to the [GhostKoala online annotation & pathway mapping tool](https://www.kegg.jp/ghostkoala/) for sample-specific metabolic and taxonomic annotation outside of the WMSA pipeline.

#### annotation-related files 
##### within `$SampName_asmb/genes/annotations`
    
Folder containing information about successfully annotated features - features recognized as known genes or their homologues.

 - `annots.emapper.{annotations, hits, seed_orthologs}.txt` files: raw outputs of EggNOG-mapper2, from which various annotation types are extracted for analysis. These files also provide detailed (too much) and interweaved information about each annotated gene.
 - `annots.{ko, ec, KEGGmap, COG}.txt` files: extracted annotations for each annotation type (KO, EC, KEGGmap and COG annotation respectively) from the emapper raw output files. 
 - `ANNOTgenes_ABUNDtab.{ko,ec}.txt`: a subset of the `PREDgenes_ABUNtab.txt` text file from `$SampName_asmb/genes`, containing only the predicted features with successfully assigned KO or EC annotations (_Note_: the provided gene information (length, cov, RPK and iTPM) is again, per instance of the gene in the sample => multiple features with the same annotation exist). 
 - `geneTPMtab.{ko,ec}.txt`: files summarizing **gene abundances for each unique gene** with KO or EC annotation types. _Note_: It is this file that is collected from each sample in the `PWYprofiles/$DBnamePWY/genebin` folder, and used to produce the gene-based community matrix in the `PWYprofiles/$DBnamePWY/merged_tables.MP`


#### pathways-related information 
##### within `$SampName_asmb/genes/pathways`

This folder contains inferred pathways information (from MinPATH) based on the predicted genes (`annots.{ko,ec}.txt`) and calculated abundance scores (iTPM values from `ANNOTgenes_ABUNDtab.{ko,ec}.txt` file) for each sample. Depending on the user-elected `$DBname`, the file names will have `$prefix` of `ko2gg` (for ko annotations mapped to KEGGdb) or `ec2mc` (for ec annotations mapped to MetaCycDB).

 - `$prefix.MP.{report,details,log}.txt` files: raw output from MinPath pathway prediction tool. See: [How to read MinPath output](https://omics.informatics.indiana.edu/MinPath/output-readme.txt) and the [MinPATH publication](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000465) for more information about how to read files.
 - `$prefix.MP_4krona.txt` file: Information from the `report` file is used to create this file, describing each complete pathway and corresponding calculated abundance score (from iTPM values). The `_4krona.txt` file from each assembled sample is copied in `$PWYprofiles/$DBnamesPWY/pwybin.MP` and is used to produce functional profile plots and matrixes in the `PWYprofiles/$DBnamePWY/` folder.
 - `missing_pathways.txt`: a raw output from MinPATH tool, which would provide information about expected but missing pathways (in most cases, this file will be empty). 


#### MAGs-related information 
##### within `$SampName_asmb/MAGs` optional folder

This folder contains metagenome assembled genomes (MAGs) information if the **MAGs** option was elected at submission. It contains binned scaffolds forming draft genomes and their quality assessments. Number of files will vary based on the community composition, organismal abundance and sequence representation.

  - mags fasta files (draft genomes):

    - `mag.{count}.fa`: fasta file containing scaffolds assumed to be representing the same organism or lineage
    - `mag.{lowDepth, tooShort, unbinned}.fa`: fasta files containing scaffolds that do not meet the binning tool's (MetaBat2) criteria for binning (see [Metabat2 publication](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6662567/)). These files are also likely to contain scaffolds affiliated with unicellular eukaryotic organisms (if such are present in the sample).

  - `magsQA` folder: Output of CheckM's bin quality assessment tool. In this folder are: `bins/`, `QCplots/`, `storage/` folders as well as `checkm.log`, `lineage.ms` files. More information can be found on [CheckM's website](https://github.com/Ecogenomics/CheckM/wiki). Of note are:

    - `magsQA/bins/`: AA and NT sequences for the predicted genes from that bin, along with gene coordinates, annotations (.gff) and other files
    - `magsQA/QCplots`: plots describing QC stats for each bin [more info](https://github.com/Ecogenomics/CheckM/wiki#plots)).

    The WMSA pipeline extracts the more descriptive information from CheckM's output to create the following reports:
    
    - `mags_SUMMARY.txt`: taxonomic, abundance, coverage and other information and stats about each MAG. This file is also used to create the MAGs-based TAX profiles reported in *TAXprofiles/MAGs_TAX* folder.
    - `mags_coverage.txt`: per scaffold coverage and read mapping stats for each MAG
    - `mags_profiles.txt`: coverage & abundance assessment stats for each MAG [more info](https://github.com/Ecogenomics/CheckM/wiki/Utility-Commands#profile)
    - `mags_qa.txt`: quality assessment stats for each MAG
    - `mags_tax.txt`: more detailed taxonomic information about each MAG




