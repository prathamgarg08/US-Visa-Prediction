# Return output of data ingestion component

from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str