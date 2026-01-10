# Show what features the API creates for a transaction
import pandas as pd
import numpy as np

# Your normal transaction
transaction_data = {
    'step': 50,
    'amount': 250.50,
    'oldbalanceOrg': 10000.0,
    'newbalanceOrig': 9749.50,
    'oldbalanceDest': 5000.0,
    'newbalanceDest': 5250.50,
    'type': 'PAYMENT',
    'nameOrig': 'C1234567890',
    'nameDest': 'M9876543210'
}

df = pd.DataFrame([transaction_data])

# Create features (same as API does)
df['amount_log'] = np.log1p(df['amount'])
df['hour'] = df['step'] % 24
df['user_avg_amount'] = df['amount']  # ← DEFAULT! Should be real average
df['tx_count_1h'] = 1  # ← DEFAULT! Should be real count
df['time_since_last_tx'] = 1.0  # ← DEFAULT! Should be real time
df['user_tx_count'] = 1  # ← DEFAULT! Should be real total

print("=" * 60)
print("FEATURES CREATED FOR YOUR 'NORMAL' TRANSACTION")
print("=" * 60)
print(f"\n📌 ORIGINAL VALUES:")
print(f"   Amount: ${transaction_data['amount']}")
print(f"   Type: {transaction_data['type']}")
print(f"   From: {transaction_data['nameOrig']}")
print(f"   To: {transaction_data['nameDest']}")

print(f"\n🔧 CALCULATED FEATURES:")
print(f"   amount_log: {df['amount_log'].values[0]:.2f}")
print(f"   hour: {df['hour'].values[0]}")

print(f"\n⚠️  PROBLEM - THESE USE DEFAULTS (NO HISTORY):")
print(f"   user_avg_amount: {df['user_avg_amount'].values[0]} ← Should be from history!")
print(f"   tx_count_1h: {df['tx_count_1h'].values[0]} ← Should count real transactions!")
print(f"   time_since_last_tx: {df['time_since_last_tx'].values[0]} ← Should be real time gap!")
print(f"   user_tx_count: {df['user_tx_count'].values[0]} ← Should be user's total!")

print(f"\n💡 WHAT TRAINING DATA HAD:")
print(f"   user_avg_amount: Maybe 1000-5000 (real average)")
print(f"   tx_count_1h: Maybe 3-10 transactions")
print(f"   time_since_last_tx: Maybe 0.5-2 hours")
print(f"   user_tx_count: Maybe 50-200 transactions")

print(f"\n❌ MODEL SEES: 'This pattern is unusual! Never seen defaults like this!'")
print(f"   Result: HIGH reconstruction error → FRAUD")
print("=" * 60)
