"""
Drift Check Script
==================
Periodically check for data drift and trigger retraining if needed
"""
import logging
from pathlib import Path
import sys
import pandas as pd
from datetime import datetime
import json

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from monitoring.drift_detection import drift_detector
from pipelines.retrain_pipeline import RetrainingPipeline
from config.config import DATA_DIR, LOGS_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_drift_and_retrain(
    reference_data_path: str,
    current_data_path: str,
    auto_retrain: bool = True
):
    """
    Check for drift and optionally trigger retraining
    
    Args:
        reference_data_path: Path to reference (training) data
        current_data_path: Path to current/recent data
        auto_retrain: Whether to automatically retrain if drift detected
    """
    logger.info("=" * 80)
    logger.info("DRIFT DETECTION & AUTO-RETRAINING")
    logger.info("=" * 80)
    
    try:
        # Load reference data
        drift_detector.load_reference_data(reference_data_path)
        
        # Load current data
        logger.info(f"Loading current data from {current_data_path}")
        current_data = pd.read_csv(current_data_path)
        
        if 'isFraud' in current_data.columns:
            current_data = current_data.drop('isFraud', axis=1)
        
        logger.info(f"Current data shape: {current_data.shape}")
        
        # Check for drift
        drift_report = drift_detector.check_drift(current_data, save_report=True)
        
        # Print results
        logger.info("\n" + "=" * 80)
        logger.info("DRIFT DETECTION RESULTS")
        logger.info("=" * 80)
        logger.info(f"Drift detected: {drift_report['is_drifted']}")
        logger.info(f"Severity: {drift_report['drift_severity'] * 100:.1f}%")
        logger.info(f"Drifted columns: {len(drift_report['drifted_columns'])}/{drift_report['num_tested']}")
        
        if drift_report['drifted_columns']:
            logger.info(f"Columns: {', '.join(drift_report['drifted_columns'])}")
        
        logger.info(f"\nRecommendation: {drift_report['recommendation']}")
        
        # Decide if retraining is needed
        should_retrain = drift_report['is_drifted'] and drift_report['drift_severity'] >= 0.3
        
        if should_retrain and auto_retrain:
            logger.info("\n" + "=" * 80)
            logger.info("Drift severity high. Triggering automatic retraining...")
            logger.info("=" * 80)
            
            # Run retraining pipeline
            pipeline = RetrainingPipeline()
            retrain_results = pipeline.run()
            
            # Save combined results
            combined_results = {
                'timestamp': datetime.now().isoformat(),
                'drift_report': drift_report,
                'retrain_results': retrain_results
            }
            
            results_file = LOGS_DIR / 'drift_retrain_log.jsonl'
            with open(results_file, 'a') as f:
                f.write(json.dumps(combined_results) + '\n')
            
            return combined_results
        
        elif should_retrain:
            logger.warning("\n⚠️  Retraining recommended but auto-retrain is disabled")
            logger.warning("Run retraining manually or enable auto_retrain")
        
        else:
            logger.info("\n✓ No retraining needed at this time")
        
        return {'drift_report': drift_report}
        
    except Exception as e:
        logger.error(f"Error in drift check: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    reference_data = DATA_DIR / "paysim_features.csv"
    
    # For testing, use test data as "current" data
    # In production, this would be recent production data
    current_data = DATA_DIR / "paysim_test.csv"
    
    if not reference_data.exists():
        logger.error(f"Reference data not found: {reference_data}")
        logger.error("Run training pipeline first to generate features")
        sys.exit(1)
    
    if not current_data.exists():
        logger.error(f"Current data not found: {current_data}")
        logger.error("Using reference data for demonstration")
        current_data = reference_data
    
    # Run drift check (without auto-retrain for safety)
    results = check_drift_and_retrain(
        str(reference_data),
        str(current_data),
        auto_retrain=False  # Set to True to enable auto-retraining
    )
    
    logger.info("\n✓ Drift check completed")
