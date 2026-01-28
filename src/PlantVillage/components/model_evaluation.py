import tensorflow as tf
from PlantVillage.utils import save_json
import mlflow
import dagshub
from PlantVillage.schemas import EvaluationSchema
from pathlib import Path

class Evaluation:
    def __init__(self, config: EvaluationSchema):
        self.config = config 
        
    def _valid_generator(self):
        
        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split = 0.2
        )
        
        dataflow_kwargs = dict(
            target_size = self.config.params_image_size[:-1],
            batch_size = self.config.params_batch_size,
            interpolation = "bilinear"
        )
        
        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )
        
        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset= "validation",
            shuffle= False,
            **dataflow_kwargs
        )
        
    def evaluation(self):
        self.model = tf.keras.models.load_model(self.config.model_path)
        self._valid_generator() 
        self.score = self.model.evaluate(self.valid_generator)
        self.save_score(self.score) 
        
    @staticmethod
    def save_score(score):
        scores = {"loss": score[0], "accuracy": score[1]}
        save_json(path= Path("scores.json"), data= scores)
        
        
    def log_into_mlflow(self):
        dagshub.init(repo_owner='youssefBedeer', repo_name='End-to-End-PlantVillage', mlflow=True)

        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1]}
            )
            mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model")
            
            