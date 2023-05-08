from ShippingCost.logger import logging
from ShippingCost.exception import ShippingException
import sys, os
from ShippingCost import utils
from ShippingCost.components.data_ingestion import DataIngestion
from ShippingCost.entity import config_entity, artifact_entity
from ShippingCost.components.data_validation import DataValidation
from ShippingCost.components.data_transformation import DataTransformation
from ShippingCost.components.model_training import ModelTrainer


def start_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())

        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation =  DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation() 
        
        
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_tranformation = DataTransformation(data_transformation_config=data_transformation_config, data_validation_artifact= data_validation_artifact)
        data_tranformation_artifact = data_tranformation.initiate_data_transformation()
    
        model_trainer_config = config_entity.ModelTrainingConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(data_transformation_artifact=data_tranformation_artifact, model_training_config=model_trainer_config)
        model_trainer_artifact = model_trainer.initiate_model_training()
        
        
    except Exception as e:
        raise ShippingException(e, sys)

