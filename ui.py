import faicons as fa

from shinywidgets import output_widget

from shiny import ui
from shared import df_tratado

idade_range = (
    df_tratado["idade"].min().item(),
    df_tratado["idade"].max().item(),
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
        ui.input_slider(
            "idade",
            "Idade",
            min=idade_range[0],
            max=idade_range[1],
            value=idade_range,
            post=" anos",
            step=1,
        ),
        ui.input_switch("permite_nulas", "Permitir idades nulas", value=True),
        ui.input_checkbox_group(
            "time",
            "Food service",
            ["Lunch", "Dinner"],
            selected=["Lunch", "Dinner"],
            inline=True,
        ),
        ui.input_action_button("reset", "Reset filter"),
        open="desktop",
    ),
    ui.layout_columns(
        ui.value_box(
            "Número de notificações",
            ui.output_ui("numero_notificacoes"),
            showcase=ICONS["user"],
        ),
        ui.value_box(
            "Average tip", ui.output_ui("average_tip"), showcase=ICONS["wallet"]
        ),
        ui.value_box(
            "Average bill",
            ui.output_ui("average_bill"),
            showcase=ICONS["currency-dollar"],
        ),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Tips data"), ui.output_data_frame("table"), full_screen=True
        ),
        ui.card(
            ui.card_header(
                "Total bill vs tip",
                ui.popover(
                    ICONS["ellipsis"],
                    ui.input_radio_buttons(
                        "scatter_color",
                        None,
                        ["none", "sex", "smoker", "day", "time"],
                        inline=True,
                    ),
                    title="Add a color variable",
                    placement="top",
                ),
                class_="d-flex justify-content-between align-items-center",
            ),
            output_widget("scatterplot"),
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
            output_widget("tip_perc"),
            full_screen=True,
        ),
        col_widths=[6, 6, 12],
    ),
    ui.include_css("styles.css"),
    title="Notificações COVID-19",
    fillable=True,
)
