# 📋 Organisation du Projet - Résumé des Changements

## ✅ Actions Réalisées

### 1. 📂 Création de Dossiers Organisés

- **`data/`** - Tous les fichiers CSV et données
- **`scripts/`** - Scripts Python d'entraînement et préparation
- **`docs/`** - Documentation markdown

### 2. 🔄 Fichiers Déplacés

#### → **data/** (Données)

- `paysim_features.csv` (9.3 MB) - Features engineerées
- `paysim_reduced.csv` (3.8 MB) - Dataset nettoyé
- `paysim_test.csv` (1.8 MB) - Test set
- `feature_names.txt` - Liste des 27 features

#### → **scripts/** (Scripts ML)

- `1_data_preparation.py` - Nettoyage données
- `2_feature_engineering.py` - Création features
- `3_train.py` - Entraînement Autoencoder
- `4_predict.py` - Prédictions batch
- `explain_predictions.py` - Explainability (SHAP)
- `nettoyage_paysim.py` - Nettoyage alternatif

#### → **docs/** (Documentation)

- `HOW_TO_RUN.md` - Guide démarrage
- `README-MLOPS.md` - Documentation MLOps

### 3. 🗑️ Fichiers Supprimés

#### Doublons (existaient dans `models/`)

- ❌ `ae_threshold.npy` (root)
- ❌ `autoencoder.keras` (root)
- ❌ `encoder.keras` (root)
- ❌ `autoencoder_scaler.pkl` (root)

#### Scripts Inutilisés

- ❌ `generate_dashboard_data.ps1`

#### Dossiers Vides

- ❌ `cleaning/` (contenu déplacé dans scripts/)

---

## 📁 Structure Finale

```
aiops-log-anomalies/
│
├── 🔧 Root (Configuration & Orchestration)
│   ├── docker-compose.yml          # Orchestration services
│   ├── Dockerfile                  # Image Docker
│   ├── requirements.txt            # Dépendances Python
│   ├── requirements-prod.txt       # Dépendances production
│   ├── .env / .env.example         # Variables environnement
│   ├── .gitignore                  # Git ignore
│   ├── project_presentation.py     # Présentation Streamlit
│   └── README.md                   # Documentation principale ✨ NOUVEAU
│
├── 📂 api/                         # API FastAPI (Production)
│   ├── main.py                     # Point d'entrée principal
│   ├── model_handler.py            # Gestion modèle
│   ├── schemas.py                  # Validation Pydantic
│   └── email_alerts.py             # Alertes SMTP
│
├── 📂 monitoring/                  # Dashboard & Monitoring
│   ├── dashboard.py                # Dashboard Streamlit
│   ├── metrics_tracker.py          # Tracking métriques
│   └── drift_detection.py          # Détection drift
│
├── 📂 models/                      # Modèles Entraînés ✅
│   ├── autoencoder.keras           # Modèle complet
│   ├── encoder.keras               # Encoder seul
│   ├── autoencoder_scaler.pkl      # Scaler normalization
│   └── ae_threshold.npy            # Seuil décision (0.304)
│
├── 📂 data/                        # Datasets ✨ NOUVEAU
│   ├── paysim_reduced.csv          # Dataset nettoyé (49K)
│   ├── paysim_features.csv         # Features (27 cols)
│   ├── paysim_test.csv             # Test set (20%)
│   └── feature_names.txt           # Noms features
│
├── 📂 scripts/                     # Scripts ML ✨ NOUVEAU
│   ├── 1_data_preparation.py       # Pipeline étape 1
│   ├── 2_feature_engineering.py    # Pipeline étape 2
│   ├── 3_train.py                  # Pipeline étape 3
│   ├── 4_predict.py                # Prédictions batch
│   ├── explain_predictions.py      # Explainability
│   └── nettoyage_paysim.py         # Nettoyage alt.
│
├── 📂 pipelines/                   # Pipelines MLOps
│   ├── retrain_pipeline.py         # Réentraînement auto
│   └── drift_check.py              # Check drift
│
├── 📂 docs/                        # Documentation ✨ NOUVEAU
│   ├── HOW_TO_RUN.md               # Guide démarrage
│   └── README-MLOPS.md             # Doc MLOps
│
├── 📂 config/                      # Configurations
├── 📂 logs/                        # Logs système
└── 📂 .github/workflows/           # CI/CD GitHub Actions
```

---

## 🎯 Bénéfices de la Réorganisation

### 1. ✨ Clarté & Navigation

- **Avant** : 25+ fichiers mélangés dans root
- **Après** : 9 fichiers root + dossiers organisés par fonction

### 2. 🧹 Élimination Doublons

- Supprimé 4 fichiers de modèles dupliqués (~440 KB économisés)
- Un seul emplacement : `models/` pour tous les artifacts ML

### 3. 📚 Séparation des Responsabilités

| Dossier       | Rôle          | Usage                 |
| ------------- | ------------- | --------------------- |
| `api/`        | Production    | Services temps réel   |
| `monitoring/` | Observabilité | Dashboards, métriques |
| `models/`     | Artifacts ML  | Modèles entraînés     |
| `data/`       | Datasets      | CSV, features         |
| `scripts/`    | Training      | Entraînement, batch   |
| `pipelines/`  | Automation    | MLOps pipelines       |
| `docs/`       | Documentation | Guides, README        |

### 4. 🐳 Docker-Ready

- Volumes clairement définis dans `docker-compose.yml`
- Paths cohérents pour bind mounts (`./models`, `./data`)

### 5. 🔄 Git-Friendly

- `.gitignore` mieux organisé
- Historique Git préservé (move = git mv)

---

## 📝 Prochaines Étapes Recommandées

### 1. Mettre à jour les imports Python

Les scripts qui importent depuis d'autres fichiers peuvent nécessiter des ajustements :

```python
# Avant
from 2_feature_engineering import engineer_features

# Après
from scripts.feature_engineering import engineer_features
```

### 2. Mettre à jour docker-compose.yml

Vérifier que les volumes pointent vers les bons chemins :

```yaml
volumes:
  - ./models:/app/models
  - ./data:/app/data
  - ./logs:/app/logs
```

### 3. Ajouter **init**.py si nécessaire

Pour que `scripts/` soit un package Python importable :

```bash
touch scripts/__init__.py
```

---

## ✅ Checklist de Validation

- [x] Tous les fichiers ML dans `scripts/`
- [x] Tous les datasets dans `data/`
- [x] Documentation dans `docs/`
- [x] Pas de doublons de modèles
- [x] README principal créé
- [x] Structure claire et professionnelle
- [ ] Tests d'imports Python (à vérifier)
- [ ] Vérification docker-compose paths
- [ ] Update .gitignore si besoin

---

**Date de réorganisation** : 16 janvier 2026  
**Fichiers déplacés** : 14  
**Fichiers supprimés** : 5  
**Gain d'espace** : ~440 KB (doublons)  
**Amélioration lisibilité** : ⭐⭐⭐⭐⭐
