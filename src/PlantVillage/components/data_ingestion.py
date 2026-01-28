from PlantVillage.schemas import DataIngestionSchema 
from ensure import ensure_annotations
import os 
import kagglehub 
import shutil
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionSchema):
        self.config = config
        
    @ensure_annotations
    def download_data(self):
        try:
            # download data from kagglehub
            data_url = self.config.source_url
            if "datasets" in data_url:
                data_url = data_url.split("datasets/")[-1]
                
            # custom download path
            os.environ["KAGGLEHUB_CACHE"] = self.config.local_path
            # start download
            path = kagglehub.dataset_download(data_url)
            csv_path = os.path.join(path, os.listdir(path)[0])
            
            # copy csv to destination 
            shutil.copy2(csv_path, self.config.local_path)
            
            # delete old folders and files
            shutil.rmtree(Path("artifacts/data_ingestion/datasets"))

        except Exception as e:
            raise ValueError(f"Invalid URL: must be user/dataset-name ERROR: {e}")