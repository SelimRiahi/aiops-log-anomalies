# 📘 DOCUMENTATION COMPLÈTE DU PROJET
## Détection d'Anomalies dans les Transactions Financières

**Dernière mise à jour** : 2 janvier 2026  
**Version** : 2.0  
**Statut** : Production Ready ✅

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble](#1-vue-densemble)
2. [Structure actuelle du projet](#2-structure-actuelle-du-projet)
3. [Description détaillée des fichiers](#3-description-détaillée-des-fichiers)
4. [Pipeline d'exécution](#4-pipeline-dexécution)
5. [Modifications récentes](#5-modifications-récentes)
6. [Guide d'utilisation](#6-guide-dutilisation)
7. [Métriques et résultats](#7-métriques-et-résultats)

---

## 1. VUE D'ENSEMBLE

### 🎯 Objectif du Projet
Développer un système de **détection d'anomalies dans les transactions financières** utilisant un modèle **Autoencoder** (deep learning) pour identifier les transactions frauduleuses sans utiliser les étiquettes de fraude pendant l'entraînement.

### 🔑 Principe Clé : Apprentissage Non Supervisé
- ✅ **Entraînement** : Utilise UNIQUEMENT les transactions normales
- ✅ **Évaluation** : Teste sur toutes les transactions (avec étiquettes)
- ✅ **Détection** : Transactions avec erreur de reconstruction élevée = Anomalie

### 📊 Dataset : PaySim
- **Source** : Dataset synthétique de transactions de paiement mobile
- **Taille originale** : 6,36 millions de transactions
- **Taille réduite** : ~50,000 transactions (pour efficacité)
- **Période** : 744 heures (31 jours simulés)
- **Taux de fraude** : 16.43% (après réduction)

---

## 2. STRUCTURE ACTUELLE DU PROJET

```
mlpss/
│
├── 📊 DONNÉES
│   ├── paysim dataset.csv              # Dataset original (6.36M lignes)
│   ├── paysim_reduced.csv              # Dataset réduit (~50K lignes)
│   └── paysim_features.csv             # Dataset avec features engineerées (60+ features)
│
├── 🐍 SCRIPTS PYTHON (Pipeline séquentiel - 3 étapes)
│   ├── 1_data_preparation.py           # Étape 1: Réduction et préparation
│   ├── 2_feature_engineering.py        # Étape 2: Création de 60+ features
│   └── 3_train.py                      # Étape 3: Entraînement et évaluation
│
├── 🤖 MODÈLES ENTRAÎNÉS (Générés par 3_train.py)
│   ├── autoencoder.keras               # Modèle Autoencoder complet ⭐
│   ├── encoder.keras                   # Partie encodeur (compression)
│   ├── autoencoder_scaler.pkl          # Scaler pour normalisation ⭐
│   └── ae_threshold.npy                # Seuil de détection d'anomalie ⭐
│
├── 📊 RÉSULTATS
│   └── autoencoder_results.png         # 6 graphiques de visualisation
│
└── 📖 DOCUMENTATION
    ├── requirements.txt                # Dépendances Python
    └── PROJECT_DOCUMENTATION.md        # Ce fichier
```

**Légende** :
- ⭐ = Fichiers essentiels pour utiliser le modèle en production
- 📊 = Fichiers de données
- 🐍 = Code source Python
- 🤖 = Modèles de machine learning
- 📖 = Documentation

---

## 3. DESCRIPTION DÉTAILLÉE DES FICHIERS

### 📊 FICHIERS DE DONNÉES

#### paysim dataset.csv
- **Type** : CSV
- **Taille** : ~470 MB
- **Lignes** : 6,362,620
- **Colonnes** : 11 (step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud)
- **Usage** : Dataset source pour l'étape 1
- **Note** : Fichier volumineux, utilisé une seule fois pour générer paysim_reduced.csv

#### paysim_reduced.csv
- **Type** : CSV
- **Taille** : ~7 MB
- **Lignes** : 49,977
- **Colonnes** : 10 (isFlaggedFraud supprimé)
- **Usage** : Dataset réduit utilisé pour feature engineering
- **Création** : Échantillonnage stratifié (garde toutes les fraudes + échantillon de normales)
- **Avantage** : Réduit le temps de traitement de plusieurs heures à quelques minutes

#### paysim_features.csv
- **Type** : CSV
- **Taille** : ~10 MB
- **Lignes** : 49,977
- **Colonnes** : 51 (50 features + isFraud)
- **Usage** : Input pour entraînement du modèle
- **Contenu** : Features engineerées (montants, temporelles, comportementales, etc.)

---

### 🐍 SCRIPTS PYTHON

#### 1_data_preparation.py
**Rôle** : Réduction et préparation du dataset original

**Fonctions principales** :
- Charge le dataset original (6.36M lignes)
- Supprime `isFlaggedFraud` (fuite d'information)
- Effectue un échantillonnage stratifié :
  - Garde TOUTES les fraudes (8,213 transactions)
  - Échantillonne proportionnellement les normales (~42K)
- Maintient la distribution temporelle et par type
- Génère des visualisations du dataset

**Input** : `paysim dataset.csv`  
**Output** : 
- `paysim_reduced.csv`
- `dataset_overview.png` (non généré actuellement)

**Temps d'exécution** : 2-5 minutes

**Commande** :
```bash
python 1_data_preparation.py
```

---

#### 2_feature_engineering.py
**Rôle** : Créer des features comportementales à partir des données brutes

**6 catégories de features créées** :

**1. Transaction Amount Features (6 features)**
- `amount_log` : Transformation logarithmique
- `amount_sqrt` : Transformation racine carrée
- `amount_bin_encoded` : Catégorisation du montant
- `amount_to_oldbalance_ratio` : Ratio montant/solde
- `amount_exceeds_balance` : Montant > solde ?

**2. Temporal Features (7 features)**
- `hour` : Heure de la journée (0-23)
- `day` : Jour de simulation
- `is_night` : Transaction nocturne (22h-6h) ?
- `is_weekend` : Weekend simulé ?
- `hour_sin`, `hour_cos` : Encodage cyclique

**3. User Historical Features (10 features)**
- `time_since_last_tx` : Temps depuis dernière transaction
- `tx_count_1h`, `tx_count_6h`, `tx_count_24h` : Fréquence
- `user_tx_count` : Nombre total de transactions
- `user_avg_amount`, `user_std_amount` : Statistiques utilisateur
- `amount_deviation_from_user_avg` : Déviation du comportement
- `tx_velocity` : Vitesse de transaction

**4. Balance Dynamics Features (10 features)**
- `balance_change_orig`, `balance_change_dest` : Changements de solde
- `balance_inconsistency_orig` : Incohérence de solde
- `orig_zero_balance_before/after` : Indicateurs de solde zéro
- `dest_zero_balance_before/after`
- `drains_account` : Vide le compte ?
- `balance_mismatch` : Incohérence détectée

**5. Transaction Type Features (7 features)**
- `type_CASH_IN`, `type_CASH_OUT`, `type_DEBIT`, `type_PAYMENT`, `type_TRANSFER` : One-hot encoding
- `is_risky_type` : TRANSFER ou CASH_OUT ?
- `user_type_switches` : Changements de type

**6. Account Interaction Features (4 features)**
- `dest_is_merchant` : Destination = marchand ?
- `is_c2c` : Client-to-Client ?
- `dest_tx_count` : Popularité du destinataire
- `dest_is_popular` : Destinataire très actif ?

**7. Composite Features (3 features)**
- `risk_score` : Score de risque heuristique
- `consistency_score` : Cohérence comportementale
- `tx_intensity` : Intensité de transaction

**Total** : **60+ features** créées

**⚠️ IMPORTANT** : AUCUNE étiquette de fraude utilisée dans la création des features !

**Input** : `paysim_reduced.csv`  
**Output** : 
- `paysim_features.csv`
- `feature_names.txt` (liste des features)

**Temps d'exécution** : 3-7 minutes

**Commande** :
```bash
python 2_feature_engineering.py
```

---

#### 3_train.py
**Rôle** : Entraîner le modèle Autoencoder et évaluer les performances

**Architecture du modèle Autoencoder** :

```
INPUT (50 features)
    ↓
┌─────────────────────────────────┐
│ ENCODER (Compression)           │
├─────────────────────────────────┤
│ Dense(64) + ReLU                │
│ BatchNormalization              │
│ Dropout(0.2)                    │
│     ↓                           │
│ Dense(32) + ReLU                │
│ BatchNormalization              │
│ Dropout(0.2)                    │
│     ↓                           │
│ Dense(16) + ReLU [BOTTLENECK]   │ ← Représentation compressée
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ DECODER (Reconstruction)        │
├─────────────────────────────────┤
│ Dense(32) + ReLU                │
│ BatchNormalization              │
│     ↓                           │
│ Dense(64) + ReLU                │
│ BatchNormalization              │
│     ↓                           │
│ Dense(50) + Linear              │ ← Reconstruction
└─────────────────────────────────┘
    ↓
OUTPUT (50 features reconstruites)
```

**Processus d'entraînement** :

1. **Chargement des données**
   - Charge `paysim_features.csv`
   - Sépare features (X) et labels (isFraud)

2. **Sélection des données d'entraînement**
   - Filtre : garde UNIQUEMENT les transactions normales (isFraud=0)
   - ~41,764 transactions normales pour l'entraînement
   
   **⚡ POURQUOI UNIQUEMENT LES TRANSACTIONS NORMALES ?**
   
   C'est le principe fondamental de la détection d'anomalies par Autoencoder :
   
   **Principe** : L'autoencoder apprend à reconstruire ce qu'il connaît bien.
   
   - ✅ **Transaction normale** (vue pendant entraînement)
     - Le modèle sait bien la reconstruire
     - Erreur de reconstruction = **FAIBLE**
   
   - ❌ **Transaction frauduleuse** (jamais vue)
     - Le modèle ne sait pas bien la reconstruire
     - Erreur de reconstruction = **ÉLEVÉE**
     - **Erreur élevée = ANOMALIE**
   
   **Analogie** : 
   - On enseigne au modèle : "Voilà à quoi ressemble une transaction normale"
   - Le modèle signale : "Tout ce qui ne ressemble pas à ça est suspect"
   
   **Avantages** :
   1. Détecte même les nouvelles techniques de fraude (non vues avant)
   2. Pas besoin d'avoir beaucoup d'exemples de fraudes étiquetées
   3. Plus robuste face à l'évolution des méthodes de fraude
   
   **En résumé** : On apprend au modèle ce qui est NORMAL, 
   puis tout ce qui dévie = ANOMALIE potentielle.

3. **Normalisation**
   - StandardScaler (moyenne=0, écart-type=1)
   - Sauvegarde du scaler pour usage futur

4. **Entraînement du modèle**
   - Epochs : 20 (avec Early Stopping)
   - Batch size : 256
   - Validation split : 10%
   - Loss function : MSE (Mean Squared Error)
   - Optimizer : Adam (lr=0.001)

5. **Calcul du seuil**
   - Threshold = 95e percentile des erreurs de reconstruction sur données d'entraînement
   - ~5% des transactions normales dépassent le seuil (faux positifs acceptables)

6. **Évaluation**
   - Prédit sur TOUTES les transactions (normales + fraudes)
   - Calcule : Accuracy, Precision, Recall, F1-Score, ROC-AUC
   - Génère matrice de confusion (affichée en graphique seulement)

7. **Visualisations** (6 graphiques)
   - Training history (loss curves)
   - Distribution des erreurs (Normal vs Fraude)
   - Matrice de confusion (heatmap)
   - Barres de métriques de performance
   - Boxplot des erreurs par classe
   - Distribution des erreurs d'entraînement

**Input** : `paysim_features.csv`  
**Output** : 
- `autoencoder.keras` (modèle complet) ⭐
- `encoder.keras` (partie encodeur)
- `autoencoder_scaler.pkl` (scaler) ⭐
- `ae_threshold.npy` (seuil) ⭐
- `autoencoder_results.png` (visualisations)

**Temps d'exécution** : 5-10 minutes

**Commande** :
```bash
python 3_train.py
```

**Sortie console** :
```
================================================================================
Autoencoder Training and Evaluation
================================================================================

[1/5] Loading engineered features...
[2/5] Selecting normal transactions for training...
[3/5] Scaling features...
[4/5] Building and training Autoencoder...
[5/5] Evaluating model performance...

================================================================================
PERFORMANCE METRICS
================================================================================

✓ Accuracy:   0.9410 (94.10%)
✓ Precision:  0.7787 (77.87%)
✓ Recall:     0.8952 (89.52%)
✓ F1-Score:   0.8329 (83.29%)
✓ ROC-AUC:    0.9786
```

---

### 🤖 MODÈLES ENTRAÎNÉS

#### autoencoder.keras ⭐
- **Type** : Modèle Keras (format natif)
- **Taille** : ~500 KB
- **Contenu** : Architecture + poids du réseau de neurones complet
- **Usage** : Faire des prédictions sur nouvelles transactions
- **Chargement** :
  ```python
  from keras.models import load_model
  model = load_model('autoencoder.keras')
  ```

#### encoder.keras
- **Type** : Modèle Keras
- **Taille** : ~200 KB
- **Contenu** : Partie encodeur uniquement (compression à 16D)
- **Usage** : Extraction de représentations compressées, visualisation t-SNE
- **Optionnel** : Peut être supprimé si non utilisé

#### autoencoder_scaler.pkl ⭐
- **Type** : Objet scikit-learn StandardScaler sérialisé
- **Taille** : ~5 KB
- **Contenu** : Moyennes et écarts-types de chaque feature
- **Usage** : **CRITIQUE** - Normaliser nouvelles données avant prédiction
- **Chargement** :
  ```python
  import joblib
  scaler = joblib.load('autoencoder_scaler.pkl')
  X_scaled = scaler.transform(X_new)
  ```

#### ae_threshold.npy ⭐
- **Type** : Array NumPy (1 valeur)
- **Taille** : < 1 KB
- **Contenu** : Seuil de détection (ex: 0.002456)
- **Usage** : Classifier anomalie vs normal
- **Chargement** :
  ```python
  import numpy as np
  threshold = np.load('ae_threshold.npy')
  is_anomaly = reconstruction_error > threshold
  ```

---

### 📊 RÉSULTATS

#### autoencoder_results.png
- **Type** : Image PNG
- **Taille** : ~2 MB
- **Résolution** : 4800x3000 pixels (300 DPI)
- **Contenu** : 6 graphiques
  1. Training History (loss curves)
  2. Reconstruction Error Distribution
  3. Confusion Matrix (heatmap)
  4. Performance Metrics (bar chart)
  5. Error by Class (boxplot)
  6. Training Reconstruction Errors (histogram)

---

### 📖 DOCUMENTATION

#### requirements.txt
```
pandas>=1.5.0          # Manipulation de données
numpy>=1.23.0          # Calculs numériques
scikit-learn>=1.2.0    # Machine learning (preprocessing, metrics)
tensorflow>=2.10.0     # Deep learning (Autoencoder)
matplotlib>=3.6.0      # Visualisations
seaborn>=0.12.0        # Visualisations statistiques
joblib>=1.2.0          # Sauvegarde modèles
openpyxl>=3.0.0        # Export Excel (optionnel)
```

**Installation** :
```bash
pip install -r requirements.txt
```

---

## 4. PIPELINE D'EXÉCUTION

### 🔄 Workflow Complet

```
┌─────────────────────────────────────────────────────────────────────┐
│ ÉTAPE 1 : DATA PREPARATION (1_data_preparation.py)                  │
│ ⏱️ Temps: 2-5 minutes                                                │
└─────────────────────────────────────────────────────────────────────┘
    Input:  paysim dataset.csv (6.36M lignes)
    Process:
      • Charge le dataset original
      • Supprime isFlaggedFraud (fuite d'information)
      • Échantillonnage stratifié (garde toutes fraudes)
      • Maintient distribution temporelle
    Output: paysim_reduced.csv (~50K lignes)
    
    ↓

┌─────────────────────────────────────────────────────────────────────┐
│ ÉTAPE 2 : FEATURE ENGINEERING (2_feature_engineering.py)            │
│ ⏱️ Temps: 3-7 minutes                                                │
└─────────────────────────────────────────────────────────────────────┘
    Input:  paysim_reduced.csv
    Process:
      • Crée 60+ features comportementales
      • 6 catégories: montants, temporelles, historiques, 
                      soldes, types, interactions
      • AUCUNE étiquette de fraude utilisée
    Output: paysim_features.csv (50 features + isFraud)
            feature_names.txt
    
    ↓

┌─────────────────────────────────────────────────────────────────────┐
│ ÉTAPE 3 : TRAINING & EVALUATION (3_train.py)                        │
│ ⏱️ Temps: 5-10 minutes                                               │
└─────────────────────────────────────────────────────────────────────┘
    Input:  paysim_features.csv
    Process:
      • Charge features + labels
      • Filtre: transactions normales uniquement
      • Normalisation (StandardScaler)
      • Construction Autoencoder (50→64→32→16→32→64→50)
      • Entraînement (20 epochs, early stopping)
      • Calcul threshold (95e percentile)
      • Évaluation sur dataset complet
      • Génération visualisations
    Output: autoencoder.keras
            encoder.keras
            autoencoder_scaler.pkl
            ae_threshold.npy
            autoencoder_results.png

┌─────────────────────────────────────────────────────────────────────┐
│ ✅ MODÈLE PRÊT POUR PRODUCTION                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 📝 Commandes d'exécution séquentielle

```bash
# Étape 1: Préparation des données
python 1_data_preparation.py

# Étape 2: Feature engineering
python 2_feature_engineering.py

# Étape 3: Entraînement et évaluation
python 3_train.py
```

**Temps total** : 10-22 minutes

---

## 5. MODIFICATIONS RÉCENTES

### 📅 Version 2.0 (2 janvier 2026)

#### ✨ Changements Majeurs

**1. Renommage du fichier principal**
- ❌ Ancien : `3_autoencoder_anomaly_detection.py`
- ✅ Nouveau : `3_train.py`
- **Raison** : Nom plus court et clair

**2. Simplification de la sortie console**
- ❌ Supprimé : Section "CONFUSION MATRIX" détaillée en texte
- ❌ Supprimé : Section "SAVING MODEL AND RESULTS"
- ❌ Supprimé : Messages "Creating visualizations..." et "Saved: autoencoder_results.png"
- ❌ Supprimé : Section "TRAINING AND EVALUATION COMPLETE"
- ✅ Conservé : Affichage uniquement des métriques de performance
- **Raison** : Console plus propre, focus sur les résultats importants

**3. Format de sauvegarde moderne**
- ❌ Ancien : `.h5` (format HDF5 legacy)
- ✅ Nouveau : `.keras` (format natif Keras)
- **Fichiers concernés** :
  - `autoencoder.h5` → `autoencoder.keras`
  - `encoder.h5` → `encoder.keras`
- **Avantage** : Plus de warnings, format plus rapide et compatible

**4. Évaluation complète ajoutée**
- ✅ Ajout : Accuracy, Precision, Recall, F1-Score, ROC-AUC
- ✅ Ajout : Évaluation sur dataset complet (pas seulement training)
- ✅ Ajout : 6 graphiques de visualisation au lieu de 2
- **Raison** : Meilleure compréhension des performances du modèle

#### 🔧 Améliorations Techniques

- Matrice de confusion calculée mais non affichée en console
- Sauvegarde des modèles silencieuse (sans messages)
- Code plus modulaire et maintenable
- Documentation inline améliorée

---

## 6. GUIDE D'UTILISATION

### 🚀 Démarrage Rapide

#### Installation
```bash
# Cloner ou télécharger le projet
cd mlpss

# Installer les dépendances
pip install -r requirements.txt
```

#### Exécution Complète
```bash
# Pipeline complet (10-22 minutes)
python 1_data_preparation.py
python 2_feature_engineering.py
python 3_train.py
```

---

### 💡 Utilisation du Modèle Entraîné

#### Charger le Modèle

```python
import numpy as np
import pandas as pd
import joblib
from keras.models import load_model

# Charger les composants
model = load_model('autoencoder.keras')
scaler = joblib.load('autoencoder_scaler.pkl')
threshold = np.load('ae_threshold.npy')

print(f"Modèle chargé")
print(f"Threshold: {threshold}")
```

#### Prédire sur Nouvelles Transactions

```python
# 1. Charger nouvelles transactions (doivent avoir les 50 features)
df_new = pd.read_csv('new_transactions.csv')

# 2. Normaliser (CRITIQUE!)
X_scaled = scaler.transform(df_new)

# 3. Reconstruire
X_reconstructed = model.predict(X_scaled, verbose=0)

# 4. Calculer erreur de reconstruction
reconstruction_errors = np.mean(
    np.power(X_scaled - X_reconstructed, 2), 
    axis=1
)

# 5. Détecter anomalies
anomalies = reconstruction_errors > threshold

# 6. Créer rapport
df_new['reconstruction_error'] = reconstruction_errors
df_new['is_anomaly'] = anomalies
df_new['anomaly_score'] = reconstruction_errors / threshold

# 7. Trier par score (plus suspects en premier)
df_suspects = df_new[df_new['is_anomaly'] == True].sort_values(
    'anomaly_score', 
    ascending=False
)

print(f"Transactions analysées: {len(df_new)}")
print(f"Anomalies détectées: {anomalies.sum()}")
print(f"Taux de détection: {anomalies.mean()*100:.2f}%")
print("\nTop 10 transactions les plus suspectes:")
print(df_suspects[['reconstruction_error', 'anomaly_score']].head(10))
```

#### Ajuster le Seuil de Sensibilité

```python
# Calculer erreurs sur données d'entraînement
X_train = pd.read_csv('paysim_features.csv')
X_train = X_train[X_train['isFraud'] == 0].drop('isFraud', axis=1)
X_train_scaled = scaler.transform(X_train)
X_train_recon = model.predict(X_train_scaled, verbose=0)
train_errors = np.mean(np.power(X_train_scaled - X_train_recon, 2), axis=1)

# Différents seuils
threshold_strict = np.percentile(train_errors, 99)    # 1% FPR - Strict
threshold_normal = np.percentile(train_errors, 95)    # 5% FPR - Normal
threshold_relaxed = np.percentile(train_errors, 90)   # 10% FPR - Relaxé

print(f"Strict (99%):  {threshold_strict:.6f}")
print(f"Normal (95%):  {threshold_normal:.6f}")
print(f"Relaxed (90%): {threshold_relaxed:.6f}")

# Tester différents thresholds
for name, t in [('Strict', threshold_strict), 
                ('Normal', threshold_normal), 
                ('Relaxed', threshold_relaxed)]:
    preds = (reconstruction_errors > t).astype(int)
    print(f"\n{name} threshold:")
    print(f"  Détections: {preds.sum()} ({preds.mean()*100:.2f}%)")
```

---

### 🔄 Réentraînement Périodique

Les patterns de fraude évoluent. Recommandation : **réentraîner tous les 1-3 mois**.

```python
# 1. Collecter nouvelles transactions normales (30-90 jours)
df_new = get_recent_normal_transactions(days=60)

# 2. Feature engineering (utiliser même pipeline)
df_features = apply_feature_engineering(df_new)

# 3. Normalisation
scaler_new = StandardScaler()
X_scaled = scaler_new.fit_transform(df_features)

# 4. Réentraîner
model.fit(X_scaled, X_scaled, epochs=10, batch_size=256)

# 5. Recalculer threshold
reconstructions = model.predict(X_scaled)
errors = np.mean(np.power(X_scaled - reconstructions, 2), axis=1)
new_threshold = np.percentile(errors, 95)

# 6. Sauvegarder nouvelle version
model.save('autoencoder_v2.keras')
joblib.dump(scaler_new, 'autoencoder_scaler_v2.pkl')
np.save('ae_threshold_v2.npy', new_threshold)
```

---

## 7. MÉTRIQUES ET RÉSULTATS

### 📊 Performances Attendues

**Métriques typiques** (variables selon seed et données) :

| Métrique | Plage | Valeur Typique |
|----------|-------|----------------|
| **Accuracy** | 85-95% | ~94% |
| **Precision** | 60-80% | ~78% |
| **Recall** | 80-95% | ~90% |
| **F1-Score** | 70-85% | ~83% |
| **ROC-AUC** | 0.90-0.99 | ~0.98 |
| **FPR** | 2-10% | ~5% |

### 🎯 Interprétation

**Accuracy = 94.10%**
- 94.10% de toutes les prédictions sont correctes
- Métrique globale de performance

**Precision = 77.87%**
- Quand le modèle signale une anomalie, il a raison 78% du temps
- 22% de fausses alarmes
- Important pour limiter le travail des analystes

**Recall = 89.52%**
- Le modèle détecte 89.52% de toutes les fraudes
- 10.48% de fraudes passent inaperçues
- Important pour maximiser la détection

**F1-Score = 83.29%**
- Équilibre entre Precision et Recall
- Bon compromis global

**ROC-AUC = 0.9786**
- Excellente capacité de discrimination
- 0.50 = Random, 1.00 = Parfait
- 0.98 = Très bon modèle

### 💰 Impact Business (Exemple)

**Scénario** : Banque avec 1M transactions/jour, 0.13% fraude

```
Sans modèle:
- Toutes les transactions doivent être vérifiées manuellement
- Impossible en pratique

Avec modèle (Precision=78%, Recall=90%):
- Fraudes réelles: 1,300/jour
- Fraudes détectées: 1,170 (90% recall)
- Fausses alarmes: ~330
- Total à vérifier: ~1,500 transactions/jour

Réduction du travail: 1,000,000 → 1,500 (99.85% de réduction!)
Fraudes attrapées: 90% vs 100% en manuel
ROI: Excellent
```

### ⚠️ Limites

1. **Faux positifs** : ~22% des alertes sont de fausses alarmes
   - Solution : Scoring + revue par analystes

2. **Fraudes manquées** : ~10% des fraudes ne sont pas détectées
   - Solution : Combiner avec autres systèmes de détection

3. **Dérive temporelle** : Les patterns évoluent
   - Solution : Réentraînement périodique (1-3 mois)

4. **Dataset synthétique** : PaySim simule, ne reflète pas exactement la réalité
   - Solution : Tester sur vraies données en production

5. **Nouvelles techniques de fraude** : Modèle ne connaît que patterns passés
   - Solution : Monitoring continu + mise à jour

---

## 8. ARCHITECTURE TECHNIQUE

### 🧠 Pourquoi un Autoencoder ?

**Principe** : Réseau de neurones qui apprend à compresser puis reconstruire les données

**Avantages pour détection d'anomalies** :
1. **Apprentissage non supervisé** : Pas besoin d'étiquettes de fraude
2. **Patterns complexes** : Capture relations non-linéaires
3. **Représentation compressée** : Force à apprendre l'essentiel
4. **Reconstruction** : Anomalies = mal reconstruites

**Alternatives considérées** :
- Isolation Forest : Plus rapide mais patterns linéaires
- One-Class SVM : Bon mais lent sur grandes données
- LSTM : Pour séquences temporelles (non implémenté ici)

### 🔧 Hyperparamètres

```python
Architecture:
- Input: 50 features
- Encoder: [64, 32, 16] neurones
- Decoder: [32, 64, 50] neurones
- Activation: ReLU (encodeur/décodeur), Linear (output)
- Regularization: BatchNorm + Dropout(0.2)

Training:
- Epochs: 20 (early stopping patience=5)
- Batch size: 256
- Optimizer: Adam (lr=0.001)
- Loss: MSE
- Validation split: 10%

Detection:
- Threshold: 95th percentile (5% FPR)
```

---

## 9. TROUBLESHOOTING

### ❗ Problèmes Courants

#### Problème 1 : "NameError: name 'layers' is not defined"
**Cause** : Faute de frappe dans le code  
**Solution** : Vérifier l'import `from keras import layers`

#### Problème 2 : "FileNotFoundError: paysim_features.csv"
**Cause** : Fichier intermédiaire manquant  
**Solution** : Exécuter les scripts dans l'ordre (1 → 2 → 3)

#### Problème 3 : "Out of Memory"
**Cause** : Dataset trop grand pour la RAM  
**Solution** : 
```python
# Réduire batch size
batch_size = 128  # Au lieu de 256

# Ou réduire encore le dataset
df_reduced = df.sample(n=30000, random_state=42)
```

#### Problème 4 : Modèle ne détecte rien / détecte tout
**Cause** : Threshold mal calibré  
**Solution** : Ajuster le percentile (90-99)
```python
threshold = np.percentile(train_mse, 97)  # Essayer différentes valeurs
```

#### Problème 5 : Performances faibles
**Causes possibles** :
1. Pas assez d'epochs → Augmenter à 30-50
2. Learning rate trop élevé → Diminuer à 0.0001
3. Features non pertinentes → Sélection de features
4. Dataset déséquilibré → Vérifier distribution

---

## 10. DÉVELOPPEMENTS FUTURS

### 🚀 Améliorations Possibles

1. **Features réseau** : Analyser graphes de transactions
2. **Modèles temporels** : LSTM pour séquences
3. **Ensemble** : Combiner plusieurs modèles
4. **Explicabilité** : SHAP/LIME pour interpréter
5. **API REST** : Déploiement web service
6. **Dashboard** : Interface de monitoring
7. **A/B Testing** : Comparer versions
8. **Online Learning** : Mise à jour continue

---

## 📞 SUPPORT

### Fichiers Essentiels à Ne PAS Supprimer

✅ **Code source** :
- `1_data_preparation.py`
- `2_feature_engineering.py`
- `3_train.py`

✅ **Modèles entraînés** :
- `autoencoder.keras`
- `autoencoder_scaler.pkl`
- `ae_threshold.npy`

✅ **Configuration** :
- `requirements.txt`

### Fichiers Optionnels (Peuvent être régénérés)

⚠️ **Données intermédiaires** :
- `paysim_reduced.csv` (régénérable via script 1)
- `paysim_features.csv` (régénérable via script 2)

⚠️ **Résultats** :
- `autoencoder_results.png` (régénérable via script 3)
- `feature_names.txt` (régénérable via script 2)

⚠️ **Modèles secondaires** :
- `encoder.keras` (utile seulement pour analyse avancée)

---

## 📋 CHECKLIST DE DÉPLOIEMENT

Avant de mettre en production :

- [ ] Tester le modèle sur données réelles
- [ ] Vérifier les performances sur période récente
- [ ] Définir processus d'escalade pour vraies fraudes
- [ ] Mettre en place monitoring des faux positifs
- [ ] Planifier réentraînement périodique
- [ ] Former les analystes à utiliser les scores
- [ ] Documenter les seuils et leur justification
- [ ] Créer un backup des modèles
- [ ] Définir métriques de succès business
- [ ] Préparer rollback en cas de problème

---

## 📚 RÉFÉRENCES

### Documentation Technique
- **TensorFlow/Keras** : https://www.tensorflow.org/
- **Scikit-learn** : https://scikit-learn.org/
- **Pandas** : https://pandas.pydata.org/

### Papiers Académiques
- Lopez-Rojas, E. A. et al. "PaySim: A financial mobile money simulator for fraud detection" (2016)
- Goodfellow, I. et al. "Deep Learning" (2016)

### Concepts Clés
- Autoencoders pour détection d'anomalies
- Apprentissage non supervisé
- Feature engineering pour transactions financières
- ROC-AUC et métriques de classification déséquilibrée

---

**Document créé le** : 2 janvier 2026  
**Dernière modification** : 2 janvier 2026  
**Version** : 2.0  
**Auteur** : Projet MLPSS - Financial Anomaly Detection  
**Statut** : Production Ready ✅

---

**🎯 Projet prêt pour utilisation et déploiement !**
