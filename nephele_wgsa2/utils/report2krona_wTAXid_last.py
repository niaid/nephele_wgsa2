#!/usr/bin/env python3
####################################################################
# kreport2krona.py converts a Kraken-style report into Krona-compatible format
# Copyright (C) 2019-2020 Jennifer Lu, jennifer.lu717@gmail.com

# This file is part of KrakenTools.
# KrakenTools is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the license, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

####################################################################
# Jennifer Lu, jlu26@jhmi.edu
# Updated: 05/30/2019
#
# This program reads in a Kraken report file and generates
# a Krona-compatible Text report that can be imported into Krona using ktImportText.
#
# Parameters:
#   -h, --help...............show help message
#   -r X, --report-file X....input kraken report filename
#   -o X, --output X.........output Krona text filename
#   --intermediate-ranks.....include non-traditional taxonomic ranks
#   --no-intermediate-ranks..do not include non-traditional ranks [default]
# Input file format (tab-delimited)
#   - percentage of total reads
#   - number of reads (including reads within subtree)
#   - number of reads (only at this level)
#   - taxonomic classification of level (U, D, P, C, O, F, G, S,...etc)
#   - NCBI taxonomic ID
#   - name of level
# Output file format (tab-delimited)
#   - Number of reads within subtree of the specified level
#   - Taxonomy tree levels tab-delimited, with level type [k,p,c,o,f,g,s,x]
#
# Methods
#   - main
#   - process_kraken_report
####################################################################
# Poorani Subramanian, github.com/pooranis
# Modified 05/20/2022
# Made to work with output of Nephele WGSA2 pipeline.  operates
# on directory of kraken reports and can merge the output.

import argparse

####################################################################
import os
import re
import sys
import traceback


####################################################################
# process_kraken_report
# usage: parses a single line in the kraken report and extracts relevant information
# input: kraken report file with the following tab delimited lines
#   - percent of total reads
#   - number of reads (including at lower levels)
#   - number of reads (only at this level)
#   - taxonomy classification of level
#       (U, D, P, C, O, F, G, S, -)
#   - taxonomy ID (0 = unclassified, 1 = root, 2 = Bacteria,...etc)
#   - spaces + name
# returns:
#   - classification/genome name
#   - level name (U, -, D, P, C, O, F, G, S)
#   - reads classified at this level and below in the tree
def process_kraken_report(curr_str):
    split_str = curr_str.strip().split("\t")
    # if len(split_str) < 2:
    #    return []
    try:
        int(split_str[1])
    except ValueError:
        return []
    all_reads = int(split_str[1])
    lvl_reads = int(split_str[2])
    taxid = split_str[4]
    level_type = split_str[-3]
    type2main = {
        "superkingdom": "D",
        "phylum": "P",
        "class": "C",
        "order": "O",
        "family": "F",
        "genus": "G",
        "species": "S",
    }
    if len(level_type) > 1:
        if level_type in type2main:
            level_type = type2main[level_type]
        else:
            level_type = "-"
    # Get name and spaces
    spaces = 0
    name = split_str[-1]
    for char in name:
        if char == " ":
            name = name[1:]
            spaces += 1
        else:
            break
    name = name.replace(" ", "_")
    # Determine level based on number of spaces
    level_num = spaces / 2
    return [name, level_num, level_type, lvl_reads, taxid]  ## amended line


###################################################################
# kreport2krona_all
# usage: prints all levels for a kraken report
# input: kraken report file and output krona file names
# returns: none
def kreport2krona_all(report_file, out_file):
    # Process report file and output
    curr_path = []
    prev_lvl_num = -1
    r_file = open(report_file, "r")
    o_file = open(out_file, "w")
    # Read through report file
    main_lvls = ["D", "P", "C", "O", "F", "G", "S"]
    for line in r_file:
        report_vals = process_kraken_report(line)
        # If header line, skip
        if len(report_vals) < 5:
            continue
        # Get relevant information from the line
        [name, level_num, level_type, lvl_reads] = report_vals
        if level_type == "U":
            o_file.write(str(lvl_reads) + "\tUnclassified\n")
            continue
        # Create level name
        if level_type not in main_lvls:
            level_type = "x"
        elif level_type == "D":
            level_type = "K"
        level_str = level_type.lower() + "__" + name
        # Determine full string to add
        if prev_lvl_num == -1:
            # First level
            prev_lvl_num = level_num
            curr_path.append(level_str)
            o_file.write(str(lvl_reads) + "\t" + level_str + "\n")
        else:
            o_file.write(str(lvl_reads))
            # Move back if needed
            while level_num != (prev_lvl_num + 1):
                prev_lvl_num -= 1
                curr_path.pop()
            # Print all ancestors of current level followed by |
            for string in curr_path:
                if string[0] != "r":
                    o_file.write("\t" + string)
            # Print final level and then number of reads
            o_file.write("\t" + level_str + "\n")
            # Update
            curr_path.append(level_str)
            prev_lvl_num = level_num
    o_file.close()
    r_file.close()


### PRNi: find element of path mynames that begins with taxlevel string levelpre
### AA: Error " unexpected indent" from the try line here. Removed "" from comments
def match_taxlevels(mynames, levelpre):
    try:
        taxname = [i for i in mynames if i.startswith(levelpre)][0]
    except IndexError:
        taxname = ""
    return taxname


###################################################################
# kreport2krona_main
# usage: prints only main taxonomy levels for a kraken report
# input: kraken report file and output krona file names
# returns: none
def kreport2krona_main(report_file, out_file, tax_exclude):
    # Process report file and output
    main_lvls = ["D", "P", "C", "O", "F", "G", "S"]
    level_strings = ["k__", "p__", "c__", "o__", "f__", "g__", "s__"]
    curr_path = []
    prev_lvl_num = -1
    num2path = {}
    path2reads = {}
    num2taxid = {}
    line_num = -1
    # Read through report file
    r_file = open(report_file, "r")
    for line in r_file:
        line_num += 1
        #########################################
        report_vals = process_kraken_report(line)
        # If header line, skip
        if len(report_vals) < 5:
            continue
        # Get relevant information from the line
        [name, level_num, level_type, lvl_reads, taxid] = report_vals
        if level_type == "U":
            num2path[line_num] = ["k__Unclassified"]
            num2taxid[line_num] = "0"
            path2reads["k__Unclassified"] = lvl_reads
            continue
        #########################################
        # Create level name
        if level_type not in main_lvls:
            level_type = "x"
        elif level_type == "D":
            level_type = "K"
        level_str = level_type.lower() + "__" + name
        #########################################
        # Determine full string to add
        if prev_lvl_num == -1:
            # First level
            prev_lvl_num = level_num
            curr_path.append(level_str)
            # Save
            if curr_path[-1][0] == "x":
                num2path[line_num] = ""
                num2taxid[line_num] = "1"
            else:
                path2reads[curr_path[-1]] = lvl_reads
                num2path[line_num] = []
                num2taxid[line_num] = taxid
                for i in curr_path:
                    num2path[line_num].append(i)
            continue
        else:
            #########################################
            # Move back if needed
            while level_num != (prev_lvl_num + 1):
                prev_lvl_num -= 1
                curr_path.pop()
            # Update the list
            curr_path.append(level_str)
            prev_lvl_num = level_num
            #########################################
            # IF AT NON-TRADITIONAL LEVEL, ADD TO PARENT
            if level_type == "x":
                test_num = len(curr_path) - 1
                while test_num >= 0:
                    if curr_path[test_num][0] != "x":
                        path2reads[curr_path[test_num]] += lvl_reads
                        test_num = -1
                    test_num = test_num - 1
                num2path[line_num] = ""
                num2taxid[line_num] = "1"
            # IF AT TRADITIONAL LEVEL, SAVE
            if level_type != "x":
                path2reads[curr_path[-1]] = lvl_reads
                num2path[line_num] = []
                num2taxid[line_num] = taxid
                for i in curr_path:
                    num2path[line_num].append(i)
    r_file.close()

    # WRITE OUTPUT FILE
    o_file = open(out_file, "w")
    ## print header
    samplename = os.path.basename(report_file).replace("_taxREPORT.txt", "")
    o_file.write("#")  ## AA: hash the first line, for kronaPlot
    o_file.write(
        "\t".join(
            [
                samplename,
                "kingdom",
                "phylum",
                "class",
                "order",
                "family",
                "genus",
                "species",
                "taxid",
            ]
        )
    )
    o_file.write("\n")
    for i in range(0, line_num + 1):
        # Get values
        if i not in num2path:
            continue
        curr_path = num2path[i]
        if len(curr_path) > 0:
            curr_reads = path2reads[curr_path[-1]]
            if curr_path[-1][0] != "x":
                o_file.write("%i" % curr_reads)
                # o_file.write(f"\t{num2taxid[i]}") ## AA: we dont want taxID as second column
            for l in range(0, len(main_lvls)):
                name = match_taxlevels(curr_path, level_strings[l])
                if tax_exclude:
                    name = re.sub("^[kpcofgs]__", "", name)
                o_file.write("\t%s" % name)
            if (
                curr_path[-1][0] != "x"
            ):  ## AA: we want taxID as last column (better KronaPlot)
                o_file.write(f"\t{num2taxid[i]}")
            o_file.write("\n")
    o_file.close()


## PRNi  merges input_files on taxid and taxonomy and outputs tsv to merged_file
def merge_tables(input_files, merged_file):
    from functools import reduce

    import pandas as pd

    dfs = [pd.read_csv(f, sep="\t") for f in input_files]

    merge_cols = [
        "kingdom",
        "phylum",
        "class",
        "order",
        "family",
        "genus",
        "species",
        "taxid",
    ]
    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on=merge_cols, how="outer"), dfs
    )
    ## move taxonomy to beginning of file - might be slow
    df_merged = df_merged[
        merge_cols + [col for col in df_merged.columns if col not in merge_cols]
    ]

    ## make sample columns ints as they are counts and shouldn't have decimal:
    sample_cols = list(set(df_merged.columns) - set(merge_cols))
    df_merged[sample_cols] = df_merged[sample_cols].astype("Int64")

    df_merged.to_csv(merged_file, sep="\t", index=False)


######################################################################
# Main method
def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="""This script is modified to specifically parse the
    kraken reports output from Nephele's WGSA2 pipeline, i.e. TAXprofiles/TEDreadsTAX/reports/*_taxREPORT.txt."""
    )

    req = parser.add_argument_group("required arguments")
    inputr = req.add_mutually_exclusive_group(required=True)
    inputr.add_argument(
        "-r",
        "--report-file",
        dest="r_file",
        help="Input kraken report file for converting",
    )
    inputr.add_argument(
        "-d",
        "--report-dir",
        dest="r_dir",
        help="Input directory containing kraken report files for converting.  All files in the directory will be attempted to convert.  Must specify either --report-file or --report-dir (not both).  Will produce filenames ending in *_wTAXid_4krona.txt.",
    )
    req.add_argument(
        "-o",
        "--output",
        required=True,
        dest="o_file",
        help="Output krona-report file name (if using --report-file input) or output directory (if using --report-dir input).  For the latter, the output directory must exist.",
    )
    parser.add_argument(
        "--intermediate-ranks",
        action="store_true",
        dest="x_include",
        default=False,
        required=False,
        help="Include non-traditional taxonomic ranks in output",
    )
    parser.add_argument(
        "--no-intermediate-ranks",
        action="store_false",
        dest="x_include",
        default=False,
        required=False,
        help="Do not include non-traditional taxonomic ranks in output [default: no intermediate ranks]",
    )
    parser.add_argument(
        "--no-tax-prefixes",
        action="store_true",
        dest="tax_exclude",
        default=False,
        required=False,
        help='Do not include taxonomy prefixes, e.g. "k__, p__" only works if using the default --no-intermediate-ranks',
    )
    parser.add_argument(
        "-m",
        "--merge",
        dest="m_file",
        help="Merge converted files and output to this filename.  Merging only works with --report-dir and without intermediate ranks for now.  Must have pandas installed.",
    )
    parser._action_groups.reverse()
    args = parser.parse_args()

    print(args, file=sys.stderr)

    if args.m_file and args.r_file:
        print(
            "ERROR: --report-file and --merge are incompatible.  Exiting",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.r_dir:
        if not os.path.isdir(args.r_dir):
            print(
                "ERROR:",
                args.r_dir,
                "is not a directory or does not exist.  Exiting.",
                file=sys.stderr,
            )
            sys.exit(1)
        if not os.path.isdir(args.o_file):
            print(
                "ERROR:",
                args.o_file,
                "is not a directory or does not exist.  Exiting.",
                file=sys.stderr,
            )
            sys.exit(1)
        ## list objects in directory and get just the files
        r_files = [os.path.join(args.r_dir, f) for f in os.listdir(args.r_dir)]
        r_files = [f for f in r_files if os.path.isfile(f)]
        o_files = [
            os.path.join(
                args.o_file,
                os.path.basename(f).replace("_taxREPORT.txt", "")
                + "_wTAXid_4krona.txt",
            )
            for f in r_files
        ]
    else:
        r_files = [args.r_file]
        o_files = [args.o_file]

    for r in range(0, len(r_files)):
        try:
            # Determine which krona report to make
            if args.x_include:
                kreport2krona_all(r_files[r], o_files[r])
            else:
                kreport2krona_main(r_files[r], o_files[r], args.tax_exclude)
        except Exception as e:
            if args.r_file:
                traceback.print_exc(file=sys.stderr)
                sys.exit(1)
            print("ERROR converting file:", r_files[r], e, file=sys.stderr)
            print(
                "For full traceback try converting the file by itself with --report-file.  Converting next file.",
                file=sys.stderr,
            )
            continue

    ## merge converted files
    if args.m_file:
        ## look for files that successfully converted
        good_o_files = list(
            set(
                [
                    os.path.join(args.o_file, f)
                    for f in os.listdir(args.o_file)
                    if os.path.isfile(os.path.join(args.o_file, f))
                ]
            )
            & set(o_files)
        )
        if len(good_o_files) < 2:
            print(
                "WARNING: At least 2 successfully converted files needed to merge.  No merged file made.",
                file=sys.stderr,
            )
            sys.exit(0)

        merge_tables(good_o_files, args.m_file)


#################################################################
if __name__ == "__main__":
    main()
#########################END OF PROGRAM##########################
