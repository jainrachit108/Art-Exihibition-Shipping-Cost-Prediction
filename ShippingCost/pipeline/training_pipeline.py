from ShippingCost.logger import logging
from ShippingCost.exception import ShippingException
import sys, os
from ShippingCost import utils
from ShippingCost.components.data_ingestion import DataIngestion
from ShippingCost.entity import config_entity, artifact_entity


def start_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())

        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        

    except Exception as e:
        raise ShippingException(e, sys)

