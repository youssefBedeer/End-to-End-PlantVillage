import streamlit as st 
import requests 

FastAPI_URL = "http://127.0.0.1:8000" 
st.title("Plant Disease Detection") 

uploaded_file = st.file_uploader("Choose and image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=False)
    with col2:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }
        with st.spinner("Predicting..."):
            response = requests.post(f"{FastAPI_URL}/predict", files=files)
        if response.status_code == 200:
            json_response = response.json()
            st.success(f"Prediction: {json_response['predicted_class']}")
        else:
            st.write(f"Error: {response.status_code}")
            st.write(response.text)