import pandas as pd

df = pd.read_csv('paysim_test.csv')

print("=" * 80)
print("ACTUAL FRAUD LABELS vs PREDICTIONS")
print("=" * 80)
print()
print(f"{'Sample':<8} {'Amount':<12} {'Type':<10} {'ACTUAL LABEL':<15} {'Model Prediction'}")
print("-" * 80)

for idx in [0, 13, 25, 50, 100]:
    row = df.iloc[idx]
    
    tx_type = "TRANSFER" if row['type_TRANSFER'] == 1 else \
              "CASH_OUT" if row['type_CASH_OUT'] == 1 else \
              "PAYMENT" if row['type_PAYMENT'] == 1 else \
              "DEBIT" if row['type_DEBIT'] == 1 else "CASH_IN"
    
    actual = "FRAUD" if row['isFraud'] == 1 else "NORMAL"
    
    # Prediction based on reconstruction error vs threshold
    recon_error = 0  # Will be calculated by model
    predicted = "?"  # We'll show what model predicted
    
    print(f"{idx:<8} ${row['amount']:<11.2f} {tx_type:<10} {actual:<15} (See API result)")

print()
print("Compare with your test results above!")
print("=" * 80)
