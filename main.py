import os
import subprocess
import sys

def run_script(script_path):


    print(f" INICIANDO: {script_path}")

    

    result = subprocess.run([sys.executable, script_path], capture_output=False, text=True, check=False)
    
    if result.returncode != 0:
        print(f"\n ERRO: O script {script_path} falhou com código de saída {result.returncode}. Parando o pipeline.")
        sys.exit(result.returncode)
    
    print(f"\n SUCESSO: {script_path} concluído.")

if __name__ == "__main__":
    

    scripts = [
        "src/data_collection.py",
        "src/data_processing.py",
        "src/feature_engineering.py",
        "src/model.py"
    ]
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"Erro: Arquivo '{script}' não encontrado. Verifique se os nomes dos arquivos estão corretos.")
            sys.exit(1)
            

    print("       INICIANDO PIPELINE DE ML AGRÍCOLA (COMPLETO)")

    try:

        run_script(scripts[0])
        

        run_script(scripts[1])
    
        run_script(scripts[2])

        run_script(scripts[3])
        
    except Exception as e:
        print(f"\n ERRO FATAL no pipeline: {e}")
        

    print("             PIPELINE COMPLETO CONCLUÍDO!")
 