from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
import sys
from us_visa.entity.config_entity import (DataIngestionConfig,DataValidationConfig)
from us_visa.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact)
from us_visa.exception import USVisaException
from us_visa.logger import logging

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
    
    def start_data_ingestion(self)->DataIngestionArtifact:

        try:
            logging.info('Entered the start data ingestion method of trainpipeline class')
            logging.info("Getting the data from mongodb")

            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact
        except Exception as e:
            raise USVisaException(e,sys) from e
        

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        logging.info(f"Entered the start data validation method of TrainPipeline class")

        try:
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=self.data_validation_config)
            
            data_validation_artifact=data_validation.initiate_data_validation()

            logging.info("Performed data validation operation")
            logging.info("Exited the start data validation method of TrainPipeline class")
             
            return data_validation_artifact
        except Exception as e:
            raise USVisaException(e,sys) from e
        
    
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise USVisaException(e,sys)