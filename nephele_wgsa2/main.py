import os
import shutil
import traceback

from psutil import virtual_memory
import sh

from nephele_pipeline_utils.decorators import pre_post_step
from nephele_pipeline_utils.utils import log, exec_cmnd

from config import pipeline_config
from parser import parser, parse_args


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
        "snakemake -p --cores --nocolor --use-conda --rerun-incomplete --forcerun PWY_collation",
        f"--resources mem_gb={mem_gb} --keep-going --keep-incomplete", ## --notemp", ##--reason --summary",
        f"--directory {tmp_dir} --latency-wait 10 --rerun-triggers code params",
    ]
    snakemake_config = [
        f"--config num_cpus={num_cpus} map_file={args.mapping_file_path}",
        f"output_dir={outputs_dir_path} total_mem_gb={mem_gb} tmp_dir={tmp_dir}",
        f"trim_filter={args.trim_filter} include_ted_files={args.include_ted_files}",
        f"ted_file_name={pipeline_config.ted_file_name}",
        f"biom_file_name={pipeline_config.biom_file_name}",
        f"decontaminate={args.decontaminate_db_path}",
        f"kr2confidence_host={args.kr2confidence_host}",
        f"classification_db_name={args.classification_db_name}",
        f"classification_db={args.classification_db_path}",
        f"kr2confidence_taxonomic={args.kr2confidence_taxonomic}",
        f"find_args={args.find_args}",
        f"read_norm={args.read_norm}",
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
    if args.read_norm:
        snakemake_config.extend(
            [
                f"readCoverage={args.readCoverage}",
            ]
        )
    if args.find_args:
        snakemake_config.extend(
            [
                f"args_db_path={args.args_db_path}",
            ]
        )

    base_command.extend(snakemake_config)
    main_pipeline = " ".join(base_command)
    exec_cmnd(main_pipeline)


if __name__ == "__main__":
    main()
