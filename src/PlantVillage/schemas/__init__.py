from dataclasses import dataclass 
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionSchema:
    root_dir: Path 
    source_url: str
    local_path: str
    

@dataclass 
class PrepareBaseModelSchema:
    root_dir: Path 
    base_model_path: Path 
    updated_base_model_path: Path
    params_image_size : list 
    params_learning_rate: float 
    params_weights: str 
    params_classes: int
    params_include_top: bool
    
    
@dataclass(frozen=True)
class TrainingSchema:
    root_dir: Path 
    trained_model_path: Path 
    updated_base_model_path: Path 
    training_data_path: Path 
    params_epochs: int 
    params_batch_size: int 
    params_augmentation: bool 
    params_image_size: list
    
    
@dataclass 
class EvaluationSchema:
    track_url: str
    model_path: Path
    training_data: Path 
    all_params: dict 
    params_image_size: list 
    params_batch_size: int 