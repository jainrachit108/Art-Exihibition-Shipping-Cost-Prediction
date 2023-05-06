from ShippingCost import utils
from ShippingCost.exception import ShippingException
import sys, os
from datetime import datetime
import pandas as pd
TRAINING_FILE_NAME = 'training_file.csv'
VALIDATED_FILE_NAME = 'validated_dataset.csv'
class TrainingPipelineConfig:
    
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise ShippingException(e,sys)

class DataIngestionConfig:
    
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name = 'Art_Exibition_Shipping_cost'
            self.collection_name  = 'Shipping_Cost_dataset'
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_ingestion')
            self.training_file_path = os.path.join(self.data_ingestion_dir, 'Training dataset', TRAINING_FILE_NAME)

        except Exception as e:
            raise ShippingException
        
        
    def to_dict(self):
        try:
            return self.__dict__
        except Exception as e:
            raise ShippingException
        
        
class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        try:
            #if 50% of data in any feature is missing, it is dropped
            self.max_missing_features = 0.5 
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data validation")
            self.validated_dataset_path = os.path.join(self.data_validation_dir, 'Validated dataset', VALIDATED_FILE_NAME)               
            
        except Exception as e:
            ShippingException(e, sys)