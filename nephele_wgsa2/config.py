from nephele_pipeline_utils.config import SharedConfig


class WGSA2Config(SharedConfig):
    mapping_file_name: str
    output_details_file_name: str
    ted_file_name: str
    biom_file_name: str


pipeline_config = WGSA2Config.from_json("./config.json")
