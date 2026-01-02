"""
Autoencoder Training and Evaluation
====================================
Train Autoencoder model on normal transactions and evaluate performance.
Uses unsupervised learning - NO fraud labels in training.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, roc_auc_score, confusion_matrix
import tensorflow as tf
import keras
from keras import layers
import joblib
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
tf.random.set_seed(42)

print("=" * 80)
print("Autoencoder Training and Evaluation")
print("=" * 80)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================
print("\n[1/5] Loading engineered features...")
df = pd.read_csv('paysim_features.csv')
print(f"Dataset shape: {df.shape}")

# Separate features and labels
fraud_labels = df['isFraud'].copy()
X = df.drop('isFraud', axis=1)

print(f"Features: {X.shape[1]}")
print(f"Fraud rate: {fraud_labels.mean() * 100:.4f}%")

# Train on NORMAL transactions only (unsupervised learning)
print("\n[2/5] Selecting normal transactions for training...")

# Use only normal transactions for training
normal_mask = fraud_labels == 0
X_train_normal = X[normal_mask].copy()

print(f"\nTraining set (normal only): {X_train_normal.shape}")

# Scale features
print("\n[3/5] Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_normal)

# Also scale the full dataset for evaluation
X_full_scaled = scaler.transform(X)

# Save scaler
joblib.dump(scaler, 'autoencoder_scaler.pkl')
print("Saved: autoencoder_scaler.pkl")

# ============================================================================
# 2. BUILD AND TRAIN AUTOENCODER
# ============================================================================
print("\n" + "=" * 80)
print("AUTOENCODER MODEL")
print("=" * 80)
print("""
Autoencoder Algorithm:
- Neural network that learns to compress and reconstruct normal data
- High reconstruction error = anomaly
- Can learn complex non-linear patterns
- Best performing model for this task

Architecture:
- Encoder: 50 → 64 → 32 → 16 (compressed representation)
- Decoder: 16 → 32 → 64 → 50 (reconstruction)
- Batch norm5lization and dropout for regularization
""")

print("\n[4/6] Building and training Autoencoder...")

input_dim = X_train_scaled.shape[1]
encoding_dim = 16  # Compressed representation

# Build autoencoder architecture
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

print("\nAutoencoder Architecture:")
autoencoder.summary()

# Train on normal transactions only
print("\nTraining autoencoder on normal transactions...")
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

# ============================================================================
# 3. EVALUATE MODEL PERFORMANCE
# ============================================================================
print("\n[5/5] Evaluating model performance...")

# Calculate reconstruction errors on training set
train_reconstructions = autoencoder.predict(X_train_scaled, verbose=0)
train_mse = np.mean(np.power(X_train_scaled - train_reconstructions, 2), axis=1)

# Set threshold at 95th percentile of training errors
threshold = np.percentile(train_mse, 95)
print(f"\nThreshold (95th percentile): {threshold:.6f}")

# Evaluate on full dataset (including frauds)
full_reconstructions = autoencoder.predict(X_full_scaled, verbose=0)
full_mse = np.mean(np.power(X_full_scaled - full_reconstructions, 2), axis=1)

# Predict anomalies
predictions = (full_mse > threshold).astype(int)

# Calculate metrics
print("\n" + "=" * 80)
print("PERFORMANCE METRICS")
print("=" * 80)

accuracy = accuracy_score(fraud_labels, predictions)
precision = precision_score(fraud_labels, predictions, zero_division=0)
recall = recall_score(fraud_labels, predictions, zero_division=0)
f1 = f1_score(fraud_labels, predictions, zero_division=0)
roc_auc = roc_auc_score(fraud_labels, full_mse)

print(f"\n✓ Accuracy:   {accuracy:.4f} ({accuracy * 100:.2f}%)")
print(f"✓ Precision:  {precision:.4f} ({precision * 100:.2f}%)")
print(f"✓ Recall:     {recall:.4f} ({recall * 100:.2f}%)")
print(f"✓ F1-Score:   {f1:.4f} ({f1 * 100:.2f}%)")
print(f"✓ ROC-AUC:    {roc_auc:.4f}")

# Calculate confusion matrix (for visualizations only, not printed)
cm = confusion_matrix(fraud_labels, predictions)
tn, fp, fn, tp = cm.ravel()

# Save model and components (silently)
autoencoder.save('autoencoder.keras')
encoder.save('encoder.keras')
np.save('ae_threshold.npy', threshold)

# ============================================================================
# 4. CREATE VISUALIZATIONS
# ============================================================================

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

# 1. Training history
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(history.history['loss'], label='Training Loss', linewidth=2, color='blue')
ax1.plot(history.history['val_loss'], label='Validation Loss', linewidth=2, color='orange')
ax1.set_title('Training History', fontsize=12, fontweight='bold')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('MSE Loss')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Reconstruction error distribution
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(full_mse[fraud_labels==0], bins=50, alpha=0.6, label='Normal', color='blue', density=True)
ax2.hist(full_mse[fraud_labels==1], bins=50, alpha=0.6, label='Fraud', color='red', density=True)
ax2.axvline(threshold, color='green', linestyle='--', linewidth=2, label=f'Threshold: {threshold:.4f}')
ax2.set_title('Reconstruction Error Distribution', fontsize=12, fontweight='bold')
ax2.set_xlabel('MSE')
ax2.set_ylabel('Density')
ax2.legend()
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

# 3. Confusion Matrix
ax3 = fig.add_subplot(gs[0, 2])
sns.heatmap([[tn, fp], [fn, tp]], annot=True, fmt='d', cmap='Blues', ax=ax3,
            cbar_kws={'label': 'Count'}, annot_kws={'fontsize': 14})
ax3.set_title('Confusion Matrix', fontsize=12, fontweight='bold')
ax3.set_xlabel('Predicted')
ax3.set_ylabel('Actual')
ax3.set_xticklabels(['Normal', 'Fraud'])
ax3.set_yticklabels(['Normal', 'Fraud'])

# 4. Performance Metrics
ax4 = fig.add_subplot(gs[1, 0])
metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
values = [accuracy, precision, recall, f1, roc_auc]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
bars = ax4.bar(metrics, values, color=colors, alpha=0.7)
ax4.set_title('Performance Metrics', fontsize=12, fontweight='bold')
ax4.set_ylabel('Score')
ax4.set_ylim(0, 1.0)
ax4.grid(True, alpha=0.3, axis='y')
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
            f'{height:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

# 5. Error by class
ax5 = fig.add_subplot(gs[1, 1])
ax5.boxplot([full_mse[fraud_labels==0], full_mse[fraud_labels==1]], 
            labels=['Normal', 'Fraud'], patch_artist=True,
            boxprops=dict(facecolor='lightblue', alpha=0.7),
            medianprops=dict(color='red', linewidth=2))
ax5.axhline(threshold, color='green', linestyle='--', linewidth=2, label='Threshold')
ax5.set_title('Reconstruction Error by Class', fontsize=12, fontweight='bold')
ax5.set_ylabel('MSE')
ax5.set_yscale('log')
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# 6. Training vs Threshold
ax6 = fig.add_subplot(gs[1, 2])
ax6.hist(train_mse, bins=50, alpha=0.7, edgecolor='black', color='steelblue')
ax6.axvline(threshold, color='red', linestyle='--', linewidth=2.5, 
            label=f'Threshold (95th): {threshold:.4f}')
ax6.axvline(train_mse.mean(), color='green', linestyle='--', linewidth=2, 
            label=f'Mean: {train_mse.mean():.4f}')
ax6.set_title('Training Reconstruction Errors', fontsize=12, fontweight='bold')
ax6.set_xlabel('MSE')
ax6.set_ylabel('Frequency')
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

plt.suptitle('Autoencoder Training and Evaluation Results', 
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('autoencoder_results.png', dpi=300, bbox_inches='tight')

# ============================================================================
# 5. SUMMARY
# ============================================================================
