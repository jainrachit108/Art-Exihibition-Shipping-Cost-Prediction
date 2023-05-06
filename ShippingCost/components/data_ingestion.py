import pandas as pd
import numpy as np
from ShippingCost import utils
from ShippingCost.entity import config_entity
from ShippingCost.exception import ShippingException
import sys, os
from ShippingCost.logger import logging
from ShippingCost.entity import artifact_entity


class DataIngestion:
    
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig) -> artifact_entity.DataIngestionArtifact:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ShippingException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            logging.info('Extracting dataset from mongodb')
            df: pd.DataFrame = utils.get_collection_as_dataFrame(self.data_ingestion_config.database_name, self.data_ingestion_config.collection_name)
            logging.info('Extracted Dataset successfully')
            logging.info('Creating data ingestion artifact folder to store training dataset')
            train_file_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(train_file_dir, exist_ok=True)
            logging.info('Loading dataset into data ingestion artifact folder')
            df.to_csv(path_or_buf=self.data_ingestion_config.training_file_path, index = False, header = True)
            logging.info('Successfully Loaded Data info the given directory')
            
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path)
            logging.info(f'Data ingestion Artifact {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            raise ShippingException(e, sys)