## End-to-End PlantVillage – Plant Disease Detection

This project is an **end-to-end computer vision pipeline** for detecting plant diseases from leaf images using a **VGG16-based TensorFlow/Keras model**, tracked with **MLflow/Dagshub**, orchestrated with **DVC**, and exposed through:

- **FastAPI** backend (`app/app.py`, `app/api/predict.py`) serving a production model from MLflow Registry.
- **Streamlit** frontend (`app.py` at the repo root) that lets users upload images and see predictions.
- **Training pipeline** under `src/PlantVillage` to ingest data, prepare the base model, train, and evaluate.

The environment used during development is the Conda env at `D:\Programming\ML\End-to-End\CV\DLenv`. For a lightweight runtime, you can instead install only the libraries listed in `requirements.txt`.

---

## Project Structure

- **`app.py`**: Streamlit UI to upload an image and call the FastAPI `/predict` endpoint.
- **`app/app.py`**: FastAPI application, loads the production model from MLflow (via Dagshub) and exposes routes.
- **`app/api/predict.py`**: `/predict` endpoint that:
  - Validates the uploaded image (`app/core/validators.py`).
  - Preprocesses the image (`app/core/preprocess.py`).
  - Calls the loaded MLflow model and maps predictions to class labels (`app/core/labels.py`).
- **`app/core`**:
  - `validators.py`: File type and size validation for uploaded images.
  - `preprocess.py`: PIL/numpy-based preprocessing (resize, normalize, batch dimension).
  - `labels.py`: Ordered list of PlantVillage class labels used to decode argmax predictions.
- **`src/PlantVillage`**:
  - `__init__.py`: Central logger configuration used across the project.
  - `components/`:
    - `data_ingestion.py`: Downloads data from Kaggle via `kagglehub` into the local artifacts folder.
    - `prepare_base_model.py`: Loads VGG16 with ImageNet weights and builds the classification head.
    - `model_trainer.py`: Defines the training loop using TensorFlow data generators.
    - `model_evaluation.py`: Evaluates the trained model and logs metrics to MLflow.
  - `config/configuration.py`: Reads YAML configs and returns strongly-typed dataclass schemas for each stage.
  - `constants/__init__.py`: Paths to `config/config.yaml` and `params.yaml`.
  - `pipeline/`:
    - `stage_01_data_ingestion.py`
    - `stage_02_prepare_base_model.py`
    - `stage_03_model_trainer.py`
    - `stage_04_model_evaluation.py`
    - `prediction_pipeline.py` (for loading the production model and performing predictions from Python code).
  - `schemas/__init__.py`: Dataclasses defining configuration structures for all stages.
  - `utils/__init__.py`: Helper functions for reading YAML, creating directories, and saving JSON scores.
- **`main.py`**: Orchestrates all training/evaluation pipeline stages sequentially.
- **`dvc.yaml`, `dvc.lock`**: DVC pipeline definition and lockfile for data and experiment tracking.
- **`config/config.yaml`, `params.yaml`**: Main configuration and hyperparameter files.

---

## Installation

### 1. Using Conda (recommended for development)

You can reuse the existing environment or create a fresh one:

```bash
conda create -n plantvillage-cv python=3.11
conda activate plantvillage-cv
pip install -r requirements.txt
```

If you want to use the original env, it lives at:

```text
D:\Programming\ML\End-to-End\CV\DLenv
```

### 2. System Requirements

- Python 3.11+
- CUDA-capable GPU (optional but recommended for training)
- Git, DVC, and (optionally) Kaggle credentials for data access

---

## Configuration

Key configuration files:

- **`config/config.yaml`**:
  - Defines artifact directories, data ingestion settings, base model paths, training output paths, and evaluation settings.
- **`params.yaml`**:
  - Hyperparameters like:
    - `IMAGE_SIZE` (e.g. `[224, 224, 3]`)
    - `EPOCHS`
    - `BATCH_SIZE`
    - `AUGMENTATION`
    - `LEARNING_RATE`
    - `WEIGHTS` (`"imagenet"`)
    - `CLASSES`

Before training, update:

- **Data source** in `config/config.yaml` (`data_ingestion.source_url`).
- **Hyperparameters** in `params.yaml` as needed.

---

## Training Pipeline

The training pipeline is composed of four main stages:

1. **Data Ingestion (`stage_01_data_ingestion.py`)**
   - Uses `kagglehub` to download the PlantVillage dataset from Kaggle.
   - Stores data under the artifacts root defined in `config/config.yaml`.
2. **Prepare Base Model (`stage_02_prepare_base_model.py`)**
   - Loads a VGG16 base model with ImageNet weights.
   - Saves both the base model and an “updated” base model with a custom classification head.
3. **Model Training (`stage_03_model_trainer.py`)**
   - Builds training and validation generators using `tf.keras.preprocessing.image.ImageDataGenerator`.
   - Trains the model with augmentation (if enabled) and saves the trained weights.
4. **Model Evaluation & Logging (`stage_04_model_evaluation.py`)**
   - Evaluates the trained model on the validation set.
   - Saves metrics to `scores.json`.
   - Logs parameters, metrics, and the model itself to MLflow, registering it under `VGG16Model`.

To run the full pipeline from scratch:

```bash
python main.py
```

Make sure your `config/config.yaml` and `params.yaml` are correctly set before running.

---

## Model Tracking with Dagshub & MLflow

The project uses **Dagshub** as a remote backend for **MLflow**:

- Training and evaluation code call `dagshub.init(...)` to connect to the repository.
- Metrics, params, and models are logged to MLflow and pushed to Dagshub.
- The FastAPI app and prediction pipeline **load the production model** from the MLflow Model Registry via:

```python
MODEL_URI = "models:/VGG16Model/production"
```

You should configure MLflow/Dagshub credentials in your environment so that:

- Training can log to Dagshub.
- Inference services can load the production model.

---

## Running the FastAPI Backend

The backend is defined in `app/app.py`. It:

- Initializes Dagshub/MLflow in the FastAPI lifespan handler.
- Loads the **production** model from the MLflow Model Registry.
- Wires the `/predict` route from `app/api/predict.py`.
- Enables CORS so the Streamlit app can call it.

From the project root, run:

```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

The root endpoint `/` returns a simple JSON to verify the app is running, and `/predict` accepts an image file via multipart upload.

---

## Running the Streamlit Frontend

The Streamlit client is in the top-level `app.py` and:

- Lets the user upload a leaf image (`jpg`, `jpeg`, `png`).
- Displays the uploaded image.
- Sends the file to the FastAPI `/predict` endpoint.
- Displays the predicted class returned by the backend.

Run it from the project root:

```bash
streamlit run app.py
```

Make sure the FastAPI backend is running (by default at `http://127.0.0.1:8000`). You can change `FastAPI_URL` in `app.py` if needed.

---

## Inference API – `/predict`

**Endpoint**: `POST /predict`  
**Defined in**: `app/api/predict.py`

Steps:

1. **Validation** (`app/core/validators.py`)
   - Ensures the file is an image (`image/jpeg`, `image/png`, `image/jpg`).
   - Enforces a max size of 5 MB.
2. **Preprocessing** (`app/core/preprocess.py`)
   - Opens the image with Pillow, resizes to \(224 \times 224\).
   - Converts to numpy, normalizes to \([0, 1]\), and adds batch dimension.
3. **Prediction**
   - Uses `request.app.state.model` (loaded from MLflow) to run `.predict`.
   - Takes `argmax` over class probabilities.
   - Maps the index to a human-readable label from `LABELS` in `app/core/labels.py`.

Response example:

```json
{
  "predicted_class": "Tomato_Leaf_Mold"
}
```

---

## Data & DVC

- Data download and preparation are tracked via **DVC**.
- `dvc.yaml` describes the pipeline stages and their dependencies/outputs.
- After configuring your remote (e.g., S3, GDrive, or Dagshub storage), you can:

```bash
dvc repro
```

to rerun the pipeline, or:

```bash
dvc pull
```

to fetch data and artifacts from the remote.

---

## Dependencies

The core Python dependencies that this project **directly uses in code** are listed in `requirements.txt`, including:

- Web/API & UI: `fastapi`, `uvicorn`, `streamlit`, `requests`
- ML & CV: `tensorflow`, `numpy`, `Pillow`
- Experiment tracking: `mlflow`, `dagshub`
- Data & config utilities: `kagglehub`, `ensure`, `PyYAML`, `python-box`

Install them with:

```bash
pip install -r requirements.txt
```

---

## How to Reproduce End-to-End

1. **Clone the repo** and install dependencies.
2. **Configure**:
   - Update `config/config.yaml` (data paths, artifact dirs).
   - Update `params.yaml` (hyperparameters).
3. **Run training pipeline**:
   - `python main.py`
   - Or use `dvc repro` if you rely on DVC stages.
4. **Verify model registration**:
   - Check MLflow UI (remote via Dagshub) for the registered `VGG16Model`.
5. **Start backend and frontend**:
   - `uvicorn app.app:app --reload --port 8000`
   - `streamlit run app.py`
6. **Upload images** from the Streamlit UI and check predictions.

---

## Notes

- For production, restrict CORS in `app/app.py` to only allow your deployed Streamlit (or other client) origin.
- Consider pinning versions in `requirements.txt` if you want fully reproducible installs across environments.