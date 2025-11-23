"""Grafico de Pirâmide Etária"""

import math

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from model.tipo_grafico.barra import GraficoBarra
from model.grafico import Grafico
import locale
import platform

try:
    if platform.system() == "Windows":
        # Windows
        locale.setlocale(locale.LC_ALL, "Portuguese_Brazil")
    else:
        # Linux e sistemas unix
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
except locale.Error as e:
    # Erro, fallback default
    print("Locale not supported")
    locale.setlocale(locale.LC_ALL, "")


class GraficoPiramideEtaria(Grafico):
    """Cria um gráfico de pirâmide etária com duas barras.

    :param grafico_esquerda: Gráfico de barra da esquerda
    :type grafico_esquerda: GraficoBarra
    :param grafico_direita: Gráfico de barra da esquerda
    :type grafico_direita: GraficoBarra
    :param valor_maximo: Valor máximo da coluna
    :type valor_maximo: int
    """

    def __init__(
        self,
        grafico_esquerda: GraficoBarra,
        grafico_direita: GraficoBarra,
        valor_maximo: int,
    ):

        self.grafico = go.Figure()

        grafico_esquerda = grafico_esquerda.get_grafico_figure()
        grafico_direita = grafico_direita.get_grafico_figure()

        self.grafico.add_traces(grafico_esquerda.data)
        self.grafico.add_traces(grafico_direita.data)

        # Tickvals
        step_approx = 1000 * math.ceil(valor_maximo / 1000) / 4
        step_10 = 1000 * math.ceil(step_approx / 1000)
        tickvals_neg = [-i * step_10 for i in range(4, 0, -1)]
        tickvals_pos = [i * step_10 for i in range(1, 5)]
        tickvals = tickvals_neg + [0] + tickvals_pos

        # Cria os rótulos usando os valores absolutos e formatando com separador de milhar
        ticktext = [
            locale.format_string("%d", abs(int(x)), grouping=True) for x in tickvals
        ]

        self.__setup_grafico__()

        self.grafico.update_layout(
            barmode="overlay",
            xaxis=dict(
                range=[tickvals[0], tickvals[-1]],
                tickmode="array",
                tickvals=tickvals,
                ticktext=ticktext,  # Define os rótulos customizados
            ),
            barcornerradius=4,
        )

    def set_ordem(self, ordem: list):
        self.grafico.update_yaxes(categoryorder="array", categoryarray=ordem)
