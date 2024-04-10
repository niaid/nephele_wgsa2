import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

import sh
from config import pipeline_config
from nephele_pipeline_utils.exceptions import NephelePipelineError
from nephele_pipeline_utils.utils import get_num_cpus, log
from psutil import virtual_memory
from schema import WGSA2Pipeline


def get_samples(samples):
    results = {}
    for sample in samples:
        results[sample.id] = {
            "f": str(sample.forward_fastq_file_path),
            "r": str(sample.reverse_fastq_file_path),
        }
    return json.dumps(results)


def main(args):
    try:
        exit_status = 0
        pipeline = WGSA2Pipeline.from_json(args.json_file_path)
        args = pipeline.pipeline_arguments
        outputs_dir_path = args.outputs_dir_path
        tmp_dir = outputs_dir_path / "tmp"
        log(tmp_dir)
        sh.mkdir("-p", str(tmp_dir))
        num_cpus = get_num_cpus(pipe_args.num_cpus)
        # # for bbmap (avoid heap memory issue)
        mem = virtual_memory()
        mem_gb = int(mem.total / 1024 / 1024 / 1024)
        # Generate mapping file
        mapping_file_path = outputs_dir_path / pipeline_config.mapping_file_name
        # pipeline.generate_mapping_file(mapping_file_path)
        pipeline.generate_mapping_file(mapping_file_path)
        log("Starting WGSA pipeline...")
        # log(args)
        base_command = [
            f"snakemake -p --cores --nocolor",
            f"--resources mem_gb={mem_gb}",
            f"--directory {tmp_dir}",
        ]
        snakemake_config = [
            f"--config num_cpus={num_cpus} map_file={mapping_file_path}",
            f"output_dir={outputs_dir_path} total_mem_gb={mem_gb} tmp_dir={tmp_dir}",
            f"trim_filter={args.trim_filter} include_ted_files={args.include_ted_files} ted_file_name={pipeline_config.ted_file_name}",
            f"biom_file_name={pipeline_config.biom_file_name}",
            f"decontaminate={args.decontaminate_db_path}",
            f"classification_db_name={args.classification_db_name}",
            f"classification_db={args.classification_db_path}",
            f"amrfind={args.amrfind}",
            f"eggnog_db={args.eggnog_db_path}",
            f"annotations_type={args.annotations_type}",
            f"annotations_map={args.annotations_map_db_path}",
            f"annotations_hrr={args.annotations_hrr_db_path}",
            f"tax_genes={args.tax_genes}",
            f"krona_tax_db={args.krona_tax_db_path}",
            f"tax_scaffolds={args.tax_scaffolds}",
            f"mag={args.mag}",
            f"samples='{get_samples(pipeline.samples)}'",
        ]
        if args.trim_filter:
            snakemake_config.extend(
                [
                    f"average_read_quality={args.average_read_quality} min_read_length={args.min_read_length}",
                    f"trim_of_5={args.trim_of_5} trim_of_3={args.trim_of_3}",
                ]
            )
        base_command.extend(snakemake_config)
        main_pipeline = " ".join(base_command)
        log(main_pipeline)
        main_pipeline_args = shlex.split(main_pipeline)
        process = subprocess.run(main_pipeline_args)

        if process.returncode == 1:
            error_message = (
                "There is an error while executing the pipeline. Please see logfile.txt for more information. "
                "Tip: search for keyword, i.e., Error in rule, to figure out which step(s) cause the failure."
            )
            raise NephelePipelineError(error_message)
    except Exception:
        exit_status = 1
        error_msg = f"Pipeline Error:\n{traceback.format_exc()}"
        # explicitly writing to stderr
        print(error_msg, file=sys.stderr, flush=True)
    else:
        log("Pipeline completed")
    finally:
        # Copy output details into main/root output folder
        shutil.copy2(pipeline_config.output_details_file_name, outputs_dir_path)
        sh.rm("-rf", tmp_dir)
        exit(exit_status)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "--version",
        action="version",
        version=pipeline_config.version,
        help="show program's version number and exit",
    )
    PARSER.add_argument(
        "--json_file_path",
        type=Path,
        required=True,
        help=f"Input JSON file",
    )
    ARGS = PARSER.parse_args()
    main(ARGS)
