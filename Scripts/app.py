from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError, MeanAbsoluteError
from sklearn.preprocessing import MinMaxScaler
import joblib
import logging
import os
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import preprocessing and training modules
import importlib.util
import sys

def import_module_from_file(file_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Create Flask app
app = Flask(__name__)
CORS(app)

# Get the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = current_dir
project_root = os.path.dirname(current_dir)  # Go up one level from Scripts

def load_models_and_scalers():
    models = {}
    scalers = {}

    # Defining correct paths relative to project structure
    soil_model_path = os.path.join(project_root, "Models", "Soil_Analysis", "soil_tabular_model.h5")
    soil_scaler_path = os.path.join(project_root, "Models", "Soil_analysis", "scaler.pkl")
    weather_model_path = os.path.join(project_root, "Models", "Weather_Forecast", "weather_model.h5")
    weather_scaler_path = os.path.join(project_root, "Models", "Weather_Forecast", "scaler.pkl")
    
    preprocess_path = os.path.join(scripts_dir, "preprocess.py")
    train_soil_path = os.path.join(project_root, "Models", "Soil_analysis", "train_soil_model.py")
    train_weather_path = os.path.join(project_root, "Models", "Weather_Forecast", "train_weather_model.py")
    
    # Run preprocessing if necessary
    if (not os.path.exists(soil_scaler_path) or 
        not os.path.exists(os.path.join(project_root, "data", "soil", "X_train_scaled.csv"))):
        logger.info("Running soil data preprocessing...")
        try:
            if os.path.exists(preprocess_path):
                preprocess = import_module_from_file(preprocess_path, "preprocess")
                logger.info("Soil preprocessing completed")
            else:
                logger.error(f"Preprocessing script not found at {preprocess_path}")
        except Exception as e:
            logger.error(f"Error in soil preprocessing: {e}")
            logger.error(traceback.format_exc())
    
    # Run soil model training if necessary
    if not os.path.exists(soil_model_path):
        logger.info("Training soil model...")
        try:
            if os.path.exists(train_soil_path):
                train_soil = import_module_from_file(train_soil_path, "train_soil")
                logger.info("Soil model training completed")
            else:
                logger.error(f"Soil training script not found at {train_soil_path}")
        except Exception as e:
            logger.error(f"Error in soil model training: {e}")
            logger.error(traceback.format_exc())
    
    # Run weather model training if necessary
    if not os.path.exists(weather_model_path) or not os.path.exists(weather_scaler_path):
        logger.info("Training weather model...")
        try:
            if os.path.exists(train_weather_path):
                train_weather = import_module_from_file(train_weather_path, "train_weather")
                logger.info("Weather model training completed")
            else:
                logger.error(f"Weather training script not found at {train_weather_path}")
        except Exception as e:
            logger.error(f"Error in weather model training: {e}")
            logger.error(traceback.format_exc())

    try:
        # Soil Analysis Model
        if os.path.exists(soil_model_path):
            models['soil'] = load_model(soil_model_path)
            logger.info(f"Soil analysis model loaded successfully from {soil_model_path}")
        else:
            logger.error(f"Soil model not found at {soil_model_path}")

        # Soil Analysis Scaler
        if os.path.exists(soil_scaler_path):
            scalers['soil'] = joblib.load(soil_scaler_path)
            logger.info(f"Soil scaler loaded successfully from {soil_scaler_path}")
        else:
            logger.error(f"Soil scaler not found at {soil_scaler_path}")

        # Weather Forecast Model
        if os.path.exists(weather_model_path):
            models['weather'] = load_model(
                weather_model_path, 
                custom_objects={
                    "mse": MeanSquaredError(),
                    "mae": MeanAbsoluteError()
                }
            )
            logger.info(f"Weather model loaded successfully from {weather_model_path}")
        else:
            logger.error(f"Weather model not found at {weather_model_path}")

        # Weather Scaler
        if os.path.exists(weather_scaler_path):
            scalers['weather'] = joblib.load(weather_scaler_path)
            logger.info(f"Weather scaler loaded successfully from {weather_scaler_path}")
        else:
            logger.error(f"Weather scaler not found at {weather_scaler_path}")

    except Exception as e:
        logger.error(f"Error loading models/scalers: {e}")
        logger.error(traceback.format_exc())
        models = {}
        scalers = {}

    return models, scalers

MODELS, SCALERS = load_models_and_scalers()

@app.route("/", methods=["GET"])
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "models_loaded": {
            "soil_analysis": "soil" in MODELS,
            "weather_prediction": "weather" in MODELS
        }
    }), 200

@app.route("/soil-analysis", methods=["POST"])
def soil_analysis():
    """Soil fertility analysis endpoint"""
    try:
        if 'soil' not in MODELS or 'soil' not in SCALERS:
            return jsonify({"error": "Soil analysis model not loaded"}), 500

        # Extract features from request
        data = request.json
        if not data:
            return jsonify({"error": "No soil data provided"}), 400

        # Required feature names
        feature_names = ["N", "P", "K", "pH", "EC", "OC", "S", "Zn", "Fe", "Cu", "Mn", "B"]
        
        # Validate input features
        if not all(feature in data for feature in feature_names):
            return jsonify({"error": "Missing required soil features"}), 400

        # Prepare features
        features = [data[feature] for feature in feature_names]
        features_array = np.array([features])

        # Scale features
        scaled_features = SCALERS['soil'].transform(features_array)

        # Make prediction
        prediction = MODELS['soil'].predict(scaled_features)
        
        # Convert prediction to interpretable result
        fertility_status = "High" if prediction[0][0] > 0.5 else "Low"
        confidence = float(prediction[0][0] * 100)

        return jsonify({
            "fertility_status": fertility_status,
            "confidence": confidence
        }), 200

    except Exception as e:
        logger.error(f"Soil analysis error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error during soil analysis"}), 500

@app.route("/weather-prediction", methods=["POST"])
def weather_prediction():
    """Weather prediction endpoint"""
    try:
        if 'weather' not in MODELS or 'weather' not in SCALERS:
            return jsonify({
                "error": "Weather prediction model or scaler not loaded. Please ensure the weather model and scaler files are available."
            }), 500

        # Extract features from request
        data = request.json
        if isinstance(data, dict): 
            data = data.get("data", None)
        elif isinstance(data, list): 
            pass
        else:
            return jsonify({"error": "Invalid input format. Expected a JSON array or object."}), 400

        # Validate the input size (checks for 3 values)
        if not data or len(data) != 3:
            return jsonify({
                "error": f"Invalid input size. Expected a JSON array with exactly 3 values, but got {len(data)} values."
            }), 400

        # Convert to numpy array and reshape to (1, 1, 3)
        input_array = np.array(data).reshape(1, 1, 3)

        # Normalize input using the scaler
        scaled_features = SCALERS['weather'].transform(input_array.reshape(-1, 3))
        scaled_features = scaled_features.reshape(1, 1, 3)

        # Make prediction
        prediction = MODELS['weather'].predict(scaled_features)

        return jsonify({
            "predicted_temperature": float(prediction[0][0])
        }), 200

    except Exception as e:
        logger.error(f"Weather prediction error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error during weather prediction"}), 500


if __name__ == "__main__":
    app.run(debug=True)
