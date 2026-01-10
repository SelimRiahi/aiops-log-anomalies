"""
Model loading and prediction logic
"""
import numpy as np
import pandas as pd
import keras
import joblib
from pathlib import Path
import logging
from typing import Dict, Tuple
import sys

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from config.config import AUTOENCODER_PATH, SCALER_PATH, THRESHOLD_PATH, MODEL_VERSION

logger = logging.getLogger(__name__)


class FraudDetectionModel:
    """Handles model loading and predictions"""
    
    def __init__(self):
        self.autoencoder = None
        self.scaler = None
        self.threshold = None
        self.model_version = MODEL_VERSION
        self.feature_names = None
        
    def load_model(self) -> bool:
        """Load trained model and components"""
        try:
            logger.info("Loading fraud detection model...")
            
            # Load autoencoder
            if not AUTOENCODER_PATH.exists():
                logger.error(f"Model file not found: {AUTOENCODER_PATH}")
                return False
            self.autoencoder = keras.models.load_model(str(AUTOENCODER_PATH))
            logger.info("✓ Loaded autoencoder model")
            
            # Load scaler
            if not SCALER_PATH.exists():
                logger.error(f"Scaler file not found: {SCALER_PATH}")
                return False
            self.scaler = joblib.load(str(SCALER_PATH))
            logger.info("✓ Loaded feature scaler")
            
            # Load threshold
            if not THRESHOLD_PATH.exists():
                logger.error(f"Threshold file not found: {THRESHOLD_PATH}")
                return False
            self.threshold = np.load(str(THRESHOLD_PATH))
            logger.info(f"✓ Loaded threshold: {self.threshold:.6f}")
            
            logger.info(f"Model loaded successfully (version {self.model_version})")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def engineer_features(self, transaction_data: Dict) -> pd.DataFrame:
        """
        Apply feature engineering matching EXACT training features.
        Uses defaults for historical features (user behavior, destination stats).
        """
        df = pd.DataFrame([transaction_data])
        
        # EXACT ORDER FROM SCALER: 50 features
        # 1-6: Original features
        # Already have: step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest
        
        # 7-11: Amount features
        df['amount_log'] = np.log1p(df['amount'])
        df['amount_sqrt'] = np.sqrt(df['amount'])
        df['amount_bin_encoded'] = 2  # Default: medium bin
        df['amount_to_oldbalance_ratio'] = df['amount'] / (df['oldbalanceOrg'] + 1)
        df['amount_exceeds_balance'] = (df['amount'] > df['oldbalanceOrg']).astype(int)
        
        # 12-17: Temporal features
        df['hour'] = df['step'] % 24
        df['day'] = df['step'] // 24
        df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)
        df['is_weekend'] = (df['day'] % 7 >= 5).astype(int)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        
        # 18-26: User behavior (defaults - no history available)
        df['time_since_last_tx'] = 1.0  # Assume 1 hour
        df['tx_count_1h'] = 1
        df['tx_count_6h'] = 1
        df['tx_count_24h'] = 1
        df['user_tx_count'] = 1
        df['user_avg_amount'] = df['amount']
        df['user_std_amount'] = 0.0
        df['amount_deviation_from_user_avg'] = 0.0
        df['tx_velocity'] = 1.0
        
        # 27-36: Balance dynamics
        df['balance_change_orig'] = df['newbalanceOrig'] - df['oldbalanceOrg']
        df['balance_change_dest'] = df['newbalanceDest'] - df['oldbalanceDest']
        df['expected_balance_change'] = -df['amount']  # For origin account
        df['balance_inconsistency_orig'] = np.abs(df['balance_change_orig'] + df['amount'])
        df['orig_zero_balance_before'] = (df['oldbalanceOrg'] == 0).astype(int)
        df['orig_zero_balance_after'] = (df['newbalanceOrig'] == 0).astype(int)
        df['dest_zero_balance_before'] = (df['oldbalanceDest'] == 0).astype(int)
        df['dest_zero_balance_after'] = (df['newbalanceDest'] == 0).astype(int)
        df['drains_account'] = (df['newbalanceOrig'] == 0).astype(int)
        df['balance_mismatch'] = (df['balance_inconsistency_orig'] > 0.01).astype(int)
        
        # 37-42: Transaction type features
        for tx_type in ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']:
            df[f'type_{tx_type}'] = (df['type'] == tx_type).astype(int)
        df['is_risky_type'] = df['type'].isin(['TRANSFER', 'CASH_OUT']).astype(int)
        
        # 43: User type switches (default - no history)
        df['user_type_switches'] = 0
        
        # 44-47: Destination account features (defaults)
        df['dest_is_merchant'] = df['nameDest'].str.startswith('M').astype(int)
        df['is_c2c'] = (~df['nameDest'].str.startswith('M')).astype(int)
        df['dest_tx_count'] = 1  # Default
        df['dest_is_popular'] = 0  # Default: not popular
        
        # 48-50: Risk/consistency scores (defaults)
        df['risk_score'] = 0.5  # Medium risk default
        df['consistency_score'] = 1.0  # Consistent default
        df['tx_intensity'] = 1.0  # Normal intensity
        
        # Select features in EXACT order expected by scaler
        feature_cols = [
            'step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest',
            'amount_log', 'amount_sqrt', 'amount_bin_encoded', 'amount_to_oldbalance_ratio', 'amount_exceeds_balance',
            'hour', 'day', 'is_night', 'is_weekend', 'hour_sin', 'hour_cos',
            'time_since_last_tx', 'tx_count_1h', 'tx_count_6h', 'tx_count_24h', 'user_tx_count',
            'user_avg_amount', 'user_std_amount', 'amount_deviation_from_user_avg', 'tx_velocity',
            'balance_change_orig', 'balance_change_dest', 'expected_balance_change', 'balance_inconsistency_orig',
            'orig_zero_balance_before', 'orig_zero_balance_after', 'dest_zero_balance_before', 'dest_zero_balance_after',
            'drains_account', 'balance_mismatch',
            'type_CASH_IN', 'type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT', 'type_TRANSFER', 'is_risky_type',
            'user_type_switches',
            'dest_is_merchant', 'is_c2c', 'dest_tx_count', 'dest_is_popular',
            'risk_score', 'consistency_score', 'tx_intensity'
        ]
        
        return df[feature_cols]
    
    def predict(self, transaction_data: Dict) -> Tuple[bool, float, float, float]:
        """
        Make fraud prediction
        
        Returns:
            (is_fraud, fraud_probability, reconstruction_error, confidence)
        """
        try:
            # Engineer features
            features_df = self.engineer_features(transaction_data)
            
            # Scale features
            features_scaled = self.scaler.transform(features_df)
            
            # Get reconstruction
            reconstruction = self.autoencoder.predict(features_scaled, verbose=0)
            
            # Calculate reconstruction error
            mse = np.mean(np.power(features_scaled - reconstruction, 2))
            
            # Determine if fraud
            is_fraud = mse > self.threshold
            
            # Calculate fraud probability (normalized error)
            # Higher error = higher probability
            fraud_probability = min(mse / (self.threshold * 2), 1.0)
            
            # Calculate confidence
            # How far from threshold (either direction)
            distance_from_threshold = abs(mse - self.threshold) / self.threshold
            confidence = min(distance_from_threshold, 1.0)
            
            return bool(is_fraud), float(fraud_probability), float(mse), float(confidence)
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return (self.autoencoder is not None and 
                self.scaler is not None and 
                self.threshold is not None)


# Global model instance
model_handler = FraudDetectionModel()
