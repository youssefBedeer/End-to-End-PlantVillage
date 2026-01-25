import os 
from pathlib import Path 
import logging 

logging.basicConfig(level=logging.INFO, format= '[%(asctime)s]: %(message)s:')

project_name = "PlantVillage"

list_of_paths = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/schemas/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "research/trials.ipynb",
    "api/predict.py",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "main.py",
    "app.py"
]

for path in list_of_paths:
    path = Path(path)
    folder, file = os.path.split(path)
    
    if folder != "":
        os.makedirs(folder, exist_ok=True)
        logging.info(f"Folder {folder} Created Successfully.")
        
    if (not os.path.exists(path)) or (os.path.getsize(path)==0):
        with open(path, "w") as f:
            logging.info(f"Creating empty file: {path}")
            
    else:
        logging.info(f"{file} is already exist.")