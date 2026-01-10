"""
Unit tests for model handler
"""
import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from api.model_handler import FraudDetectionModel


def test_model_initialization():
    """Test model handler initialization"""
    model = FraudDetectionModel()
    assert model.autoencoder is None
    assert model.scaler is None
    assert model.threshold is None
    assert not model.is_loaded()


def test_feature_engineering():
    """Test feature engineering pipeline"""
    model = FraudDetectionModel()
    
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
    
    # Mock scaler
    class MockScaler:
        n_features_in_ = 30
    
    model.scaler = MockScaler()
    
    features = model.engineer_features(transaction)
    
    # Check output
    assert features is not None
    assert features.shape[0] == 1  # Single transaction
    assert 'amount_log' in features.columns
    assert 'balance_change_orig' in features.columns


def test_model_is_loaded():
    """Test is_loaded method"""
    model = FraudDetectionModel()
    
    # Initially not loaded
    assert not model.is_loaded()
    
    # Mock loading
    model.autoencoder = "mock"
    model.scaler = "mock"
    model.threshold = 0.1
    
    # Now should be loaded
    assert model.is_loaded()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
