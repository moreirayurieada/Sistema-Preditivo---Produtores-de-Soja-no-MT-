import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

DATA_FEATURE_DIR = 'data/features'
FEATURES_FILE = os.path.join(DATA_FEATURE_DIR, 'features_soja_mt_2022.csv')

def run_ml_model():
    """
    """
    print("--- Iniciando Módulo de Machine Learning ---")
    
    try:
        df = pd.read_csv(FEATURES_FILE)
        
        df['rendimento_medio_ton_ha'] = 3.7
        
        print("\nDataset Final (Features + Target Simulado):")
        print(df[['municipio', 'prec_total_anual_mm', 'temp_comp_media_c', 'rendimento_medio_ton_ha']].head())
        
        X = df[['prec_total_anual_mm', 'temp_max_media_c', 'temp_min_media_c', 'temp_comp_media_c']]
        y = df['rendimento_medio_ton_ha']
        
        model = LinearRegression()
        model.fit(X, y)
        
        prediction = model.predict(X)
        
        print("\n--- Resultados do Modelo ---")
        print(f"Modelo Treinado: Linear Regression")
        print(f"Predição do Rendimento (ton/ha) para Sorriso (2022): {prediction[0]:.2f}")
        print(f"Target Real (Simulado): {y.iloc[0]:.2f}")
        
        print("\nSUCESSO! O pipeline de dados está funcional.")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo de features não encontrado: {FEATURES_FILE}")
        print("Certifique-se de que o 'src/feature_engineering.py' foi executado com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro no módulo ML: {e}")

if __name__ == "__main__":
    run_ml_model()