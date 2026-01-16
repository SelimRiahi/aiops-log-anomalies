"""
Feature Engineering for Anomaly Detection and Incident Prediction
==================================================================
Creates behavioral features WITHOUT using fraud labels.
Focus: Transaction patterns, temporal features, balance dynamics.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

print("=" * 80)
print("Feature Engineering - Behavioral Pattern Analysis")
print("=" * 80)

# Load reduced dataset
print("\n[1/9] Loading reduced dataset...")
df = pd.read_csv('paysim_reduced.csv')
print(f"Dataset shape: {df.shape}")

# Store fraud labels separately (for evaluation only, NOT for training)
fraud_labels = df['isFraud'].copy()
df = df.drop('isFraud', axis=1)

print("\n" + "=" * 80)
print("FEATURE CATEGORIES")
print("=" * 80)
print("""
We will create features in these categories (NO FRAUD LABELS USED):

1. TRANSACTION AMOUNT FEATURES
   - Log-transformed amount
   - Amount-to-balance ratios
   - High amount indicators

2. TEMPORAL FEATURES
   - Cyclical hour encoding (sin/cos)
   - Night/weekend indicators
   
3. BALANCE DYNAMICS
   - Balance changes and inconsistencies
   - Zero balance indicators
   - Account drain detection

4. TRANSACTION TYPE FEATURES
   - Risky type indicators (TRANSFER, CASH_OUT)
   - Type encoding

5. ACCOUNT INTERACTION FEATURES
   - Merchant vs Customer transactions
   - Customer-to-customer patterns

REMOVED (Won't work in production):
✗ User historical features (user_avg_amount, user_tx_count)
✗ Time-based aggregations (tx_count_1h, tx_count_6h)
✗ User-specific patterns requiring account history
""")

# ============================================================================
# 1. TRANSACTION AMOUNT FEATURES
# ============================================================================
print("\n[2/5] Creating transaction amount features...")

df['amount_log'] = np.log1p(df['amount'])

# Amount-to-balance ratios
df['amount_to_oldbalance_ratio'] = df['amount'] / (df['oldbalanceOrg'] + 1)
df['amount_exceeds_balance'] = (df['amount'] > df['oldbalanceOrg']).astype(int)

# High amount indicator (top 5%)
df['is_high_amount'] = (df['amount'] > df['amount'].quantile(0.95)).astype(int)

print(f"   Created {4} amount features")

# ============================================================================
# 2. TEMPORAL FEATURES
# ============================================================================
print("\n[3/5] Creating temporal features...")

hour = df['step'] % 24
day = df['step'] // 24

df['is_night'] = ((hour >= 22) | (hour <= 6)).astype(int)
df['is_weekend'] = (day % 7 >= 5).astype(int)  # Simulated weekend

# Cyclical encoding for hour (best for neural networks)
df['hour_sin'] = np.sin(2 * np.pi * hour / 24)
df['hour_cos'] = np.cos(2 * np.pi * hour / 24)

print(f"   Created {4} temporal features")

# ============================================================================
# 3. BALANCE DYNAMICS FEATURES
# ============================================================================
print("\n[4/5] Creating balance dynamics features...")

# Balance change
df['balance_change_orig'] = df['newbalanceOrig'] - df['oldbalanceOrg']
df['balance_change_dest'] = df['newbalanceDest'] - df['oldbalanceDest']

# Expected vs actual balance change
df['expected_balance_change'] = -df['amount']  # For origin
df['balance_inconsistency_orig'] = np.abs(
    df['balance_change_orig'] - df['expected_balance_change']
)

# Zero balance indicators (combined)
df['has_zero_balances'] = (
    (df['oldbalanceOrg'] == 0) | (df['newbalanceOrig'] == 0) |
    (df['oldbalanceDest'] == 0) | (df['newbalanceDest'] == 0)
).astype(int)

# Balance drain (empties account)
df['drains_account'] = (
    (df['oldbalanceOrg'] > 0) & (df['newbalanceOrig'] == 0)
).astype(int)

# Suspicious balance patterns
df['balance_mismatch'] = (
    (df['oldbalanceOrg'] != 0) & 
    (df['newbalanceOrig'] != 0) & 
    (df['balance_inconsistency_orig'] > 0.01)
).astype(int)

print(f"   Created {7} balance features")

# ============================================================================
# 4. TRANSACTION TYPE & ACCOUNT FEATURES
# ============================================================================
print("\n[5/5] Creating transaction type and account features...")

# Keep only risky types (TRANSFER and CASH_OUT are fraud-prone)
df['is_transfer'] = (df['type'] == 'TRANSFER').astype(int)
df['is_cashout'] = (df['type'] == 'CASH_OUT').astype(int)
df['is_risky_type'] = df['type'].isin(['TRANSFER', 'CASH_OUT']).astype(int)

# Account interaction patterns
df['dest_is_merchant'] = df['nameDest'].str.startswith('M').astype(int)
df['is_c2c'] = (
    df['nameOrig'].str.startswith('C') & 
    df['nameDest'].str.startswith('C')
).astype(int)

# Composite risk score (heuristic - NOT using fraud labels)
df['risk_score'] = (
    df['is_risky_type'] * 3 +
    df['is_night'] * 1 +
    df['amount_exceeds_balance'] * 2 +
    df['drains_account'] * 3 +
    df['balance_mismatch'] * 2 +
    df['is_c2c'] * 1 +
    df['is_high_amount'] * 1
)

print(f"   Created {8} type and account features")

# ============================================================================
# 5. FINAL PREPARATION
# ============================================================================
print("\nPreparing final dataset...")

# Drop non-numeric and identifier columns
columns_to_drop = ['nameOrig', 'nameDest', 'type']
df_features = df.drop(columns=columns_to_drop)

# Add fraud labels back (for evaluation only)
df_features['isFraud'] = fraud_labels.values

# Fill any remaining NaN values
df_features = df_features.fillna(0)

# Save engineered features
df_features.to_csv('paysim_features.csv', index=False)
print(f"\nFeature engineering complete!")
print(f"Final shape: {df_features.shape}")
print(f"Total features created: {df_features.shape[1] - 1} (excluding isFraud)")

# Save feature names for reference
feature_names = [col for col in df_features.columns if col != 'isFraud']
with open('feature_names.txt', 'w') as f:
    f.write("FEATURE LIST\n")
    f.write("=" * 80 + "\n\n")
    for i, feature in enumerate(feature_names, 1):
        f.write(f"{i:2d}. {feature}\n")

print("\nSaved files:")
print("  - paysim_features.csv (engineered dataset)")
print("  - feature_names.txt (feature list)")

print("\n" + "=" * 80)
print("OPTIMIZED FEATURE SUMMARY")
print("=" * 80)
print(f"""
Total features: {len(feature_names)} (OPTIMIZED from 50)

Feature categories:
✓ Original features (6): step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest
✓ Amount features (4): amount_log, ratios, exceeds_balance, high_amount
✓ Temporal features (4): night, weekend, hour_sin, hour_cos
✓ Balance features (7): changes, inconsistencies, drains, zero indicators
✓ Type & Account (8): transfer, cashout, risky_type, merchant, c2c, risk_score

REMOVED (Won't work in production):
✗ User-specific history (user_avg_amount, user_tx_count, etc.)
✗ Time-based aggregations (tx_count_1h, tx_count_6h, tx_count_24h)
✗ Redundant transformations (amount_sqrt, hour, day)
✗ Multiple one-hot encodings for transaction types

IMPORTANT: No fraud labels were used in feature creation!
All features work in production without account history.

Next: Run 3_train.py to train the autoencoder model
""")
