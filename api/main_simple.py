"""
Simple Prediction Endpoint - Uses Test Data
============================================
For now, predict on existing test samples since feature engineering
needs to match training exactly (60+ features with historical data).

This demonstrates the MLOps infrastructure while we work on
full feature parity for arbitrary transactions.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import keras
import joblib
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fraud Detection API - Simple Version")

# Global variables
model = None
scaler = None
threshold = None
test_data = None

@app.on_event("startup")
async def load_model():
    """Load model and test data"""
    global model, scaler, threshold, test_data
    
    try:
        # Load model
        model = keras.models.load_model('models/autoencoder.keras')
        scaler = joblib.load('models/autoencoder_scaler.pkl')
        threshold = np.load('models/ae_threshold.npy')
        
        # Load test data with proper features
        test_data = pd.read_csv('paysim_test.csv')
        
        logger.info("✓ Model loaded successfully")
        logger.info(f"✓ Test data loaded: {len(test_data)} samples")
        logger.info(f"✓ Threshold: {threshold:.6f}")
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")


class PredictionRequest(BaseModel):
    """Request to predict by sample index"""
    sample_index: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "sample_index": 0
            }
        }


class PredictionResponse(BaseModel):
    """Prediction response"""
    sample_index: int
    is_fraud: bool
    actual_fraud: bool
    fraud_probability: float
    reconstruction_error: float
    threshold: float
    confidence: float
    correct_prediction: bool


@app.get("/")
def root():
    return {
        "message": "Fraud Detection API - Simple Version",
        "info": "Use /predict with sample_index to test on pre-processed samples",
        "total_samples": len(test_data) if test_data is not None else 0
    }


@app.get("/health")
def health():
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "samples_available": len(test_data) if test_data is not None else 0
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Predict fraud for a test sample"""
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if test_data is None:
        raise HTTPException(status_code=503, detail="Test data not loaded")
    
    if request.sample_index < 0 or request.sample_index >= len(test_data):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid index. Must be 0-{len(test_data)-1}"
        )
    
    try:
        # Get sample
        sample = test_data.iloc[request.sample_index]
        actual_fraud = bool(sample['isFraud'])
        
        # Prepare features (drop label)
        features = sample.drop('isFraud').values.reshape(1, -1)
        
        # Scale
        features_scaled = scaler.transform(features)
        
        # Predict
        reconstruction = model.predict(features_scaled, verbose=0)
        mse = float(np.mean(np.power(features_scaled - reconstruction, 2)))
        
        # Determine fraud
        is_fraud = mse > threshold
        fraud_prob = min(mse / (threshold * 2), 1.0)
        confidence = min(abs(mse - threshold) / threshold, 1.0)
        
        return PredictionResponse(
            sample_index=request.sample_index,
            is_fraud=bool(is_fraud),
            actual_fraud=actual_fraud,
            fraud_probability=float(fraud_prob),
            reconstruction_error=float(mse),
            threshold=float(threshold),
            confidence=float(confidence),
            correct_prediction=(is_fraud == actual_fraud)
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/samples/random")
def get_random_sample():
    """Get a random sample index"""
    if test_data is None:
        raise HTTPException(status_code=503, detail="Test data not loaded")
    
    import random
    
    # Get random normal and fraud samples
    normal_idx = test_data[test_data['isFraud'] == 0].sample(1).index[0]
    fraud_idx = test_data[test_data['isFraud'] == 1].sample(1).index[0]
    
    return {
        "normal_sample_index": int(normal_idx),
        "fraud_sample_index": int(fraud_idx),
        "message": "Use these indices with /predict endpoint"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
