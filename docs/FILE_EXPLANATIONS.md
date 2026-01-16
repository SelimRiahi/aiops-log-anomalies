# 📚 Complete File & Folder Explanations

## 📁 Folder Structure Overview

```
aiops-log-anomalies/
├── 📂 api/              → Production API (FastAPI)
├── 📂 monitoring/       → Dashboard & observability
├── 📂 models/           → Trained ML models & artifacts
├── 📂 data/             → Datasets (CSV files)
├── 📂 scripts/          → Training & data preparation
├── 📂 pipelines/        → MLOps automation
├── 📂 docs/             → Documentation
├── 📂 config/           → Configuration files
├── 📂 logs/             → Application logs
└── 📂 .github/          → CI/CD workflows
```

---

## 🚀 1. API Folder (`api/`)

**Purpose**: Production-ready REST API for real-time fraud detection

### Files:

#### `main.py` ⭐ **MAIN API ENTRY POINT**

- **What it does**: FastAPI application that receives transaction requests and returns fraud predictions
- **Key features**:
  - POST `/predict` - Accepts 9 transaction fields, returns fraud prediction
  - GET `/health` - Health check endpoint for Docker
  - GET `/metrics` - System metrics (latency, throughput)
- **Flow**: Receives request → Validates data → Loads model → Engineers features → Predicts → Logs → **Sends alert if fraud** → Returns response
- **Used by**: External systems, dashboard, Docker healthchecks
- **Runs on**: Port 8000 (configurable)

#### `email_alerts.py` 🚨 **ALERT SYSTEM** ← THIS IS THE ALERT FILE!

- **What it does**: Sends email alerts when fraud is detected
- **Key features**:
  - Connects to SMTP server (Gmail/Outlook/SendGrid)
  - Sends HTML-formatted email with transaction details
  - Includes fraud score, reconstruction error, and recommended actions
  - Only triggers when `is_fraud=true`
- **Configuration**: Uses environment variables from `.env`:
  ```
  ALERT_ENABLED=true
  SMTP_SERVER=smtp.gmail.com
  SENDER_EMAIL=your@email.com
  RECIPIENT_EMAIL=team@company.com
  ```
- **Called by**: `main.py` after prediction
- **Latency**: 2-3 seconds to send email

#### `model_handler.py` 🧠 **MODEL MANAGER**

- **What it does**: Loads and manages the ML model components
- **Responsibilities**:
  - Loads `autoencoder.keras` (neural network)
  - Loads `autoencoder_scaler.pkl` (feature normalizer)
  - Loads `ae_threshold.npy` (decision threshold = 0.304)
  - Performs predictions (calculates reconstruction error)
  - Engineers 27 features from 9 input fields
- **Called by**: `main.py` during startup and predictions
- **Memory**: Keeps model in RAM for fast inference (~50ms)

#### `schemas.py` 📋 **DATA VALIDATION**

- **What it does**: Defines data structures using Pydantic
- **Schemas**:
  - `TransactionRequest` - Validates incoming API requests (9 fields)
  - `PredictionResponse` - Formats prediction output (is_fraud, error, confidence)
  - `HealthResponse` - Health check format
- **Purpose**: Type safety, automatic validation, API documentation
- **Benefits**: Rejects invalid requests with HTTP 422 error

#### `main_simple.py` 🧪 **SIMPLIFIED API**

- **What it does**: Lightweight version of API without email alerts
- **Use case**: Testing, debugging, minimal deployment
- **Difference**: No SMTP dependencies, faster startup

#### `__init__.py`

- **What it does**: Makes `api/` a Python package
- **Purpose**: Allows imports like `from api.model_handler import ...`

---

## 📊 2. Monitoring Folder (`monitoring/`)

**Purpose**: Real-time dashboard and system observability

### Files:

#### `dashboard.py` 📈 **STREAMLIT DASHBOARD**

- **What it does**: Multi-page interactive dashboard for monitoring
- **5 Pages**:
  1. **Overview** - KPIs, transaction volume, fraud rate
  2. **Deep Analytics** - Distributions, patterns, correlations
  3. **Model Performance** - Confusion matrix, ROC curve, metrics
  4. **Real-Time Monitor** - Live predictions (auto-refresh 5s)
  5. **Business Insights** - Financial impact, trends, top frauds
- **Data source**: Reads `logs/metrics.jsonl` file
- **Runs on**: Port 8501 (Streamlit default)
- **Features**: Interactive Plotly charts, filters, time windows
- **Used by**: Data scientists, business analysts, ops team

#### `metrics_tracker.py` 📝 **METRICS LOGGER**

- **What it does**: Tracks and logs API performance metrics
- **Logged metrics** (15+ fields):
  - Transaction details (type, amount, timestamp)
  - Prediction results (is_fraud, error, confidence)
  - Performance (latency, processing time)
  - System status (alert_sent, model_version)
- **Output**: `logs/metrics.jsonl` (one JSON per line)
- **Called by**: `main.py` after each prediction
- **Purpose**: Historical analysis, debugging, compliance

#### `drift_detection.py` 🔍 **DRIFT DETECTOR**

- **What it does**: Detects when data distribution changes (model degradation)
- **Monitors**:
  - Feature distributions (KS test)
  - Fraud rate changes
  - Prediction confidence drops
  - Reconstruction error patterns
- **Triggers**: Retraining pipeline if drift detected
- **Methods**: Statistical tests, rolling windows
- **Used by**: `pipelines/retrain_pipeline.py`

---

## 🤖 3. Models Folder (`models/`)

**Purpose**: Stores trained ML models and artifacts

### Files:

#### `autoencoder.keras` 🧠 **MAIN MODEL** (220 KB)

- **What it is**: Trained deep learning autoencoder neural network
- **Architecture**: 27 → 64 → 32 → **16** → 32 → 64 → 27 (bottleneck)
- **Training**: Learned to reconstruct normal transactions
- **How it works**:
  - Input: 27 features → Compress → Decompress → Output: 27 reconstructed values
  - Normal transactions: low reconstruction error (< 0.304)
  - Fraudulent transactions: high reconstruction error (> 0.304)
- **Format**: Keras/TensorFlow SavedModel
- **Parameters**: 9,579 trainable weights
- **Created by**: `scripts/3_train.py`
- **Used by**: `api/model_handler.py` for predictions

#### `encoder.keras` 📦 **ENCODER ONLY** (59 KB)

- **What it is**: First half of autoencoder (compression part)
- **Purpose**:
  - Dimensionality reduction (27 → 16 dimensions)
  - Feature extraction for visualization
  - Transfer learning base
- **Use cases**: t-SNE plots, clustering, embeddings
- **Created by**: `scripts/3_train.py` (extracted from autoencoder)
- **Used by**: `scripts/explain_predictions.py`, visualization tools

#### `autoencoder_scaler.pkl` ⚖️ **FEATURE NORMALIZER** (3 KB)

- **What it is**: StandardScaler fitted on training data
- **Purpose**: Normalizes features to mean=0, std=1
- **Why needed**: Neural networks work better with normalized inputs
- **Contains**:
  - Mean values for each of 27 features
  - Standard deviation for each feature
- **Applied**: Before feeding data to model
- **Format**: Scikit-learn pickle file
- **Created by**: `scripts/3_train.py`
- **Used by**: `api/model_handler.py` before every prediction

#### `ae_threshold.npy` 🎯 **DECISION THRESHOLD** (136 bytes)

- **What it is**: Single number = 0.304
- **Purpose**: Decision boundary for fraud classification
- **Logic**:
  ```python
  if reconstruction_error > 0.304:
      is_fraud = True
  else:
      is_fraud = False
  ```
- **How calculated**:
  - Computed on validation set
  - Optimizes F1-score (balance precision/recall)
  - Trade-off: Higher = fewer false positives, more false negatives
- **Format**: NumPy array file
- **Created by**: `scripts/3_train.py`
- **Used by**: `api/model_handler.py` for classification

---

## 📊 4. Data Folder (`data/`)

**Purpose**: All datasets and feature definitions

### Files:

#### `paysim_reduced.csv` 💾 **CLEANED DATASET** (3.8 MB)

- **What it is**: Preprocessed and balanced dataset
- **Size**: 49,977 transactions
- **Columns**: 11 (step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud)
- **Fraud rate**: 16.43% (8,213 frauds)
- **Source**: PaySim mobile money simulator (6.36M original)
- **Processing**: Undersampled normals, kept all frauds
- **Created by**: `scripts/1_data_preparation.py`
- **Used by**: `scripts/2_feature_engineering.py`

#### `paysim_features.csv` 📊 **ENGINEERED FEATURES** (9.3 MB)

- **What it is**: Dataset with 27 engineered features
- **Size**: 49,977 rows × 28 columns (27 features + isFraud label)
- **Features include**:
  - Transaction metadata (type_TRANSFER, type_CASH_OUT, etc.)
  - Amount ratios (amt_to_balance_ratio, amt_to_dest_ratio)
  - Balance changes (balance_change_orig, balance_drain_pct)
  - Interaction features (high_amt_drain, zero_balance_dest)
- **Created by**: `scripts/2_feature_engineering.py`
- **Used by**: `scripts/3_train.py` for model training

#### `paysim_test.csv` 🧪 **TEST SET** (1.8 MB)

- **What it is**: Hold-out test data (20% split)
- **Size**: 9,996 transactions
- **Purpose**: Evaluate final model performance
- **Contains**: Same 27 features as training set
- **Never used in training**: Ensures unbiased evaluation
- **Created by**: `scripts/3_train.py` during train/test split
- **Used by**: Model evaluation, performance metrics

#### `feature_names.txt` 📝 **FEATURE DOCUMENTATION**

- **What it is**: List of all 27 feature names
- **Purpose**: Documentation, API validation, debugging
- **Format**: One feature per line
- **Created by**: `scripts/2_feature_engineering.py`
- **Used by**: `api/model_handler.py`, documentation

---

## 🛠️ 5. Scripts Folder (`scripts/`)

**Purpose**: ML pipeline - data preparation, training, evaluation

### Files (executed in order):

#### `1_data_preparation.py` 🧹 **STEP 1: DATA CLEANING**

- **What it does**: Cleans and balances the raw PaySim dataset
- **Input**: Raw PaySim CSV (6.36M transactions)
- **Processing**:
  - Removes duplicate transactions
  - Filters irrelevant transaction types (DEBIT only)
  - Undersamples normal transactions (keeps all 8,213 frauds)
  - Balances dataset to ~16% fraud rate
- **Output**: `data/paysim_reduced.csv` (49,977 rows)
- **Run once**: Before training new model
- **Execution time**: ~30 seconds

#### `2_feature_engineering.py` ⚙️ **STEP 2: FEATURE CREATION**

- **What it does**: Creates 27 features from 11 raw columns
- **Input**: `data/paysim_reduced.csv`
- **Feature types**:
  - One-hot encoding (transaction types)
  - Numeric transformations (log amounts)
  - Ratio features (amount/balance)
  - Boolean flags (zero balances, drains)
  - Interaction terms (high_amt × drain)
- **Output**: `data/paysim_features.csv` (27 columns)
- **Run once**: After data preparation
- **Execution time**: ~10 seconds

#### `3_train.py` 🏋️ **STEP 3: MODEL TRAINING**

- **What it does**: Trains the autoencoder model
- **Input**: `data/paysim_features.csv`
- **Process**:
  1. Split data (80% train, 20% test)
  2. Train StandardScaler on training data
  3. Build autoencoder architecture (Keras)
  4. Train on **NORMAL transactions only** (unsupervised)
  5. Calculate reconstruction errors
  6. Find optimal threshold (maximize F1-score)
  7. Evaluate on test set
  8. Save model, scaler, encoder, threshold
- **Outputs**:
  - `models/autoencoder.keras`
  - `models/encoder.keras`
  - `models/autoencoder_scaler.pkl`
  - `models/ae_threshold.npy`
- **Training time**: ~5 minutes (CPU), ~1 minute (GPU)
- **Epochs**: 50 (with early stopping)
- **Final metrics**: Accuracy 93.49%, Recall 87.10%, ROC-AUC 98.20%

#### `4_predict.py` 🔮 **BATCH PREDICTIONS**

- **What it does**: Runs predictions on entire test set
- **Input**: `data/paysim_test.csv`
- **Process**:
  - Loads trained model
  - Makes predictions for all test transactions
  - Saves results with scores
- **Output**: CSV with predictions + probabilities
- **Use case**: Batch scoring, model evaluation, debugging
- **Execution time**: ~5 seconds

#### `explain_predictions.py` 🔍 **MODEL EXPLAINABILITY**

- **What it does**: Explains why model flagged specific transactions
- **Methods**:
  - **SHAP values** - Feature importance per prediction
  - **LIME** - Local explanations
  - **Feature contribution** - Which features drove the decision
- **Input**: Transaction ID or batch
- **Output**: Visualization plots, importance scores
- **Use case**: Debugging false positives, compliance, trust
- **Execution time**: ~30 seconds per explanation

#### `nettoyage_paysim.py` 🧽 **ALTERNATIVE CLEANING**

- **What it does**: Alternative data cleaning approach
- **Difference**: Different sampling strategy or filters
- **Use case**: Experimentation, A/B testing different preprocessing
- **Input**: Raw PaySim CSV
- **Output**: Cleaned dataset (different from 1_data_preparation.py)

---

## 🔄 6. Pipelines Folder (`pipelines/`)

**Purpose**: Automated MLOps workflows

### Files:

#### `retrain_pipeline.py` 🔄 **AUTOMATED RETRAINING**

- **What it does**: Automatically retrains model when needed
- **Triggers**:
  - Scheduled (weekly/monthly)
  - Drift detected (data distribution change)
  - Performance degradation
  - Manual trigger
- **Process**:
  1. Backup current model
  2. Load new data (accumulated predictions)
  3. Retrain autoencoder
  4. Evaluate new model
  5. Compare with old model
  6. Deploy if better (or rollback)
  7. Log results
- **Safety**: Always backs up before replacing model
- **Used by**: Cron jobs, Kubernetes CronJob, manual runs

#### `drift_check.py` 📉 **DRIFT MONITORING**

- **What it does**: Monitors for data/model drift
- **Checks**:
  - Feature distribution changes (KS test)
  - Fraud rate trends
  - Prediction confidence decay
  - Reconstruction error inflation
- **Output**: Drift report (JSON/log)
- **Action**: Triggers retraining if drift > threshold
- **Runs**: Hourly/daily (scheduled)
- **Used by**: `retrain_pipeline.py`, alerting system

---

## 📚 7. Docs Folder (`docs/`)

**Purpose**: Project documentation

### Files:

#### `HOW_TO_RUN.md` 🚀 **QUICK START GUIDE**

- Setup instructions
- Docker commands
- Local development setup
- Troubleshooting

#### `README-MLOPS.md` 📖 **MLOPS DOCUMENTATION**

- MLOps best practices used
- CI/CD pipeline explanation
- Monitoring strategy
- Deployment architecture

#### `FILE_EXPLANATIONS.md` 📄 **THIS FILE**

- Complete file/folder explanations
- Architecture overview
- Dependencies map

#### `PROJECT_REORGANIZATION.md` 🔄 **REORGANIZATION LOG**

- Changes made to structure
- Files moved/deleted
- Before/after comparison

---

## ⚙️ 8. Config Folder (`config/`)

**Purpose**: Centralized configuration

### Files:

#### `config.py` ⚙️ **MAIN CONFIGURATION**

- **What it does**: Central configuration for all components
- **Contains**:
  - File paths (MODEL_DIR, DATA_DIR, LOGS_DIR)
  - API settings (host, port, version)
  - Model parameters (threshold, version)
  - Feature names list
- **Imported by**: All other modules
- **Benefits**: Single source of truth, easy updates

---

## 📝 9. Logs Folder (`logs/`)

**Purpose**: Application logs and metrics

### Files:

#### `api.log` 📋 **API LOGS**

- **What it is**: Application log file
- **Contains**:
  - Startup messages
  - Request/response logs
  - Errors and warnings
  - Model loading status
- **Format**: Text, one line per log entry
- **Rotation**: Can be configured to rotate daily/weekly

#### `metrics.jsonl` 📊 **PREDICTION METRICS**

- **What it is**: Structured log of all predictions
- **Format**: JSON Lines (one JSON object per line)
- **Fields per prediction**:
  ```json
  {
    "timestamp": "2026-01-16T14:23:45",
    "transaction_type": "TRANSFER",
    "amount": 352487.5,
    "is_fraud": true,
    "reconstruction_error": 0.512,
    "threshold": 0.304,
    "confidence": 0.85,
    "latency_ms": 137,
    "alert_sent": true,
    "model_version": "v1.0"
  }
  ```
- **Used by**: `monitoring/dashboard.py`, analytics
- **Size**: Grows continuously (can be archived/rotated)

---

## 🐳 10. Root Configuration Files

### `docker-compose.yml` 🐳 **SERVICE ORCHESTRATION**

- **What it does**: Defines and orchestrates 2 Docker services
- **Services**:
  1. **fraud-api** (port 8000) - FastAPI prediction service
  2. **fraud-dashboard** (port 8501) - Streamlit monitoring dashboard
- **Features**:
  - Shared network (fraud-detection-network)
  - Volume mounts (./models, ./data, ./logs)
  - Environment variables from .env
  - Health checks
  - Auto-restart policy

### `Dockerfile` 🐳 **CONTAINER IMAGE**

- **What it does**: Builds Docker image for both services
- **Base**: Python 3.10-slim
- **Installs**: All requirements from requirements-prod.txt
- **Exposes**: Ports 8000 and 8501
- **Entrypoint**: Can run API or dashboard based on command

### `requirements.txt` 📦 **DEVELOPMENT DEPENDENCIES**

- TensorFlow, Keras, scikit-learn
- FastAPI, Uvicorn
- Streamlit, Plotly
- Pandas, NumPy
- Development tools (pytest, black, flake8)

### `requirements-prod.txt` 📦 **PRODUCTION DEPENDENCIES**

- Minimal production dependencies
- No dev tools (lighter image)
- Only runtime essentials

### `.env` / `.env.example` 🔐 **ENVIRONMENT VARIABLES**

- **ALERT_ENABLED** - Enable/disable email alerts
- **SMTP credentials** - Email server config
- **API settings** - Port, host, version
- **.env**: Actual credentials (gitignored)
- **.env.example**: Template for users

### `project_presentation.py` 🎨 **PROJECT PRESENTATION**

- **What it is**: Streamlit app showcasing the entire project
- **10 pages**: Overview, data cleaning, features, model, API, Docker, dashboard, alerts, results, architecture
- **Purpose**: Demo, documentation, interviews, presentations
- **Run**: `streamlit run project_presentation.py`

---

## 🚨 ALERT SYSTEM - DETAILED FLOW

### Where Alerts Happen:

```
1. Transaction arrives → api/main.py POST /predict
2. Model predicts → api/model_handler.py
3. If fraud detected (error > 0.304):
   ↓
4. Call alert system → api/email_alerts.py
   ↓
5. email_alerter.send_fraud_alert()
   - Connects to SMTP server
   - Creates HTML email
   - Sends to RECIPIENT_EMAIL
   - Logs success/failure
   ↓
6. Returns to main.py
7. Logs alert status → logs/metrics.jsonl
8. Returns API response
```

### Alert Configuration (.env):

```bash
ALERT_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=fraud-alerts@mycompany.com
SENDER_PASSWORD=app_password_here
RECIPIENT_EMAIL=fraud-team@mycompany.com
```

### Alert Email Contains:

- 🚨 Subject: "FRAUD ALERT - $352,487.50 Transaction"
- Transaction details (type, amount, accounts, timestamp)
- Model scoring (reconstruction error, threshold, confidence)
- Recommended actions (block account, investigate, contact customer)
- System info (model version, API instance)

### Alert Latency:

- **Detection**: < 10ms (model inference)
- **Email send**: 2-3 seconds (SMTP)
- **Total**: ~ 3 seconds from transaction to email received

---

## 📊 Quick Reference

| Need to...                   | Use this file                      |
| ---------------------------- | ---------------------------------- |
| **Send fraud alerts**        | `api/email_alerts.py` 🚨           |
| **Run API in production**    | `api/main.py`                      |
| **Load/predict with model**  | `api/model_handler.py`             |
| **View real-time dashboard** | `monitoring/dashboard.py`          |
| **Train new model**          | `scripts/3_train.py`               |
| **Clean data**               | `scripts/1_data_preparation.py`    |
| **Create features**          | `scripts/2_feature_engineering.py` |
| **Explain predictions**      | `scripts/explain_predictions.py`   |
| **Detect drift**             | `pipelines/drift_check.py`         |
| **Retrain automatically**    | `pipelines/retrain_pipeline.py`    |
| **Configure everything**     | `config/config.py`                 |
| **Deploy with Docker**       | `docker-compose.yml`               |

---

**Last Updated**: January 16, 2026  
**Total Files**: 40+  
**Alert System**: `api/email_alerts.py` 🚨
