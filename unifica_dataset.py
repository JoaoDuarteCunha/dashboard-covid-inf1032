import plotly.express as px

# Load data and compute static values
from shinywidgets import render_plotly

from shiny import reactive, render, ui
import glob
import pandas as pd

from tratamento_dado import tratamento

print("INICIA CARREGAMENTO DOS DATASETS")
# Unificação e tratamento dos arquivos de lote
lista_arqs = glob.glob("dados/*.csv")

lista_dfs = []
for arq in lista_arqs:
    df_novo = pd.read_csv(arq, sep=";", low_memory=False)
    lista_dfs.append(df_novo)

df_final = pd.concat(lista_dfs)
print("UNIFICAÇÃO DOS DATASETS FINALIZADO")

print("TRATAMENTO DOS DATASETS INICIADO")
df_tratado = tratamento(df_final)
print("TRATAMENTO DOS DATASETS FINALIZADO")
df_tratado.to_csv("dataset_final.csv", sep=";")
print("FINALIZADO")
