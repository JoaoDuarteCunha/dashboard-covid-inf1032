"""Grafico de Área"""

from typing import Literal
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from model.grafico import Grafico


class GraficoArea(Grafico):

    def __init__(
        self,
        dataframe: pd.DataFrame,
        eixo_x: str,
        eixo_y: str | list[str],
        cor: str | None = None,
        hex_cores: list[str] | dict[str] | str | None = None,
        data_custom_hover: list[str] | str | None = None,
        ordem: dict[str] | None = None,
        markers: bool | None = False,
    ):
        """ "Construtor"""
        super().__init__(dataframe, cor, hex_cores)
        params = dict(
            x=eixo_x,
            y=eixo_y,
            category_orders=ordem,
            labels={eixo_x: "", eixo_y: ""},
            color=self.cor,
            custom_data=data_custom_hover,
            markers=markers,
        )

        # Se for dict
        if isinstance(self.hex_cores, dict):
            # Passa para color_discrete_map
            params["color_discrete_map"] = self.hex_cores
        elif isinstance(self.hex_cores, list):
            # Se for lista, passa color_discrete_sequence
            params["color_discrete_sequence"] = self.hex_cores

        self.grafico = px.area(self.dataframe, **params)
        self.__setup_grafico__()

        self.grafico.update_xaxes(type="category")

    def set_hover(self, texto_hover: str):
        """Adiciona texto para quando o usuario passa o mouse por cima do grafico

        :param texto_hover: Texto para o hover
        :type texto_hover: str
        """
        self.grafico.update_traces(
            hovertemplate=texto_hover,
            line=dict(width=2),
            marker=dict(size=6),
            mode="lines+markers",
        )

    def set_eixos(self, xaxis_title: str = "", yaxis_title: str = ""):
        """Define os títulos dos eixos X e Y

        :param xaxis_title: Nome do eixo X, defaults to ""
        :type xaxis_title: str, optional
        :param yaxis_title: Nome do eixo Y, defaults to ""
        :type yaxis_title: str, optional
        """
        self.grafico.update_layout(
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
        )

    def add_grafico_linha(self, eixo_x, eixo_y, nome):
        self.grafico.add_trace(
            go.Scatter(
                x=self.dataframe[eixo_x],
                y=self.dataframe[eixo_y],
                mode="lines",
                name=nome,
                line=dict(color="red", width=2, dash="dash"),
                marker=dict(size=0),
                hovertemplate=" %{y}<br>" + "<extra></extra>",
            )
        )

    def adiciona_legenda(self, nome):
        self.grafico.update_traces(name=nome, showlegend=True)
