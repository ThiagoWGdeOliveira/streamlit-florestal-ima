
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st # type: ignore
import seaborn as sns
import matplotlib.font_manager as fm
import plotly.express as px

# Funções para calculo e processamento:

def percentual_area_total(df, idade=None, periodo=None):
    if idade:
        df=df[df['idade']==idade]
    if periodo:
        df=df[df['periodo']==periodo]
    area_total_tipo = df.groupby(['idade','periodo'])['area'].sum().reset_index().rename(columns={'area':'Area_total'})
    return area_total_tipo

def ima_medio(df, idade=None, periodo=None):
    if idade:
        df=df[df['idade']==idade]
    if periodo:
        df=df[df['periodo']==periodo]
    ima_mean = df.groupby(['idade','periodo'])['IMA'].mean().reset_index()
    return ima_mean


def data_describe_gen(df):
    df_resultado = df.groupby(['idade', 'periodo','genotipo']).apply(
        lambda x: pd.Series({
        'Média': x['IMA'].mean(),
        'Desvio Padrão': x['IMA'].std(),
        'Mediana': x['IMA'].median(),
        'Média Ponderada': (x['IMA'] * x['area']).sum() / x['area'].sum(),
        'Máximo': x['IMA'].max(),
        'Mínimo': x['IMA'].min(),
        'CV (%)': (x['IMA'].std()/ x['IMA'].mean())*100 if x['IMA'].mean() != 0 else 0})
    ).reset_index()
    return df_resultado

def data_describe_fazenda(df):
    df_resultado = df.groupby(['idade', 'periodo','fazenda']).apply(
        lambda x: pd.Series({
        'Média': x['IMA'].mean(),
        'Desvio Padrão': x['IMA'].std(),
        'Mediana': x['IMA'].median(),
        'Média Ponderada': (x['IMA'] * x['area']).sum() / x['area'].sum(),
        'Máximo': x['IMA'].max(),
        'Mínimo': x['IMA'].min(),
        'CV (%)': (x['IMA'].std()/ x['IMA'].mean())*100 if x['IMA'].mean() !=0 else 0})
    ).reset_index()
    return df_resultado

def data_describe(df):
    df_resultado = df.groupby(['idade', 'periodo']).apply(
        lambda x: pd.Series({
        'Média': x['IMA'].mean(),
        'Desvio Padrão': x['IMA'].std(),
        'Mediana': x['IMA'].median(),
        'Média Ponderada': (x['IMA'] * x['area']).sum() / x['area'].sum(),
        'Máximo': x['IMA'].max(),
        'Mínimo': x['IMA'].min(),
        'CV (%)': (x['IMA'].std()/ x['IMA'].mean())*100 if x['IMA'].mean() != 0 else 0})
    ).reset_index()
    
    return df_resultado


def graficos_distribuicao_ima(df):
        plt.figure(figsize=(12,6))
        sns.kdeplot(data=df,x='IMA', hue='periodo', fill=True, alpha=0.5, palette=['#4DA1FF','#2E8B57'],common_norm=False, linewidth=1)
        plt.xlabel('IMA (m³/ha ano)', fontsize=14)
        plt.ylabel('')
        plt.xlim(1,70)
        plt.xticks(fontsize=14)
        plt.yticks([])
        plt.ylim(0,0.1)
        plt.gca().spines[['top','right', 'left', 'bottom']].set_visible(False)
        st.pyplot(plt)

def graficos_ima_geral(df):
    df_media = df.groupby(['idade', 'periodo'])['IMA'].mean().reset_index()

    fig = px.line(df_media, x='idade', y='IMA', color='periodo', markers=True,
                  labels={'idade': 'Idade (anos)', 'IMA': 'IMA (m³/ha ano)', 'periodo': 'Períodos'},
                  color_discrete_map={'Atual':'#2E8B57', 'Historico': '#4DA1FF'}
    )

    fig.update_layout(
        title_x=0.5,
        title_font=dict(color='white'),
        font=dict(size=14, color='black'),
        legend_title_text='Período',
        plot_bgcolor='white',
        hovermode= 'x unified'
    )

    st.plotly_chart(fig, use_container_width=True)



    #fig, ax = plt.subplots(figsize=(12,6))
    #sns.lineplot(data=df_media, x='idade', y='IMA', hue='periodo', palette=['#4DA1FF','#2E8B57'], linewidth=2, ax=ax)
    #ax.set_xlabel('Idade (anos)', size=12)
    #ax.set_ylabel('IMA (m³/ha ano)',size=12)
    #ax.set_xlim(1.5,6.5)
    #ax.tick_params(axis='both',size=1, labelsize=12)
    #ax.set_ylim(15,70)
    #ax.legend(title='Período', title_fontsize=12, fontsize=10, loc='upper right')
    #ax.spines[['top','right', 'left', 'bottom']].set_visible(False)
    #st.pyplot(fig)


st.set_page_config(
    page_title= 'Crescimento Florestal',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown("""
            <h1 style='text-align: center, color: #2c3e50;'>🌳 Análise de Crescimento Florestal</h1>
            <h4 style='text-align: center, color: #6c757d;'> 📈 Visualização do Incremento Médio Anual (IMA) com Dados simulados</h4>
""", unsafe_allow_html=True)

st.markdown("---")

df = pd.read_excel('data/dados_simulados.xlsx')

st.sidebar.header('🎛️ Filtros', divider='gray')
st.sidebar.subheader('📈 Dados Historicos: 2001 até 2012', divider='gray')
st.sidebar.subheader('📈 Dados Atuais: 2013 to 2024', divider='gray')

lista_idades = st.sidebar.multiselect('🕒 Idade', sorted(df['idade'].unique()))
lista_fazenda = st.sidebar.multiselect('🌱 Local', df['fazenda'].unique())
lista_genotipos = st.sidebar.multiselect('🧬 Genótipos', sorted(df['genotipo'].unique()))

df_filtrado = df.copy()
if lista_idades:
    df_filtrado = df_filtrado[df_filtrado['idade'].isin(lista_idades)]
if lista_genotipos:
    df_filtrado = df_filtrado[df_filtrado['genotipo'].isin(lista_genotipos)]
if lista_fazenda:
    df_filtrado = df_filtrado[df_filtrado['fazenda'].isin(lista_fazenda)]

st.markdown("### 🔎 Resumo dos dados")
col1, col2, col3 = st.columns(3)

col1.metric("Nº de Fazendas", f"{df_filtrado['fazenda'].nunique()}")
col2.metric("Nº de Talhões", f"{df_filtrado['talhao'].nunique()}")
col3.metric("Nº de Genótipos", f"{df_filtrado['genotipo'].nunique()}")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(['Dados Gerais','IMA por Genótipo', 'IMA por Local', 'Incremento Médio Anual'])

with tab1:
    df_filtrado2 = df.copy()
    df_area_total_tipo = percentual_area_total(df_filtrado2)
    st.subheader('Área total por Idade e Período (ha)')
    idades = df_area_total_tipo['idade'].unique()
    periodos = df_area_total_tipo['periodo'].unique()
    for periodo in periodos:
        cols = st.columns(len(idades))
        for i, idade in enumerate(idades):
            area_total = df_area_total_tipo[(df_area_total_tipo['idade']==idade) & (df_area_total_tipo['periodo']==periodo)]['Area_total'].sum()
            with cols[i]:
                st.metric(label=f'{idade} anos - {periodo}', value=f'{area_total:,.0f}')
    
    st.markdown("----")

    ima_medio_idade_tipo = ima_medio(df_filtrado2)
    st.subheader('IMA médio por Idade e Período (m³/ha ano)')
    idades = ima_medio_idade_tipo['idade'].unique()
    periodos = ima_medio_idade_tipo['periodo'].unique()
    for periodo in periodos:
        cols = st.columns(len(idades))
        for i, idade in enumerate(idades):
            ima_medio2 = ima_medio_idade_tipo[(ima_medio_idade_tipo['idade']==idade) & (ima_medio_idade_tipo['periodo']==periodo)]['IMA'].mean()
            with cols[i]:
                st.metric(label=f'{idade} anos - {periodo}', value=f'{ima_medio2:,.1f}')


with tab2:
    df_filtrado = df.copy()
    if lista_idades:
        df_filtrado = df_filtrado[df_filtrado['idade'].isin(lista_idades)]
    if lista_genotipos:
        df_filtrado = df_filtrado[df_filtrado['genotipo'].isin(lista_genotipos)]
    df_result = data_describe_gen(df_filtrado)
    st.subheader('📊 Estatística Descritiva do IMA por Idade e Genotipo')
    st.dataframe(df_result)
    graficos_distribuicao_ima(df_filtrado)


with tab3:
    df_filtrado = df.copy()
    if lista_idades:
        df_filtrado = df_filtrado[df_filtrado['idade'].isin(lista_idades)]
    if lista_fazenda:
        df_filtrado = df_filtrado[df_filtrado['fazenda'].isin(lista_fazenda)]
    df_result = data_describe_fazenda(df_filtrado)
    st.subheader('📊 Estatística Descritiva do IMA por Idade e Fazenda')
    st.dataframe(df_result)
    graficos_distribuicao_ima(df_filtrado)


with tab4:
    df_filtrado3 = df.copy()
    if lista_genotipos:
        df_filtrado3 = df_filtrado3[df_filtrado3['genotipo'].isin(lista_genotipos)]
    if lista_fazenda:
        df_filtrado3 = df_filtrado3[df_filtrado3['fazenda'].isin(lista_fazenda)]
    st.subheader('📊 Gráfico do IMA por Idade e Período')
    graficos_ima_geral(df_filtrado3)

st.markdown("---")
st.caption("🚀 Projeto desenvolvido por [Thiago WG de Oliveira](https://github.com/ThiagoWGdeOliveira) · Simulação e Visualização de dados florestais com Streamlit")