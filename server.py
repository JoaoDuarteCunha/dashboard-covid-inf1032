import plotly.express as px

# Load data and compute static values
from shinywidgets import render_plotly

from shiny import reactive, render
from shared import df_tratado

import pandas as pd


def server(input, output, session):

    @reactive.calc
    def df_filtrado():
        df = df_tratado.copy()

        print(df["racaCor"].unique().tolist())
        # Idade
        idade = input.idade()
        # Se permitir nulas
        if input.permite_nulas():
            df = df[df["idade"].between(idade[0], idade[1]) | df["idade"].isna()]
        else:
            df = df[df["idade"].between(idade[0], idade[1])]

        # Raça/cor
        if "nan" in input.racaCor():
            df = df[df["racaCor"].isin(input.racaCor()) | df["racaCor"].isna()]
        else:
            df = df[df["racaCor"].isin(input.racaCor())]

        return df

    @render.ui
    def numero_notificacoes():
        return len(df_filtrado())

    @render.data_frame
    def table():
        return render.DataGrid(df_filtrado().head(500))
