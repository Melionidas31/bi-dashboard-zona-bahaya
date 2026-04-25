"""Halaman 2 — Statistik Deskriptif."""

import dash
from dash import html, dcc, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import (
    COLORS, ZONE_COLORS, ZONE_LABELS,
    COL_INPUT_X, COL_INPUT_LABEL, COL_OUTPUT_Y,
    PLOTLY_LAYOUT_DEFAULTS,
)
from data_loader import load_main_dataset, filter_dataset
from components.sidebar import make_filter_sidebar

dash.register_page(__name__, path="/statistik", name="Statistik", title="Statistik Deskriptif — BI Dashboard")


df = load_main_dataset()


# ── HELPER: Build figures ───────────────────────────────────────────────────
def _input_histograms(dff):
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=[COL_INPUT_LABEL[c] for c in COL_INPUT_X],
        horizontal_spacing=0.08, vertical_spacing=0.18,
    )
    palette = ["#0D6EFD", "#6F42C1", "#198754", COLORS["red"], COLORS["orange"], "#20C997"]
    for i, col in enumerate(COL_INPUT_X):
        r, c = (i // 3) + 1, (i % 3) + 1
        fig.add_trace(
            go.Histogram(x=dff[col], marker_color=palette[i], opacity=0.85,
                         marker_line=dict(color="white", width=1),
                         hovertemplate=f"{col}: %{{x}}<br>Frekuensi: %{{y}}<extra></extra>"),
            row=r, col=c,
        )
    fig.update_layout(
        title=dict(text="Distribusi 6 Parameter Input (X)", font=dict(size=15, color=COLORS["text"])),
        showlegend=False, height=520, **PLOTLY_LAYOUT_DEFAULTS,
    )
    fig.update_annotations(font_size=11)
    return fig


def _output_histograms(dff):
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=[ZONE_LABELS[c] for c in COL_OUTPUT_Y],
        horizontal_spacing=0.08,
    )
    for i, col in enumerate(COL_OUTPUT_Y):
        fig.add_trace(
            go.Histogram(x=dff[col], marker_color=ZONE_COLORS[col], opacity=0.85,
                         marker_line=dict(color="white", width=1),
                         hovertemplate=f"{ZONE_LABELS[col]}: %{{x}} m<br>Frekuensi: %{{y}}<extra></extra>"),
            row=1, col=i + 1,
        )
        fig.update_xaxes(title_text="Jarak (meter)", row=1, col=i + 1)
    fig.update_layout(
        title=dict(text="Distribusi Target Zona Bahaya (Y)", font=dict(size=15, color=COLORS["text"])),
        showlegend=False, height=380, **PLOTLY_LAYOUT_DEFAULTS,
    )
    fig.update_annotations(font_size=11)
    return fig


def _boxplot_by_stability(dff):
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=[ZONE_LABELS[c] for c in COL_OUTPUT_Y],
        horizontal_spacing=0.08,
    )
    for i, col in enumerate(COL_OUTPUT_Y):
        for stab in sorted(dff["Stability"].unique()):
            sub = dff[dff["Stability"] == stab]
            fig.add_trace(
                go.Box(y=sub[col], name=stab, marker_color=ZONE_COLORS[col],
                       boxmean=True, opacity=0.7,
                       hovertemplate=f"Stabilitas {stab}<br>{ZONE_LABELS[col]}: %{{y}} m<extra></extra>"),
                row=1, col=i + 1,
            )
        fig.update_xaxes(title_text="Stabilitas", row=1, col=i + 1)
        fig.update_yaxes(title_text="Jarak (m)", row=1, col=i + 1)
    fig.update_layout(
        title=dict(text="Boxplot Zona Bahaya per Kelas Stabilitas",
                   font=dict(size=15, color=COLORS["text"])),
        showlegend=False, height=420, **PLOTLY_LAYOUT_DEFAULTS,
    )
    fig.update_annotations(font_size=11)
    return fig


def _summary_table_data(dff):
    cols_to_describe = COL_INPUT_X[:2] + COL_INPUT_X[3:] + COL_OUTPUT_Y  # skip Stability (string)
    desc = dff[cols_to_describe].describe().T.round(2)
    desc.insert(0, "Variabel", desc.index)
    desc = desc.rename(columns={
        "count": "N", "mean": "Mean", "std": "Std Dev",
        "min": "Min", "25%": "Q1", "50%": "Median", "75%": "Q3", "max": "Max",
    })
    return desc.to_dict("records")


# ── LAYOUT ──────────────────────────────────────────────────────────────────
layout = dbc.Container(
    [
        html.Div(
            [
                html.H3("Statistik Deskriptif", className="page-title"),
                html.P("Distribusi parameter input dan target zona bahaya — dengan filter interaktif.",
                       className="page-subtitle"),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                # Sidebar filter
                dbc.Col(make_filter_sidebar("stat"), md=12, lg=3, className="mb-3"),

                # Konten utama
                dbc.Col(
                    [
                        # Histogram input
                        dbc.Card(
                            dbc.CardBody(dcc.Loading(
                                dcc.Graph(id="stat-fig-input", config={"displayModeBar": False}),
                                type="circle", color=COLORS["red"])),
                            className="shadow-sm mb-3",
                        ),

                        # Histogram output Y
                        dbc.Card(
                            dbc.CardBody(dcc.Loading(
                                dcc.Graph(id="stat-fig-output", config={"displayModeBar": False}),
                                type="circle", color=COLORS["orange"])),
                            className="shadow-sm mb-3",
                        ),

                        # Boxplot
                        dbc.Card(
                            dbc.CardBody(dcc.Loading(
                                dcc.Graph(id="stat-fig-box", config={"displayModeBar": False}),
                                type="circle", color=COLORS["yellow"])),
                            className="shadow-sm mb-3",
                        ),

                        # Tabel ringkasan
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6([html.I(className="bi bi-table me-2"),
                                             "Ringkasan Statistik"],
                                            className="fw-bold mb-3"),
                                    dash_table.DataTable(
                                        id="stat-table-summary",
                                        page_size=10,
                                        style_table={"overflowX": "auto"},
                                        style_cell={
                                            "fontFamily": "Inter, Segoe UI, sans-serif",
                                            "fontSize": "13px", "padding": "10px",
                                            "textAlign": "right",
                                        },
                                        style_cell_conditional=[
                                            {"if": {"column_id": "Variabel"},
                                             "textAlign": "left", "fontWeight": "600"},
                                        ],
                                        style_header={
                                            "backgroundColor": COLORS["dark"],
                                            "color": "white",
                                            "fontWeight": "700",
                                            "border": "none",
                                        },
                                        style_data={"border": f"1px solid {COLORS['border']}"},
                                    ),
                                ]
                            ),
                            className="shadow-sm mb-3",
                        ),
                    ],
                    md=12, lg=9,
                ),
            ],
            className="g-3",
        ),
    ],
    fluid=True,
    className="px-4 py-3",
)


# ── CALLBACK ────────────────────────────────────────────────────────────────
@callback(
    Output("stat-fig-input", "figure"),
    Output("stat-fig-output", "figure"),
    Output("stat-fig-box", "figure"),
    Output("stat-table-summary", "data"),
    Output("stat-table-summary", "columns"),
    Output("stat-filter-info", "children"),
    Input("stat-stability", "value"),
    Input("stat-wind", "value"),
    Input("stat-temp", "value"),
    Input("stat-rate", "value"),
)
def update_descriptive(stability, wind, temp, rate):
    dff = filter_dataset(df, stability=stability, wind_range=wind,
                         temp_range=temp, rate_range=rate)

    summary_data = _summary_table_data(dff)
    columns = [{"name": c, "id": c} for c in summary_data[0].keys()] if summary_data else []

    info = f"Menampilkan {len(dff):,} dari {len(df):,} skenario"

    return (
        _input_histograms(dff),
        _output_histograms(dff),
        _boxplot_by_stability(dff),
        summary_data,
        columns,
        info,
    )
