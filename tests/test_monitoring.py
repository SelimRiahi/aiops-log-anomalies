"""
Unit tests for monitoring components
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from monitoring.metrics_tracker import MetricsTracker
from monitoring.drift_detection import DriftDetector


def test_metrics_tracker_initialization():
    """Test metrics tracker initialization"""
    tracker = MetricsTracker(max_history=100)
    
    assert tracker.total_predictions == 0
    assert tracker.fraud_detected == 0
    assert len(tracker.predictions) == 0


def test_metrics_tracker_record_prediction():
    """Test recording a prediction"""
    tracker = MetricsTracker(max_history=100)
    
    tracker.record_prediction(
        is_fraud=True,
        reconstruction_error=0.5,
        response_time_ms=50.0,
        transaction_data={'amount': 1000, 'type': 'TRANSFER'}
    )
    
    assert tracker.total_predictions == 1
    assert tracker.fraud_detected == 1
    assert len(tracker.predictions) == 1


def test_metrics_tracker_statistics():
    """Test statistics calculation"""
    tracker = MetricsTracker(max_history=100)
    
    # Record some predictions
    for i in range(10):
        tracker.record_prediction(
            is_fraud=(i % 2 == 0),  # 50% fraud rate
            reconstruction_error=0.5,
            response_time_ms=50.0,
            transaction_data={'amount': 1000, 'type': 'TRANSFER'}
        )
    
    stats = tracker.get_statistics()
    
    assert stats['total_predictions'] == 10
    assert stats['fraud_detected'] == 5
    assert stats['fraud_rate'] == 0.5
    assert stats['avg_response_time_ms'] == 50.0


def test_drift_detector_initialization():
    """Test drift detector initialization"""
    detector = DriftDetector(threshold=0.05)
    
    assert detector.threshold == 0.05
    assert detector.reference_data is None
    assert len(detector.reference_stats) == 0


def test_drift_detector_reference_data():
    """Test loading reference data"""
    detector = DriftDetector()
    
    # Create mock reference data
    reference_df = pd.DataFrame({
        'amount': np.random.normal(1000, 100, 100),
        'balance': np.random.normal(5000, 500, 100),
        'isFraud': [0] * 100
    })
    
    # Save temporarily
    temp_file = Path(__file__).parent / 'temp_reference.csv'
    reference_df.to_csv(temp_file, index=False)
    
    try:
        detector.load_reference_data(str(temp_file))
        
        assert detector.reference_data is not None
        assert 'amount' in detector.reference_stats
        assert 'balance' in detector.reference_stats
        assert 'mean' in detector.reference_stats['amount']
        
    finally:
        # Cleanup
        if temp_file.exists():
            temp_file.unlink()


if __name__ == "__main__":
    import numpy as np
    pytest.main([__file__, "-v"])
