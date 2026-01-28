from fastapi import FastAPI 
from contextlib import asynccontextmanager 
import dagshub
import mlflow.pyfunc
from api.predict import router as predict_router
from fastapi.middleware.cors import CORSMiddleware # for Streamlit to call FastAPI
## load production model on app startup
@asynccontextmanager 
async def lifespan(app: FastAPI):
    # Load the ML model
    dagshub.init(repo_owner='youssefBedeer', repo_name='End-to-End-PlantVillage', mlflow=True)

    MODEL_URI = "models:/VGG16Model/production"
    app.state.model = mlflow.pyfunc.load_model(model_uri= MODEL_URI)
    yield
    # Clean up the ML models and release the resources
    app.state.model.clear()
    
    
app = FastAPI(lifespan=lifespan)

# allow Streamlit to call FastAPI
app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # for production, set Streamlit URL here
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

@app.get("/")
async def read_users():
    return [{"username": "Youssef"}, {"username": "Bedeer"}]

app.include_router(predict_router)