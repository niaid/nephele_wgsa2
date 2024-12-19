from nephele_pipeline_utils.enums import StrEnum


class ClassificationDbType(StrEnum):
    PLUSPFV = "plusPFV"
    MGBCDB = "MGBCdb"
    EUPATHDB = "EuPATHdb"


class AnnotationsType(StrEnum):
    KO = "ko"
    EC = "ec"
