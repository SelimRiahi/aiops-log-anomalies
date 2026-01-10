"""
Metrics tracking for model predictions and performance
"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import deque
import pandas as pd

logger = logging.getLogger(__name__)


class MetricsTracker:
    """Track and store prediction metrics"""
    
    def __init__(self, max_history: int = 10000):
        self.max_history = max_history
        self.predictions = deque(maxlen=max_history)
        self.total_predictions = 0
        self.fraud_detected = 0
        self.total_response_time = 0.0
        self.start_time = datetime.now()
        
        # Storage path
        self.metrics_file = Path(__file__).parent.parent / 'logs' / 'metrics.jsonl'
        self.metrics_file.parent.mkdir(exist_ok=True)
    
    def record_prediction(
        self,
        is_fraud: bool,
        reconstruction_error: float,
        response_time_ms: float,
        transaction_data: Dict
    ):
        """Record a prediction"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'is_fraud': is_fraud,
            'reconstruction_error': reconstruction_error,
            'response_time_ms': response_time_ms,
            'transaction_amount': transaction_data.get('amount'),
            'transaction_type': transaction_data.get('type')
        }
        
        # Add to in-memory storage
        self.predictions.append(record)
        
        # Update counters
        self.total_predictions += 1
        if is_fraud:
            self.fraud_detected += 1
        self.total_response_time += response_time_ms
        
        # Persist to file
        try:
            with open(self.metrics_file, 'a') as f:
                f.write(json.dumps(record) + '\n')
        except Exception as e:
            logger.error(f"Error writing metrics: {e}")
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        if self.total_predictions == 0:
            return {
                'total_predictions': 0,
                'fraud_detected': 0,
                'fraud_rate': 0.0,
                'avg_response_time_ms': 0.0,
                'uptime_hours': 0.0
            }
        
        uptime = (datetime.now() - self.start_time).total_seconds() / 3600
        
        return {
            'total_predictions': self.total_predictions,
            'fraud_detected': self.fraud_detected,
            'fraud_rate': self.fraud_detected / self.total_predictions if self.total_predictions > 0 else 0.0,
            'avg_response_time_ms': self.total_response_time / self.total_predictions if self.total_predictions > 0 else 0.0,
            'uptime_hours': uptime
        }
    
    def get_recent_predictions(self, limit: int = 100) -> List[Dict]:
        """Get recent predictions"""
        return list(self.predictions)[-limit:]
    
    def get_time_series_data(self, hours: int = 24) -> pd.DataFrame:
        """Get time series data for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent = [
            p for p in self.predictions 
            if datetime.fromisoformat(p['timestamp']) > cutoff_time
        ]
        
        if not recent:
            return pd.DataFrame()
        
        df = pd.DataFrame(recent)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def get_fraud_by_type(self) -> Dict[str, int]:
        """Get fraud count by transaction type"""
        fraud_by_type = {}
        for pred in self.predictions:
            if pred['is_fraud']:
                tx_type = pred.get('transaction_type', 'UNKNOWN')
                fraud_by_type[tx_type] = fraud_by_type.get(tx_type, 0) + 1
        return fraud_by_type


# Global metrics tracker instance
metrics_tracker = MetricsTracker()
