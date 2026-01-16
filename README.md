# 🚨 Fraud Detection MLOps System

Système de détection de fraude en temps réel utilisant un Autoencoder et une infrastructure MLOps complète.

## 📁 Structure du Projet

```
aiops-log-anomalies/
│
├── 📂 api/                          # API FastAPI de prédiction
│   ├── main.py                      # Point d'entrée API principal
│   ├── main_simple.py               # Version simplifiée de l'API
│   ├── model_handler.py             # Gestion du modèle (load, predict)
│   ├── schemas.py                   # Schémas Pydantic (validation)
│   └── email_alerts.py              # Système d'alertes SMTP
│
├── 📂 monitoring/                   # Dashboard et monitoring
│   ├── dashboard.py                 # Dashboard Streamlit multi-pages
│   ├── metrics_tracker.py           # Suivi des métriques API
│   └── drift_check.py               # Détection de drift (data/model)
│
├── 📂 models/                       # Modèles ML entraînés
│   ├── autoencoder.keras            # Modèle Autoencoder complet
│   ├── encoder.keras                # Partie encoder uniquement
│   ├── autoencoder_scaler.pkl       # StandardScaler pour normalisation
│   └── ae_threshold.npy             # Seuil de décision (0.304)
│
├── 📂 data/                         # Datasets
│   ├── paysim_reduced.csv           # Dataset nettoyé (49,977 trans.)
│   ├── paysim_features.csv          # Features engineerées (27 cols)
│   ├── paysim_test.csv              # Test set (20%)
│   └── feature_names.txt            # Noms des 27 features
│
├── 📂 scripts/                      # Scripts d'entraînement
│   ├── 1_data_preparation.py        # Nettoyage dataset PaySim
│   ├── 2_feature_engineering.py     # Création 27 features
│   ├── 3_train.py                   # Entraînement Autoencoder
│   ├── 4_predict.py                 # Prédictions batch
│   ├── nettoyage_paysim.py          # Nettoyage alternatif
│   └── explain_predictions.py       # Explainability (SHAP, LIME)
│
├── 📂 pipelines/                    # Pipelines MLOps
│   ├── retrain_pipeline.py          # Pipeline de réentraînement
│   └── drift_check.py               # Détection drift automatique
│
├── 📂 docs/                         # Documentation
│   ├── HOW_TO_RUN.md                # Guide de démarrage
│   └── README-MLOPS.md              # Documentation MLOps détaillée
│
├── 📂 config/                       # Configurations
├── 📂 logs/                         # Logs système
│
├── 🐳 docker-compose.yml            # Orchestration services
├── 🐳 Dockerfile                    # Image Docker API/Dashboard
├── 📋 requirements.txt              # Dépendances Python (dev)
├── 📋 requirements-prod.txt         # Dépendances production
├── 🎨 project_presentation.py       # Présentation Streamlit du projet
├── 🔒 .env.example                  # Template variables d'environnement
└── 📄 .gitignore                    # Fichiers à ignorer Git
```

## 🚀 Démarrage Rapide

### Option 1 : Docker (Recommandé)

```bash
# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos credentials SMTP

# Lancer les services
docker-compose up -d

# Accès
# API: http://localhost:8000
# Dashboard: http://localhost:8501
```

### Option 2 : Local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
cd api
uvicorn main:app --port 8000

# Lancer le dashboard (nouveau terminal)
cd monitoring
streamlit run dashboard.py --server.port 8501
```

## 📊 Pipeline de Données

1. **Nettoyage** → `scripts/1_data_preparation.py`

   - Source : PaySim (6.36M transactions)
   - Output : `data/paysim_reduced.csv` (49,977 trans.)

2. **Feature Engineering** → `scripts/2_feature_engineering.py`

   - Input : paysim_reduced.csv
   - Output : `data/paysim_features.csv` (27 features)

3. **Entraînement** → `scripts/3_train.py`

   - Modèle : Autoencoder (27→64→32→16→32→64→27)
   - Output : `models/autoencoder.keras`, threshold

4. **Prédiction** → `api/main.py` (temps réel)
   - Input : 9 champs transaction
   - Output : is_fraud, error, confidence

## 🎯 Endpoints API

- **POST /predict** - Détection fraude temps réel
- **GET /health** - Healthcheck
- **GET /metrics** - Métriques système

## 📈 Métriques Modèle

| Métrique        | Valeur |
| --------------- | ------ |
| Accuracy        | 93.49% |
| Rappel (Fraude) | 87.10% |
| Précision       | 76.52% |
| F1-Score        | 81.47% |
| ROC-AUC         | 98.20% |

## 🔍 Présentation du Projet

Pour une présentation interactive complète :

```bash
streamlit run project_presentation.py
```

**10 pages incluant :**

- Vue d'ensemble du projet
- Nettoyage des données
- Feature engineering
- Architecture Autoencoder
- API de prédiction
- Docker & MLOps
- Tableau de bord monitoring
- Alertes email
- Résultats & KPIs
- Architecture technique

## 📧 Alertes Email

Configuration SMTP dans `.env` :

```env
ALERT_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=alerts@company.com
```

## 🛠️ Technologies

- **ML/Data**: TensorFlow/Keras, scikit-learn, Pandas, NumPy
- **API**: FastAPI, Uvicorn, Pydantic
- **Dashboard**: Streamlit, Plotly, Altair
- **DevOps**: Docker, Docker Compose
- **Alerting**: SMTP (Gmail/Outlook)

## 📝 License

Projet éducatif - MLOps Fraud Detection System
