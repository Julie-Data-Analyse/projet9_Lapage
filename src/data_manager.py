# CREATION D'UNE FONCTION PERMETTANT D'INSPECTER LE DATAFRAME EN DRY

def inspection (df) : 
    print('\n---------------------------------------------------------------------')
    print('INSPECTION DU DATAFRAME')
    print('---------------------------------------------------------------------')

    print('\n---------------------------------------------------------------------')
    print('Affichage de la structure du df (colonnes, lignes):')
    print('---------------------------------------------------------------------')
    print('nombre de lignes :', df.shape[0])
    print('nombre de colonnes :', df.shape[1])

    print('\n---------------------------------------------------------------------')
    print('Noms des colonnes :')
    print('---------------------------------------------------------------------')
    print (df.columns) 

    print('\n---------------------------------------------------------------------')
    print('Affichage des principales informations statistiques des données du df :')
    print('---------------------------------------------------------------------')
    print(df.describe())

    print('\n---------------------------------------------------------------------')
    print('Types des données :')
    print('---------------------------------------------------------------------')
    print(df.dtypes)

    print('\n---------------------------------------------------------------------')
    print('Affichage du nombre de valeurs uniques (afin de définir ce qui pourrait représenter une PK / FK):')
    print('---------------------------------------------------------------------')
    print(df.nunique())

    print('\n---------------------------------------------------------------------')
    print('Affichage du nombre de valeurs manquantes :')
    print('---------------------------------------------------------------------')
    print(df.isnull().sum())

    print('\n---------------------------------------------------------------------')
    print('Affichage du nombre de doublons :')
    print('---------------------------------------------------------------------')
    print (df.duplicated().sum())

    print('\n---------------------------------------------------------------------')
    print('Affichage des 5 premières lignes :')
    print('---------------------------------------------------------------------')
    print(df.head())
    print('\n---------------------------------------------------------------------')

# créer une itération sur chaque colonne

    valeurs_uniques = df.nunique()
    pk_possible = [col for col in df.columns if valeurs_uniques[col] == df.shape[0]]

    if pk_possible:
        print("Colonnes pouvant constituer une clé primaire :", pk_possible)
    else:
        print("Aucune colonne ne peut constituer une clé primaire en l'état.")

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------

import pandas as pd
def verification_df (df, col1, col2):
    if not isinstance (df, pd.DataFrame) :
        print('KO, ce n\'est pas un dataframe')
        return
    if col1 not in df.columns or col2 not in df.columns :
        print('KO, la/les colonne(s) n\'existe(nt) pas dans le dataframe')
        return
    if not pd.api.types.is_numeric_dtype(df['col1']) or not pd.api.types.is_numeric_dtype(['col2']) :
        print('KO, la/les colonne(s) n\'est pas au format entier')
        return
print('ok, étape suivante')

# ----------------------------------------------------------------------------------------
# from scipy.stats import norm
# from scipy.stats import pearsonr
# from scipy.stats import spearmanr
# def correlation_quanti_quanti(df, col1, col2) :
#     # calcul de la moyenne de l'écart type
#     col1=df['col1'].
#     st.pearsonr(df['col1'],-df['col2'][0])