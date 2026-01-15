import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Charger les données
df_original = pd.read_csv('paysim dataset.csv')
df_features = pd.read_csv('paysim_features (1).csv')

print("=" * 80)
print("NETTOYAGE DU DATASET PAYSIM")
print("=" * 80)

# 1. INFORMATIONS INITIALES
print("\n1. INFORMATIONS INITIALES")
print(f"Dimension du dataset original: {df_original.shape}")
print(f"Dimension du dataset features: {df_features.shape}")
print(f"\nColonnes du dataset original:\n{df_original.columns.tolist()}")
print(f"\nColonnes du dataset features:\n{df_features.columns.tolist()}")

# 2. VERIFIER LES VALEURS MANQUANTES
print("\n2. VALEURS MANQUANTES")
missing_original = df_original.isnull().sum()
print(f"\nValeurs manquantes dans dataset original:\n{missing_original[missing_original > 0]}")

missing_features = df_features.isnull().sum()
print(f"\nValeurs manquantes dans dataset features:\n{missing_features[missing_features > 0]}")

# 3. SUPPRIMER LES DOUBLONS
print("\n3. SUPPRESSION DES DOUBLONS")
duplicates_before = len(df_original)
df_original = df_original.drop_duplicates()
duplicates_removed = duplicates_before - len(df_original)
print(f"Doublons supprimés: {duplicates_removed}")

# 4. NETTOYER LES TYPES DE DONNÉES
print("\n4. NETTOYAGE DES TYPES DE DONNÉES")
# Convertir les colonnes numériques
numeric_cols = df_original.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_cols:
    df_original[col] = pd.to_numeric(df_original[col], errors='coerce')

print(f"Colonnes numériques: {list(numeric_cols)}")

# 5. VERIFIER LES VALEURS NEGATIVES
print("\n5. VERIFIER LES VALEURS ANORMALES")
# Vérifier les montants négatifs
amount_col = 'amount' if 'amount' in df_original.columns else None
if amount_col:
    negative_amounts = (df_original[amount_col] < 0).sum()
    print(f"Montants négatifs trouvés: {negative_amounts}")
    if negative_amounts > 0:
        df_original = df_original[df_original[amount_col] >= 0]
        print(f"Montants négatifs supprimés")

# 6. VERIFIER LES VALEURS INFINIES
print("\n6. SUPPRESSION DES VALEURS INFINIES")
initial_rows = len(df_original)
df_original = df_original.replace([np.inf, -np.inf], np.nan)
df_original = df_original.dropna()
rows_removed = initial_rows - len(df_original)
print(f"Lignes avec valeurs infinies supprimées: {rows_removed}")

# 7. NETTOYER LES COLONNES TEXT
print("\n7. NETTOYAGE DES COLONNES TEXTE")
text_cols = df_original.select_dtypes(include=['object']).columns
for col in text_cols:
    # Supprimer les espaces avant et après
    if df_original[col].dtype == 'object':
        df_original[col] = df_original[col].str.strip()
        # Convertir en minuscules si applicable
        if col in ['type', 'TYPE']:
            df_original[col] = df_original[col].str.upper()

print(f"Colonnes texte nettoyées: {list(text_cols)}")

# 8. FUSIONNER AVEC LES FEATURES SI MEMES DIMENSIONS
print("\n8. FUSION AVEC LES FEATURES")
if len(df_original) == len(df_features):
    print("Les deux datasets ont la même dimension - Fusion réussie")
    df_cleaned = pd.concat([df_original, df_features], axis=1)
    # Supprimer les doublons de colonnes
    df_cleaned = df_cleaned.loc[:, ~df_cleaned.columns.duplicated()]
    print(f"Dimension finale après fusion: {df_cleaned.shape}")
else:
    print(f"Attention: Les datasets n'ont pas la même dimension")
    print(f"Original: {len(df_original)} lignes, Features: {len(df_features)} lignes")
    # Fusionner les deux datasets
    min_rows = min(len(df_original), len(df_features))
    df_original = df_original.iloc[:min_rows]
    df_features = df_features.iloc[:min_rows]
    df_cleaned = pd.concat([df_original, df_features], axis=1)
    df_cleaned = df_cleaned.loc[:, ~df_cleaned.columns.duplicated()]
    print(f"Fusion réalisée avec les {min_rows} premières lignes")

# 9. SUPPRIMER LES LIGNES AVEC TROP DE VALEURS MANQUANTES
print("\n9. SUPPRESSION DES LIGNES AVEC TROP DE VALEURS MANQUANTES")
initial_rows = len(df_cleaned)
# Supprimer les lignes où plus de 50% des valeurs sont manquantes
df_cleaned = df_cleaned.dropna(thresh=len(df_cleaned.columns) * 0.5)
rows_removed = initial_rows - len(df_cleaned)
print(f"Lignes avec trop de valeurs manquantes supprimées: {rows_removed}")

# 10. REMPLIR LES VALEURS MANQUANTES
print("\n10. REMPLISSAGE DES VALEURS MANQUANTES")
for col in df_cleaned.columns:
    if df_cleaned[col].isnull().sum() > 0:
        if df_cleaned[col].dtype in ['float64', 'int64']:
            # Remplir avec la médiane pour les colonnes numériques
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
        else:
            # Remplir avec 'Unknown' pour les colonnes texte
            df_cleaned[col] = df_cleaned[col].fillna('Unknown')

print(f"Total valeurs manquantes après remplissage: {df_cleaned.isnull().sum().sum()}")

# 11. STATISTIQUES FINALES
print("\n11. STATISTIQUES FINALES")
print(f"\nDimension finale du dataset: {df_cleaned.shape}")
print(f"\nStatistiques descriptives:")
print(df_cleaned.describe())

# 12. SAUVEGARDER LE DATASET NETTOYÉ
print("\n12. SAUVEGARDE")
output_file = 'paysim_cleaned.csv'
df_cleaned.to_csv(output_file, index=False)
print(f"Dataset nettoyé sauvegardé dans: {output_file}")

# Résumé final
print("\n" + "=" * 80)
print("RÉSUMÉ DU NETTOYAGE")
print("=" * 80)
print(f"Lignes supprimées: {duplicates_removed + rows_removed}")
print(f"Valeurs manquantes finales: {df_cleaned.isnull().sum().sum()}")
print(f"Colonnes finales: {df_cleaned.shape[1]}")
print(f"Lignes finales: {df_cleaned.shape[0]}")
print("=" * 80)
