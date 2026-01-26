from src.PlantVillage.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH 
from src.PlantVillage.utils import read_yaml, create_directories 
from src.PlantVillage.schemas import DataIngestionSchema

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
        
        
        