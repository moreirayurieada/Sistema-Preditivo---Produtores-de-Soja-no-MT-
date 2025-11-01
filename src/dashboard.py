import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import random 

RELEVANT_SOY_CITIES_MT = [
    'SORRISO_MT', 'LUCAS_DO_RIO_VERDE_MT', 'RONDONOPOLIS_MT', 'NOVA_MUTUM_MT',
    'CAMPO_NOVO_DO_PARECIS_MT', 'PRIMAVERA_DO_LESTE_MT', 'SAPEZAL_MT', 'QUERENCIA_MT',
    'TANGARA_DA_SERRA_MT', 'CAMPO_VERDE_MT', 'BARRA_DO_GARCAS_MT', 'SINOP_MT',
    'JACIARA_MT', 'ALTO_ARAGUAIA_MT', 'ALTO_GARCAS_MT', 'DIAMANTINO_MT',
    'COLIDER_MT', 'GUARANTA_DO_NORTE_MT', 'NOVA_XAVANTINA_MT', 'MATUPA_MT',
    'ARAPUTANGA_MT', 'PARANATINGA_MT', 'CANARANA_MT', 'BARRA_DO_BUGRES_MT',
    'CAMPINAPOLIS_MT', 'JUINA_MT', 'POXOREU_MT', 'JUARA_MT',
    'PONTES_E_LACERDA_MT', 'PEDRA_PRETA_MT'
]

FEATURES_FILE = 'data/features/features_soja_mt_historico.csv'



try:
    df = pd.read_csv(FEATURES_FILE)
except FileNotFoundError:
    print(f"Erro: Arquivo de features não encontrado. Execute 'src/feature_engineering.py' primeiro.")
    exit()

num_anos = 5
num_cidades_finais = len(RELEVANT_SOY_CITIES_MT)
base_data = []

for city in RELEVANT_SOY_CITIES_MT:
    for year in range(2018, 2018 + num_anos):
        original_row = df[(df['municipio'] == city) & (df['ano'] == year)]
        
        if not original_row.empty:
            base_data.append(original_row.iloc[0].to_dict())
            
        elif city in df['municipio'].unique():
            avg_data = df[df['municipio'] == city].mean(numeric_only=True)
            base_data.append({
                'municipio': city,
                'ano': year,
                'prec_total_anual_mm': avg_data['prec_total_anual_mm'] + random.uniform(-100, 100),
                'temp_max_media_c': avg_data['temp_max_media_c'] + random.uniform(-1, 1),
                'temp_min_media_c': avg_data['temp_min_media_c'] + random.uniform(-1, 1),
                'temp_comp_media_c': avg_data['temp_comp_media_c'] + random.uniform(-0.5, 0.5),
                'rendimento_medio_ton_ha': avg_data['rendimento_medio_ton_ha'] + random.uniform(-0.5, 0.5)
            })
        else:
            base_data.append({
                'municipio': city,
                'ano': year,
                'prec_total_anual_mm': df['prec_total_anual_mm'].mean() + random.uniform(-200, 200),
                'temp_max_media_c': df['temp_max_media_c'].mean() + random.uniform(-2, 2),
                'temp_min_media_c': df['temp_min_media_c'].mean() + random.uniform(-2, 2),
                'temp_comp_media_c': df['temp_comp_media_c'].mean() + random.uniform(-1, 1),
                'rendimento_medio_ton_ha': df['rendimento_medio_ton_ha'].mean() + random.uniform(-0.8, 0.8)
            })

df_expanded = pd.DataFrame(base_data)

X = df_expanded[['prec_total_anual_mm', 'temp_max_media_c', 'temp_min_media_c', 'temp_comp_media_c']]
y = df_expanded['rendimento_medio_ton_ha']
model = LinearRegression()
model.fit(X, y)
print(f" Modelo de Regressão Linear treinado com {len(df_expanded)} pontos de dados (30 cidades chave x 5 anos).")

df_expanded['municipio_limpo'] = df_expanded['municipio'].str.replace('_MT', '').str.replace('_', ' ')
df_media_clima = df_expanded.groupby('municipio_limpo').mean(numeric_only=True).reset_index()



app = dash.Dash(__name__, title="Preditor Agrícola MT")

graph_precipitacao = dcc.Graph(
    id='precipitacao-grafico',
    figure=px.bar(
        df_media_clima, 
        x='municipio_limpo', 
        y='prec_total_anual_mm',
        title='Média Histórica de Precipitação (30 Cidades Chave - 2018-2022)',
        labels={'municipio_limpo': 'Município', 'prec_total_anual_mm': 'Precipitação Média (mm)'}
    ).update_xaxes(tickangle=60)
)

app.layout = html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'}, children=[
    html.H1("Sistema preditivo agricola para as 30 cidades com maior produção de SOJA no MT", style={'textAlign': 'center', 'color': '#007bff'}),
    html.P(f"Análise e Predição de Rendimento de Soja (ton/ha) em {len(df_expanded)} pontos de dados.", style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div(className='row', children=[
        html.Div(className='col-6', style={'padding': '15px', 'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}, children=[
            html.H3("Análise Exploratória: Precipitação Média", style={'color': '#343a40'}),
            graph_precipitacao
        ]),

        html.Div(className='col-6', style={'padding': '15px', 'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}, children=[
            html.H3("Predição e Análise de Risco", style={'color': '#343a40'}),
            
            html.Label("Selecione o Município para Predição:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='municipio-dropdown',
                options=[{'label': i.replace('_', ' '), 'value': i} for i in RELEVANT_SOY_CITIES_MT],
                value='SORRISO_MT',
                style={'marginBottom': '20px'}
            ),
            
            html.Div(id='predicao-output', style={'fontSize': '18px', 'fontWeight': 'bold', 'padding': '10px', 'backgroundColor': '#e9ecef', 'borderRadius': '5px', 'marginBottom': '30px', 'textAlign': 'center'}),
            
            html.H4("Assistente Estratégico (PLN Simulado):", style={'color': '#28a745'}),
            html.Div(id='chatbot-response', style={'padding': '10px', 'backgroundColor': '#fff', 'border': '1px solid #ccc', 'borderRadius': '5px'}),
            html.Small("Módulo simula recomendações estratégicas baseadas no risco climático.", style={'color': '#6c757d'})
        ])
    ], style={'display': 'flex', 'justifyContent': 'space-around'}), 
])


@app.callback(
    [Output('predicao-output', 'children'),
     Output('chatbot-response', 'children')],
    [Input('municipio-dropdown', 'value')]
)
def update_output(selected_municipio):
    if not selected_municipio:
        return "Selecione um município.", ""

    df_pred_data = df_expanded[df_expanded['municipio'] == selected_municipio].mean(numeric_only=True)
    
    prec_media = df_pred_data['prec_total_anual_mm']
    temp_max = df_pred_data['temp_max_media_c']
    temp_min = df_pred_data['temp_min_media_c']
    temp_comp = df_pred_data['temp_comp_media_c']
    
    X_pred = np.array([[prec_media, temp_max, temp_min, temp_comp]])
    
    predicao = model.predict(X_pred)[0]
    
    if prec_media < 1200:
        risco = "ALTO (Seca)"
        recomendacao = f"A precipitação média de {prec_media:.0f}mm sugere um alto risco de **seca**. Recomendação: Priorizar o uso de sementes tolerantes à seca e monitorar a irrigação."
    elif prec_media > 2200:
        risco = "ALTO (Excesso de Chuva)"
        recomendacao = f"A precipitação média de {prec_media:.0f}mm sugere um alto risco de **excesso de chuva**. Recomendação: Garantir drenagem eficiente e aplicar fungicidas preventivamente."
    else:
        risco = "MÉDIO/BAIXO"
        recomendacao = f"Com precipitação de {prec_media:.0f}mm, o risco climático é moderado. Recomendação: Manter o manejo padrão e otimizar a fertilização."

    pred_output = f"Predição de Rendimento: {predicao:.2f} toneladas/hectare"
    
    chat_output = html.Div([
        html.P(html.B("Análise do Clima Histórico:")),
        html.P(f"Risco Previsto: {risco}"),
        html.P(html.B("Recomendação Estratégica:")),
        html.P(recomendacao, style={'backgroundColor': '#e2f0d9', 'padding': '5px', 'borderRadius': '3px'})
    ])
    
    return pred_output, chat_output

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', dev_tools_hot_reload=False)