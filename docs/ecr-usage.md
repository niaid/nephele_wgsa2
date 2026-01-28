# Usage

## Pull the Image

```bash
docker pull public.ecr.aws/niaid_nephele/pipeline/nephele_wgsa2:latest
```

## Run the Pipeline

We recommend using Docker and ensuring you have `root` access. For Singularity or Apptainer, see below for additional details.

Run the pipeline by providing required parameters as command-line arguments:

```bash
docker run -v /path/to/inputs:/inputs \
  -v /path/to/outputs:/outputs \
  -v /path/to/databases:/dbs \
  public.ecr.aws/niaid_nephele/pipeline/nephele_wgsa2:latest \
  --mapping_file_path /inputs/mapping_file.txt \
  --outputs_dir_path /outputs \
  --decontaminate_db_path /dbs/decontam_db/decontam_marine_db \
  --classification_db_name plusPFV \
  --classification_db_path /dbs/classification_db/plusPFV_Mar2023 \
  --krona_tax_db_path /dbs/KronaTools_taxonomy \
  --denovo_mtx False \
  --eggnog_db_path /dbs/eggnog_data \
  --annotations_map_db_path /dbs/minpath_data/KEGGdb_0624/KEGGpwy-ko2map_0624.txt \
  --annotations_hrr_db_path /dbs/minpath_data/KEGGdb_0624/KEGGhrr_brite_0624.txt 
```

## Required Arguments

### Input Files

- `--mapping_file_path`: Path to mapping file containing sample metadata (tab-delimited)
- `--outputs_dir_path` (path, default: "/outputs"): Path to outputs directory

### Database Paths

- `--decontaminate_db_path`: Path to the decontamination database, inclusive of the host organism of your dataset
- `--classification_db_path`: Path to the taxonomic classification database that best suits your dataset
- `--eggnog_db_path`: Path to your eggNOG database
- `--annotations_map_db_path`: Path to your annotations map file
- `--annotations_hrr_db_path`: Path to your annotations hierarchy file
- `--krona_tax_db_path`: Path to your Krona taxonomy database

### Database Selection

- `--classification_db_name` (required): Classification database name
  - `plusPFV`: PlusPFV database (default)
  - `MGBCdb`: Microbial Genomes Bacterial Collection database
  - `UHGGdb`: Unified Human Gastrointestinal Genome database
  - `EuPATHdb`: Eukaryotic Pathogen database

- `--annotations_type` (required): Annotations type
  - `ko`: KEGG Orthology (default)
  - `ec`: Enzyme Commission

## Optional Analysis Features

- `--kr2confidence_host` (integer, default: 0.05, range: 0-1). Kraken2 confidence value for identifying host reads during decontamination steps.
- `--kr2confidence_taxonomic` (integer, default 0.15, range: 0-1). Kraken2 confidence value for taxonomic classifications. Higher values produce more unclassified reads. Lower values produce more sporadic annotations at lower abundance reads. 
- `--find_args` (boolean, default: false): Add Antimicrobial Resistance genes & peptide finding
- `--tax_genes` (boolean, default: false): Add taxonomic annotation to be produced from genes per sample
- `--tax_scaffolds` (boolean, default: false): Add taxonomic annotation to be produced from scaffolds per sample
- `--mag` (boolean, default: false): Produce metagenome assembled genomes (MAGs) & MAG-based taxonomic profiles from scaffolds per sample (Note: time consuming & functional only for prokaryotic organisms)
- `--include_ted_files` (boolean, default: false): The Trimmed, Error-corrected and Decontaminated (TED) fastq files are omitted in default results output due to their size! Elect this option for pipeline to produce the file
- `--read_norm` (boolean, default: false): for large samples, use read normalization to reduce time and resource demands of the pipeline
- `--readCoverage` (integer, default: 50, range: 10-80). Coverage of reads will be normalized down to this level for assembly (not used in abundance estimations)
- `--denovo_mtx` (boolean, default: false): Enable de novo transcriptomics assembly

## Quality Control and Trimming Parameters

- `--trim_filter` (boolean, default: false): Allows for additional trimming and filtering of reads, post-QA processing (if needed)

The following parameters come into effect when `trim_filter=true`:

- `--average_read_quality` (integer, default: 10, range: 0-35): Filter reads with this read-wide average quality threshold
- `--min_read_length` (integer, default: 60, range: 0-150): Filter out reads below this read length
- `--trim_of_5` (integer, default: 20, range: 0-35): Quality threshold for 5'-end trimming
- `--trim_of_3` (integer, default: 15, range: 0-35): Quality threshold for 3'-end trimming

## Output Files

The pipeline generates comprehensive outputs organized into several directories:

### Global Files
- `WGSA2plus_output_details.pdf`: Complete output documentation
- `logfile.txt`: Pipeline execution log
- `for_analyze_with_microbiomedb.biom`: BIOM file for MicrobiomeDB upload
- `mapping_file.txt`: Copy of submitted mapping file

### TAXprofiles Folder
Contains dataset-wide taxonomic results including:
- `ReadsTAX_<DBname>` folder: TED reads taxonomic classification
  - Interactive Krona charts (`TAXplots_ReadsTAX_<DBname>.html`)
  - BIOM format files
  - Kraken2 reports
  - Diversity plots (alpha and beta diversity, heatmaps, rarefaction curves)
- `geneTAX_<DBname>` folder (optional): Gene-based taxonomic annotations
- `scaffTAX_<DBname>` folder (optional): Scaffold-based taxonomic annotations
- `MAGs_TAX` folder (optional): MAG-based taxonomic profiles

### PWYprofiles Folder
Contains dataset-wide functional analysis results:
- Interactive pathway visualizations (`PWYplots_[ko2gg or ec2cc].html`)
- Per-sample pathway and gene abundance files
- Merged abundance matrices (≥2 samples)
- Functional diversity plots (≥3 samples)

### asmb_files Folder
Contains per-sample final assembly FASTA and BAM files for downstream processing

### Per-Sample Folders
Each sample gets a dedicated folder with:
- Assembly files
- Gene annotations
- Taxonomic classifications
- Quality control reports

## Example with Metagenomics

```bash
docker run \
  -v $(pwd)/inputs:/inputs \
  -v $(pwd)/outputs:/outputs \
  -v $(pwd)/databases:/dbs \
  public.ecr.aws/niaid_nephele/pipeline/nephele_wgsa2:latest \
  --mapping_file_path /inputs/mapping_file.txt \
  --decontaminate_db_path /dbs/decontam_db/decontam_marine_db \
  --classification_db_name UHGGdb \
  --classification_db_path /dbs/classification_db/UHGG \
  --read_norm True \
  --readCoverage 40 \
  --denovo_mtx False \
 	--sortmerna_db_path None \
  --eggnog_db_path /dbs/eggnog_data \
  --annotations_type ko \
  --annotations_map_db_path /dbs/minpath_data/KEGG_myfiles_0922/KEGG-ko2map-092022.txt \
  --annotations_hrr_db_path /dbs/minpath_data/KEGG_myfiles_0922/KEGG-HRCHY-092022.txt \
  --krona_tax_db_path /dbs/KronaTools_taxonomy \
  --amrfind \
  --tax_genes \
  --mag \
  --trim_filter \
  --average_read_quality 15 \
  --min_read_length 80
```

## Example with Transcriptomics

```bash
docker run \
  -v $(pwd)/inputs:/inputs \
  -v $(pwd)/outputs:/outputs \
  -v $(pwd)/databases:/dbs \
  public.ecr.aws/niaid_nephele/pipeline/nephele_wgsa2:latest \
  --mapping_file_path /inputs/mapping_file.txt \
  --decontaminate_db_path /dbs/decontam_db/decontam_marine_db \
  --classification_db_name plusPFV \
  --classification_db_path /dbs/classification_db/plusPFV_Mar2023 \
  --eggnog_db_path /dbs/eggnog_data \
  --annotations_type ko \
  --annotations_map_db_path /dbs/minpath_data/KEGG_myfiles_0922/KEGG-ko2map-092022.txt \
  --annotations_hrr_db_path /dbs/minpath_data/KEGG_myfiles_0922/KEGG-HRCHY-092022.txt \
  --krona_tax_db_path /dbs/KronaTools_taxonomy \
  --denovo_mtx true \
  --sortmerna_db_path /dbs/sortmerna_db
```

For complete documentation, see the [GitHub README](https://github.com/niaid/nephele_wgsa2/blob/main/README.md).





## Singularity or Apptainer

To run the pipeline with Singularity or Apptainer, the command needs to be adjusted slightly.

```
singularity exec -B {bind_paths} wgsa2.img \
    sh -c "cd /pipeline && python main.py {user_options}"
```

Here, all user options will need to stay within the quotation marks to be read accurately by the pipeline.

## Input Files Format

The pipeline expects:
- **Mapping file**: Tab-delimited file with sample metadata that also specifies the location of FASTQ files
- **FASTQ files**: Paired-end FASTQ files (R1 and R2) for each sample

### Example Mapping File Format

```
SampleID	ForwardFastqFile	ReverseFastqFile	TreatmentGroup	Animal	Day	Description
S1	/inputs/S1_R1.fastq.gz	/inputs/S1_R2.fastq.gz	Control	RhDCBC	347	SwabJejunum
S6	/inputs/S6_R1.fastq.gz	/inputs/S6_R2.fastq.gz	Control	RhDCBC	347	SwabJejunum
```

**Note**: For basic visualizations, you need at least 2 samples. For ordination plots (PCoA, nMDS), you need at least 3 samples.

The mapping file must include columns named `SampleID`, `ForwardFastqFile`, and `ReverseFastqFile` (used in processing) and `TreatmentGroup` (used for visualizations). Additional metadata columns (`Description`, `Age`, etc) are not used by pipeline but propagate to outputted tables and can be used by external softwares.
