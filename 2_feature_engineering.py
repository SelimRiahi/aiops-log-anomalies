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
   - Raw amount, log amount, amount bins
   - Deviation from user's typical amount
   - Amount-to-balance ratios

2. TEMPORAL FEATURES
   - Hour of day, day of simulation
   - Time since last transaction (user-level)
   - Transaction frequency (last 1h, 6h, 24h)
   
3. BALANCE DYNAMICS
   - Balance change rate
   - Balance volatility
   - Zero balance indicators
   - Balance inconsistencies

4. TRANSACTION TYPE FEATURES
   - One-hot encoding
   - Type switching frequency
   - Risky type indicators (TRANSFER, CASH_OUT)

5. USER BEHAVIOR FEATURES
   - Transaction count history
   - Average transaction size
   - Transaction velocity
   - Behavioral consistency scores

6. ACCOUNT INTERACTION FEATURES
   - Merchant vs Customer transactions
   - Destination account patterns
""")

# ============================================================================
# 1. TRANSACTION AMOUNT FEATURES
# ============================================================================
print("\n[2/9] Creating transaction amount features...")

df['amount_log'] = np.log1p(df['amount'])
df['amount_sqrt'] = np.sqrt(df['amount'])

# Amount bins
df['amount_bin'] = pd.cut(df['amount'], 
                          bins=[0, 1000, 10000, 100000, 1000000, np.inf],
                          labels=['tiny', 'small', 'medium', 'large', 'huge'])
df['amount_bin_encoded'] = df['amount_bin'].cat.codes

# Amount-to-balance ratios
df['amount_to_oldbalance_ratio'] = df['amount'] / (df['oldbalanceOrg'] + 1)
df['amount_exceeds_balance'] = (df['amount'] > df['oldbalanceOrg']).astype(int)

print(f"   Created {6} amount features")

# ============================================================================
# 2. TEMPORAL FEATURES
# ============================================================================
print("\n[3/9] Creating temporal features...")

df['hour'] = df['step'] % 24  # Hour of day (0-23)
df['day'] = df['step'] // 24  # Day of simulation
df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)
df['is_weekend'] = (df['day'] % 7 >= 5).astype(int)  # Simulated weekend

# Cyclical encoding for hour
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

print(f"   Created {7} temporal features")

# ============================================================================
# 3. USER HISTORICAL FEATURES (Rolling Window)
# ============================================================================
print("\n[4/9] Creating user historical features...")
print("   This may take a few minutes...")

# Sort by customer and time
df_sorted = df.sort_values(['nameOrig', 'step']).reset_index(drop=True)

# Calculate time since last transaction
df_sorted['time_since_last_tx'] = df_sorted.groupby('nameOrig')['step'].diff()
df_sorted['time_since_last_tx'] = df_sorted['time_since_last_tx'].fillna(999)

# Transaction count in windows
for window_name, window_hours in [('1h', 1), ('6h', 6), ('24h', 24)]:
    # Count transactions in rolling window
    df_sorted[f'tx_count_{window_name}'] = df_sorted.groupby('nameOrig')['step'].transform(
        lambda x: x.rolling(window=window_hours, min_periods=1).count()
    )

# Cumulative transaction count per user
df_sorted['user_tx_count'] = df_sorted.groupby('nameOrig').cumcount() + 1

# User's average transaction amount (up to current transaction)
df_sorted['user_avg_amount'] = df_sorted.groupby('nameOrig')['amount'].transform(
    lambda x: x.expanding().mean().shift(1)
).fillna(df_sorted['amount'])

df_sorted['user_std_amount'] = df_sorted.groupby('nameOrig')['amount'].transform(
    lambda x: x.expanding().std().shift(1)
).fillna(0)

# Amount deviation from user's average
df_sorted['amount_deviation_from_user_avg'] = (
    df_sorted['amount'] - df_sorted['user_avg_amount']
) / (df_sorted['user_std_amount'] + 1)

# Transaction velocity (amount per hour)
df_sorted['tx_velocity'] = df_sorted['amount'] / (df_sorted['time_since_last_tx'] + 1)

# Merge back to original order
df = df.merge(
    df_sorted[['nameOrig', 'step', 'time_since_last_tx', 'tx_count_1h', 
               'tx_count_6h', 'tx_count_24h', 'user_tx_count', 'user_avg_amount',
               'user_std_amount', 'amount_deviation_from_user_avg', 'tx_velocity']],
    on=['nameOrig', 'step'],
    how='left'
)

print(f"   Created {10} user historical features")

# ============================================================================
# 4. BALANCE DYNAMICS FEATURES
# ============================================================================
print("\n[5/9] Creating balance dynamics features...")

# Balance change
df['balance_change_orig'] = df['newbalanceOrig'] - df['oldbalanceOrg']
df['balance_change_dest'] = df['newbalanceDest'] - df['oldbalanceDest']

# Expected vs actual balance change
df['expected_balance_change'] = -df['amount']  # For origin
df['balance_inconsistency_orig'] = np.abs(
    df['balance_change_orig'] - df['expected_balance_change']
)

# Zero balance indicators
df['orig_zero_balance_before'] = (df['oldbalanceOrg'] == 0).astype(int)
df['orig_zero_balance_after'] = (df['newbalanceOrig'] == 0).astype(int)
df['dest_zero_balance_before'] = (df['oldbalanceDest'] == 0).astype(int)
df['dest_zero_balance_after'] = (df['newbalanceDest'] == 0).astype(int)

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

print(f"   Created {10} balance features")

# ============================================================================
# 5. TRANSACTION TYPE FEATURES
# ============================================================================
print("\n[6/9] Creating transaction type features...")

# One-hot encoding for transaction type
type_dummies = pd.get_dummies(df['type'], prefix='type')
df = pd.concat([df, type_dummies], axis=1)

# Risky transaction types
df['is_risky_type'] = df['type'].isin(['TRANSFER', 'CASH_OUT']).astype(int)

# User's transaction type diversity
df_sorted = df.sort_values(['nameOrig', 'step']).reset_index(drop=True)
df_sorted['user_type_switches'] = (
    df_sorted.groupby('nameOrig')['type'].transform(
        lambda x: (x != x.shift(1)).cumsum()
    )
)

df = df.merge(
    df_sorted[['nameOrig', 'step', 'user_type_switches']],
    on=['nameOrig', 'step'],
    how='left'
)

print(f"   Created {7} transaction type features")

# ============================================================================
# 6. ACCOUNT INTERACTION FEATURES
# ============================================================================
print("\n[7/9] Creating account interaction features...")

# Merchant transactions (destination starts with M)
df['dest_is_merchant'] = df['nameDest'].str.startswith('M').astype(int)

# Customer to customer transactions
df['is_c2c'] = (
    df['nameOrig'].str.startswith('C') & 
    df['nameDest'].str.startswith('C')
).astype(int)

# Destination account activity
dest_tx_count = df.groupby('nameDest').size().to_dict()
df['dest_tx_count'] = df['nameDest'].map(dest_tx_count)
df['dest_is_popular'] = (df['dest_tx_count'] > df['dest_tx_count'].quantile(0.75)).astype(int)

print(f"   Created {4} account interaction features")

# ============================================================================
# 7. AGGREGATE AND COMPOSITE FEATURES
# ============================================================================
print("\n[8/9] Creating composite features...")

# Risk score (heuristic - NOT using fraud labels)
df['risk_score'] = (
    df['is_risky_type'] * 3 +
    df['is_night'] * 1 +
    df['amount_exceeds_balance'] * 2 +
    df['drains_account'] * 3 +
    df['balance_mismatch'] * 2 +
    df['is_c2c'] * 1 +
    (df['time_since_last_tx'] < 1).astype(int) * 2 +
    (df['amount'] > df['amount'].quantile(0.95)).astype(int) * 1
)

# Behavioral consistency score
df['consistency_score'] = (
    1.0 / (1.0 + df['amount_deviation_from_user_avg'].abs()) *
    1.0 / (1.0 + df['user_type_switches'] / (df['user_tx_count'] + 1))
)

# Transaction intensity
df['tx_intensity'] = df['tx_count_1h'] + df['tx_count_6h'] * 0.5 + df['tx_count_24h'] * 0.25

print(f"   Created {3} composite features")

# ============================================================================
# 8. FINAL PREPARATION
# ============================================================================
print("\n[9/9] Preparing final dataset...")

# Drop non-numeric and identifier columns
columns_to_drop = ['nameOrig', 'nameDest', 'type', 'amount_bin']
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
print("FEATURE SUMMARY")
print("=" * 80)
print(f"""
Total features: {len(feature_names)}

Key behavioral features created:
✓ Transaction amount patterns (deviation from user norms)
✓ Temporal patterns (time-based features)
✓ Transaction frequency (rolling windows: 1h, 6h, 24h)
✓ Balance dynamics (changes, inconsistencies, drains)
✓ User behavior (consistency, velocity, history)
✓ Account interaction patterns (C2C, merchant transactions)
✓ Risk indicators (heuristic-based, NO fraud labels)

IMPORTANT: No fraud labels were used in feature creation!
Labels are kept only for evaluation purposes.

Next: Run 3_anomaly_detection.py to train models
""")
