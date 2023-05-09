from ShippingCost import utils
from ShippingCost.exception import ShippingException
import sys, os
from datetime import datetime
import pandas as pd
import shutil
TRAINING_FILE_NAME = 'training_file.csv'
VALIDATED_FILE_NAME = 'validated_dataset.csv'
X_TRAIN_DATA = 'X_train.npz'
X_TEST_DATA = 'X_test.npz'
Y_TRAIN_DATA = 'Y_train.npz'
Y_TEST_DATA = 'Y_test.npz'
OHE_OBJ_FILE = 'ohe_obj.pkl'
MODEL_OBJ_FILE = 'model.pkl'
SCALER_OBJ_FILE = 'scaler.pkl'
dir_path = 'artifact'

class TrainingPipelineConfig:
    
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), dir_path)
            if os.path.exists(dir_path):
                # If it exists, remove it and its contents
                shutil.rmtree(dir_path)
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
            raise ShippingException(e, sys)
        
class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) -> None:
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_transformation")
            self.Xtrain_dataset_path = os.path.join(self.data_transformation_dir,'X_train array',X_TRAIN_DATA)
            self.Xtest_dataset_path = os.path.join(self.data_transformation_dir,'X_test array',  X_TEST_DATA)
            self.Ytrain_dataset_path = os.path.join(self.data_transformation_dir,'Y_train array', Y_TRAIN_DATA)
            self.Ytest_dataset_path = os.path.join(self.data_transformation_dir,'Y_test array', Y_TEST_DATA)
            self.ohe_object_path = os.path.join(self.data_transformation_dir, 'ohe object', OHE_OBJ_FILE)
            self.scaler_object_path = os.path.join(self.data_transformation_dir, 'scaler_object', SCALER_OBJ_FILE)
        except Exception as e:
            raise ShippingException(e, sys)
            
class ModelTrainingConfig:
    def __init__(self, training_pipeline_config : TrainingPipelineConfig) -> None:
        try:
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir, 'Model trainer')
            self.model_obj_path = os.path.join(self.model_trainer_dir, 'model_object', MODEL_OBJ_FILE)
            
            
        except Exception as e:
            raise ShippingException(e ,sys)