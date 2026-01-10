"""
Automated Retraining Pipeline
==============================
Automatically retrain model when drift is detected or on schedule
"""
import logging
import shutil
from datetime import datetime
from pathlib import Path
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
import keras
from keras import layers
import joblib

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from config.config import (
    MODEL_DIR, DATA_DIR, LOGS_DIR,
    AUTOENCODER_PATH, SCALER_PATH, THRESHOLD_PATH
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetrainingPipeline:
    """Automated model retraining pipeline"""
    
    def __init__(self):
        self.backup_dir = MODEL_DIR / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.results = {}
    
    def backup_current_model(self) -> bool:
        """Backup current model before retraining"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / timestamp
            backup_path.mkdir(exist_ok=True)
            
            # Backup model files
            if AUTOENCODER_PATH.exists():
                shutil.copy(AUTOENCODER_PATH, backup_path / "autoencoder.keras")
            if SCALER_PATH.exists():
                shutil.copy(SCALER_PATH, backup_path / "autoencoder_scaler.pkl")
            if THRESHOLD_PATH.exists():
                shutil.copy(THRESHOLD_PATH, backup_path / "ae_threshold.npy")
            
            logger.info(f"✓ Model backed up to {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error backing up model: {e}")
            return False
    
    def load_training_data(self) -> tuple:
        """Load and prepare training data"""
        try:
            logger.info("Loading training data...")
            
            # Load features
            features_path = DATA_DIR / "paysim_features.csv"
            if not features_path.exists():
                raise FileNotFoundError(f"Features file not found: {features_path}")
            
            df = pd.read_csv(features_path)
            logger.info(f"Loaded {len(df)} samples")
            
            # Separate features and labels
            fraud_labels = df['isFraud'].copy()
            X = df.drop('isFraud', axis=1)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, fraud_labels,
                test_size=0.2,
                random_state=42,
                stratify=fraud_labels
            )
            
            # Use only normal transactions for training
            normal_mask = y_train == 0
            X_train_normal = X_train[normal_mask]
            
            logger.info(f"Training samples (normal): {len(X_train_normal)}")
            logger.info(f"Test samples: {len(X_test)}")
            
            return X_train_normal, X_test, y_test
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def train_model(self, X_train: pd.DataFrame) -> tuple:
        """Train new autoencoder model"""
        try:
            logger.info("Training new model...")
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            
            # Build model
            input_dim = X_train_scaled.shape[1]
            encoding_dim = 16
            
            encoder_input = layers.Input(shape=(input_dim,))
            encoded = layers.Dense(64, activation='relu')(encoder_input)
            encoded = layers.BatchNormalization()(encoded)
            encoded = layers.Dropout(0.2)(encoded)
            encoded = layers.Dense(32, activation='relu')(encoded)
            encoded = layers.BatchNormalization()(encoded)
            encoded = layers.Dropout(0.2)(encoded)
            encoded = layers.Dense(encoding_dim, activation='relu', name='encoding')(encoded)
            
            decoded = layers.Dense(32, activation='relu')(encoded)
            decoded = layers.BatchNormalization()(decoded)
            decoded = layers.Dense(64, activation='relu')(decoded)
            decoded = layers.BatchNormalization()(decoded)
            decoder_output = layers.Dense(input_dim, activation='linear')(decoded)
            
            autoencoder = keras.Model(encoder_input, decoder_output)
            encoder = keras.Model(encoder_input, encoded)
            
            autoencoder.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='mse'
            )
            
            logger.info("Model architecture created")
            
            # Train
            history = autoencoder.fit(
                X_train_scaled,
                X_train_scaled,
                epochs=20,
                batch_size=256,
                validation_split=0.1,
                verbose=1,
                callbacks=[
                    keras.callbacks.EarlyStopping(
                        monitor='val_loss',
                        patience=5,
                        restore_best_weights=True
                    )
                ]
            )
            
            # Calculate threshold
            train_reconstructions = autoencoder.predict(X_train_scaled, verbose=0)
            train_mse = np.mean(np.power(X_train_scaled - train_reconstructions, 2), axis=1)
            threshold = np.percentile(train_mse, 95)
            
            logger.info(f"✓ Model trained. Threshold: {threshold:.6f}")
            
            return autoencoder, encoder, scaler, threshold
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def evaluate_model(
        self,
        autoencoder,
        scaler,
        threshold: float,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> dict:
        """Evaluate model performance"""
        try:
            logger.info("Evaluating model...")
            
            # Scale test data
            X_test_scaled = scaler.transform(X_test)
            
            # Get predictions
            test_reconstructions = autoencoder.predict(X_test_scaled, verbose=0)
            test_mse = np.mean(np.power(X_test_scaled - test_reconstructions, 2), axis=1)
            predictions = (test_mse > threshold).astype(int)
            
            # Calculate metrics
            precision = precision_score(y_test, predictions, zero_division=0)
            recall = recall_score(y_test, predictions, zero_division=0)
            f1 = f1_score(y_test, predictions, zero_division=0)
            roc_auc = roc_auc_score(y_test, test_mse)
            
            metrics = {
                'precision': float(precision),
                'recall': float(recall),
                'f1_score': float(f1),
                'roc_auc': float(roc_auc),
                'threshold': float(threshold)
            }
            
            logger.info(f"Precision: {precision:.4f}")
            logger.info(f"Recall: {recall:.4f}")
            logger.info(f"F1-Score: {f1:.4f}")
            logger.info(f"ROC-AUC: {roc_auc:.4f}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            raise
    
    def save_model(
        self,
        autoencoder,
        encoder,
        scaler,
        threshold: float
    ) -> bool:
        """Save trained model"""
        try:
            logger.info("Saving model...")
            
            MODEL_DIR.mkdir(exist_ok=True)
            
            autoencoder.save(str(AUTOENCODER_PATH))
            encoder.save(str(MODEL_DIR / "encoder.keras"))
            joblib.dump(scaler, str(SCALER_PATH))
            np.save(str(THRESHOLD_PATH), threshold)
            
            logger.info("✓ Model saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def compare_with_previous(self, new_metrics: dict) -> bool:
        """
        Compare new model with previous model
        
        Returns:
            True if new model is better or comparable
        """
        # For now, simple comparison based on F1 score
        # In production, use more sophisticated comparison
        
        # Check if we have a backup to compare with
        if not list(self.backup_dir.glob("*")):
            logger.info("No previous model to compare with. Accepting new model.")
            return True
        
        # Simple threshold: new F1 should be > 0.7
        if new_metrics['f1_score'] >= 0.70:
            logger.info(f"✓ New model performance acceptable (F1: {new_metrics['f1_score']:.4f})")
            return True
        else:
            logger.warning(f"⚠️  New model performance poor (F1: {new_metrics['f1_score']:.4f})")
            return False
    
    def restore_backup(self, backup_name: str = None):
        """Restore model from backup"""
        try:
            if backup_name is None:
                # Get latest backup
                backups = sorted(self.backup_dir.glob("*"))
                if not backups:
                    logger.error("No backups available")
                    return False
                backup_path = backups[-1]
            else:
                backup_path = self.backup_dir / backup_name
            
            if not backup_path.exists():
                logger.error(f"Backup not found: {backup_path}")
                return False
            
            # Restore files
            shutil.copy(backup_path / "autoencoder.keras", AUTOENCODER_PATH)
            shutil.copy(backup_path / "autoencoder_scaler.pkl", SCALER_PATH)
            shutil.copy(backup_path / "ae_threshold.npy", THRESHOLD_PATH)
            
            logger.info(f"✓ Model restored from {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    def run(self) -> dict:
        """
        Run complete retraining pipeline
        
        Returns:
            Results dictionary with metrics and status
        """
        logger.info("=" * 80)
        logger.info("AUTOMATED RETRAINING PIPELINE")
        logger.info("=" * 80)
        
        try:
            # 1. Backup current model
            if not self.backup_current_model():
                return {'status': 'error', 'message': 'Failed to backup model'}
            
            # 2. Load data
            X_train, X_test, y_test = self.load_training_data()
            
            # 3. Train new model
            autoencoder, encoder, scaler, threshold = self.train_model(X_train)
            
            # 4. Evaluate new model
            metrics = self.evaluate_model(autoencoder, scaler, threshold, X_test, y_test)
            
            # 5. Compare with previous model
            if self.compare_with_previous(metrics):
                # 6. Save new model
                if self.save_model(autoencoder, encoder, scaler, threshold):
                    logger.info("=" * 80)
                    logger.info("✓ RETRAINING SUCCESSFUL - New model deployed")
                    logger.info("=" * 80)
                    
                    return {
                        'status': 'success',
                        'message': 'Model retrained and deployed successfully',
                        'metrics': metrics,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {'status': 'error', 'message': 'Failed to save new model'}
            else:
                # New model is worse, restore backup
                logger.warning("New model performance is worse. Restoring previous model...")
                self.restore_backup()
                
                return {
                    'status': 'rollback',
                    'message': 'New model rejected. Previous model restored.',
                    'metrics': metrics,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Retraining pipeline failed: {e}")
            
            # Try to restore backup
            logger.info("Attempting to restore previous model...")
            self.restore_backup()
            
            return {
                'status': 'error',
                'message': f'Pipeline failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }


if __name__ == "__main__":
    # Run retraining pipeline
    pipeline = RetrainingPipeline()
    results = pipeline.run()
    
    print("\n" + "=" * 80)
    print("RETRAINING RESULTS")
    print("=" * 80)
    print(f"Status: {results['status']}")
    print(f"Message: {results['message']}")
    
    if 'metrics' in results:
        print("\nMetrics:")
        for key, value in results['metrics'].items():
            print(f"  {key}: {value}")
