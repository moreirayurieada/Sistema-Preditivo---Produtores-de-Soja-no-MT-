import pandas as pd
import os
import numpy as np
from datetime import datetime


DATA_PROCESSED_DIR = 'data/processed'
DATA_FEATURE_DIR = 'data/features'
os.makedirs(DATA_FEATURE_DIR, exist_ok=True)


CLIMA_PROCESSED_FILE = os.path.join(DATA_PROCESSED_DIR, 'clima_diario_mt_2022.csv')

FEATURES_FILE = os.path.join(DATA_FEATURE_DIR, 'features_soja_mt_historico.csv')

def create_weather_features():

    print(f"Iniciando Feature Engineering (Criando dataset simulado com 30 cidades)...")
    

    try:
        df_clima = pd.read_csv(CLIMA_PROCESSED_FILE, index_col='data', parse_dates=True)
    except FileNotFoundError:
        print(f"Erro: Arquivo processado não encontrado: {CLIMA_PROCESSED_FILE}")
        print("Execute o 'src/data_processing.py' primeiro.")
        return

    df_clima_diario = df_clima.resample('D').agg({
        'precipitacao_mm': 'sum',
        'temp_max_c': 'max',
        'temp_min_c': 'min'
    }).fillna(0) 

    prec_sorriso_2022 = df_clima_diario['precipitacao_mm'].sum()
    temp_max_sorriso_2022 = df_clima_diario['temp_max_c'].mean()
    temp_min_sorriso_2022 = df_clima_diario['temp_min_c'].mean()


    municipios = [
        'SORRISO_MT', 'NOVA_MUTUM_MT', 'SAPEZAL_MT', 'DIAMANTINO_MT', 
        'CAMPO_NOVO_DO_PARECIS_MT', 'NOVA_UBIRATÃ_MT', 'QUERÊNCIA_MT', 
        'PRIMAVERA_DO_LESTE_MT', 'BRASNORTE_MT', 'CAMPO_VERDE_MT', 
        'CAMPOS_DE_JÚLIO_MT', 'CUIABÁ_MT', 'LUCAS_DO_RIO_VERDE_MT', 
        'CANARANA_MT', 'IPIRANGA_DO_NORTE_MT', 'TABAPORÃ_MT', 
        'NOVA_MARINGÁ_MT', 'ITIQUIRA_MT', 'SÃO_JOSÉ_DO_RIO_CLARO_MT', 
        'TANGARÁ_DA_SERRA_MT'
    ]
    anos = np.arange(2018, 2023)
    

    index_mult = pd.MultiIndex.from_product([municipios, anos], names=['municipio', 'ano'])
    df_features = pd.DataFrame(index=index_mult).reset_index()


    df_features['prec_total_anual_mm'] = np.random.uniform(1000, 2500, size=len(df_features))


    df_features['temp_max_media_c'] = np.random.uniform(30.0, 35.0, size=len(df_features))
    df_features['temp_min_media_c'] = np.random.uniform(18.0, 22.0, size=len(df_features))


    df_features['temp_comp_media_c'] = (df_features['temp_max_media_c'] + df_features['temp_min_media_c']) / 2
    
 
    rendimento_base = 3.8
    
    prec_ideal = 1800
    temp_ideal = 25
    
    penalidade_prec = np.abs(df_features['prec_total_anual_mm'] - prec_ideal) / 1000 * 0.2
    penalidade_temp = np.abs(df_features['temp_comp_media_c'] - temp_ideal) / 5 * 0.3
    
    df_features['rendimento_medio_ton_ha'] = (
        rendimento_base - penalidade_prec - penalidade_temp + np.random.uniform(-0.3, 0.5, size=len(df_features))
    )
    
    df_features['rendimento_medio_ton_ha'] = np.clip(df_features['rendimento_medio_ton_ha'], 3.0, 4.5)
    
    df_features.to_csv(FEATURES_FILE, index=False)
    
    print(f"\n Features HISTÓRICAS SIMULADAS (ESCALADAS) criadas e salvas em: {FEATURES_FILE}")
    print(f"Dataset criado com {len(df_features)} linhas (30 municípios x 5 anos).")
    print("\nFeatures prontas para ML (Amostra):")
    print(df_features.head(25))
    
    return FEATURES_FILE

if __name__ == "__main__":
    create_weather_features()