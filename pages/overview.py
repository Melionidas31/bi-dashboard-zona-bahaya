"""Halaman 1 — Beranda (Overview & KPI Utama)."""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from config import COLORS, ZONE_COLORS, ZONE_LABELS, PLOTLY_LAYOUT_DEFAULTS
from data_loader import load_main_dataset
from components.kpi_card import make_kpi_card

dash.register_page(__name__, path="/", name="Beranda", title="Beranda — BI Dashboard")


# ── DATA ────────────────────────────────────────────────────────────────────
df = load_main_dataset()

total_skenario = len(df)
mean_red    = df["Zone Red (m)"].mean()
mean_orange = df["Zone orange (m)"].mean()
mean_yellow = df["Zone yellow (m)"].mean()
max_yellow  = df["Zone yellow (m)"].max()


# ── CHART 1: Donut distribusi Stability ─────────────────────────────────────
def chart_stability_donut():
    counts = df["Stability"].value_counts().sort_index()
    stab_label = {"B": "B — Tidak Stabil", "D": "D — Netral", "F": "F — Sangat Stabil"}
    fig = go.Figure(
        go.Pie(
            labels=[stab_label.get(s, s) for s in counts.index],
            values=counts.values,
            hole=0.55,
            marker=dict(colors=[COLORS["red"], COLORS["orange"], COLORS["yellow"]],
                        line=dict(color="white", width=2)),
            textinfo="percent",
            textfont=dict(size=14, color="white"),
            hovertemplate="<b>%{label}</b><br>Jumlah: %{value} skenario<br>%{percent}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text="Distribusi Kelas Stabilitas Atmosfer", font=dict(size=14, color=COLORS["text"])),
        annotations=[dict(text=f"<b>{total_skenario}</b><br><span style='font-size:10px'>Skenario</span>",
                          x=0.5, y=0.5, font=dict(size=18, color=COLORS["dark"]),
                          showarrow=False)],
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        height=340,
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── CHART 2: Top 10 skenario zona kuning terbesar ───────────────────────────
def chart_top10_dangerous():
    top = df.nlargest(10, "Zone yellow (m)").copy()
    top["Label"] = (
        "Skenario #" + top["No"].astype(str)
        + " (Stab=" + top["Stability"]
        + ", T_eff=" + top["T_eff (menit)"].astype(str) + "m)"
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top["Label"], x=top["Zone Red (m)"], name="Zona Merah",
        orientation="h", marker_color=COLORS["red"],
        hovertemplate="<b>%{y}</b><br>Zona Merah: %{x:.0f} m<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=top["Label"], x=top["Zone orange (m)"] - top["Zone Red (m)"], name="Zona Oranye",
        orientation="h", marker_color=COLORS["orange"],
        hovertemplate="<b>%{y}</b><br>Δ Oranye: %{x:.0f} m<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=top["Label"], x=top["Zone yellow (m)"] - top["Zone orange (m)"], name="Zona Kuning",
        orientation="h", marker_color=COLORS["yellow"],
        hovertemplate="<b>%{y}</b><br>Δ Kuning: %{x:.0f} m<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Top 10 Skenario dengan Zona Kuning Terjauh", font=dict(size=14, color=COLORS["text"])),
        barmode="stack",
        xaxis_title="Jarak (meter)",
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5),
        height=440,
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── CHART 3: Tren rata-rata zona vs T_eff ───────────────────────────────────
def chart_zone_vs_teff():
    grp = df.groupby("T_eff (menit)")[["Zone Red (m)", "Zone orange (m)", "Zone yellow (m)"]].mean().reset_index()
    fig = go.Figure()
    for col in ["Zone Red (m)", "Zone orange (m)", "Zone yellow (m)"]:
        fig.add_trace(go.Scatter(
            x=grp["T_eff (menit)"], y=grp[col],
            mode="lines+markers",
            name=ZONE_LABELS[col],
            line=dict(color=ZONE_COLORS[col], width=3),
            marker=dict(size=9, line=dict(color="white", width=1.5)),
            hovertemplate=f"<b>{ZONE_LABELS[col]}</b><br>T_eff: %{{x}} menit<br>Rata-rata: %{{y:.1f}} m<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text="Tren Rata-rata Jarak Zona vs Waktu Efektif Tumpahan",
                   font=dict(size=14, color=COLORS["text"])),
        xaxis_title="T_eff (menit)",
        yaxis_title="Jarak Zona (meter)",
        legend=dict(orientation="h", yanchor="top", y=-0.28, xanchor="center", x=0.5),
        height=400,
        hovermode="x unified",
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── CHART 4: Distribusi zona max per Stability ──────────────────────────────
def chart_zone_by_stability():
    grp = df.groupby("Stability")[["Zone Red (m)", "Zone orange (m)", "Zone yellow (m)"]].mean().reset_index()
    fig = go.Figure()
    for col in ["Zone Red (m)", "Zone orange (m)", "Zone yellow (m)"]:
        fig.add_trace(go.Bar(
            x=grp["Stability"], y=grp[col],
            name=ZONE_LABELS[col],
            marker_color=ZONE_COLORS[col],
            text=grp[col].round(1),
            textposition="outside",
            hovertemplate=f"<b>{ZONE_LABELS[col]}</b><br>Stabilitas: %{{x}}<br>Rata-rata: %{{y:.1f}} m<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text="Rata-rata Zona Bahaya per Kelas Stabilitas",
                   font=dict(size=14, color=COLORS["text"])),
        xaxis_title="Kelas Stabilitas",
        yaxis_title="Rata-rata Jarak (meter)",
        barmode="group",
        legend=dict(orientation="h", yanchor="top", y=-0.28, xanchor="center", x=0.5),
        height=400,
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── LAYOUT ──────────────────────────────────────────────────────────────────
layout = dbc.Container(
    [
        # Header halaman
        html.Div(
            [
                html.H3("Ringkasan Eksekutif", className="page-title"),
                html.P(
                    "Tinjauan menyeluruh dataset simulasi ALOHA — 1.215 skenario overfill bahan bakar "
                    "yang dianalisis untuk memprediksi zona bahaya dispersi uap.",
                    className="page-subtitle",
                ),
            ],
            className="mb-4",
        ),

        # KPI Cards (5 cards)
        dbc.Row(
            [
                dbc.Col(make_kpi_card("Total Skenario Simulasi", f"{total_skenario:,}", "",
                                      COLORS["primary"], "bi-database-fill",
                                      "Hasil simulasi ALOHA"), md=12, lg=True, className="mb-3"),
                dbc.Col(make_kpi_card("Rata-rata Zona Merah", f"{mean_red:.1f}", "m",
                                      COLORS["red"], "bi-exclamation-octagon-fill",
                                      "Zona Bahaya"), md=6, lg=True, className="mb-3"),
                dbc.Col(make_kpi_card("Rata-rata Zona Oranye", f"{mean_orange:.1f}", "m",
                                      COLORS["orange"], "bi-exclamation-triangle-fill",
                                      "Zona Awas"), md=6, lg=True, className="mb-3"),
                dbc.Col(make_kpi_card("Rata-rata Zona Kuning", f"{mean_yellow:.1f}", "m",
                                      COLORS["yellow"], "bi-info-circle-fill",
                                      "Zona Waspada"), md=6, lg=True, className="mb-3"),
                dbc.Col(make_kpi_card("Skenario Terbahaya", f"{max_yellow:.0f}", "m",
                                      COLORS["dark"], "bi-fire",
                                      "Maksimum Zona Kuning"), md=6, lg=True, className="mb-3"),
            ],
            className="g-3",
        ),

        html.Br(),

        # Row 2: Donut + Top 10
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=chart_stability_donut(),
                                                       config={"displayModeBar": False})),
                                 className="shadow-sm h-100"), md=12, lg=4, className="mb-3"),
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=chart_top10_dangerous(),
                                                       config={"displayModeBar": False})),
                                 className="shadow-sm h-100"), md=12, lg=8, className="mb-3"),
            ],
            className="g-3",
        ),

        # Row 3: Trend & Stability bar
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=chart_zone_vs_teff(),
                                                       config={"displayModeBar": False})),
                                 className="shadow-sm h-100"), md=12, lg=6, className="mb-3"),
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=chart_zone_by_stability(),
                                                       config={"displayModeBar": False})),
                                 className="shadow-sm h-100"), md=12, lg=6, className="mb-3"),
            ],
            className="g-3",
        ),

        # Insight Box
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6([html.I(className="bi bi-lightbulb-fill me-2", style={"color": COLORS["yellow"]}),
                             "Wawasan Utama"], className="fw-bold mb-3"),
                    html.Ul(
                        [
                            html.Li([html.B("Stabilitas atmosfer F (sangat stabil)"),
                                     " menghasilkan zona bahaya rata-rata terjauh — kondisi ini menyebabkan uap terkumpul di permukaan."]),
                            html.Li([html.B("Waktu efektif tumpahan (T_eff)"),
                                     " adalah faktor dominan: semakin lama tumpahan, semakin jauh dispersi uap."]),
                            html.Li([html.B("Skenario terbahaya"),
                                     f" mencapai jangkauan {max_yellow:.0f} meter — perlu perimeter evakuasi minimum sejauh itu."]),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className="shadow-sm border-start border-warning border-4 mt-2",
        ),
    ],
    fluid=True,
    className="px-4 py-3",
)
