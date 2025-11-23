"""Super classe de graficos"""

import json
import plotly.graph_objects as go
import pandas as pd
from shiny import ui
import json
import plotly.io as pio
from shiny import ui
import inspect

# pull this straight from https://github.com/plotly/plotly.js/blob/master/build/ploticon.js
iconePlotlyCamera = {
    "path": "m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z",
    "width": 1024,
    "ascent": 896,
    "descent": 128,
}


class Grafico:
    """Gráfico vazio, classe contém os módulos úteis para diferentes tipos de gráficos"""

    def __init__(
        self,
        dataframe: pd.DataFrame,
        cor: str | None = None,
        hex_cores: list[str] | dict[str] | str | None = None,
        hover_name: str | None = None,
    ):
        """Cria um gráfico vazio"""
        self.grafico = None
        self.dataframe = dataframe
        self.cor = cor
        self.hex_cores = hex_cores
        self.hover_name = hover_name

    def __setup_grafico__(self):
        """Setup interno dos gráficos, útil para padronização global
        independentemente do tipo do gráfico plotado."""
        self.grafico.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            legend_title="",
            autosize=True,
            margin=dict(l=8, r=8, t=8, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.1,
                xanchor="center",
                x=0.5,
                title_text="",
            ),
        )

        self.grafico.update_yaxes(
            mirror=True,
            showline=True,
            gridcolor="lightgrey",
            tickformat=",",
        )  # talvez nao funcione com pie chart

        self.grafico.update_xaxes(tickformat=",")

    def set_eixo_x_as_categorico(self):
        """Modifica o eixo x de contínuo para categórico.
        Útil por exemplo quando há dados numéricos como anos em que
        o gráfico mostra os dados como 2021.5, 2022.5, etc."""
        self.grafico.update_xaxes(type="category")

    def set_eixo_y_as_percentual(self):
        """Modifica o eixo y para mostrar os dados como percentual"""
        self.grafico.update_yaxes(tickformat=".0%")
        self.grafico.update_yaxes(range=[0, None])

    def set_inverte_legenda(self):
        """Inverte a legenda"""
        self.grafico.update_layout(legend_traceorder="reversed")

    def remove_legenda(self):
        """Remove a legenda"""
        self.grafico.update_layout(coloraxis_showscale=False)

    def get_grafico_figure(self) -> go.Figure:
        """Retorna o gráfico com as modificações feitas pelo usuário pronto para renderização

        :return: Retorna o Gráfico
        :rtype: go.Figure
        """
        return self.grafico

    def add_linha_horizontal(
        self,
        ponto: int,
        line_color: str = "lightgray",
        dash: str = "solid",
        width: int = 2,
        nome: str = None,
    ):
        """Plota uma linha horizontal a partir do ponto indicado

        :param ponto: Recebe o ponto no qual a linha será plotada
        :type ponto: int
        """
        self.grafico.add_hline(
            y=ponto,
            line_width=width,
            line_color=line_color,
            line_dash=dash,
        )

        # Se tiver nome, cria uma trace "fantasma" só pra legenda
        if nome:
            self.grafico.add_scatter(
                x=[None],
                y=[None],
                mode="lines",
                line=dict(color=line_color, dash=dash, width=width),
                name=nome,
                showlegend=True,
            )

    def add_linha_vertical(self, ponto: int | None = 0):
        """Plota uma linha vertical a partir do ponto indicado

        :param ponto: _description_, defaults to 0
        :type ponto: int | None, optional
        """

        self.grafico.add_vline(x=ponto, line_width=2, line_color="lightgray")
