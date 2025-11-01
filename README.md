

https://github.com/user-attachments/assets/4b01f279-be0f-4757-a002-963c4767e674

# Sistema preditivo agrícola para as 30 maiores cidades produtora de SOJA

## Objetivo do Projeto

Desenvolvimento de um Produto Mínimo Viável (MVP) de Machine Learning para prever o Rendimento Médio de Soja (toneladas/hectare) no estado do Mato Grosso mais especificamente nas 30 maiores produtores de soja. O sistema é dimensionado para prover *insights* acionáveis e estratégicos para o setor.

## Escalabilidade e Coerência

O projeto foi validado com foco em **30 Cidades** de alta relevância agrícola em produçao de soja no MT

1.  **Dataset:** Base de 150 observações (30 cidades x 5 anos de histórico) criada com *Feature Engineering*.
2.  **Coerência:** O **EDA** (`EDA.ipynb`), o **Modelo** e o **Dashboard** utilizam a mesma base de dados.

##  Estrutura do Repositório

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `EDA.ipynb` | Análise Exploratória de Dados (EDA), Matriz de Correlação e Validação do Modelo de ML. |
| `dashboard.py` | Aplicação web interativa (Dashboard) com predição e **Recomendações Estratégicas**. |
| `requirements.txt` | Dependências Python necessárias para rodar todo o projeto. |
| `modelos/` | Pasta que armazena o modelo treinado (`modelo_soja_mt.joblib`). |

---

## 🚀 Guia de Execução Completo (Passo a Passo)

Siga este guia para reproduzir o ambiente e rodar o projeto.

### 1. Preparação do Ambiente

**Pré-requisito:** Python (versão 3.8+) instalado no sistema.

1.  **Baixe/Clone o Repositório.**
2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python -m venv venv
    # Windows (PowerShell/CMD)
    .\venv\Scripts\activate
    # Linux/macOS
    source venv/bin/activate
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Treinamento e Validação do Modelo (EDA.ipynb)

O modelo precisa ser treinado e salvo para uso no Dashboard.

1.  **Inicie o Jupyter Notebook/Lab:**
    ```bash
    jupyter notebook
    ```
2.  **Execute o `EDA.ipynb`:**
    * **Execute todas as células** em ordem (Célula 1 até Célula 6).
    * A **Célula 6** treinará o `LinearRegression`, exibirá as métricas (R², MSE) e simulará o salvamento do modelo.

### 3. Rodar o Dashboard (Entrega Final)

Com o modelo treinado (etapa 2), inicie a aplicação web.

1.  **Volte ao Terminal** (certifique-se de que o ambiente virtual está ativo).
2.  **Execute o Script Principal:**
    ```bash
    python src/dashboard.py
    ```
3.  **Acesse o Dashboard:** Copie e cole o link gerado (Ex: `http://127.0.0.1:8050/`) no seu navegador.
|

### Diferencial Estratégico

O Dashboard inclui um assistente estratégico (PLN Simulado) que analisa o risco climático e gera recomendações acionáveis (ex: gestão de irrigação ou escolha de sementes), elevando o valor da predição para o usuário final.

---

**Autor:** Yuri A. Moreira4aa
**Disciplina:** Inteligência Artificial
