"""
Unit tests for the API endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns service info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data['service'] == 'Fraud Detection API'
    assert 'version' in data
    assert 'status' in data


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert 'model_loaded' in data
    assert 'model_version' in data


def test_predict_endpoint_valid():
    """Test prediction endpoint with valid data"""
    transaction = {
        "step": 1,
        "amount": 9839.64,
        "oldbalanceOrg": 170136.0,
        "newbalanceOrig": 160296.36,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 0.0,
        "type": "PAYMENT",
        "nameOrig": "C1231006815",
        "nameDest": "M1979787155"
    }
    
    response = client.post("/predict", json=transaction)
    
    # Check response
    assert response.status_code in [200, 503]  # 503 if model not loaded
    
    if response.status_code == 200:
        data = response.json()
        assert 'is_fraud' in data
        assert 'fraud_probability' in data
        assert 'reconstruction_error' in data
        assert 'confidence' in data
        assert isinstance(data['is_fraud'], bool)


def test_predict_endpoint_invalid():
    """Test prediction endpoint with invalid data"""
    invalid_transaction = {
        "step": 1,
        "amount": -100,  # Invalid: negative amount
        "type": "INVALID_TYPE"
    }
    
    response = client.post("/predict", json=invalid_transaction)
    assert response.status_code == 422  # Validation error


def test_predict_endpoint_missing_fields():
    """Test prediction endpoint with missing required fields"""
    incomplete_transaction = {
        "step": 1,
        "amount": 1000
        # Missing many required fields
    }
    
    response = client.post("/predict", json=incomplete_transaction)
    assert response.status_code == 422


def test_metrics_endpoint():
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert 'total_predictions' in data
    assert 'fraud_detected' in data
    assert 'fraud_rate' in data
    assert 'avg_response_time_ms' in data


def test_detailed_metrics_endpoint():
    """Test detailed metrics endpoint"""
    response = client.get("/metrics/detailed")
    assert response.status_code == 200
    data = response.json()
    assert 'statistics' in data
    assert 'recent_predictions' in data
    assert 'uptime_seconds' in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
