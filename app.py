
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st # type: ignore
import seaborn as sns
import matplotlib.font_manager as fm

# Funções para calculo e processamento:

def percentual_area_total(df, ano=None, periodo=None):
    if ano:
        df=df[df['ano']==ano]
    if periodo:
        df=df[df['periodo']==periodo]
    area_total_tipo = df_filtrado2.groupby(['ano','periodo'])['area'].sum().reset_index().rename(columns={'area':'Area_total'})
    return area_total_tipo

def percentual_area_genotipo(df, ano=None, periodo=None):
    if ano:
        df=df[df['ano'] == ano]
    if periodo:
        df=df[df['periodo'] == periodo]
    area_total_tipo = df.groupby(['ano','periodo'])['area'].sum().reset_index().rename(columns={'area':'Area_total'})
    area_total_tipo_gen = df.groupby(['ano', 'periodo', 'genotipo'])['area'].sum().reset_index()
    area_percentual = area_total_tipo_gen.merge(area_total_tipo, on=['ano','periodo'])
    area_percentual['Percentual_area'] = (area_percentual['area'] / area_percentual['Area_total']) *100
    area_percentual = area_percentual[area_percentual['Percentual_area'] > 1].reset_index(drop=True)
    area_percentual_ordenada = area_percentual.sort_values(by=['ano', 'periodo', 'Percentual_area'], ascending=[True, False, False]).reset_index(drop=True)
    
    return area_percentual_ordenada

def percentual_area_horto(df, ano=None, periodo=None):
    if ano:
        df=df[df['ano']==ano]
    if periodo:
        df=df[df['periodo']==periodo]
    area_total_tipo = df.groupby(['ano','periodo'])['area'].sum().reset_index().rename(columns={'area':'Area_total'})
    area_total_tipo_gen = df.groupby(['ano','periodo', 'fazenda'])['area'].sum().reset_index()
    area_percentual = area_total_tipo_gen.merge(area_total_tipo, on=['ano','periodo'])
    area_percentual['Percentual_area'] = (area_percentual['area'] / area_percentual['Area_total']) *100
    area_percentual = area_percentual[area_percentual['Percentual_area'] > 1].reset_index(drop=True)
    area_percentual_ordenada_horto = area_percentual.sort_values(by=['ano','periodo', 'Percentual_area'], ascending=[True, False, False]).reset_index(drop=True)
    
    return area_percentual_ordenada_horto

def graficos_barra_gen(df):
    anos = df['ano'].unique()
    periodos = df['periodo'].unique()
    for ano in anos:
        st.subheader(f'Area por Genótipo - {ano}')
        cols = st.columns(len(periodos))

        for i, periodo in enumerate(periodos):
            df = df[(df['ano']==ano) & (df['periodo']==periodo)]
            if df.empty:
                continue
            with cols[i]:
                fig, ax = plt.subplots(figsize=(12,10))
                sns.barplot(x='genotipo', y='Percentual_area', data=df, palette='viridis_r', hue='Percentual_area', legend=False, ax=ax)
                ax.set_xlabel('')
                ax.set_ylabel('Área (%)', fontsize=20)
                ax.set_title(f'{type}', fontsize=26)
                ax.set_xticklabels(ax.get_xticklabels(), fontsize=20, rotation=45)
                ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)
                ax.set_ylim(0,100)
                st.pyplot(fig)

def graficos_barra_horto(df):
    anos = df['ano'].unique()
    periodos = df['periodo'].unique()
    for ano in anos:
        st.subheader(f'Área por Fazenda - {ano}')
        cols = st.columns(len(periodos))
        for i, periodo in enumerate(periodos):
            df = df[(df['ano']==ano) & (df['periodo']==periodo)]
            if df.empty:
                continue
            with cols[i]:
                fig, ax = plt.subplots(figsize=(12,10))
                sns.barplot(x='fazenda', y='Percentual_area', data=df, palette='viridis_r', hue='Percentual_area', legend=False, ax=ax)
                ax.set_xlabel('')
                ax.set_ylabel('Área (%)', fontsize=20)
                ax.set_title(f'{type}', fontsize=26)
                ax.set_xticklabels(ax.get_xticklabels(), fontsize=16, rotation=45)
                ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)
                ax.set_ylim(0,100)
                st.pyplot(fig)


def data_describe(df):
    df_resultado = df.groupby(['ano', 'periodo']).apply(
        lambda x: pd.Series({
        'Média': x['ima'].mean(),
        'Desvio Padrão': x['ima'].std(),
        'Mediana': x['ima'].median(),
        'Média Ponderada': (x['ima'] * x['area']).sum() / x['area'].sum(),
        'Máximo': x['ima'].max(),
        'Mínimo': x['ima'].min(),
        'CV (%)': (x['ima'].std()/ x['ima'].mean())*100})
    ).reset_index()
    
    return df_resultado


def graficos_distribuicao_ima(df):
        plt.figure(figsize=(12,6))
        sns.kdeplot(data=df,x='ima', hue='periodo', fill=True, alpha=0.5, palette=['gold','indigo'],common_norm=False, linewidth=0)
        plt.xlabel('IMA (m³/ha yr)', fontsize=20, fontweight='bold')
        plt.ylabel('')
        plt.xlim(1,90)
        plt.xticks(fontsize=20, fontweight='bold')
        plt.yticks([])
        plt.ylim(0,0.06)
        plt.gca().spines[['top','right', 'left', 'bottom']].set_visible(False)
        st.pyplot(plt)

#graficos_distribuicao_ima(df_todos_modificado)

df = pd.read_excel('data/dados_simulados.xlsx')

st.write("""
# Growth Analysis
""")

st.sidebar.header('Filtros', divider='gray')
st.sidebar.subheader('Dados Historicos: 2001 até 2012', divider='gray')
st.sidebar.subheader('Dados Atuais: 2013 to 2024', divider='gray')

lista_anos = st.sidebar.multiselect('Idade', df['ano'].unique())
lista_fazenda = st.sidebar.multiselect('Local', df['fazenda'].unique())
lista_genotipos = st.sidebar.multiselect('Genótipos', df['genotipo'].unique())

tab1, tab2, tab3, tab4 = st.tabs(['Geral','Área por Genótipo', 'Área por Local', 'Incremento Médio Anual'])

with tab1:
    df_filtrado2 = df.copy()
    df_area_total_tipo = percentual_area_total(df_filtrado2)
    st.subheader('Área total por Idade e Período')
    anos = df_area_total_tipo['ano'].unique()
    periodos = df_area_total_tipo['periodo'].unique()
    for ano in anos:
        cols = st.columns(len(periodos))
        for i, periodo in enumerate(periodos):
            area_total = df_area_total_tipo[(df_area_total_tipo['ano']==ano) & (df_area_total_tipo['periodo']==periodo)]['Area_total'].sum()
            with cols[i]:
                st.metric(label=f'{ano} - {periodo}', value=f'{area_total:,.0f} ha')

with tab2:
    df_filtrado = df.copy()
    if lista_anos:
        df_filtrado = df_filtrado[df_filtrado['ano'].isin(lista_anos)]
    if lista_fazenda:
        df_filtrado = df_filtrado[df_filtrado['fazenda'].isin(lista_fazenda)]
    df_todos_area_gen = percentual_area_genotipo(df_filtrado)
    if lista_genotipos:
        df_todos_area_gen = df_todos_area_gen[df_todos_area_gen['genotipo'].isin(lista_genotipos)]
    graficos_barra_gen(df_todos_area_gen)

with tab3:
    df_filtrado = df.copy()
    if lista_anos:
        df_filtrado = df_filtrado[df_filtrado['ano'].isin(lista_anos)]
    if lista_genotipos:
        df_filtrado = df_filtrado[df_filtrado['genotipo'].isin(lista_genotipos)]
    df_todos_area_horto = percentual_area_horto(df_filtrado)
    if lista_fazenda:
        df_todos_area_horto = df_todos_area_horto[df_todos_area_horto['fazenda'].isin(lista_fazenda)]
    graficos_barra_horto(df_todos_area_horto)


with tab4:
    df_filtrado3 = df.copy()
    if lista_anos:
        df_filtrado3 = df_filtrado3[df_filtrado3['ano'].isin(lista_anos)]
    if lista_fazenda:
        df_filtrado3 = df_filtrado3[df_filtrado3['fazenda'].isin(lista_fazenda)]
    df_result = data_describe(df_filtrado3)
    st.subheader('Estatística Descritiva do IMA por Idade e Período')
    st.dataframe(df_result)
    graficos_distribuicao_ima(df_filtrado3)
