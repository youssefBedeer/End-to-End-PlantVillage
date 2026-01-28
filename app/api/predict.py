from fastapi import APIRouter, UploadFile, File, Depends, Request
from core.validators import validate_image_file
from core.preprocess import preprocess_image
import numpy as np
from core.labels import LABELS

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile=File(...), request: Request=None): # request It gives you access to the FastAPI app object
    
    # validate file type 
    image_bytes = await validate_image_file(file)
    
    # image preprocessing 
    img_array = preprocess_image(image_bytes)
    
    # load model 
    model = request.app.state.model
    
    # predict 
    preds = model.predict(img_array)
    class_index = np.argmax(preds)
    predicted_class = LABELS[class_index]
    return {"predicted_class": predicted_class}