from PIL import Image 
import numpy as np 
import io 

def preprocess_image(image_bytes, img_size=(224,224)):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB") #uint8
    img = img.resize(img_size)
    
    img_array = np.array(img) / 255.0 # normalize float
    
    return np.expand_dims(img_array, axis=0)