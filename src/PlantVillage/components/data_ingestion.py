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
            first_entry = os.listdir(path)[0]
            src_path = os.path.join(path, first_entry)
            
            # copy downloaded content (file or directory) to destination
            dest_path = self.config.local_path
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            if os.path.isdir(src_path):
                # if a folder (e.g. PlantVillage images), copy the whole tree
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(src_path, dest_path)
            else:
                # if a single file (e.g. CSV), copy it
                shutil.copy2(src_path, dest_path)
            
            # delete old folders and files (best-effort)
            shutil.rmtree(Path("artifacts/data_ingestion/datasets"), ignore_errors=True)

        except Exception as e:
            raise ValueError(f"Data ingestion failed. Please ensure source_url is 'user/dataset-name'. ERROR: {e}")