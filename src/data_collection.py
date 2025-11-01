import requests
import os
import json
import zipfile  
import io      


DATA_RAW_DIR = 'data/raw'
os.makedirs(DATA_RAW_DIR, exist_ok=True)



def fetch_ibge_pam_data():

    print("Tentando API do IBGE (Tabela 1612)...")
    base_url = "https://servicodados.ibge.gov.br/api/v3/agregados/1612/periodos/2022/variaveis/216"
    params = {
        "localidades": "N6[N3[51]]",
        "classificacao": "C48[40129]", 
        "view": "json"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=45) 
        if response.status_code == 200:
            data = response.json()
            file_path = os.path.join(DATA_RAW_DIR, 'pam_soja_mt_rendimento_2022_raw.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Sucesso (IBGE)! Dados salvos em: {file_path}")
            return data
        else:
            print(f"Erro IBGE. Status Code: {response.status_code}. Resposta: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API do IBGE: {e}")
        return None

def fetch_inmet_historical_data():
   
    print("Iniciando coleta de dados da API do INMET (Clima)...")
    
    url_zip = "https://portal.inmet.gov.br/uploads/dadoshistoricos/2022.zip"
    
    estacao_codigo = "A906"
    
    print(f"Baixando arquivo ZIP de 2022 de {url_zip}...")
    print("(Isso pode demorar alguns minutos, o arquivo é grande)...")

    try:
        response = requests.get(url_zip, timeout=600) 
        
        if response.status_code == 200:
            print("Download do ZIP completo. Procurando estação...")
            

            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            

            target_csv_name = None
            for name in zip_file.namelist():
                if f"_{estacao_codigo}_" in name and name.endswith(".CSV"):
                    target_csv_name = name
                    break
            
            if target_csv_name:
                print(f"Estação {estacao_codigo} (Sorriso) encontrada: {target_csv_name}")
                
                file_path = os.path.join(DATA_RAW_DIR, 'inmet_clima_sorriso_2022_raw.csv')
                
                zip_file.extract(target_csv_name, path=DATA_RAW_DIR)
                
                os.rename(os.path.join(DATA_RAW_DIR, target_csv_name), file_path)
                
                print(f"\nUFA! SUCESSO!")
                print(f"Arquivo CSV salvo em: {file_path}")
                return file_path
            else:
                print(f"Erro: Não foi possível encontrar a estação {estacao_codigo} dentro do arquivo ZIP.")
                return None
        
        else:
            print(f"Erro ao baixar o arquivo ZIP. Status Code: {response.status_code}")
            return None

    except requests.exceptions.Timeout:
        print("Erro: O download demorou demais (Timeout).")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com o INMET: {e}")
        return None
    except zipfile.BadZipFile:
        print("Erro: O arquivo baixado não é um ZIP válido.")
        return None

if __name__ == "__main__":
    
    print("--- Iniciando Pipeline de Coleta de Dados ---")
    

    fetch_inmet_historical_data()
    

    print("\n--- API do IBGE em espera---")

    
    print("\n--- Pipeline de Coleta Finalizado ---")