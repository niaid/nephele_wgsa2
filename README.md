# Nephele WGSA2 pipeline

## Introduction
The WGSA2 pipeline uses raw paired end (PE) shotgun reads to produce de novo assemblies for each sample in a metagenomic dataset, as well as extract optimal levels of information about the taxonomic and functional composition of a microbial community.

## Datafiles
Note: Need to provide links to download files
The following datafiles are needed to run the pipeline
- decontaminate
- classification
- eggnog
- annotations
- krona

## Sample input.json
```
{
    "samples": [
        {
            "id": "S1",
            "forward_fastq_file_path": "/inputs/S1_GItract_camiHiSeq_sub1M_R1.fastq.gz",
            "reverse_fastq_file_path": "/inputs/S1_GItract_camiHiSeq_sub1M_R2.fastq.gz",
            "metadata": {
                "TreatmentGroup": "Control",
                "Animal": "RhDCBC",
                "Day": "347",
                "Description": "SwabJejunum"
            }
        },
        {
            "id": "S6",
            "forward_fastq_file_path": "/inputs/S6_Oral_camiHiSeq_sub1M_R1.fastq.gz",
            "reverse_fastq_file_path": "/inputs/S6_Oral_camiHiSeq_sub1M_R2.fastq.gz",
            "metadata":{
                "TreatmentGroup": "Control",
                "Animal": "RhDCBC",
                "Day": "347",
                "Description": "SwabJejunum"
            }
        }
    ],
    "pipeline_arguments": {
        "decontaminate_db_path": "/dbs/decontam_db/decontam_marine_db",
        "classification_db_name": "plusPFV",
        "classification_db_path": "/dbs/classification_db/plusPFV_Mar2023",
        "eggnog_db_path": "/dbs/eggnog_data",
        "annotations_type": "ko",
        "annotations_map_path": "/dbs/minpath_data/KEGG_myfiles_0922/KEGG-ko2map-092022.txt",
        "annotations_hrr_path": "/dbs/minpath_data/KEGG_myfiles_0922/KEGG-HRCHY-092022.txt",
        "krona_tax_db_path": "KronaTools_taxonomy",
        "amrfind": true,
        "tax_genes": true,
        "tax_scaffolds": true,
        "mag": true,
        "include_ted_files": true,
    }
}
```

## Pipeline's parameters

```
decontaminate_db_path: str - path to the decontamination database, inclusive of the host organism of your dataset
classification_db_name: str {plusPFV | MGBCdb | EuPATHdb}
classification_db_path: str - path to the taxonomic classification DB that best suits your dataset
eggnog_db_path: str - path to your eggnog datafile
annotations_type: str {ko | ec}
annotations_map_path: str - path to your annotations map file
annotations_hrr_path: str - path to your annotations hrr file
krona_tax_db_path: str - path to your krona tax datafile
amrfind: bool (default=false) - Add Antimicrobial Resistance genes & peptide finding
tax_genes: bool (default=false) - Add taxonomic annotation to be produced from genes per sample
tax_scaffolds: bool (default=false) - Add taxonomic annotation to be produced from scaffolds per sample
mag: bool (default=false) - Add metagenome assembled genomes (MAGs) & MAG-based taxonomic profiles to be produced from scaffolds per sample (Note: time consuming & functional only for prokaryotic organisms)
include_ted_files: bool (default=false) - The Trimmed, Error-corrected and Decontaminated (TED) fastq files are large and therefore omitted in default results output! Elect this option for pipeline to produce the file
trim_filter: bool (default=false) - Allows for additional trimming and filtering of reads, post-QA processing (if needed)
average_read_quality: int (default=10) - Filter reads with this read-wide average quality threshold. Come into effect when trim_filter=true
min_read_length: int (default=60) - Filter out reads below this read length. Come into effect when trim_filter=true
trim_of_5: int (default=20) - Quality threshold for 5'-end trimming. Come into effect when trim_filter=true
trim_of_3: int (default=15) - Quality threshold of 3'-end trimming. Come into effect when trim_filter=true
```
