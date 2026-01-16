"""
Fraud Detection Predictions
============================
Load trained Autoencoder model and make predictions on test data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import keras
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("FRAUD DETECTION - PREDICTIONS ON TEST DATA")
print("=" * 80)

# ============================================================================
# 1. LOAD TRAINED MODEL AND COMPONENTS
# ============================================================================
print("\n[1/4] Loading trained model and components...")

# Load the trained autoencoder
autoencoder = keras.models.load_model('autoencoder.keras')
print("✓ Loaded: autoencoder.keras")

# Load the scaler
scaler = joblib.load('autoencoder_scaler.pkl')
print("✓ Loaded: autoencoder_scaler.pkl")

# Load the threshold
threshold = np.load('ae_threshold.npy')
print(f"✓ Loaded threshold: {threshold:.6f}")

# ============================================================================
# 2. LOAD TEST DATA
# ============================================================================
print("\n[2/4] Loading test data (20% of dataset)...")

# Load the test set created by training script
df_test = pd.read_csv('paysim_test.csv')
print(f"Test set shape: {df_test.shape}")

# Separate features and labels
y_true = df_test['isFraud'].values
X_test = df_test.drop('isFraud', axis=1).values

print(f"Total test samples: {len(X_test)}")
print(f"Normal transactions: {(y_true == 0).sum()} ({(y_true == 0).mean() * 100:.2f}%)")
print(f"Fraud transactions: {(y_true == 1).sum()} ({(y_true == 1).mean() * 100:.2f}%)")

# ============================================================================
# 3. MAKE PREDICTIONS
# ============================================================================
print("\n[3/4] Making predictions...")

# Scale the test data
X_test_scaled = scaler.transform(X_test)
print("✓ Features scaled")

# Get reconstructions
reconstructions = autoencoder.predict(X_test_scaled, verbose=0)
print("✓ Reconstructions generated")

# Calculate reconstruction errors (MSE)
mse = np.mean(np.power(X_test_scaled - reconstructions, 2), axis=1)
print("✓ Reconstruction errors calculated")

# Predict: 1 if error > threshold, 0 otherwise
y_pred = (mse > threshold).astype(int)
print("✓ Predictions made")

# ============================================================================
# 4. EVALUATION METRICS
# ============================================================================
print("\n" + "=" * 80)
print("PREDICTION RESULTS (TEST SET - 20%)")
print("=" * 80)

# Classification report
print("\nClassification Report:")
print(classification_report(y_true, y_pred, 
                          target_names=['Normal', 'Fraud'],
                          digits=4))

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = cm.ravel()

print("\nConfusion Matrix:")
print(f"True Negatives (TN):  {tn:5d} - Correctly identified normal transactions")
print(f"False Positives (FP): {fp:5d} - Normal flagged as fraud (False Alarm)")
print(f"False Negatives (FN): {fn:5d} - Fraud missed (Dangerous!)")
print(f"True Positives (TP):  {tp:5d} - Correctly detected frauds")

# Additional metrics
print("\nDetailed Metrics:")
print(f"Total Predictions: {len(y_pred)}")
print(f"Frauds Detected: {y_pred.sum()} ({y_pred.mean() * 100:.2f}%)")
print(f"True Frauds: {y_true.sum()} ({y_true.mean() * 100:.2f}%)")
print(f"Detection Rate: {tp / y_true.sum() * 100:.2f}% of frauds caught")
print(f"False Alarm Rate: {fp / (tn + fp) * 100:.4f}% of normal transactions flagged")

# ============================================================================
# 5. VISUALIZATIONS
# ============================================================================
print("\n[4/4] Generating visualizations...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

# 1. Reconstruction Error Distribution
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(mse[y_true==0], bins=50, alpha=0.6, label='Normal', color='blue', density=True)
ax1.hist(mse[y_true==1], bins=50, alpha=0.6, label='Fraud', color='red', density=True)
ax1.axvline(threshold, color='green', linestyle='--', linewidth=2, label=f'Threshold: {threshold:.4f}')
ax1.set_xlabel('Reconstruction Error (MSE)')
ax1.set_ylabel('Density')
ax1.set_title('Reconstruction Error Distribution', fontweight='bold')
ax1.legend()
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)

# 2. Confusion Matrix Heatmap
ax2 = fig.add_subplot(gs[0, 1])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2,
            xticklabels=['Normal', 'Fraud'],
            yticklabels=['Normal', 'Fraud'],
            cbar_kws={'label': 'Count'})
ax2.set_xlabel('Predicted')
ax2.set_ylabel('Actual')
ax2.set_title('Confusion Matrix', fontweight='bold')

# 3. ROC Curve
ax3 = fig.add_subplot(gs[0, 2])
fpr, tpr, _ = roc_curve(y_true, mse)
roc_auc = auc(fpr, tpr)
ax3.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
ax3.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
ax3.set_xlabel('False Positive Rate')
ax3.set_ylabel('True Positive Rate')
ax3.set_title('ROC Curve', fontweight='bold')
ax3.legend(loc='lower right')
ax3.grid(True, alpha=0.3)

# 4. Prediction Distribution
ax4 = fig.add_subplot(gs[1, 0])
prediction_counts = pd.Series(y_pred).value_counts().sort_index()
colors = ['#2ca02c', '#d62728']
bars = ax4.bar(['Normal', 'Fraud'], prediction_counts.values, color=colors, alpha=0.7)
ax4.set_ylabel('Count')
ax4.set_title('Prediction Distribution', fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontweight='bold')

# 5. Error Boxplot by Class
ax5 = fig.add_subplot(gs[1, 1])
ax5.boxplot([mse[y_true==0], mse[y_true==1]], 
            labels=['Normal', 'Fraud'],
            patch_artist=True,
            boxprops=dict(facecolor='lightblue', alpha=0.7),
            medianprops=dict(color='red', linewidth=2))
ax5.axhline(threshold, color='green', linestyle='--', linewidth=2, label='Threshold')
ax5.set_ylabel('Reconstruction Error (MSE)')
ax5.set_title('Error Distribution by Class', fontweight='bold')
ax5.set_yscale('log')
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# 6. Prediction Accuracy
ax6 = fig.add_subplot(gs[1, 2])
categories = ['Correct\nPredictions', 'Incorrect\nPredictions']
correct_count = (y_pred == y_true).sum()
incorrect_count = (y_pred != y_true).sum()
counts = [correct_count, incorrect_count]
colors_acc = ['#2ca02c', '#d62728']
bars = ax6.bar(categories, counts, color=colors_acc, alpha=0.7)
ax6.set_ylabel('Count')
ax6.set_title('Prediction Accuracy', fontweight='bold')
ax6.grid(True, alpha=0.3, axis='y')
for bar, count in zip(bars, counts):
    height = bar.get_height()
    percentage = count / len(y_pred) * 100
    ax6.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}\n({percentage:.2f}%)',
            ha='center', va='bottom', fontweight='bold')

plt.suptitle('Fraud Detection - Prediction Results', 
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('prediction_results.png', dpi=300, bbox_inches='tight')
print("✓ Saved: prediction_results.png")

print("\n" + "=" * 80)
print("PREDICTION COMPLETED SUCCESSFULLY!")
print("=" * 80)
