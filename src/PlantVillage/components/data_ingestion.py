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
            data_url = self.config.source_url

            # extract "user/dataset-name" if full URL is passed
            if "datasets" in data_url:
                data_url = data_url.split("datasets/")[-1]

            # set kagglehub cache
            os.environ["KAGGLEHUB_CACHE"] = self.config.local_path

            # download dataset
            path = Path(kagglehub.dataset_download(data_url))

            # copy everything from downloaded folder into local_path
            destination = Path(self.config.local_path)
            destination.mkdir(parents=True, exist_ok=True)

            for item in path.iterdir():
                target = destination / item.name
                if item.is_dir():
                    shutil.copytree(item, target, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, target)

            # cleanup old datasets folder
            old_path = Path("artifacts/data_ingestion/datasets")
            if old_path.exists():
                shutil.rmtree(old_path)

            print(f"✅ Dataset downloaded and copied into: {destination}")

        except Exception as e:
            raise ValueError(
                f"Invalid URL: must be user/dataset-name (example: 'emmarex/plantdisease') ERROR: {e}"
            )