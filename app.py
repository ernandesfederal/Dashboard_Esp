import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Configurações de estilo do Seaborn
sns.set(style="ticks")  # Usar estilo "ticks" para evitar grades

# Título da Universidade e Informações do Aluno
st.markdown("""
# Universidade Federal do Maranhão - UFMA  
**Disciplina:** Visualização de Dados
**Especialização em Análise de Dados e Inteligência Artificial**  
Aluno: **Ernandes Guedes Moura**  
Email: [ernandesfedera1@gmail.com](mailto:ernandesfedera1@gmail.com)
""")

# Título do dashboard
st.title("🏠 Dashboard de Aluguel de Imóveis")

# Descrição
st.markdown("Este dashboard explora dados de aluguel de imóveis, exibindo informações como número de banheiros, quartos e valores de aluguel. Explore os dados com os filtros e gráficos interativos!")

# Carregar os dados
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("houses_to_rent_limp.csv", sep=",") #pd.read_csv("C:/Users/Acer/OneDrive - ifpi.edu.br/Documentos/Ciência de Dados/Espec_Ciecia_Dados_UFMA/Visualização de dados/Dashboard_UFMA4/Dashboard_Esp/houses_to_rent_limp.csv", sep=",")
        return data
    except FileNotFoundError:
        st.error("Arquivo 'houses_to_rent_limp.csv' não encontrado. Verifique o caminho do arquivo.")
        return None



# Carregar a imagem
def load_image():
    return "fig.png"

# Exibir a imagem na lateral
st.sidebar.image(load_image(), caption="Aluguel de Imóveis", use_column_width=True, width=500)
# Exibir a imagem na lateral com largura ajustada
#st.sidebar.image(load_image(), caption="Aluguel de Imóveis", use_column_width=True, width=300)  # Ajuste o valor de width conforme necessário
# Carregar dados
df = load_data()

# Verificar se os dados foram carregados com sucesso
if df is not None:
    # Exibir tabela de dados (primeiras 10 linhas)
    st.subheader("🔍 Visualização dos Dados")
    st.write(df.head(4))

    # Filtros no sidebar
    st.sidebar.header("🔧 Filtros")

    # Filtro para cidade
    city_filter = st.sidebar.selectbox("Selecione a cidade (1: Sim, 0: Não)", options=[0, 1])

    # Filtro de faixa de aluguel
    rent_filter = st.sidebar.slider("Selecione a faixa de preço do aluguel", 
                                    min_value=int(df['rent_amount'].min()), 
                                    max_value=int(df['rent_amount'].max()), 
                                    value=(int(df['rent_amount'].min()), int(df['rent_amount'].max())))

    # Aplicar os filtros
    filtered_df = df[(df['city'] == city_filter) & (df['rent_amount'].between(rent_filter[0], rent_filter[1]))]

    # Adicionar botão de exibir ou esconder tabela
    if st.sidebar.button("📋 Exibir Dados Filtrados"):
        st.subheader("🔍 Dados Filtrados")
        st.write(filtered_df)

    # Gráfico de dispersão - Banheiro vs Valor do Aluguel
    st.subheader("📊 Gráfico: Banheiros vs Valor do Aluguel")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='bathroom', y='rent_amount', data=filtered_df, hue='city', ax=ax)
    ax.set_title("Banheiros vs Valor do Aluguel")
    ax.set_xlabel("Número de Banheiros")
    ax.set_ylabel("Valor do Aluguel (R$)")
    ax.spines['top'].set_visible(False)  # Remove a borda superior
    ax.spines['right'].set_visible(False)  # Remove a borda direita
    st.pyplot(fig)

    # Gráfico de barras - Aluguel médio por número de quartos
    st.subheader("🏠 Aluguel Médio por Número de Quartos")
    mean_rent_rooms = filtered_df.groupby('rooms')['rent_amount'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='rooms', y='rent_amount', data=mean_rent_rooms, ax=ax, palette="Blues_d")
    ax.set_title("Aluguel Médio por Número de Quartos")
    ax.set_xlabel("Número de Quartos")
    ax.set_ylabel("Aluguel Médio (R$)")
    ax.spines['top'].set_visible(False)  # Remove a borda superior
    ax.spines['right'].set_visible(False)  # Remove a borda direita
    st.pyplot(fig)

 # Gráficos de distribuição - Boxplot interativo e Histograma
if st.sidebar.checkbox("📊 Exibir Boxplot por Cidade e Histograma"):
    st.subheader("📊 Distribuição do Valor do Aluguel por Cidade e Histograma")

    # Filtrar dados sem aplicar o filtro de cidade (para comparar ambas)
    all_cities_df = df[df['rent_amount'].between(rent_filter[0], rent_filter[1])]

    # Boxplot interativo do valor do aluguel para ambas as cidades
    fig_box = px.box(all_cities_df, x='city', y='rent_amount', color='city',
                     labels={'city': 'Cidade', 'rent_amount': 'Valor do Aluguel (R$)'},
                     title="Boxplot do Valor do Aluguel por Cidade")

    # Remover bordas superiores e direita
    fig_box.update_layout(showlegend=False, 
                          plot_bgcolor='rgba(0, 0, 0, 0)',
                          xaxis=dict(showline=True, linewidth=1, linecolor='black'),
                          yaxis=dict(showline=True, linewidth=1, linecolor='black'))
    fig_box.update_xaxes(showgrid=False)
    fig_box.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray')

    st.plotly_chart(fig_box)

    # Histograma interativo com linha de densidade vermelha (contínua)
    fig_hist = go.Figure()

    # Histograma
    fig_hist.add_trace(go.Histogram(x=all_cities_df['rent_amount'], nbinsx=20, marker_color='skyblue', name='Histograma'))

    # Linha de densidade vermelha contínua
    fig_hist.add_trace(go.Scatter(x=np.sort(all_cities_df['rent_amount']),
                                  y=np.histogram(all_cities_df['rent_amount'], bins=20, density=True)[0],
                                  mode='lines', name='Densidade', line=dict(color='red', width=2)))  # Linha contínua

    # Ajustar layout do histograma
    fig_hist.update_layout(title="Distribuição do Valor do Aluguel",
                           xaxis_title="Valor do Aluguel (R$)",
                           yaxis_title="Frequência",
                           plot_bgcolor='rgba(0, 0, 0, 0)',
                           showlegend=False,
                           xaxis=dict(showline=True, linewidth=1, linecolor='black'),
                           yaxis=dict(showline=True, linewidth=1, linecolor='black'))

    fig_hist.update_xaxes(showgrid=False)
    fig_hist.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray')

    st.plotly_chart(fig_hist)
