from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_transformation import DataTransformation
from us_visa.components.model_trainer import ModelTrainer
from us_visa.components.model_evaluation import ModelEvaluation
from us_visa.components.model_pusher import ModelPusher
import sys
from us_visa.entity.config_entity import (DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,
                                          ModelEvaluationConfig,ModelPusherConfig)
from us_visa.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,
                                            ModelEvaluationArtifact,ModelPusherArtifact)
from us_visa.exception import USVisaException
from us_visa.logger import logging

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
        self.data_transformation_config=DataTransformationConfig()
        self.model_trainer_config=ModelTrainerConfig()
        self.model_evaluation_config=ModelEvaluationConfig()
        self.model_pusher_config=ModelPusherConfig()
    
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
    
    
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:

        try:
            data_transformation=DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                   data_validation_artifact=data_validation_artifact,
                                                   data_transformation_config=self.data_transformation_config)
            
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            
            return data_transformation_artifact
        except Exception as e:
            raise USVisaException(e,sys)
    

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer=ModelTrainer(data_transofrmation_artifact=data_transformation_artifact,
                                       model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_trainer.initiate_model_trainer()

            return model_trainer_artifact
        except Exception as e:
            raise USVisaException(e,sys)
    

    def start_model_evaluation(self,data_ingestion_artifact:DataIngestionArtifact,
                               model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            model_evaluation=ModelEvaluation(data_ingestion_artifact=data_ingestion_artifact,
                                             model_trainer_artifact=model_trainer_artifact,
                                             model_eval_config=self.model_evaluation_config)
            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise USVisaException(e,sys)
    
    
    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact)->ModelPusherArtifact:
        try:
            model_pusher=ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                     model_pusher_config=self.model_pusher_config)
            
            model_pusher_artifact=model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise USVisaException(e,sys)
            
        
    
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                        data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact=self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                  model_trainer_artifact=model_trainer_artifact)
            
            if not model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model not accepted.")
                return None
            model_pusher_artifact=self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
        
        except Exception as e:
            raise USVisaException(e,sys)