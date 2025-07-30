import os
import shlex
import shutil
import subprocess
import traceback

from psutil import virtual_memory
import sh

from nephele_pipeline_utils.decorators import pre_post_step
from nephele_pipeline_utils.exceptions import NephelePipelineError
from nephele_pipeline_utils.utils import log

from config import pipeline_config
from parser import parser, parse_args

print("Demonstration of Workflow Actions -- Katie")

def post_clean_up(args):
    try:
        # Copy output details into main/root output folder
        shutil.copy2(pipeline_config.output_details_file_name, args.outputs_dir_path)
        sh.rm("-rf", args.outputs_dir_path / "tmp")
    except Exception:
        log(f"Warning: {traceback.format_exc()}")


@pre_post_step(parse_args, pipeline_config, post_clean_up)
def main(args):
    outputs_dir_path = args.outputs_dir_path
    tmp_dir = outputs_dir_path / "tmp"
    sh.mkdir("-p", str(tmp_dir))
    num_cpus = os.cpu_count()
    if num_cpus > 48:
        num_cpus = int(num_cpus / 1.25)
    # # for bbmap (avoid heap memory issue)
    mem = virtual_memory()
    mem_gb = int(mem.total / 1024 / 1024 / 1024)

    samples = parser.get_samples_files(
        {"f": "ForwardFastqFile", "r": "ReverseFastqFile"}
    )

    log("Starting WGSA pipeline...")
    # log(args)
    base_command = [
        "snakemake -p --cores --nocolor --use-conda",
        f"--resources mem_gb={mem_gb}",
        f"--directory {tmp_dir}",
    ]
    snakemake_config = [
        f"--config num_cpus={num_cpus} map_file={args.mapping_file_path}",
        f"output_dir={outputs_dir_path} total_mem_gb={mem_gb} tmp_dir={tmp_dir}",
        f"trim_filter={args.trim_filter} include_ted_files={args.include_ted_files} ted_file_name={pipeline_config.ted_file_name}",
        f"biom_file_name={pipeline_config.biom_file_name}",
        f"decontaminate={args.decontaminate_db_path}",
        f"classification_db_name={args.classification_db_name}",
        f"classification_db={args.classification_db_path}",
        f"amrfind={args.amrfind}",
        f"denovo_mtx={args.denovo_mtx}",
        f"eggnog_db={args.eggnog_db_path}",
        f"annotations_type={args.annotations_type}",
        f"annotations_map={args.annotations_map_db_path}",
        f"annotations_hrr={args.annotations_hrr_db_path}",
        f"tax_genes={args.tax_genes}",
        f"krona_tax_db={args.krona_tax_db_path}",
        f"tax_scaffolds={args.tax_scaffolds}",
        f"mag={args.mag}",
        f"samples='{samples}'",
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


if __name__ == "__main__":
    main()
