#!/usr/bin/env python3

"""
Requires python >= 3.9 and pandas and numpy
"""

import argparse
import os
import pandas as pd
import numpy as np
import sys
import glob

parser = argparse.ArgumentParser(description="Create TPM table of ARGs")
parser.add_argument("directory", type=str, help="path to wgsa2 assembly outputs")

args = parser.parse_args()

merged_data = []

directory = args.directory

all_data = []

final_data = []

for sample in os.listdir(directory):

    sampName=sample.removesuffix('_asmb')

    genes = f"functional/genes/{sampName}_PREDgenes_ABUNtab.txt"

    rgi_main = f"functional/RGI/{sampName}_RGI_main.txt"

    ## import gene_TPM
    gene_TPM = pd.read_csv(os.path.join(directory, sample, genes), sep="\t")

    # sanity check
    # gene_TPM.to_csv("checking_TPM_file.csv")

    # import AMR genes
    rgi = pd.read_csv(os.path.join(directory, sample, rgi_main), sep="\t")

    rgi_select = rgi[["ORF_ID", "ARO"]]

    # sanity check
    # rgi_select.to_csv("select_check.tsv", sep="\t")

    # select columns of interest

    rgi_annotation = rgi[
        [
            "ARO",
            "Best_Hit_ARO",
            "AMR Gene Family",
            "Antibiotic",
            "Drug Class",
            "Resistance Mechanism",
        ]
    ]

    all_data.append(rgi_annotation)

    rgi_annotation_all = pd.concat(all_data, ignore_index=True)

    # sanity check
    # rgi_annotation_all.to_csv("rgi_annotations_all.tsv", sep="\t")

    # remove any duplicate annotations from multiple hits per sample (creating fake taxonomy/ARO info)
    rgi_annotation_unique = rgi_annotation_all.drop_duplicates()

    # Add unknown for annotations with NAs
    rgi_annotation_na = rgi_annotation_unique.fillna("Unknown")

    # sanity check
    # rgi_annotation_na.to_csv("rgi_annotations_unique.tsv", sep="\t")

    # format annotations
    rgi_annotation_agg = (
        rgi_annotation_na.groupby("ARO")
        .agg(
            {
                "Best_Hit_ARO": ", ".join,
                "AMR Gene Family": ", ".join,
                "Antibiotic": ", ".join,
                "Drug Class": ", ".join,
                "Resistance Mechanism": ", ".join,
            }
        )
        .reset_index()
    )

    # select columns of interest in gene info files
    gene_TPMselect = gene_TPM[["#name", "iTPM"]]

    # sanity check
    # gene_TPMselect.to_csv("gene_TPMselect.tsv", sep="\t")

    # merge data frames
    merged = rgi_select.merge(gene_TPMselect, left_on="ORF_ID", right_on="#name")

    # sanity check
    # merged.to_csv("merged_rgi_tpm_check.tsv", sep = "\t")

    # remove unnecessary columns that might be making an issue with sum

    pruned = merged.drop(["#name", "ORF_ID"], axis=1)

    # sanity check
    # pruned.to_csv("check_removal.tsv", sep = "\t")

    # move the ARO column to be the names of the rows
    pruned.insert(0, "ARO", pruned.pop("ARO"))

    # sanity check
    # pruned.to_csv("pruned_reorder_test.tsv", sep = "\t")

    # sum by rgi genes
    sum = pruned.groupby(["ARO"]).sum()

    sum_final = sum.rename(columns={"iTPM": sample})

    final_data.append(sum_final)


# merge all samples together
merged_df = final_data[0]

for df in final_data[1:]:
    merged_df = pd.merge(merged_df, df, on="ARO", how="outer")

merged_df.fillna(0, inplace=True)

# export tsv with no descriptions
# merged_df.to_csv("merged_data_raw.tsv", sep= "\t")

# merge annotations with table
merged2 = pd.merge(merged_df, rgi_annotation_agg, on="ARO", how="inner")

# final tsv file
# merged2.to_csv("jointRGI_table.tsv", sep = "\t")
out_dir = glob.glob(os.path.join(directory, "../PWYprofiles/*.MP/merged_tables"))
merged2.to_csv(os.path.join(out_dir[0], "merged_argsTPMtable.txt"), sep="\t")
