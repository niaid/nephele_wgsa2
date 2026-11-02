# Nephele WGSA2 pipeline

## Introduction
The WGSA2+ pipeline uses raw paired end (PE) shotgun reads to produce de novo assemblies for each sample in a metagenomic or metatranscriptomics dataset, as well as extract information about the taxonomic and functional composition of microbial communities.


## Pipeline's parameters
### Commandline usage
```
Usage: [-h] [--version] --mapping_file_path {mappingFile.txt} \
               --outputs_dir_path {outputDIR} \
               --denovo_mtx  {bool} \
               --trim_filter {bool} --average_read_quality {int} \
                   --min_read_length {int} --trim_of_5 {int}  --trim_of_3 {int} \
               --include_ted_files  {bool} \
               --decontaminate_db_path  {decontaminate_db_path}  \
                   --kr2confidence_host {int} \
               --classification_db_name {classification_db_name} \
               --classification_db_path {classification_db_path} \
                   --kr2confidence_taxonomic {int} \
               --krona_tax_db_path      {krona_tax_db_path} \
               --read_norm  {bool} \
                   --readCoverage {int} \
               --tax_genes  {bool} \
               --tax_scaffolds {bool} \
               --mag {bool} \
               --find_args {bool}  --args_db_path {args_db_path} \
               --annotations_type {annotations_type} \
                   --eggnog_db_path {eggnog_db_path} \
                   --annotations_map_db_path {annotations_map_db_path} \
                   --annotations_hrr_db_path {annotations_hrr_db_path} 
```

### User options

- `trim_filter`: bool (default=false) - Allows for additional trimming and filtering of reads, post-QA processing (if needed)
  - `average_read_quality`: int (default=10) - Filter reads with this read-wide average quality threshold. Come into effect when `trim_filter=true`
  - `min_read_length`: int (default=60) - Filter out reads below this read length. Come into effect when `trim_filter=true`
  - `trim_of_5`: int (default=10) - Quality threshold for 5'-end trimming. Come into effect when `trim_filter=true`
  - `trim_of_3`: int (default=5) - Quality threshold of 3'-end trimming. Come into effect when `trim_filter=true`
- `decontaminate_db_path`: str - path to the decontamination database, inclusive of the host organism of your dataset
- `kr2confidence_host`: float (default=0.05) - kraken2 confidence value for identifying host reads
- `classification_db_name`: str {plusPFV | MGBCdb | UHGGdb | EuPATHdb}
- `classification_db_path`: str - path to the taxonomic classification DB that best suits your dataset
- `krona_tax_db_path`: str - path to your krona tax datafile
- `kr2confidence_taxonomic`: float (default=0.15) -kraken2 confidence value for taxonomic classifications
- `read_norm`: bool (default=False) - Run read normalization
  - `readCoverage`: int (default=50) - Normalize reads to this coverage. Comes into effect when `read_norm=true`
- `denovo_mtx`: bool (default=false) - Run pipeline in metagenomics or metatranscriptomics mode
- `tax_scaffolds`: bool (default=false) - Add taxonomic annotation to be produced from scaffolds per sample
- `tax_genes`: bool (default=false) - Add taxonomic annotation to be produced from genes per sample
- `eggnog_db_path`: str - path to your eggnog datafile
- `annotations_type`: str {ko | ec}
- `annotations_map_db_path`: str - path to your annotations map file
- `annotations_hrr_db_path`: str - path to your annotations hrr file
- `find_args`: bool (default=false) - Add Antimicrobial Resistance genes identification
  - `args_db_path`: str - path to your CARD db. Comes into effect when `find_args=true` 
- `mag`: bool (default=false) - Add metagenome assembled genomes (MAGs) & MAG-based taxonomic profiles to be produced from scaffolds per sample (Note: time consuming & functional only for prokaryotic organisms)
- `include_ted_files`: bool (default=false) - The Trimmed, Error-corrected and Decontaminated (TED) fastq files are large and therefore omitted in default results output! Elect this option for pipeline to produce the file
- `set_cpus`: int (default = automatic) - customize CPU settings. If automatic, all accessible will be used.



## Datafiles and notes
```
DecontaminateDBpathValues {
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
 
ClassificationDBpathValues {
  PlusPF = "/dbs/wgsa2plus_lora/plus_PFV_Oct2025/",
  MGBCdb = "/dbs/wgsa2plus_lora/MGBCdb/",
  UHGGdb = "/dbs/wgsa2plus_lora/UHGG2_Nov2022/",
  EuPATHdb = "/dbs/wgsa2plus_lora/EuPATH_db46_Mar2023/",
}

KronaFILEpathValues {
  krona_tax_db_path = ClassificationDBpath + "/taxdump/"
}


AnnotationsDBpathValues {
  eggnogDB= "/dbs/eggnog_data/"
  RGIdb = "/dbs/CARD_db_v4.0.1/"
}

FunctionalDBpathValues {
  KEGGdb = "/dbs/minpath_data/KEGGdb_data/"
  metaCycDB = "/dbs/minpath_data/metaCycdb_files/"
}
```



## Design, development and documentation
* Angelina Angelova,   Metagenomics Analysis Specialist, Science Support Section, BCBB/OCICB/OSMO/OD/NIAID/NIH
* Katie McCauley,      Metagenomics Specialist, Science Support Section, BCBB/OCICB/OSMO/OD/NIAID/NIH
* Duc Doan,            Software Engineer, Bioinformatics Software Section, BCBB/OCICB/OSMO/OD/NIAID/NIH
* Bikram Basnet,       Software Engineer, Bioinformatics Software Section, BCBB/OCICB/OSMO/OD/NIAID/NIH
* Poorani Subramanian, Metagenomics Specialist, Science Support Section, BCBB/OCICB/OSMO/OD/NIAID/NIH
* Lauren Krausfeldt,   Metagenomics Specialist, Science Support Section, BCBB/OCICB/OSMO/OD/NIAID/NIH
