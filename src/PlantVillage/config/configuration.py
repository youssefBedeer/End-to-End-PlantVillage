from pathlib import Path 
import os 

from src.PlantVillage.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH 
from src.PlantVillage.utils import read_yaml, create_directories 
from src.PlantVillage.schemas import DataIngestionSchema, PrepareBaseModelSchema, TrainingSchema, EvaluationSchema

class ConfigurationManager:
    def __init__(
        self, 
        config_file_path = CONFIG_FILE_PATH,
        params_file_path = PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        
        create_directories([self.config.artifacts_root])
        

    def get_data_ingestion_config(self) -> DataIngestionSchema:
        config = self.config.data_ingestion 
        
        create_directories([config.root_dir])
        
        return DataIngestionSchema(
            root_dir= config.root_dir, 
            source_url= config.source_url,
            local_path= config.local_path
        )
        
        
    def get_base_model_config(self) -> PrepareBaseModelSchema:
        config = self.config.prepare_base_model 
        params = self.params 
        create_directories([config.root_dir])
        
        return PrepareBaseModelSchema(
            root_dir= config.root_dir,
            base_model_path= config.base_model_path,
            updated_base_model_path= config.updated_base_model_path,
            params_image_size= params.IMAGE_SIZE,
            params_learning_rate=params.LEARNING_RATE,
            params_weights=params.WEIGHTS,
            params_classes=params.CLASSES,
            params_include_top=params.INCLUDE_TOP
        )
        
        
    def get_training_config(self) -> TrainingSchema:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model 
        params = self.params 
        training_data = Path(os.path.join(self.config.data_ingestion.local_path,"PlantVillage" ))
        create_directories([training.root_dir])
        
        return TrainingSchema(
            root_dir= training.root_dir, 
            trained_model_path= training.trained_model_path, 
            updated_base_model_path= prepare_base_model.updated_base_model_path, 
            training_data_path= training_data, 
            params_epochs=params.EPOCHS, 
            params_batch_size=params.BATCH_SIZE, 
            params_augmentation= params.AUGMENTATION, 
            params_image_size= params.IMAGE_SIZE,
        )
        

        
    def get_evaluation_config(self) -> EvaluationSchema:
        training_data_path = Path(os.path.join(self.config.data_ingestion.local_path, "PlantVillage"))
        
        
        return EvaluationSchema(
            track_url= self.config.evaluation.track_url,
            model_path= self.config.training.trained_model_path,
            training_data= training_data_path,
            all_params=  self.params,
            params_image_size= self.params.IMAGE_SIZE,
            params_batch_size= self.params.BATCH_SIZE,
        )