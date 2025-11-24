import faicons as fa

from shinywidgets import output_widget

from shiny import ui
from shared import df_tratado

idade_range = (
    df_tratado["idade"].min().item(),
    df_tratado["idade"].max().item(),
)
raca_cor_lista = df_tratado["racaCor"].unique().tolist()
sexo_lista = df_tratado["sexo"].unique().tolist()
municipio_lista = df_tratado["municipio"].unique().tolist()
classificacao_final_lista = df_tratado["classificacaoFinal"].unique().tolist()
data_range = (
    df_tratado["dataNotificacao"].min(),
    df_tratado["dataNotificacao"].max(),
)

ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "wallet": fa.icon_svg("wallet"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "ellipsis": fa.icon_svg("ellipsis"),
}

# Add page title and sidebar
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_date_range(
            "data",
            "Data",
            start=data_range[0],
            end=data_range[1],
            min=data_range[0],
            max=data_range[1],
        ),
        ui.input_switch("permite_nulas_data", "Permitir datas nulas", value=True),
        ui.input_slider(
            "idade",
            "Idade",
            min=idade_range[0],
            max=idade_range[1],
            value=idade_range,
            post=" anos",
            step=1,
        ),
        ui.input_switch("permite_nulas_idade", "Permitir idades nulas", value=True),
        ui.input_checkbox_group(
            "racaCor",
            "Raça/Cor",
            raca_cor_lista,
            selected=raca_cor_lista,
            inline=True,
        ),
        ui.input_checkbox_group(
            "sexo",
            "Sexo",
            sexo_lista,
            selected=sexo_lista,
            inline=True,
        ),
        ui.input_selectize(
            "municipio",
            "Município",
            choices=municipio_lista,
            multiple=True,
        ),
        ui.input_selectize(
            "classificacaoFinal",
            "Classificação Final",
            choices=classificacao_final_lista,
            multiple=True,
        ),
        ui.input_action_button("reset", "Limpar filtro"),
        open="desktop",
    ),
    ui.layout_columns(
        ui.value_box(
            "Número de notificações",
            ui.output_ui("numero_notificacoes"),
            showcase=ICONS["user"],
        ),
        ui.value_box(
            "Porcentagem de notificações positivas",
            ui.output_ui("porcentagem_notificacoes_positivas"),
            showcase=ICONS["wallet"],
        ),
        ui.value_box(
            "Idade média",
            ui.output_ui("idade_media"),
            showcase=ICONS["currency-dollar"],
        ),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Dados de Notificação"),
            ui.output_data_frame("table"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header(
                "Pirâmide Etária",
            ),
            output_widget(
                "grafico_piramide_etaria",
            ),
            full_screen=True,
        ),
        ui.card(
            ui.card_header(
                "Tip percentages",
                ui.popover(
                    ICONS["ellipsis"],
                    ui.input_radio_buttons(
                        "tip_perc_y",
                        "Split by:",
                        ["sex", "smoker", "day", "time"],
                        selected="day",
                        inline=True,
                    ),
                    title="Add a color variable",
                ),
                class_="d-flex justify-content-between align-items-center",
            ),
            output_widget("grafico_linha_classificacao"),
            output_widget("grafico_numero_casos"),
            full_screen=True,
        ),
        col_widths=[6, 6, 12],
    ),
    ui.include_css("styles.css"),
    title="Notificações COVID-19",
    fillable=True,
)
