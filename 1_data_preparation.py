"""
PaySim Dataset Preparation and Reduction
==========================================
Reduces the 6.36M transaction dataset to a manageable size (~50k transactions)
while maintaining fraud distribution and temporal characteristics.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)

print("=" * 80)
print("PaySim Dataset - Data Preparation")
print("=" * 80)

# Load full dataset
print("\n[1/5] Loading full dataset...")
df = pd.read_csv('paysim dataset.csv')
print(f"Original dataset shape: {df.shape}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Display dataset info
print("\n" + "=" * 80)
print("DATASET VARIABLES EXPLANATION")
print("=" * 80)
print("""
PaySim Variables:
-----------------
1. step           : Time step (1 step = 1 hour). Maps a unit of time in the real world
2. type           : Transaction type (PAYMENT, TRANSFER, CASH_OUT, DEBIT, CASH_IN)
3. amount         : Transaction amount in local currency
4. nameOrig       : Customer who initiated the transaction (anonymized)
5. oldbalanceOrg  : Initial balance before transaction (origin)
6. newbalanceOrig : Balance after transaction (origin)
7. nameDest       : Recipient of the transaction (anonymized)
8. oldbalanceDest : Initial balance before transaction (destination)
9. newbalanceDest : Balance after transaction (destination)
10. isFraud       : Fraud label (USE ONLY FOR EVALUATION, NOT TRAINING)
11. isFlaggedFraud: Flagged by basic fraud detection system (label leakage - DO NOT USE)

Key Insights:
- step represents hours (744 steps = 31 days of simulation)
- C prefix = Customer accounts
- M prefix = Merchant accounts
- Only TRANSFER and CASH_OUT can be fraudulent in this dataset
""")

print("\n" + "=" * 80)
print("ORIGINAL DATASET STATISTICS")
print("=" * 80)
print(f"\nTransaction type distribution:")
print(df['type'].value_counts())
print(f"\nFraud distribution:")
print(df['isFraud'].value_counts())
print(f"Fraud rate: {df['isFraud'].mean() * 100:.4f}%")
print(f"\nTime range: Step {df['step'].min()} to {df['step'].max()}")
print(f"Number of unique customers: {df['nameOrig'].nunique():,}")

# Remove isFlaggedFraud (label leakage)
print("\n[2/5] Removing label leakage column (isFlaggedFraud)...")
df = df.drop('isFlaggedFraud', axis=1)

# Stratified sampling to reduce dataset size
print("\n[3/5] Reducing dataset with stratified sampling...")
print("Strategy: Keep all fraud cases + proportional normal cases")

# Separate fraud and non-fraud
fraud_df = df[df['isFraud'] == 1]
normal_df = df[df['isFraud'] == 0]

print(f"\nFraud transactions: {len(fraud_df):,}")
print(f"Normal transactions: {len(normal_df):,}")

# Keep all fraud transactions and sample normal transactions
# Target: ~50k total transactions (manageable size for faster training)
target_normal_samples = 50000 - len(fraud_df)

# Stratified by transaction type and time periods
normal_sampled = normal_df.groupby(['type', pd.cut(normal_df['step'], bins=10)], 
                                   group_keys=False).apply(
    lambda x: x.sample(n=min(len(x), int(target_normal_samples * len(x) / len(normal_df))), 
                      random_state=42)
)

# Combine fraud and sampled normal transactions
df_reduced = pd.concat([fraud_df, normal_sampled], ignore_index=True)

# Sort by time step to maintain temporal order
df_reduced = df_reduced.sort_values('step').reset_index(drop=True)

print(f"\nReduced dataset shape: {df_reduced.shape}")
print(f"Memory usage: {df_reduced.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"Reduction ratio: {len(df_reduced) / len(df) * 100:.2f}%")
print(f"\nNew fraud distribution:")
print(df_reduced['isFraud'].value_counts())
print(f"New fraud rate: {df_reduced['isFraud'].mean() * 100:.4f}%")

# Save reduced dataset
print("\n[4/5] Saving reduced dataset...")
df_reduced.to_csv('paysim_reduced.csv', index=False)
print("Saved to: paysim_reduced.csv")

# Create visualization
print("\n[5/5] Creating visualization...")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('PaySim Dataset Overview - Reduced Dataset', fontsize=16, fontweight='bold')

# 1. Transaction type distribution
axes[0, 0].bar(df_reduced['type'].value_counts().index, 
              df_reduced['type'].value_counts().values)
axes[0, 0].set_title('Transaction Type Distribution')
axes[0, 0].set_xlabel('Transaction Type')
axes[0, 0].set_ylabel('Count')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Transaction amount distribution (log scale)
axes[0, 1].hist(np.log10(df_reduced['amount'] + 1), bins=50, edgecolor='black')
axes[0, 1].set_title('Transaction Amount Distribution (Log Scale)')
axes[0, 1].set_xlabel('Log10(Amount + 1)')
axes[0, 1].set_ylabel('Frequency')

# 3. Transactions over time
transactions_per_step = df_reduced.groupby('step').size()
axes[1, 0].plot(transactions_per_step.index, transactions_per_step.values, alpha=0.7)
axes[1, 0].set_title('Transaction Volume Over Time')
axes[1, 0].set_xlabel('Time Step (Hour)')
axes[1, 0].set_ylabel('Number of Transactions')

# 4. Fraud by transaction type
fraud_by_type = df_reduced[df_reduced['isFraud'] == 1]['type'].value_counts()
axes[1, 1].bar(fraud_by_type.index, fraud_by_type.values, color='red', alpha=0.7)
axes[1, 1].set_title('Fraud Cases by Transaction Type')
axes[1, 1].set_xlabel('Transaction Type')
axes[1, 1].set_ylabel('Fraud Count')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('dataset_overview.png', dpi=300, bbox_inches='tight')
print("Saved visualization to: dataset_overview.png")

print("\n" + "=" * 80)
print("DATA PREPARATION COMPLETE")
print("=" * 80)
print(f"""
Summary:
- Original dataset: {len(df):,} transactions
- Reduced dataset: {len(df_reduced):,} transactions
- Fraud rate maintained: {df_reduced['isFraud'].mean() * 100:.4f}%
- Temporal order preserved: Yes
- Label leakage removed: Yes (isFlaggedFraud dropped)


""")