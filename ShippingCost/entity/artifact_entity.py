from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str 

@dataclass
class DataValidationArtifact:
    validated_dataset_path:str 

@dataclass
class DataTransformationArtifact:
    X_train_array_path : str
    X_test_array_path : str
    y_train_array_path : str
    y_test_array_path : str
        