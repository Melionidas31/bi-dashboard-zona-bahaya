"""Halaman 3 — Analisis Korelasi."""

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

from config import (
    COLORS, ZONE_COLORS, ZONE_LABELS, COL_OUTPUT_Y,
    COL_INPUT_LABEL, PLOTLY_LAYOUT_DEFAULTS,
)
from data_loader import load_main_dataset, filter_dataset
from components.sidebar import make_filter_sidebar

dash.register_page(__name__, path="/korelasi", name="Korelasi", title="Analisis Korelasi — BI Dashboard")


df = load_main_dataset()

# Kolom numerik untuk korelasi (pakai Stability_Num, bukan huruf)
NUMERIC_COLS = [
    "Wind (m/s)", "Temp (C)", "Stability_Num",
    "Rate In (kL/jam)", "T_eff (menit)", "Thickness (mm)",
    "Zone Red (m)", "Zone orange (m)", "Zone yellow (m)",
]
NUMERIC_LABELS = {
    "Wind (m/s)":       "Wind",
    "Temp (C)":         "Temp",
    "Stability_Num":    "Stability",
    "Rate In (kL/jam)": "Rate In",
    "T_eff (menit)":    "T_eff",
    "Thickness (mm)":   "Thickness",
    "Zone Red (m)":     "Zona Merah",
    "Zone orange (m)":  "Zona Oranye",
    "Zone yellow (m)":  "Zona Kuning",
}


# ── CHART: Heatmap korelasi ─────────────────────────────────────────────────
def _heatmap_corr(dff):
    corr = dff[NUMERIC_COLS].corr()
    labels = [NUMERIC_LABELS[c] for c in corr.columns]

    fig = go.Figure(
        go.Heatmap(
            z=corr.values, x=labels, y=labels,
            colorscale="RdBu", zmin=-1, zmax=1,
            text=corr.round(2).values,
            texttemplate="%{text}",
            textfont=dict(size=11),
            colorbar=dict(title="r", thickness=12, len=0.7),
            hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>Korelasi: %{z:.3f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text="Matriks Korelasi Pearson antar Variabel",
                   font=dict(size=15, color=COLORS["text"])),
        xaxis=dict(side="bottom", tickangle=-30),
        yaxis=dict(autorange="reversed"),
        height=540, **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── CHART: Bar korelasi terhadap zona target ────────────────────────────────
def _corr_to_target(dff, target_col):
    feature_cols = ["Wind (m/s)", "Temp (C)", "Stability_Num",
                    "Rate In (kL/jam)", "T_eff (menit)", "Thickness (mm)"]
    corrs = dff[feature_cols + [target_col]].corr()[target_col].drop(target_col)
    corrs = corrs.sort_values()

    colors = [COLORS["red"] if v < 0 else COLORS["success"] for v in corrs.values]
    labels = [NUMERIC_LABELS[c] for c in corrs.index]

    fig = go.Figure(
        go.Bar(
            x=corrs.values, y=labels,
            orientation="h",
            marker_color=colors,
            text=corrs.round(3),
            textposition="outside",
            hovertemplate=f"<b>%{{y}}</b> vs {ZONE_LABELS[target_col]}<br>r = %{{x:.3f}}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text=f"Korelasi terhadap {ZONE_LABELS[target_col]}",
                   font=dict(size=13, color=COLORS["text"])),
        xaxis=dict(title="Koefisien Korelasi (r)", range=[-1, 1.15]),
        yaxis=dict(title=""),
        height=320, showlegend=False,
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    fig.add_vline(x=0, line=dict(color=COLORS["muted"], width=1, dash="dot"))
    return fig


# ── CHART: Scatter matrix ───────────────────────────────────────────────────
def _scatter_matrix(dff):
    cols = ["Rate In (kL/jam)", "T_eff (menit)", "Thickness (mm)", "Zone yellow (m)"]
    sub = dff[cols + ["Stability"]].copy()
    sub.columns = ["Rate In", "T_eff", "Thickness", "Zona Kuning", "Stability"]

    fig = px.scatter_matrix(
        sub, dimensions=["Rate In", "T_eff", "Thickness", "Zona Kuning"],
        color="Stability",
        color_discrete_map={"B": COLORS["red"], "D": COLORS["orange"], "F": COLORS["yellow"]},
        opacity=0.6,
    )
    fig.update_traces(diagonal_visible=False, marker=dict(size=4, line=dict(width=0)))
    fig.update_layout(
        title=dict(text="Scatter Matrix — Hubungan antar Parameter Kunci",
                   font=dict(size=15, color=COLORS["text"])),
        height=600, **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── LAYOUT ──────────────────────────────────────────────────────────────────
layout = dbc.Container(
    [
        html.Div(
            [
                html.H3("Analisis Korelasi", className="page-title"),
                html.P("Memetakan hubungan statistik antar parameter input dan target zona bahaya.",
                       className="page-subtitle"),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                # Sidebar filter
                dbc.Col(make_filter_sidebar("kor"), md=12, lg=3, className="mb-3"),

                dbc.Col(
                    [
                        # Heatmap
                        dbc.Card(
                            dbc.CardBody(dcc.Loading(
                                dcc.Graph(id="kor-heatmap", config={"displayModeBar": False}),
                                type="circle", color=COLORS["red"])),
                            className="shadow-sm mb-3",
                        ),

                        # 3 bar korelasi (Red/Orange/Yellow)
                        dbc.Row(
                            [
                                dbc.Col(dbc.Card(
                                    dbc.CardBody(dcc.Loading(
                                        dcc.Graph(id="kor-bar-red", config={"displayModeBar": False}))),
                                    className="shadow-sm h-100"), md=12, lg=4, className="mb-3"),
                                dbc.Col(dbc.Card(
                                    dbc.CardBody(dcc.Loading(
                                        dcc.Graph(id="kor-bar-orange", config={"displayModeBar": False}))),
                                    className="shadow-sm h-100"), md=12, lg=4, className="mb-3"),
                                dbc.Col(dbc.Card(
                                    dbc.CardBody(dcc.Loading(
                                        dcc.Graph(id="kor-bar-yellow", config={"displayModeBar": False}))),
                                    className="shadow-sm h-100"), md=12, lg=4, className="mb-3"),
                            ],
                            className="g-3",
                        ),

                        # Scatter matrix
                        dbc.Card(
                            dbc.CardBody(dcc.Loading(
                                dcc.Graph(id="kor-scatter", config={"displayModeBar": False}),
                                type="circle", color=COLORS["yellow"])),
                            className="shadow-sm mb-3",
                        ),

                        # Insight
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6([html.I(className="bi bi-lightbulb-fill me-2",
                                                    style={"color": COLORS["yellow"]}),
                                             "Interpretasi Korelasi"], className="fw-bold mb-3"),
                                    html.Ul(
                                        [
                                            html.Li(["Nilai korelasi mendekati ", html.B("+1"),
                                                     " atau ", html.B("-1"),
                                                     " menunjukkan hubungan linear yang kuat."]),
                                            html.Li(["Variabel ", html.B("T_eff dan Rate In"),
                                                     " biasanya memiliki korelasi positif tertinggi terhadap zona bahaya."]),
                                            html.Li(["Variabel ", html.B("Thickness"),
                                                     " cenderung berkorelasi negatif — semakin tebal, dispersi uap berkurang."]),
                                            html.Li(["Stabilitas atmosfer berkorelasi positif: kelas F (sangat stabil) menahan dispersi lebih jauh."]),
                                        ],
                                        className="mb-0",
                                    ),
                                ]
                            ),
                            className="shadow-sm border-start border-warning border-4 mb-3",
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
    Output("kor-heatmap", "figure"),
    Output("kor-bar-red", "figure"),
    Output("kor-bar-orange", "figure"),
    Output("kor-bar-yellow", "figure"),
    Output("kor-scatter", "figure"),
    Output("kor-filter-info", "children"),
    Input("kor-stability", "value"),
    Input("kor-wind", "value"),
    Input("kor-temp", "value"),
    Input("kor-rate", "value"),
)
def update_corr(stability, wind, temp, rate):
    dff = filter_dataset(df, stability=stability, wind_range=wind,
                         temp_range=temp, rate_range=rate)

    # Safety: jika data terlalu sedikit, korelasi bisa NaN
    if len(dff) < 3:
        empty = go.Figure().update_layout(annotations=[dict(
            text="Data terlalu sedikit untuk menghitung korelasi",
            x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=COLORS["muted"])
        )], **PLOTLY_LAYOUT_DEFAULTS)
        return empty, empty, empty, empty, empty, f"Hanya {len(dff)} skenario — perluas filter"

    info = f"Menampilkan {len(dff):,} dari {len(df):,} skenario"
    return (
        _heatmap_corr(dff),
        _corr_to_target(dff, "Zone Red (m)"),
        _corr_to_target(dff, "Zone orange (m)"),
        _corr_to_target(dff, "Zone yellow (m)"),
        _scatter_matrix(dff),
        info,
    )
