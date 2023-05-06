from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str 

@dataclass
class DataValidationArtifact:
    validated_dataset_path:str 
