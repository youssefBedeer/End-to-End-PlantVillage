import mlflow 
import dagshub


class PredictionPipeline:
    def __init__(self, image_path):
        self.img_path = image_path
        
    def load_model(self):
        
        dagshub.init(repo_owner='youssefBedeer', repo_name='End-to-End-PlantVillage', mlflow=True)

        # load the production model 
        MODEL_URI = "models:/VGG16Model/production"
        model = mlflow.pyfunc.load_model(model_uri= MODEL_URI)
    def predict(self):

