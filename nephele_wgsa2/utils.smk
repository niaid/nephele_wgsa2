import csv
import json
import pandas as pd
from functools import reduce
import biom
from biom.cli.util import write_biom_table
import os
from snakemake.io import glob_wildcards

# def read_mapping_file():
#     samples = {}
#     with open(config["map_file"]) as f:
#         reader = csv.DictReader(f, delimiter='\t')
#         for row in reader:
#             if row['#SampleID'] == '':
#                 continue
#             samples[row['#SampleID']] = {}
#             if row.get('ForwardFastqFile'):
#                 samples[row['#SampleID']]["f"] = config["input_dir"] + "/" + row["ForwardFastqFile"]
#             if row.get('ReverseFastqFile'):
#                 samples[row['#SampleID']]["r"] = config["input_dir"] + "/" + row["ReverseFastqFile"]
#     return samples

def get_fastq_gz(wildcards):
    return samples[wildcards.sample]

def get_num_threads_per_job(num_samples):
    num_cpus = config["num_cpus"]
    default_threads_per_job = 16
    return min(max((num_cpus / num_samples), default_threads_per_job), num_cpus)


def run_fastp_cmd():
    average_qual, length_required, cut_front_mean_quality, cut_tail_mean_quality = 10, 60, 20, 15

    base_cmd = (
        "fastp -i {input.f} -I {input.r} "
        "-o {params.f} -O {params.r} "
        "-h {output.html} -j {params.json} "
        "--trim_poly_x --cut_window_size 4 --thread {threads} "
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

    return base_cmd + " " + trim_filter + " 2>> {output.text}"



def asmb_pass(wc):
    return glob_wildcards(ASMB_OUT_SAMPLE_DIR + "_asmb.pass").sample


def make_biom_file(profiles, taxfiles, samples, map_file, biom_file_name, tax_col, prof_col):
    """
    Make biom file from checkm profile and checkm tree_qa taxonomy across
    all samples.

    Args:
        profiles (str): profile filename template with ``{sample}`` substring to format.
        taxfiles (str): bin_TAX filename template with ``{sample}`` substring to format.
        samples (list): list of sample names
        map_file (str): mapping filename
        biom_file_name (str): output biom filename
        tax_col (str): column from bin_TAX to use
        prof_col (str): column from profiles to use

    Returns:
        nothing, but produces biom file named *biom_file_name*.
    """
    def merge_single_profile_tax(profile, taxfile, sample, prof_col, tax_col=tax_col):
        """
        Merge profile.txt and bin_TAX.txt file for single sample, and sum ``prof_col`` by ``tax_col``.
        Returns `pandas.DataFrame` with only 2 columns with tax_col column name replaced
        by sample name.
        """
        prof = pd.read_csv(profile, sep='\t')
        tax = pd.read_csv(taxfile, sep='\t')
        tax = tax.astype({tax_col: str})
        tab = pd.merge(prof, tax, how="left", on="Bin Id")
        tab = tab[[tax_col, prof_col]]
        tab = tab.groupby(tax_col).sum()
        tab.rename(columns={prof_col : sample}, inplace=True)
        return(tab)

    ## merge tables over all samples; format string to ensure files match ANGELINA note I added prof_col.format here 
    tablist = [merge_single_profile_tax(profiles.format(sample=s), taxfiles.format(sample=s), s, prof_col.format(sample=s)) for s in samples]
    if len(samples) > 1:
        mergedtable = reduce(lambda l,r: pd.merge(l,r, how="outer", on=tax_col), tablist)
    else:
        mergedtable = tablist[0]
    mergedtable = mergedtable.rename(index={'nan':'unclassified'}).fillna(0)

    ## make biom https://biom-format.org/documentation/table_objects.html
    observ_ids = [f"O{i}" for i in range(mergedtable.shape[0])]
    observ_metadata = [{ 'taxonomy' : x.split(';')} for x in mergedtable.index]
    biomtab = biom.table.Table(data=mergedtable.to_numpy(),
                               observation_ids=observ_ids,
                               sample_ids=list(mergedtable.columns),
                               observation_metadata=observ_metadata,
                               type="Taxon table")

    ## read in mapping file
    sample_met = biom.parse.MetadataMap.from_file(map_file)
    biomtab.add_metadata(sample_met, axis='sample')
    write_biom_table(biomtab, fmt="json", filepath=biom_file_name) ###"hdf5"


def clean_output():
    asm_bt2      =" ".join(expand(TMP_SAMPLE_DIR + "*.bt2"                 , sample=samples))
    asm_done     =" ".join(expand(ASMB_OUT_SAMPLE_DIR + "*.done"           , sample=samples))
    qc_plots_done=" ".join(expand(QC_PLOTS + "*.done"                      , sample=samples))
    tmp_finAsmb  =" ".join(expand(ASMB_OUT_SAMPLE_DIR + "_tmp_finAsmb.txt" , sample = samples)) ##ASMB_TMP_FINASM_FILE


    command = f"""
    set +o pipefail
    echo "Cleaning output..."
    rm -rf {asm_bt2} {asm_done} {qc_plots_done} {tmp_finAsmb}
    """ 
    return command


def handle_TED():
    if config["include_ted_files"]:
        TED_FILE_NAME = config["output_dir"] + "/" + config["ted_file_name"]


        command = f"""
        if [ -d {TED_READS_FQS} ] && [ "$(ls -A {TED_READS_FQS})" ]
        then
        tar -cf {TED_FILE_NAME} -C {config["output_dir"]} {TED_READS_FQS_NAME}
        rm -rf {TED_READS_FQS}
        fi
        """
    else:
        command = f"""
        rm -rf {TED_READS_FQS}
        """
    return command

def handle_cp_biom():
    """
    If >=2 samples are provided, step 9 will run and we use biom from step 9 for MicrobiomeDB
    If only 1 sample is provided, we use biom from tax_biom_per_sample for MicrobiomeDB
    """
    # tax_merged_biom = "{rules.TAX_collation_biom.output}"
    tax_merged_biom = TAX_MERGED_TABLES + "merged_Counts+Lineage_json.biom"
    tax_single_biom = expand(TAXBIOM + "{sample}_json.biom", sample=samples)
    cmd = "echo No biom file for MicrobiomeDB is available"

    if os.path.exists(tax_merged_biom):
        cmd = f"cp {tax_merged_biom} {BIOM_FILE_MICROBIOMEDB}"
    elif len(tax_single_biom) == 1 and os.path.exists(tax_single_biom[0]):
        cmd = f"cp {tax_single_biom[0]} {BIOM_FILE_MICROBIOMEDB}"
    return cmd


def fwd_outputs():
    asm_bam=" ".join(expand(ASMB_OUT_SAMPLE_FILE + "_asmbFinal.bam"    , sample=samples))
    asm_bai=" ".join(expand(ASMB_OUT_SAMPLE_FILE + "_asmbFinal.bam.bai", sample=samples))
    asm_fas=" ".join(expand(ASMB_OUT_SAMPLE_FILE + "_asmbFinal.fasta"  , sample=samples))
    asm_dep=" ".join(expand(ASMB_OUT_SAMPLE_FILE + "_asmbDepths.txt"   , sample=samples))
    asmbDIR = config["output_dir"] + ("/asmbMTX/" if config["denovo_mtx"] else "/asmbMGX/")
    FWD_DIR = config["output_dir"] + "/asmb_files/"

    command = f"""

    echo "---> moving FASTA & BAM files from assembly to {FWD_DIR} "

    mkdir -p {FWD_DIR}
    mv {asm_bam} {FWD_DIR} && mv {asm_bai} {FWD_DIR}
    cp {asm_fas} {FWD_DIR} && cp {asm_dep} {FWD_DIR}

    list=$(ls -1 {FWD_DIR}/*.bam |xargs basename -a -s _asmbFinal.bam)

    for i in ${{list}}; do
    echo "---> links to create ${{i}}"
        ln -rs {FWD_DIR}/${{i}}_asmbFinal.bam        {asmbDIR}/${{i}}_asmb/${{i}}_asmbFinal.bam
        ln -rs {FWD_DIR}/${{i}}_asmbFinal.bam.bai    {asmbDIR}/${{i}}_asmb/${{i}}_asmbFinal.bam.bai
        # ln -rs {FWD_DIR}/${{i}}_asmbFinal.fasta    {asmbDIR}/${{i}}_asmb/${{i}}_asmbFinal.fasta
        # ln -rs {FWD_DIR}/${{i}}_asmbDepths.txt     {asmbDIR}/${{i}}_asmb/${{i}}_asmbDepths.txt
    done
    """
    return command
