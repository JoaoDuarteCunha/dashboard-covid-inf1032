"""Grafico Donut"""

from typing import Literal
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from model.grafico import Grafico


class GraficoDonut(Grafico):
    """Cria um gráfico de donut, com as configurações iniciais para a criação desse gráfico.
    :param dataframe: DataFrame com os dados para os eixos, cores, custom data e texto da barra
    :type dataframe: pd.DataFrame
    :param hole: Decimal que determina o tamanho do buraco no meio do donut
    :type hole: float
    :param values: Coluna com os valores do gráfico
    :type values: str
    :param names: Coluna com os nomes das partes do gráfico, funciona como label
    :type names: str
    :param cor: Coluna que empilha o gráfico, definindo se vão existir múltiplas cores, defaults to None
    :type cor: str, optional
    :param hex_cores: Codigo de cores das barras, podendo ser designadas com um dicionario ou em ordem com uma lista caso hajam multiplas cores/barras empilhadas, defaults to None
    :type hex_cores: list[str] | dict[str] | str | None, optional
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        hole: float,
        values: str,
        names: str,
        cor: str | None = None,
        hex_cores: list[str] | dict[str] | str | None = None,
        data_custom_hover: list[str] | str | None = None,
        ordem_categorias: dict[str] | None = None,
    ):
        """Construtor"""
        super().__init__(dataframe, cor, hex_cores)

        self.grafico = px.pie(
            self.dataframe,
            values=values,
            names=names,
            hole=hole,
            color=self.cor,
            color_discrete_map=self.hex_cores,
            hover_data=data_custom_hover,
            category_orders=ordem_categorias,
        )

        self.__setup_grafico__()

        self.grafico.update_layout(
            legend=dict(
                yanchor="middle",
                xanchor="center",
                bgcolor="rgba(0,0,0,0)",
            )
        )

    def remove_legenda(self):
        """Remove a legenda"""
        self.grafico.update_layout(showlegend=False)

    def set_hover(self, texto_hover: str):
        """Adiciona texto para quando o usuario passa o mouse por cima do grafico"""
        self.grafico.update_traces(
            hovertemplate=texto_hover,
        )

    def adiciona_texto_fora(
        self, posicao: Literal["inside", "outside"], texto: Literal["label", "percent"]
    ):
        """Adiciona texto para quando o usuario passa o mouse por cima do grafico"""
        self.grafico.update_traces(textinfo=texto, textposition=posicao)
