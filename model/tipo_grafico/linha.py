"""Grafico de Linha"""

import plotly.express as px
import pandas as pd

from model.grafico import Grafico


class GraficoLinha(Grafico):
    """Cria um gráfico de linhas, com as configurações iniciais para a criação desse gráfico.

    :param dataframe: DataFrame com os dados para os eixos, cores, custom data e texto da barra
    :type dataframe: pd.DataFrame
    :param eixo_x: Coluna com os dados do eixo X do gráfico
    :type eixo_x: str
    :param eixo_y: Coluna com os dados do eixo y do gráfico
    :type eixo_y: str
    :param cor: Coluna que adiciona diversas linhas ao grafico, definindo se vão existir múltiplas cores, defaults to None
    :type cor: str, optional
    :param hex_cores: Codigo de cores das linhas, podendo ser designadas com um dicionario ou em ordem com uma lista caso hajam multiplas cores/linhas, defaults to None
    :type hex_cores: list[str] | dict[str] | str | None, optional
    :param data_custom_hover: Colunas com dados adicionais para o hover do mouse no grafico, defaults to None
    :type data_custom_hover: str | list[str], optional
    :param ordem: A ordem das linhas na legenda, defaults to None
    :type ordem: dict[str], optional"""

    def __init__(
        self,
        dataframe: pd.DataFrame,
        eixo_x: str,
        eixo_y: str,
        markers: bool | None = False,
        cor: str | None = None,
        hex_cores: list[str] | dict[str] | str | None = None,
        data_custom_hover: list[str] | str | None = None,
        ordem: dict[str] | None = None,
    ):
        """Construtor"""
        super().__init__(dataframe, cor, hex_cores)

        self.grafico = px.line(
            self.dataframe,
            x=eixo_x,
            y=eixo_y,
            labels={eixo_x: "", eixo_y: ""},
            color=self.cor,
            color_discrete_map=self.hex_cores,
            custom_data=data_custom_hover,
            category_orders=ordem,
            markers=markers,
        )

        self.__setup_grafico__()

        self.grafico.update_xaxes(type="category")

    def set_hover(self, texto_hover: str):
        """Adiciona texto para quando o usuario passa o mouse por cima do grafico

        :param texto_hover: Texto para o hover
        :type texto_hover: str
        """
        self.grafico.update_traces(
            hovertemplate=texto_hover,
            line=dict(width=3),
            marker=dict(size=9),
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

    def set_as_percentual(self, eixo="x"):
        """Altera o eixo x para ser um eixo percentual"""

        tickvals = list(range(0, 101, 20))
        ticktext = [f"{val}%" for val in tickvals]

        # Update x-axis with tickvals and ticktext
        if eixo == "x":
            self.grafico.update_xaxes(tickvals=tickvals, ticktext=ticktext)
        else:
            self.grafico.update_yaxes(tickvals=tickvals, ticktext=ticktext)
