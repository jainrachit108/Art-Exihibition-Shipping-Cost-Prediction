from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str 

@dataclass
class DataValidationArtifact:
    validated_dataset_path:str 

@dataclass
class DataTransformationArtifact:
  
        Xtrain_dataset_path: str
        Xtest_dataset_path : str
        Ytrain_dataset_path: str
        Ytest_dataset_path: str
        ohe_object_path : str
        
@dataclass
class ModelTrainerArtifact:
    
    model_obj_path : str
    
        