from pathlib import Path
import os
from nephele_pipeline_utils.enums import DataType
from nephele_pipeline_utils.parser import NepheleArgumentParser
from nephele_pipeline_utils.types import boolean, path, directory, field, mapping_file

from config import pipeline_config
from enums import ClassificationDbType, AnnotationsType

parser = NepheleArgumentParser(data_type=DataType.PE)


def parse_args():
    parser.add_argument(
        "--version",
        action="version",
        version=pipeline_config.version,
        help="show program's version number and exit",
    )
    parser.add_argument(
        "--output_dag",
        type=boolean,
        default=True,
        help="generate dag in pdf format",
    )
    parser.add_argument(
        "--decontaminate_db_path",
        type=directory,
        required=True,
        help="path to the decontamination database, inclusive of the host organism of your dataset",
    )
    parser.add_argument(
        "--kr2confidence_host",
        type=field(float, ge=0.0, le=1),
        default=0.05,
        required=True,
        help="kraken2 confidence value for identifying host reads",
    )
    parser.add_argument(
        "--classification_db_name",
        type=str,
        required=True,
        choices=ClassificationDbType.values(),
        help="classification db name",
    )
    parser.add_argument(
        "--kr2confidence_taxonomic",
        type=field(float, ge=0.0, le=1),
        default=0.15,
        required=True,
        help="kraken2 confidence value for taxonomic classificaitons",
    )
    parser.add_argument(
        "--classification_db_path",
        type=directory,
        required=True,
        help="path to the taxonomic classification DB that best suits your dataset",
    )
    parser.add_argument(
        "--eggnog_db_path",
        type=directory,
        required=True,
        help="path to your eggnog datafile",
    )
    parser.add_argument(
        "--annotations_type",
        type=str,
        required=True,
        choices=AnnotationsType.values(),
        help="annotations type",
    )
    parser.add_argument(
        "--annotations_map_db_path",
        type=path("db"),
        required=True,
        help="path to your annotations map file",
    )
    parser.add_argument(
        "--annotations_hrr_db_path",
        type=path("db"),
        required=True,
        help="path to your annotations hrr file",
    )
    parser.add_argument(
        "--krona_tax_db_path",
        type=directory,
        required=True,
        help="path to your krona tax data",
    )
    parser.add_argument(
        "--find_args",
        type=boolean,
        default=False,
        help="Add steps for Antimicrobial Resistance Gene identification",
    )
    parser.add_argument(
        "--args_db_path",
        type=path("db"),
        required=False,
        help="path to your CARD database for Antimicrobial Resistance Gene identification",
    )
    parser.add_argument(
        "--read_norm",
        type=boolean,
        default=False,
        help="Run read normalization",
    )
    parser.add_argument(
        "--readCoverage",
        type=field(int, ge=10, le=80),
        default=50,
        help="Normalize reads to this coverage (Min 10, Max = 80)",
    )
    parser.add_argument(
        "--denovo_mtx",
        type=boolean,
        default=False,
        help="Denovo mtx",
    )
    parser.add_argument(
        "--tax_genes",
        type=boolean,
        default=False,
        help="Add taxonomic annotation to be produced from genes per sample",
    )
    parser.add_argument(
        "--tax_scaffolds",
        type=boolean,
        default=False,
        help="Add taxonomic annotation to be produced from scaffolds per sample",
    )
    parser.add_argument(
        "--mag",
        type=boolean,
        default=False,
        help="Add metagenome assembled genomes (MAGs) & MAG-based taxonomic profiles to be produced from scaffolds per sample (Note: time consuming & functional only for prokaryotic organisms)",
    )
    parser.add_argument(
        "--include_ted_files",
        type=boolean,
        default=False,
        help="The Trimmed, Error-corrected and Decontaminated (TED) fastq files are large and therefore omitted in default results output! Elect this option for pipeline to produce the file",
    )
    parser.add_argument(
        "--trim_filter",
        type=boolean,
        default=False,
        help="Allows for additional trimming and filtering of reads, post-QA processing (if needed)",
    )
    parser.add_argument(
        "--average_read_quality",
        type=field(int, ge=0, le=35),
        default=10,
        help="Filter reads with this read-wide average quality threshold. Come into effect when trim_filter=true",
    )
    parser.add_argument(
        "--min_read_length",
        type=field(int, ge=0, le=150),
        default=60,
        help="Filter out reads below this read length. Come into effect when trim_filter=true",
    )
    parser.add_argument(
        "--trim_of_5",
        type=field(int, ge=0, le=35),
        default=20,
        help="Quality threshold for 5'-end trimming. Come into effect when trim_filter=true",
    )
    parser.add_argument(
        "--trim_of_3",
        type=field(int, ge=0, le=35),
        default=15,
        help="Quality threshold of 3'-end trimming. Come into effect when trim_filter=true",
    )
    parser.add_argument(
        "--mapping_file_path",
        type=mapping_file,
        required=True,
        help="Input path to mapping file",
    )
    parser.add_argument(
        "--outputs_dir_path",
        type=directory,
        default=Path("/outputs"),
        help="Path to outputs directory",
    )
    parser.add_argument(
        "--set_cpus",
        type=field(int, ge=16, le=96),
        default=min(
            len(os.sched_getaffinity(0)), 96
        ),  ##os.cpu_count() <-may grab unallocated notes
        help="custom cpu setting. If not set, uses all available",
    )
    return parser.parse_args()
