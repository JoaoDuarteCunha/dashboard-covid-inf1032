import plotly.express as px
import numpy as np

# Load data and compute static values
from shinywidgets import render_widget

from shiny import reactive, render, ui
from model.tipo_grafico.barra import GraficoBarra
from model.tipo_grafico.linha import GraficoLinha
from model.tipo_grafico.piramide_etaria import GraficoPiramideEtaria
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

    @render.ui
    def idade_media():
        df = df_filtrado()

        return f"{df["idade"].mean():.0f}"

    @render.data_frame
    def table():
        return render.DataGrid(df_filtrado().head(500))

    @reactive.calc
    def processa_piramide_etaria():
        df = df_filtrado().copy()

        # Criar faixa etária
        bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100, np.inf]
        labels = [
            "<18",
            "18-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",
            "80-89",
            "90-99",
            "100+",
        ]

        df["age_range"] = pd.cut(df["idade"], bins=bins, labels=labels, right=False)

        # Contagem de casos
        df_group = (
            df.groupby(["sexo", "age_range"]).size().reset_index(name="total_admissoes")
        )

        # Separar masculino e feminino
        df_masculino = df_group[df_group["sexo"] == "Masculino"].copy()
        df_feminino = df_group[df_group["sexo"] == "Feminino"].copy()

        df_masculino["total_admissoes_abs"] = df_masculino["total_admissoes"]
        df_masculino["total_admissoes"] *= -1  # para pirâmide

        ordem_idades = labels  # já definidas acima

        # Criar gráficos
        plot_1 = GraficoBarra(
            dataframe=df_masculino,
            eixo_x="total_admissoes",
            eixo_y="age_range",
            hex_cores=["#4B6BD5"],
            ordem={"age_range": ordem_idades},
            data_custom_hover=["total_admissoes_abs"],
        )
        plot_1.set_hover("<b>%{y}</b><br>Masculino: %{customdata[0]:,}<extra></extra>")
        plot_1.set_nome("Masculino")

        plot_2 = GraficoBarra(
            dataframe=df_feminino,
            eixo_x="total_admissoes",
            eixo_y="age_range",
            hex_cores=["#E91E63"],
            ordem={"age_range": ordem_idades},
        )
        plot_2.set_hover("<b>%{y}</b><br>Feminimo: %{customdata[0]:,}<extra></extra>")
        plot_2.set_nome("Feminino")

        valor_maximo = max(
            abs(df_masculino["total_admissoes"].min()),
            df_feminino["total_admissoes"].max(),
        )

        fig = GraficoPiramideEtaria(plot_1, plot_2, valor_maximo)
        fig.set_ordem(ordem_idades)

        return fig

    @render_widget
    def grafico_piramide_etaria():
        return processa_piramide_etaria().get_grafico_figure()

    @render_widget
    def grafico_numero_casos():
        df = df_filtrado()

        df["ano"] = df["dataNotificacao"].dt.year
        df["mes"] = df["dataNotificacao"].dt.month

        df["ano_mes"] = df["dataNotificacao"].dt.to_period("M")

        df_agrupado = df.groupby("ano_mes").size().reset_index(name="num_casos")

        df_agrupado = df_agrupado.sort_values("ano_mes")
        df_agrupado["ano_mes_str"] = df_agrupado["ano_mes"].astype(str)

        plot = GraficoLinha(
            df_agrupado,
            "ano_mes_str",
            "num_casos",
        )

        return plot.get_grafico_figure()

    @render_widget
    def grafico_linha_classificacao():
        df = df_filtrado().copy()

        df["ano"] = df["dataNotificacao"].dt.year
        df["mes"] = df["dataNotificacao"].dt.month

        df["ano_mes"] = df["dataNotificacao"].dt.to_period("M")

        df_agrupado = (
            df.groupby(["ano_mes", "classificacaoFinal"])
            .size()
            .reset_index(name="num_casos")
        )

        df_agrupado = df_agrupado.sort_values("ano_mes")
        df_agrupado["ano_mes_str"] = df_agrupado["ano_mes"].astype(str)
        plot = GraficoLinha(
            df_agrupado,
            eixo_x="ano_mes_str",
            eixo_y="num_casos",
            cor="classificacaoFinal",
        )

        return plot.get_grafico_figure()

    @render_widget
    def grafico_sintomas():
        df = df_filtrado()

        df = df[
            [
                "distúrbios olfativos",
                "distúrbios gustativos",
                "outros",
                "dor de garganta",
                "dor de cabeça",
                "dispneia",
                "febre",
                "tosse",
                "coriza",
                "dificuldade de respirar",
            ]
        ]

        df_sintomas = (
            df.sum(axis=0).sort_values(ascending=False).reset_index(name="contagem")
        )

        fig = GraficoBarra(
            dataframe=df_sintomas,
            eixo_x="contagem",
            eixo_y="index",
            hex_cores=["#4B6BD5"],
        )
        # plot_1.set_hover("<b>%{y}</b><br>Masculino: %{customdata[0]:,}<extra></extra>")
        # plot_1.set_nome("Masculino")

        return fig.get_grafico_figure()


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
