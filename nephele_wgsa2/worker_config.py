from nephele_pipeline_utils.enums import pn

config = dict(
    downstream_pipelines={
        r".*asmb_files/.*_asmbFinal\.bam": {pn.DISCOVIR.value},
        r".*asmb_files/.*_asmbFinal\.fasta": {pn.DISCOVIR.value},
        r".*for_microbiomedb\.biom": {pn.DOWNSTREAM_ANALYSIS.value},
        r".*TAXprofiles/readsTAX_.*/merged_tables/merged_Counts\+Lineage\.txt": {
            pn.DATASET_MERGER.value
        },
        r".*PWYprofiles/.*PWYs.MP/merged_tables/merged_Counts\+allTiers\.txt": {
            pn.DATASET_MERGER.value
        },
        r".*PWYprofiles/.*PWYs.MP/merged_tables/merged_geneTPMtable\.txt": {
            pn.DATASET_MERGER.value
        },
    },
    output_blacklisted_files=["TED.tar"],
)
