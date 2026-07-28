# Run with apptainer

1. Create a `nephele_wgsa2` directory and enter the directory. And, within `nephele_wgsa2` directory, create dbs, inputs, outputs and tmp directories.
```
mkdir nephele_wgsa2
cd nephele_wgsa2

mkdir -p inputs
mkdir -p outputs
mkdir -p dbs
mkdir -p tmp
```

2. Put the mapping file, and .fastq.gz files within `$(pwd)/inputs` directory. For running the image directly, the mapping file has to be tab delimited csv, the name of the sample id field has to be #SampleID, and the file names in the csv has to have input directory as prefix, such as, /inputs/22057_S2_R1_subsample.fastq.gz. Put the dbs within the dbs directory.

3. From within the previously created `nephele_wgsa2` directory, pull image.
```
apptainer pull nephele_wgsa2.sif docker://public.ecr.aws/niaid_nephele/pipeline/nephele_wgsa2:latest
```

4. From within the previously created `nephele_wgsa2` directory, run image.
```
apptainer run \
    -B $(pwd)/inputs:/inputs -B $(pwd)/outputs:/outputs -B $(pwd)/dbs:/dbs -B $(pwd)/tmp:/tmp \
    --contain --pwd /pipeline \
    --writable-tmpfs \
    nephele_wgsa2.sif \
    --mapping_file_path /inputs/mapping_file.csv \
    --decontaminate_db_path /dbs/wgsa2/decontam_db/decontam_human+mouse_db \
    --kr2confidence_host 0.05 \
    --classification_db_name plusPFV \
    --kr2confidence_taxonomic 0.15 \
    --classification_db_path /dbs/wgsa2plus_lora/plus_PFV_Oct2025 \
    --eggnog_db_path /dbs/wgsa2/eggnog_data \
    --annotations_type ko \
    --annotations_map_db_path /dbs/lora/minpath_data/KEGGdb_0624/KEGGpwy-ko2map_0624.txt \
    --annotations_hrr_db_path /dbs/lora/minpath_data/KEGGdb_0624/KEGGhrr_brite_0624.txt \
    --krona_tax_db_path /dbs/wgsa2/KronaTools_taxonomy \
    --find_args False \
    --read_norm False \
    --readCoverage 50 \
    --denovo_mtx False \
    --tax_genes False \
    --tax_scaffolds False \
    --mag False \
    --include_ted_files True \
    --trim_filter False \
    --average_read_quality 10 \
    --min_read_length 60 \
    --trim_of_5 20 \
    --trim_of_3 15
```