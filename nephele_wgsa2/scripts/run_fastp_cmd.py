from nephele_pipeline_utils.utils import exec_cmnd

config = snakemake.config
snakemake_input = snakemake.input
output = snakemake.output
params = snakemake.params
threads = snakemake.threads


def get_fastp_cmd():
    average_qual, length_required, cut_front_mean_quality, cut_tail_mean_quality = (
        10,
        60,
        20,
        15,
    )

    base_cmd = (
        f"fastp -i {snakemake_input.f} -I {snakemake_input.r} "
        f"fastp -i {snakemake_input.f} -I {snakemake_input.r} "
        f"-o {params.f} -O {params.r} "
        f"-h {output.html} -j {params.json} "
        f"--trim_poly_x --cut_window_size 4 --thread {threads} "
        "--low_complexity_filter --correction"
    )

    if config["trim_filter"]:
        average_qual = config["average_read_quality"]
        length_required = config["min_read_length"]
        cut_front_mean_quality = config["trim_of_5"]
        cut_tail_mean_quality = config["trim_of_3"]

    trim_filter = (
        f"--average_qual {average_qual} "
        f"--length_required {length_required} "
        f"--cut_front --cut_front_mean_quality {cut_front_mean_quality} "
        f"--cut_tail --cut_tail_mean_quality {cut_tail_mean_quality}"
    )

    return f"{base_cmd} {trim_filter} 2>> {output.text}"


if __name__ == "__main__":
    exec_cmnd(f"mkdir -p {params.tmpdir} ")
    exec_cmnd(get_fastp_cmd())
