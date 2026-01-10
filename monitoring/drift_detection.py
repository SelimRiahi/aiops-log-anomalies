"""
Data Drift Detection - Monitor distribution changes in incoming data
"""
import numpy as np
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from scipy import stats
import json

logger = logging.getLogger(__name__)


class DriftDetector:
    """Detect data drift by comparing distributions"""
    
    def __init__(self, reference_data_path: str = None, threshold: float = 0.05):
        """
        Args:
            reference_data_path: Path to reference (training) data
            threshold: P-value threshold for drift detection
        """
        self.threshold = threshold
        self.reference_data = None
        self.reference_stats = {}
        self.drift_reports = []
        
        if reference_data_path:
            self.load_reference_data(reference_data_path)
    
    def load_reference_data(self, data_path: str):
        """Load reference dataset (training data)"""
        try:
            logger.info(f"Loading reference data from {data_path}")
            self.reference_data = pd.read_csv(data_path)
            
            # Remove fraud label if present
            if 'isFraud' in self.reference_data.columns:
                # Use only normal transactions as reference
                self.reference_data = self.reference_data[
                    self.reference_data['isFraud'] == 0
                ].drop('isFraud', axis=1)
            
            # Calculate statistics for each numeric column
            for col in self.reference_data.select_dtypes(include=[np.number]).columns:
                self.reference_stats[col] = {
                    'mean': self.reference_data[col].mean(),
                    'std': self.reference_data[col].std(),
                    'min': self.reference_data[col].min(),
                    'max': self.reference_data[col].max(),
                    'median': self.reference_data[col].median()
                }
            
            logger.info(f"Reference data loaded: {self.reference_data.shape}")
            
        except Exception as e:
            logger.error(f"Error loading reference data: {e}")
            raise
    
    def detect_drift_ks_test(
        self, 
        current_data: pd.DataFrame,
        columns: List[str] = None
    ) -> Dict[str, Dict]:
        """
        Detect drift using Kolmogorov-Smirnov test
        
        Returns:
            Dictionary with drift results for each column
        """
        if self.reference_data is None:
            logger.warning("No reference data loaded")
            return {}
        
        if columns is None:
            columns = [
                col for col in self.reference_data.columns 
                if col in current_data.columns and 
                self.reference_data[col].dtype in [np.float64, np.int64]
            ]
        
        results = {}
        
        for col in columns:
            try:
                # Perform KS test
                statistic, p_value = stats.ks_2samp(
                    self.reference_data[col].dropna(),
                    current_data[col].dropna()
                )
                
                is_drifted = p_value < self.threshold
                
                results[col] = {
                    'statistic': float(statistic),
                    'p_value': float(p_value),
                    'is_drifted': is_drifted,
                    'threshold': self.threshold,
                    'reference_mean': float(self.reference_stats[col]['mean']),
                    'current_mean': float(current_data[col].mean()),
                    'mean_diff_pct': float(
                        abs(current_data[col].mean() - self.reference_stats[col]['mean']) / 
                        (self.reference_stats[col]['mean'] + 1e-10) * 100
                    )
                }
                
            except Exception as e:
                logger.error(f"Error testing drift for column {col}: {e}")
                results[col] = {'error': str(e)}
        
        return results
    
    def detect_drift_psi(
        self,
        current_data: pd.DataFrame,
        column: str,
        buckets: int = 10
    ) -> float:
        """
        Calculate Population Stability Index (PSI) for a column
        
        PSI < 0.1: No significant change
        0.1 <= PSI < 0.2: Moderate change
        PSI >= 0.2: Significant change
        """
        if self.reference_data is None:
            return None
        
        try:
            # Create buckets based on reference data
            _, bins = pd.cut(
                self.reference_data[column],
                bins=buckets,
                retbins=True,
                duplicates='drop'
            )
            
            # Calculate distributions
            ref_dist = pd.cut(
                self.reference_data[column],
                bins=bins,
                include_lowest=True
            ).value_counts(normalize=True).sort_index()
            
            curr_dist = pd.cut(
                current_data[column],
                bins=bins,
                include_lowest=True
            ).value_counts(normalize=True).sort_index()
            
            # Align indices
            ref_dist, curr_dist = ref_dist.align(curr_dist, fill_value=0.0001)
            
            # Calculate PSI
            psi = np.sum((curr_dist - ref_dist) * np.log(curr_dist / ref_dist))
            
            return float(psi)
            
        except Exception as e:
            logger.error(f"Error calculating PSI for {column}: {e}")
            return None
    
    def check_drift(
        self,
        current_data: pd.DataFrame,
        save_report: bool = True
    ) -> Dict:
        """
        Comprehensive drift check
        
        Returns:
            Drift report with all metrics
        """
        logger.info("Running drift detection...")
        
        # KS test for all numeric columns
        ks_results = self.detect_drift_ks_test(current_data)
        
        # Count drifted columns
        drifted_columns = [
            col for col, result in ks_results.items()
            if result.get('is_drifted', False)
        ]
        
        # Overall drift status
        is_drifted = len(drifted_columns) > 0
        drift_severity = len(drifted_columns) / len(ks_results) if ks_results else 0
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'is_drifted': is_drifted,
            'drift_severity': drift_severity,
            'drifted_columns': drifted_columns,
            'num_drifted': len(drifted_columns),
            'num_tested': len(ks_results),
            'column_results': ks_results,
            'recommendation': self._get_recommendation(drift_severity)
        }
        
        # Save report
        if save_report:
            self.drift_reports.append(report)
            self._save_report(report)
        
        # Log results
        if is_drifted:
            logger.warning(
                f"⚠️  DRIFT DETECTED! {len(drifted_columns)}/{len(ks_results)} columns drifted"
            )
            logger.warning(f"Drifted columns: {drifted_columns}")
        else:
            logger.info("✓ No significant drift detected")
        
        return report
    
    def _get_recommendation(self, severity: float) -> str:
        """Get recommendation based on drift severity"""
        if severity == 0:
            return "No action needed. Data distribution is stable."
        elif severity < 0.2:
            return "Minor drift detected. Monitor closely."
        elif severity < 0.5:
            return "Moderate drift detected. Consider retraining soon."
        else:
            return "Severe drift detected! Retrain model immediately."
    
    def _save_report(self, report: Dict):
        """Save drift report to file"""
        try:
            report_file = Path(__file__).parent.parent / 'logs' / 'drift_reports.jsonl'
            report_file.parent.mkdir(exist_ok=True)
            
            with open(report_file, 'a') as f:
                f.write(json.dumps(report) + '\n')
                
        except Exception as e:
            logger.error(f"Error saving drift report: {e}")


# Global drift detector instance
drift_detector = DriftDetector()
