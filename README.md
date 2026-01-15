# PaySim Dataset - Nettoyage et Préparation des Données

## 📊 À propos du Dataset PaySim

**Source:** [Kaggle - PaySim Dataset](https://www.kaggle.com/datasets/mtalaltariq/paysim-data?utm_source=chatgpt.com)

Le dataset **PaySim** est un simulateur financier de transactions de monnaie mobile synthétiques. Il contient des données de transactions mobiles qui peuvent être utilisées pour :
- Détecter la fraude financière
- Analyser les patterns de transactions
- Développer des modèles de machine learning pour la classification

### 📁 Fichiers du Dataset

| Fichier | Description | Taille |
|---------|-------------|--------|
| `paysim dataset.csv` | Données brutes originales | ~493 MB |
| `paysim_features (1).csv` | Features engineered (features enrichies) | + petit |
| `paysim_cleaned.csv` | Données nettoyées (généré par le script) | Optimisé |

---

## 🔧 Qu'est-ce que le Script de Nettoyage Fait?

Le script `nettoyage_paysim.py` exécute **11 étapes de nettoyage et préparation des données** :

### **1️⃣ Informations Initiales**
- Affiche les dimensions du dataset original et des features
- Liste toutes les colonnes disponibles
- Permet de comprendre la structure des données

### **2️⃣ Détection des Valeurs Manquantes**
- Identifie les colonnes avec valeurs `NULL` ou `NaN`
- Génère un rapport des données manquantes
- Aide à évaluer la qualité des données

### **3️⃣ Suppression des Doublons**
- Détecte les lignes identiques
- Supprime les duplicatas pour éviter le biais
- Rapporte le nombre de lignes supprimées

### **4️⃣ Nettoyage des Types de Données**
- Convertit les colonnes en types appropriés (float, int)
- Force la conversion numérique pour les calculs
- Utilise `pd.to_numeric()` avec gestion d'erreurs

### **5️⃣ Suppression des Valeurs Anormales**
- **Montants négatifs:** Supprime les transactions avec amount < 0
- Ces valeurs n'ont pas de sens dans un système de transactions réelles
- Importante pour la qualité de l'analyse

### **6️⃣ Suppression des Valeurs Infinies**
- Remplace les valeurs `inf` et `-inf` par `NaN`
- Supprime les lignes contenant ces valeurs
- Évite les erreurs de calcul lors de l'analyse

### **7️⃣ Nettoyage des Colonnes Texte**
- Supprime les espaces inutiles avant et après (`.strip()`)
- Normalise la casse (ex: `TRANSFER`, `PAYMENT`, etc.)
- Améliore la cohérence des données

### **8️⃣ Fusion avec les Features**
- **Étape critique:** Combine les données originales avec les features engineered
- Vérifie que les deux datasets ont le même nombre de lignes
- Si les dimensions diffèrent, utilise les premières N lignes communes
- Supprime les colonnes dupliquées après fusion

### **9️⃣ Suppression des Lignes Incomplètes**
- Supprime les lignes où **plus de 50%** des colonnes sont manquantes
- Règle configurable (peut être ajustée selon vos besoins)
- Préserve les données fiables

### **🔟 Remplissage des Valeurs Manquantes (Imputation)**

**Pour les colonnes numériques:**
- Remplit avec la **médiane** (plus robuste aux outliers que la moyenne)
- Exemple: Si `amount` a des valeurs manquantes → utilise `median(amount)`

**Pour les colonnes texte:**
- Remplit avec `'Unknown'`
- Préserve l'intégrité des données catégoriques

### **1️⃣1️⃣ Statistiques Finales et Sauvegarde**
- Génère des statistiques descriptives (min, max, moyenne, écart-type)
- Sauvegarde le dataset nettoyé dans `paysim_cleaned.csv`
- Crée un rapport final du nettoyage

---

## 📋 Colonnes du Dataset Original

D'après le dataset PaySim, les colonnes principales incluent :

| Colonne | Type | Description |
|---------|------|-------------|
| `step` | Numérique | Pas de temps de la transaction |
| `amount` | Numérique | Montant de la transaction |
| `oldbalanceOrg` | Numérique | Solde initial de l'origine |
| `newbalanceOrig` | Numérique | Nouveau solde de l'origine |
| `oldbalanceDest` | Numérique | Solde initial de la destination |
| `newbalanceDest` | Numérique | Nouveau solde de la destination |
| `type` | Texte | Type de transaction (CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER) |
| `isFraud` | Binaire | 1 = Fraude, 0 = Légitime |

---

## 🎯 Colonnes des Features (paysim_features)

Le fichier `paysim_features (1).csv` contient des **features engineered** (créées manuellement) :

### **Features de Montant:**
- `amount_log` - Logarithme du montant
- `amount_sqrt` - Racine carrée du montant
- `amount_bin_encoded` - Encodage binaire du montant
- `amount_to_oldbalance_ratio` - Rapport montant/solde ancien
- `amount_exceeds_balance` - Indicateur si montant > solde

### **Features Temporelles:**
- `hour` - Heure de la transaction
- `day` - Jour de la transaction
- `is_night` - Transaction de nuit (1/0)
- `is_weekend` - Transaction le weekend (1/0)
- `hour_sin`, `hour_cos` - Encodage circulaire de l'heure

### **Features de Fréquence:**
- `time_since_last_tx` - Temps depuis dernière transaction
- `tx_count_1h` - Nombre de tx en 1 heure
- `tx_count_6h` - Nombre de tx en 6 heures
- `tx_count_24h` - Nombre de tx en 24 heures

### **Features Utilisateur:**
- `user_tx_count` - Nombre total de transactions de l'utilisateur
- `user_avg_amount` - Montant moyen de l'utilisateur
- `user_std_amount` - Écart-type du montant utilisateur
- `amount_deviation_from_user_avg` - Déviation par rapport à la moyenne utilisateur

### **Features de Cohérence:**
- `balance_change_orig` - Changement de solde (origine)
- `balance_change_dest` - Changement de solde (destination)
- `balance_inconsistency_orig` - Incohérence du solde (origine)
- `balance_mismatch` - Problème d'équilibre (1/0)

### **Features de Type:**
- `type_CASH_IN` - Transaction de cash-in (1/0)
- `type_CASH_OUT` - Transaction de cash-out (1/0)
- `type_DEBIT` - Transaction de débit (1/0)
- `type_PAYMENT` - Transaction de paiement (1/0)
- `type_TRANSFER` - Transaction de transfert (1/0)

### **Features de Risque:**
- `is_risky_type` - Type de transaction risqué (1/0)
- `dest_is_merchant` - Destination est un commerçant (1/0)
- `is_c2c` - Transaction client-to-client (1/0)
- `risk_score` - Score de risque calculé
- `consistency_score` - Score de cohérence
- `tx_intensity` - Intensité de la transaction

### **Cible:**
- `isFraud` - Indicateur de fraude (1 = Fraude, 0 = Légitime)

---

## 🚀 Comment Utiliser le Script

### **Prérequis**
```bash
pip install pandas numpy
```

### **Exécution**
```bash
python nettoyage_paysim.py
```

### **Résultat Attendu**
- Fichier `paysim_cleaned.csv` généré dans le même dossier
- Rapport détaillé affiché dans la console
- Dataset prêt pour l'analyse ou le machine learning

---

## 📊 Exemple de Sortie du Script

```
================================================================================
NETTOYAGE DU DATASET PAYSIM
================================================================================

1. INFORMATIONS INITIALES
Dimension du dataset original: (6362620, 11)
Dimension du dataset features: (3000000, 45)

2. VALEURS MANQUANTES
Valeurs manquantes dans dataset original: 0

3. SUPPRESSION DES DOUBLONS
Doublons supprimés: 12345

4. NETTOYAGE DES TYPES DE DONNÉES
Colonnes numériques: ['step', 'amount', 'oldbalanceOrg', ...]

... [autres étapes] ...

11. STATISTIQUES FINALES
Dimension finale du dataset: (3000000, 56)

RÉSUMÉ DU NETTOYAGE
Lignes supprimées: 12345
Valeurs manquantes finales: 0
Colonnes finales: 56
Lignes finales: 3000000
================================================================================
```

---

## 🔍 Points Clés du Nettoyage

| Aspect | Action | Raison |
|--------|--------|--------|
| **Doublons** | Supprimés | Évite le biais d'apprentissage |
| **Types** | Convertis correctement | Nécessaire pour les calculs |
| **Montants négatifs** | Supprimés | Non-réalistes dans un système réel |
| **Valeurs infinies** | Supprimées | Erreurs numériques |
| **Texte** | Normalisé | Cohérence des catégories |
| **Fusion** | Combinaison avec features | Dataset enrichi pour ML |
| **Valeurs manquantes** | Imputation intelligente | Préserve les données avec perte minimale |

---

## 💡 Cas d'Usage

Ce dataset nettoyé peut être utilisé pour :

✅ **Détection de Fraude** - Classification binaire (Fraude/Légitime)  
✅ **Analyse de Risque** - Scoring des transactions suspectes  
✅ **Prédiction** - ML models (Random Forest, XGBoost, Neural Networks)  
✅ **Exploration** - EDA et statistiques descriptives  
✅ **Benchmark** - Tester des algorithmes de détection  

---

## 📝 Notes Importantes

- ⚠️ Le script utilise la **médiane** pour l'imputation (robuste aux outliers)
- ⚠️ Les valeurs manquantes > 50% des colonnes sont supprimées
- ⚠️ La fusion suppose que les datasets sont **alignés temporellement**
- ⚠️ Le fichier de sortie peut être volumineux (adaptez selon votre RAM)

---

## 🎓 Ressources

- [PaySim Kaggle Dataset](https://www.kaggle.com/datasets/mtalaltariq/paysim-data)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Feature Engineering Best Practices](https://scikit-learn.org/stable/)

---

**Auteur:** Script de nettoyage automatisé  
**Date:** 2026  
**Objectif:** Préparation de données PaySim pour analyse et machine learning
