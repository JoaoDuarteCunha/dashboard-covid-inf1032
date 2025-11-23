"""Grafico de Barras"""

from typing import Literal
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from model.grafico import Grafico


class GraficoBarra(Grafico):
    """Cria um gráfico de barras, com as configurações iniciais para a criação desse gráfico.

    :param dataframe: DataFrame com os dados para os eixos, cores, custom data e texto da barra
    :type dataframe: pd.DataFrame
    :param eixo_x: Coluna com os dados do eixo X do gráfico
    :type eixo_x: str
    :param eixo_y: Coluna com os dados do eixo y do gráfico
    :type eixo_y: str
    :param cor: Coluna que empilha o gráfico, definindo se vão existir múltiplas cores, defaults to None
    :type cor: str, optional
    :param hex_cores: Codigo de cores das barras, podendo ser designadas com um dicionario ou em ordem com uma lista caso hajam multiplas cores/barras empilhadas, defaults to None
    :type hex_cores: list[str] | dict[str] | str | None, optional
    :param data_custom_hover: Colunas com dados adicionais para o hover do mouse no grafico, defaults to None
    :type data_custom_hover: str | list[str], optional
    :param ordem: A ordem das barras empilhadas, defaults to None
    :type ordem: dict[str], optional
    :param texto_barra: Coluna com valor que aparece dentro da barra, defaults to None
    :type texto_barra: str, optional
    :param orientacao: Orientacao do grafico, defaults to "h"
    :type orientacao: Literal["h", "v"], optional
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        eixo_x: str,
        eixo_y: str,
        cor: str | None = None,
        hex_cores: list[str] | dict[str] | str | None = None,
        texto_barra: str | None = None,
        orientacao: Literal["h", "v"] | None = "h",
        data_custom_hover: list[str] | str | None = None,
        ordem: dict[str] | None = None,
        bar_mode: Literal["group", "stack", "relative"] | None = "stack",
        template_texto: str | None = None,
    ):
        """Construtor"""
        super().__init__(dataframe, cor, hex_cores)

        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
        self.orientacao = orientacao

        bar_params = dict(
            x=eixo_x,
            y=eixo_y,
            orientation=orientacao,
            color=self.cor,
            labels={eixo_x: "", eixo_y: ""},
            category_orders=ordem,
            custom_data=data_custom_hover,
            text=texto_barra,
            barmode=bar_mode,
        )

        # Se for dict
        if isinstance(self.hex_cores, dict):
            # Passa para color_discrete_map
            bar_params["color_discrete_map"] = self.hex_cores
        elif isinstance(self.hex_cores, list):
            # Se for lista, passa color_discrete_sequence
            bar_params["color_discrete_sequence"] = self.hex_cores

        self.grafico = px.bar(self.dataframe, **bar_params)
        self.grafico.update_layout(
            yaxis=dict(tickformat="000"), xaxis=dict(tickformat="000")
        )

        self.grafico.update_layout(barcornerradius=4)

        # Adiciona linha vertical caso o grafico seja de barras horizontais
        if orientacao == "h":
            self.add_linha_vertical()

        self.__setup_grafico__()

    def set_hover(self, texto_hover: str):
        """Adiciona texto para quando o usuario passa o mouse por cima do grafico

        :param texto_hover: Texto para o hover
        :type texto_hover: str
        """
        self.grafico.update_traces(
            textposition="inside",
            hovertemplate=texto_hover,
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

    def add_linha(
        self,
        eixo_y: str,
        nome: str | None = None,
        cor: str | None = None,
        data_custom_hover: list[str] | None = None,
        texto_hover: str | None = None,
    ):
        """Adiciona uma linha no grafico de barras. A linha segue o mesmo eixo x ja definido anteriormente.

        :param eixo_y: Coluna com os dados do eixo y do gráfico
        :type eixo_y: _type_
        :param nome: Nome da linha na legenda, defaults to None
        :type nome: str, optional
        :param cor: Codigo Hex da cor da linha, defaults to None
        :type cor: str, optional
        :param data_custom_hover: Colunas com dados adicionais para o hover do mouse no grafico, defaults to None
        :type data_custom_hover: list[str], optional
        :param texto_hover: Texto do hover do mouse nos pontos da linha, defaults to None
        :type texto_hover: str, optional
        """
        customdata = None
        if data_custom_hover:
            customdata = self.dataframe[data_custom_hover].values

        self.grafico.add_trace(
            go.Scatter(
                x=self.dataframe[self.eixo_x],
                y=self.dataframe[eixo_y],
                mode="lines+markers",
                name=nome,
                line=dict(color=cor),
                marker=dict(size=9, color=cor, symbol="circle"),
                customdata=customdata,
                hovertemplate=texto_hover,
            )
        )

    def rotaciona_eixo_x(self, angulo: int):
        return self.grafico.update_xaxes(tickangle=angulo)

    def set_nome(self, nome: str):
        """Adiciona um nome para a legenda do grafico em casos de graficos sem cores/nao empilhados mas que necessitam de uma legenda.

        :param nome: Nome do grafico na legenda
        :type nome: str
        """
        self.grafico.update_traces(name=nome, showlegend=True)

    def ordena_eixo(self, sort: str, eixo: Literal["x", "y"] | None = "x"):
        if eixo == "x":
            self.grafico.update_layout(xaxis={"categoryorder": sort})
        else:
            self.grafico.update_layout(yaxis={"categoryorder": sort})

    def ordena_barras_empilhadas(self):
        if not self.cor:
            return

        valor_col = self.eixo_x if self.orientacao == "h" else self.eixo_y

        df_agg = self.dataframe.groupby(self.cor)[valor_col].sum().reset_index()

        df_agg = df_agg.sort_values(by=valor_col, ascending=False)
        ordem_lista = df_agg[self.cor].tolist()

        traces = list(self.grafico.data)
        sorted_traces = sorted(
            traces,
            key=lambda trace: (
                ordem_lista.index(trace.name)
                if trace.name in ordem_lista
                else float("inf")
            ),
        )

        self.grafico.data = tuple(sorted_traces)

    def ajusta_texto_barra(
        self, categoria_outside: str | None = None, coluna_categoria: str | None = None
    ):
        """Posiciona o texto 'outside' para categorias específicas, e 'inside' para as demais.

        :param categoria_outside: Categoria específica para a qual o texto será posicionado fora da barra.
        :type categoria_outside: str, optional
        :param coluna_categoria: Coluna do DataFrame que contém as categorias para aplicar a lógica.
        :type coluna_categoria: str, optional
        """
        if coluna_categoria is None:
            coluna_categoria = self.eixo_x

        # Caso não tenha uma categoria específica, todas as barras terão texto dentro
        if categoria_outside is None:
            text_positions = ["inside" for _ in self.dataframe[coluna_categoria]]
        else:
            # Verifica se as barras estão agrupadas ou empilhadas e decide onde colocar o texto
            text_positions = []
            for i, categoria in enumerate(self.dataframe[coluna_categoria]):
                # Coloca "outside" apenas para a categoria de interesse, ou quando há espaço suficiente
                if categoria == categoria_outside:
                    text_positions.append("outside")
                else:
                    # Coloca "inside" por padrão para todas as outras barras
                    text_positions.append("inside")

            # Verifica se há sobreposição e ajusta posições para as últimas barras
            max_position = len(text_positions) - 1
            if max_position > 0:
                for i in range(max_position, 0, -1):
                    if text_positions[i] == "outside" and (
                        text_positions[i - 1] == "outside"
                    ):
                        # Caso duas barras consecutivas sejam "outside", ajusta para "inside"
                        text_positions[i - 1] = "inside"

        # Atualiza as posições dos textos das barras
        self.grafico.update_traces(textposition=text_positions)

    def remove_legenda(self):
        self.grafico.update_layout(showlegend=False)
