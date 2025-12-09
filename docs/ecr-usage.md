# Usage

## Pull the Image

```bash
docker pull public.ecr.aws/niaid_nephele/pipeline/nephele_wgsa2:latest
```

## Run the Pipeline

Run the pipeline by providing parameters as command-line arguments:

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
  --denovo_mtx False \
 	--sortmerna_db_path None \
  --eggnog_db_path /dbs/eggnog_data \
  --annotations_type ko \
  --annotations_map_db_path /dbs/minpath_data/KEGG_myfiles_0922/KEGG-ko2map-092022.txt \
  --annotations_hrr_db_path /dbs/minpath_data/KEGG_myfiles_0922/KEGG-HRCHY-092022.txt \
  --krona_tax_db_path /dbs/KronaTools_taxonomy
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
- `--sortmerna_db_path`: Path to sortMeRNA database or none

### Database Selection

- `--classification_db_name` (required): Classification database name
  - `plusPFV`: PlusPFV database (default)
  - `MGBCdb`: Microbial Genomes Bacterial Collection database
  - `UHGGdb`: Unified Human Gastrointestinal Genome database
  - `EuPATHdb`: Eukaryotic Pathogen database

- `--annotations_type` (required): Annotations type
  - `ko`: KEGG Orthology (default)
  - `ec`: Enzyme Commission

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

**Note**: For visualizations, you need at least 2 samples. For ordination plots (PCoA, nMDS), you need at least 3 samples.

The mapping file must include `SampleID`, `ForwardFastqFile`, and `ReverseFastqFile` columns. Additional metadata columns (like `TreatmentGroup`, `Description`) are used for grouping in visualizations.

## Optional Analysis Features

- `--amrfind` (boolean, default: false): Add Antimicrobial Resistance genes & peptide finding
- `--tax_genes` (boolean, default: false): Add taxonomic annotation to be produced from genes per sample
- `--tax_scaffolds` (boolean, default: false): Add taxonomic annotation to be produced from scaffolds per sample
- `--mag` (boolean, default: false): Add metagenome assembled genomes (MAGs) & MAG-based taxonomic profiles to be produced from scaffolds per sample (Note: time consuming & functional only for prokaryotic organisms)
- `--include_ted_files` (boolean, default: false): The Trimmed, Error-corrected and Decontaminated (TED) fastq files are large and therefore omitted in default results output! Elect this option for pipeline to produce the file
- `--denovo_mtx` (boolean, default: false): Enable de novo transcriptomics assembly
- `--sortmerna_db_path` (path, optional): Path to SortMeRNA database (required if denovo_mtx is enabled)

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
