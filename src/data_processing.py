import pandas as pd
import os
import sys

DATA_RAW_DIR = 'data/raw'
DATA_PROCESSED_DIR = 'data/processed'
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)

CLIMA_RAW_FILE = os.path.join(DATA_RAW_DIR, 'inmet_clima_sorriso_2022_raw.csv')
CLIMA_PROCESSED_FILE = os.path.join(DATA_PROCESSED_DIR, 'clima_diario_mt_2022.csv')

def process_inmet_data():
    print(f"Iniciando processamento do arquivo: {CLIMA_RAW_FILE}")
    
    try:
       
        df = pd.read_csv(
            CLIMA_RAW_FILE,
            sep=';',
            encoding='latin-1', 
            skiprows=8,
            decimal=','
        )
        
        colunas_basicas = {
            'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'precipitacao_mm',
            'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)': 'temp_max_c',
            'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)': 'temp_min_c'
        }
        

        data_col_raw = None
        if 'DATA (YYYY-MM-DD)' in df.columns:
            data_col_raw = 'DATA (YYYY-MM-DD)'
        elif 'Data' in df.columns:

            data_col_raw = 'Data'
        else:
            print("Erro crítico: Nenhuma coluna de data esperada ('DATA (YYYY-MM-DD)' ou 'Data') foi encontrada. Abortando.")
            sys.exit(1)
            
        colunas_renomear = {data_col_raw: 'data'}
        colunas_renomear.update(colunas_basicas)
        
        colunas_para_manter = [col for col in colunas_renomear.keys() if col in df.columns]
        
        if len(colunas_para_manter) < 4:
            print("Aviso: Algumas colunas (Precip, Temp Max/Min) não foram encontradas. O DataFrame pode estar incompleto.")
        
        df = df[colunas_para_manter]
        
        df = df.rename(columns=colunas_renomear)

        df['data'] = pd.to_datetime(df['data'])

        df = df.set_index('data')
        

        df = df.replace([-9999, -999.9], pd.NA)
        
        for col in ['precipitacao_mm', 'temp_max_c', 'temp_min_c']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.interpolate(method='time')
        
        df = df.fillna(0)
        
        df.to_csv(CLIMA_PROCESSED_FILE)
        
        print(f"\nSucesso! Dados climáticos processados e salvos em: {CLIMA_PROCESSED_FILE}")
        print("\nAmostra dos dados limpos:")
        print(df.head())

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {CLIMA_RAW_FILE}")
        print("Certifique-se de que o 'src/data_collection.py' foi executado com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o processamento: {e}")

if __name__ == "__main__":
    process_inmet_data()