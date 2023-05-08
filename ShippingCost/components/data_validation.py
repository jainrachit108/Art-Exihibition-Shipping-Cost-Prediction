from ShippingCost.entity import config_entity
from ShippingCost.entity import artifact_entity
import sys, os
from ShippingCost.logger import logging
from ShippingCost.exception import ShippingException
import pandas as pd

class DataValidation:
    def __init__(self, 
                 data_validation_config: config_entity.DataValidationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact) -> None:
        try:
            logging.info(f"{'<<'*20}Data Validation{'>>'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            
        except Exception as e:
            raise ShippingException(e, sys)
        
    def drop_missing_values_columns(self, df:pd.DataFrame):
        try:
            logging.info('Checking for columns with missing values greater than 50%')
            threshold = self.data_validation_config.max_missing_features 
            missing_values = df.isna().sum()/df.shape[0]
            drop_col_names = missing_values[missing_values>threshold].index
            logging.info(f"Found missing values greater than 50% in {len(drop_col_names)} : {list(drop_col_names)}")
            if len(drop_col_names)>0:
                df.drop(list(drop_col_names), axis=1, inplace=True)
            return df
        except Exception as e:
            ShippingException(e, sys)
            
    def initiate_data_validation(self):
        try:
            logging.info('Getting dataset for validation')
            df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info('Checking for missing values in dataframe')
            df_validated = self.drop_missing_values_columns(df)
            logging.info('Successfully Validated the dataset')
            logging.info('Storing the validated dataset in artifacts folder')
            validated_file_dir = os.path.dirname(self.data_validation_config.validated_dataset_path)
            os.makedirs(validated_file_dir, exist_ok=True)
            df_validated.to_csv(path_or_buf = self.data_validation_config.validated_dataset_path)
            logging.info('Saving validate dataset path in artifact')
            data_validation_artifact = artifact_entity.DataValidationArtifact(validated_dataset_path=self.data_validation_config.validated_dataset_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            ShippingException(e, sys)
