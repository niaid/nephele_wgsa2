from nephele_pipeline_utils.io import PipelineArguments, PipelinePE, StrEnum
from pydantic import DirectoryPath, Field, FilePath


class ClassificationDbType(StrEnum):
    PLUSPFV = "plusPFV"
    MGBCDB = "MGBCdb"
    EUPATHDB = "EuPATHdb"


class AnnotationsType(StrEnum):
    KO = "ko"
    EC = "ec"


class PipelineArguments(PipelineArguments):
    decontaminate_db_path: DirectoryPath
    classification_db_name: ClassificationDbType
    classification_db_path: DirectoryPath
    eggnog_db_path: DirectoryPath
    annotations_type: AnnotationsType
    annotations_map_db_path: FilePath
    annotations_hrr_db_path: FilePath
    krona_tax_db_path: DirectoryPath
    amrfind: bool = False
    tax_genes: bool = False
    tax_scaffolds: bool = False
    mag: bool = False
    trim_filter: bool = False
    average_read_quality: int = Field(default=10, ge=0, le=35)
    min_read_length: int = Field(default=60, ge=0, le=150)
    trim_of_5: int = Field(default=20, ge=0, le=35)
    trim_of_3: int = Field(default=15, ge=0, le=35)
    include_ted_files: bool = False


class WGSA2Pipeline(PipelinePE):
    pipeline_arguments: PipelineArguments
