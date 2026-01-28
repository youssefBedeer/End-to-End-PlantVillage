import yaml 
from ensure import ensure_annotations
import os 
from box import ConfigBox 
from pathlib import Path
from PlantVillage import logger
import json

@ensure_annotations 
def read_yaml(yaml_file_path: Path) -> ConfigBox:
    try:
        with open(yaml_file_path) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {yaml_file_path} loaded Successfully.")
            return ConfigBox(content)
        
    except Exception as e:
        raise ValueError(f"Error reading yaml file [{yaml_file_path}]: {str(e)}")
    
    
@ensure_annotations 
def create_directories(list_of_dirs: list):
    """Create directories from list of paths"""
    for path in list_of_dirs:
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created Successfully at: {path}")
        except Exception as e:
            raise ValueError(f"Error creating dir: [{path}] Error: {str(e)}")
        
        
@ensure_annotations 
def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
        
    logger.info(f"json file saved at: {path}")
