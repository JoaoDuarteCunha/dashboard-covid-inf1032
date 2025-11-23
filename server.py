import plotly.express as px

# Load data and compute static values
from shinywidgets import render_plotly

from shiny import reactive, render, ui
from shared import df_tratado

import pandas as pd

idade_range = (
    df_tratado["idade"].min().item(),
    df_tratado["idade"].max().item(),
)
raca_cor_lista = df_tratado["racaCor"].fillna("nan").astype(str).unique().tolist()
sexo_lista = df_tratado["sexo"].fillna("nan").astype(str).unique().tolist()
data_range = (
    df_tratado["dataNotificacao"].min(),
    df_tratado["dataNotificacao"].max(),
)


def server(input, output, session):

    @reactive.calc
    def df_filtrado():
        df = df_tratado.copy()

        # Idade
        idade = input.idade()
        # Se permitir nulas
        if input.permite_nulas_idade():
            df = df[df["idade"].between(idade[0], idade[1]) | df["idade"].isna()]
        else:
            df = df[df["idade"].between(idade[0], idade[1])]

        # Data
        inicio, fim = input.data()
        mask_intervalo = (df["dataNotificacao"] >= pd.to_datetime(inicio)) & (
            df["dataNotificacao"] <= pd.to_datetime(fim)
        )

        if input.permite_nulas_data():
            df = df[mask_intervalo | df["dataNotificacao"].isna()]
        else:
            df = df[mask_intervalo]

        df = filtro_com_nan(df, "racaCor", input.racaCor)
        df = filtro_com_nan(df, "sexo", input.sexo)
        df = filtro_selectize(df, "municipio", input.municipio)
        df = filtro_selectize(df, "classificacaoFinal", input.classificacaoFinal)

        return df

    @reactive.effect
    @reactive.event(input.reset)
    def _():
        ui.update_switch("permite_nulas_data", value=True)
        ui.update_switch("permite_nulas_idade", value=True)
        ui.update_slider("idade", value=idade_range)
        ui.update_date_range(
            "data",
            start=data_range[0],
            end=data_range[1],
            min=data_range[0],
            max=data_range[1],
        )
        print(raca_cor_lista)
        ui.update_checkbox_group("racaCor", selected=raca_cor_lista)
        ui.update_checkbox_group("sexo", selected=sexo_lista)
        ui.update_selectize("municipio", selected=[])
        ui.update_selectize("classificacaoFinal", selected=[])

    @render.ui
    def numero_notificacoes():
        return len(df_filtrado())

    @render.ui
    def porcentagem_notificacoes_positivas():
        df = df_filtrado()
        positivos = len(df[df["classificacaoFinalSimplificado"] == 1])

        return f"{positivos / len(df_filtrado()) * 100:.2f}%"

    @render.data_frame
    def table():
        return render.DataGrid(df_filtrado().head(500))


def filtro_selectize(df, coluna: str, input):
    if len(input()) > 0:
        df = df[df[coluna].isin(input())]
    return df


def filtro_com_nan(df: pd.DataFrame, coluna: str, input):
    if "nan" in input():
        df = df[df[coluna].isin(input()) | df[coluna].isna()]
    else:
        df = df[df[coluna].isin(input())]
    return df
