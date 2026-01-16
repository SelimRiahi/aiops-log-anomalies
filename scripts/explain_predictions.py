"""
Detailed Prediction Examples - Fraud vs Non-Fraud
Shows exactly how the 27 features work to detect fraud
"""

import pandas as pd
import numpy as np
import joblib
import keras

print("=" * 80)
print("DETAILED PREDICTION EXAMPLES")
print("=" * 80)

# Load model and components
autoencoder = keras.models.load_model('autoencoder.keras')
scaler = joblib.load('autoencoder_scaler.pkl')
threshold = np.load('ae_threshold.npy')

# Load test data
df = pd.read_csv('paysim_test.csv')
print(f"\nThreshold: {threshold:.6f}")
print(f"Rule: If reconstruction_error > {threshold:.6f} → FRAUD")

# Get some examples
fraud_samples = df[df['isFraud'] == 1].head(3)
normal_samples = df[df['isFraud'] == 0].head(3)

def explain_transaction(row, label, index):
    print("\n" + "=" * 80)
    print(f"EXAMPLE {index}: {label}")
    print("=" * 80)
    
    # Extract features
    features = row.drop('isFraud').values.reshape(1, -1)
    
    # Make prediction
    features_scaled = scaler.transform(features)
    reconstruction = autoencoder.predict(features_scaled, verbose=0)
    error = np.mean(np.power(features_scaled - reconstruction, 2))
    
    prediction = "FRAUD" if error > threshold else "NORMAL"
    
    print(f"\nActual Label: {label}")
    print(f"Predicted: {prediction} {'✓' if prediction == label else '✗'}")
    print(f"Reconstruction Error: {error:.6f} (threshold: {threshold:.6f})")
    print(f"Confidence: {abs(error - threshold):.6f} above/below threshold")
    
    # Show key features
    print("\n" + "-" * 80)
    print("KEY FEATURE VALUES:")
    print("-" * 80)
    
    feature_names = df.drop('isFraud', axis=1).columns
    
    # Original transaction details
    print(f"\n📊 ORIGINAL TRANSACTION:")
    print(f"  Amount: ${row['amount']:,.2f}")
    print(f"  Type: Transfer={row['is_transfer']}, CashOut={row['is_cashout']}")
    print(f"  Time: Step={row['step']}, Night={row['is_night']}, Weekend={row['is_weekend']}")
    
    # Balance info
    print(f"\n💰 BALANCE DYNAMICS:")
    print(f"  Origin Before: ${row['oldbalanceOrg']:,.2f}")
    print(f"  Origin After:  ${row['newbalanceOrig']:,.2f}")
    print(f"  Dest Before:   ${row['oldbalanceDest']:,.2f}")
    print(f"  Dest After:    ${row['newbalanceDest']:,.2f}")
    print(f"  Balance Change: {row['balance_change_orig']:,.2f}")
    print(f"  Inconsistency: {row['balance_inconsistency_orig']:.4f}")
    
    # Risk indicators
    print(f"\n🚨 RISK INDICATORS:")
    print(f"  Risky Type (TRANSFER/CASHOUT): {bool(row['is_risky_type'])}")
    print(f"  High Amount (top 5%): {bool(row['is_high_amount'])}")
    print(f"  Exceeds Balance: {bool(row['amount_exceeds_balance'])}")
    print(f"  Drains Account: {bool(row['drains_account'])}")
    print(f"  Balance Mismatch: {bool(row['balance_mismatch'])}")
    print(f"  Has Zero Balances: {bool(row['has_zero_balances'])}")
    print(f"  Customer-to-Customer: {bool(row['is_c2c'])}")
    print(f"  Is Merchant Dest: {bool(row['dest_is_merchant'])}")
    print(f"  Composite Risk Score: {row['risk_score']:.1f}")
    
    # Engineered features
    print(f"\n🔧 ENGINEERED FEATURES:")
    print(f"  Amount Log: {row['amount_log']:.4f}")
    print(f"  Amount-to-Balance Ratio: {row['amount_to_oldbalance_ratio']:.4f}")
    print(f"  Hour Sin/Cos: {row['hour_sin']:.4f}, {row['hour_cos']:.4f}")
    
    return error

print("\n" + "=" * 80)
print("FRAUD EXAMPLES")
print("=" * 80)

fraud_errors = []
for idx, (_, row) in enumerate(fraud_samples.iterrows(), 1):
    error = explain_transaction(row, "FRAUD", idx)
    fraud_errors.append(error)

print("\n\n" + "=" * 80)
print("NORMAL EXAMPLES")
print("=" * 80)

normal_errors = []
for idx, (_, row) in enumerate(normal_samples.iterrows(), 4):
    error = explain_transaction(row, "NORMAL", idx)
    normal_errors.append(error)

# Summary
print("\n\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nThreshold: {threshold:.6f}")
print(f"\nFraud Reconstruction Errors:")
for i, err in enumerate(fraud_errors, 1):
    print(f"  Fraud Example {i}: {err:.6f} ({'DETECTED' if err > threshold else 'MISSED'})")

print(f"\nNormal Reconstruction Errors:")
for i, err in enumerate(normal_errors, 1):
    print(f"  Normal Example {i}: {err:.6f} ({'FALSE ALARM' if err > threshold else 'CORRECT'})")

print(f"\n🎯 KEY INSIGHT:")
print(f"   Fraud errors are {np.mean(fraud_errors)/np.mean(normal_errors):.1f}x higher than normal!")
print(f"   This is why the autoencoder can detect fraud effectively.")
