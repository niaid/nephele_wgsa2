# Nephele WGSA2 pipeline

## Introduction
The WGSA2+ pipeline uses raw paired end (PE) shotgun reads to produce de novo assemblies for each sample in a metagenomic or metatranscriptomics dataset, as well as extract information about the taxonomic and functional composition of microbial communities.

## Datafiles
Note: Need to provide links to download files
The following datafiles are needed to run the pipeline
- decontaminate
- classification
- eggnog
- annotations
- krona

## Pipeline's parameters

```
trim_filter: bool (default=false) - Allows for additional trimming and filtering of reads, post-QA processing (if needed)
average_read_quality: int (default=10) - Filter reads with this read-wide average quality threshold. Come into effect when trim_filter=true
min_read_length: int (default=60) - Filter out reads below this read length. Come into effect when trim_filter=true
trim_of_5: int (default=20) - Quality threshold for 5'-end trimming. Come into effect when trim_filter=true
trim_of_3: int (default=15) - Quality threshold of 3'-end trimming. Come into effect when trim_filter=true
decontaminate_db_path: str - path to the decontamination database, inclusive of the host organism of your dataset
kr2confidence_host: float (default=0.05) - kraken2 confidence value for identifying host reads
classification_db_name: str {plusPFV | MGBCdb | UHGGdb | EuPATHdb}
classification_db_path: str - path to the taxonomic classification DB that best suits your dataset
krona_tax_db_path: str - path to your krona tax datafile
kr2confidence_taxonomic: float (default=0.15) -kraken2 confidence value for taxonomic classifications
read_norm: bool (default=False) - Run read normalization
readCoverage: int (default=50) - Normalize reads to this coverage
denovo_mtx: bool (default=false) - Run pipeline in metagenomics or metatranscriptomics mode
tax_scaffolds: bool (default=false) - Add taxonomic annotation to be produced from scaffolds per sample
tax_genes: bool (default=false) - Add taxonomic annotation to be produced from genes per sample
eggnog_db_path: str - path to your eggnog datafile
annotations_type: str {ko | ec}
annotations_map_db_path: str - path to your annotations map file
annotations_hrr_db_path: str - path to your annotations hrr file
find_args: bool (default=false) - Add Antimicrobial Resistance genes identification
mag: bool (default=false) - Add metagenome assembled genomes (MAGs) & MAG-based taxonomic profiles to be produced from scaffolds per sample (Note: time consuming & functional only for prokaryotic organisms)
include_ted_files: bool (default=false) - The Trimmed, Error-corrected and Decontaminated (TED) fastq files are large and therefore omitted in default results output! Elect this option for pipeline to produce the file
```


## DB Path Values
```
export enum DecontaminateDbPathValues {
  HumanMouse = "/dbs/wgsa2/decontam_db/decontam_human+mouse_db/",
  Marine = "/dbs/wgsa2/decontam_db/decontam_marine_db/",
  Mosquito = "/dbs/wgsa2/decontam_db/decontam_mosq_db/",
  Nematode = "/dbs/wgsa2/decontam_db/decontam_nematode_db/",
  Rodent = "/dbs/wgsa2/decontam_db/decontam_rodents_db/",
  Primates = "/dbs/wgsa2/decontam_db/decontam_primates_db/",
  Tick = "/dbs/wgsa2/decontam_tickDB/",
  Bat = "/dbs/wgsa2/decontam_batDB/",
  Plants = "/dbs/wgsa2/decontam_db/decontam_plants_db/",
}
 
export enum ClassificationDbPath {
  PlusPF = "/dbs/wgsa2plus_lora/plus_PFV_Oct2025/",
  MGBCdb = "/dbs/wgsa2plus_lora/MGBCdb/",
  UHGGdb = "/dbs/wgsa2plus_lora/UHGG2_Nov2022/",
  EuPATHdb = "/dbs/wgsa2plus_lora/EuPATH_db46_Mar2023/",
}
```