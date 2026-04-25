"""Halaman 4 — Perbandingan Model ML (MLR vs ANN vs Random Forest)."""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

from config import COLORS, MODEL_COLORS, MODEL_METRICS, PLOTLY_LAYOUT_DEFAULTS
from components.kpi_card import make_kpi_card

dash.register_page(__name__, path="/model", name="Model", title="Perbandingan Model — BI Dashboard")


# ── METRIK → DATAFRAME panjang ─────────────────────────────────────────────
def _metrics_to_df():
    rows = []
    for model, zones in MODEL_METRICS.items():
        for zone, metrics in zones.items():
            rows.append({
                "Model": model, "Zona": zone,
                "MAE": metrics["MAE"], "RMSE": metrics["RMSE"], "R2": metrics["R2"],
            })
    return pd.DataFrame(rows)


metrics_df = _metrics_to_df()


# ── CHART: Grouped bar MAE ──────────────────────────────────────────────────
def _bar_metric(metric: str, title: str, unit: str = "m"):
    fig = go.Figure()
    for model in metrics_df["Model"].unique():
        sub = metrics_df[metrics_df["Model"] == model]
        fig.add_trace(go.Bar(
            x=sub["Zona"], y=sub[metric], name=model,
            marker_color=MODEL_COLORS[model],
            text=sub[metric].round(2),
            textposition="outside",
            hovertemplate=f"<b>{model}</b><br>%{{x}}<br>{metric}: %{{y}} {unit}<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=COLORS["text"])),
        xaxis_title="Zona Bahaya",
        yaxis_title=f"{metric} ({unit})",
        barmode="group",
        legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5),
        height=380,
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── TABEL METRIK ────────────────────────────────────────────────────────────
def _metrics_table():
    rows = []
    for zone in ["Zona Merah", "Zona Oranye", "Zona Kuning"]:
        for model in ["MLR", "Random Forest", "ANN"]:
            m = MODEL_METRICS[model][zone]
            rows.append({
                "Zona": zone, "Model": model,
                "MAE (m)": m["MAE"], "RMSE (m)": m["RMSE"], "R² (%)": m["R2"],
            })

    header = html.Thead(html.Tr([
        html.Th("Zona"), html.Th("Model"),
        html.Th("MAE (m)", className="text-end"),
        html.Th("RMSE (m)", className="text-end"),
        html.Th("R² (%)", className="text-end"),
    ]))

    body_rows = []
    for r in rows:
        # Highlight ANN row hijau
        bg = "rgba(25, 135, 84, 0.08)" if r["Model"] == "ANN" else "transparent"
        body_rows.append(html.Tr(
            [
                html.Td(r["Zona"]),
                html.Td([
                    html.Span("●", style={"color": MODEL_COLORS[r["Model"]], "marginRight": "6px",
                                          "fontSize": "1.2rem"}),
                    r["Model"],
                ]),
                html.Td(f"{r['MAE (m)']:.2f}", className="text-end"),
                html.Td(f"{r['RMSE (m)']:.2f}", className="text-end"),
                html.Td(html.B(f"{r['R² (%)']:.2f}%"), className="text-end"),
            ],
            style={"backgroundColor": bg},
        ))

    return dbc.Table(
        [header, html.Tbody(body_rows)],
        bordered=False, hover=True, responsive=True, size="sm",
        className="mb-0",
    )


# ── LAYOUT ──────────────────────────────────────────────────────────────────
layout = dbc.Container(
    [
        html.Div(
            [
                html.H3("Perbandingan Model Machine Learning", className="page-title"),
                html.P(
                    "Evaluasi performa MLR (baseline), Random Forest, dan ANN — diuji pada 243 baris Test Dataset.",
                    className="page-subtitle",
                ),
            ],
            className="mb-4",
        ),

        # KPI Highlight (juara model)
        dbc.Row(
            [
                dbc.Col(make_kpi_card("Model Terbaik", "ANN", "",
                                      COLORS["red"], "bi-trophy-fill",
                                      "Akurasi tertinggi di semua zona"),
                        md=6, lg=3, className="mb-3"),
                dbc.Col(make_kpi_card("Akurasi ANN (R²)", "99.75", "%",
                                      COLORS["success"], "bi-check-circle-fill",
                                      "Rata-rata 3 zona"),
                        md=6, lg=3, className="mb-3"),
                dbc.Col(make_kpi_card("Pengurangan MAE", "12×", "lebih baik",
                                      COLORS["primary"], "bi-graph-down-arrow",
                                      "ANN vs MLR (Zona Merah)"),
                        md=6, lg=3, className="mb-3"),
                dbc.Col(make_kpi_card("Selisih Akurasi", "+26", "%",
                                      COLORS["orange"], "bi-arrow-up-circle-fill",
                                      "ANN vs MLR baseline"),
                        md=6, lg=3, className="mb-3"),
            ],
            className="g-3",
        ),

        html.Br(),

        # Bar charts (MAE, RMSE, R²)
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(
                    dcc.Graph(figure=_bar_metric("MAE", "MAE per Zona (semakin kecil = semakin akurat)"),
                              config={"displayModeBar": False})),
                    className="shadow-sm h-100"), md=12, lg=4, className="mb-3"),
                dbc.Col(dbc.Card(dbc.CardBody(
                    dcc.Graph(figure=_bar_metric("RMSE", "RMSE per Zona (semakin kecil = semakin akurat)"),
                              config={"displayModeBar": False})),
                    className="shadow-sm h-100"), md=12, lg=4, className="mb-3"),
                dbc.Col(dbc.Card(dbc.CardBody(
                    dcc.Graph(figure=_bar_metric("R2", "R² per Zona (semakin tinggi = semakin akurat)", unit="%"),
                              config={"displayModeBar": False})),
                    className="shadow-sm h-100"), md=12, lg=4, className="mb-3"),
            ],
            className="g-3",
        ),

        # Tabel metrik lengkap
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6([html.I(className="bi bi-table me-2"),
                             "Tabel Metrik Lengkap (Test Dataset, 243 sampel)"],
                            className="fw-bold mb-3"),
                    _metrics_table(),
                    html.Small(
                        "Baris hijau = ANN (model yang diusulkan & terbukti terbaik).",
                        className="text-muted mt-2 d-block",
                    ),
                ]
            ),
            className="shadow-sm mb-3",
        ),

        html.Br(),
        html.H5([html.I(className="bi bi-image me-2"), "Visualisasi Aktual vs Prediksi"],
                className="fw-bold mb-3"),

        # Embed gambar aktual vs prediksi
        dbc.Row(
            [
                dbc.Col(dbc.Card(
                    [
                        dbc.CardHeader([html.I(className="bi bi-graph-up-arrow me-2"),
                                        html.Span("ANN — Tebakan Mendekati Garis Ideal Y=X",
                                                  style={"fontWeight": "600"})]),
                        dbc.CardBody(html.Img(src="/assets/images/aktual_vs_ann.png",
                                              className="img-fluid rounded")),
                    ],
                    className="shadow-sm h-100"), md=12, lg=6, className="mb-3"),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardHeader([html.I(className="bi bi-graph-down-arrow me-2"),
                                        html.Span("MLR — Tebakan Tersebar & Bisa Bernilai Negatif",
                                                  style={"fontWeight": "600"})]),
                        dbc.CardBody(html.Img(src="/assets/images/aktual_vs_mlr.png",
                                              className="img-fluid rounded")),
                    ],
                    className="shadow-sm h-100"), md=12, lg=6, className="mb-3"),
            ],
            className="g-3",
        ),

        # Kurva Learning
        dbc.Card(
            [
                dbc.CardHeader([html.I(className="bi bi-activity me-2"),
                                html.Span("Kurva Pembelajaran ANN (500 Epochs)",
                                          style={"fontWeight": "600"})]),
                dbc.CardBody(
                    [
                        html.Img(src="/assets/images/kurva_learning_ann.png",
                                 className="img-fluid rounded mx-auto d-block",
                                 style={"maxHeight": "440px"}),
                        html.P(
                            "Loss training & validasi konvergen pada nilai sangat kecil — "
                            "indikasi model tidak overfitting maupun underfitting.",
                            className="text-muted mt-3 mb-0 text-center small",
                        ),
                    ]
                ),
            ],
            className="shadow-sm mb-3",
        ),

        # Insight
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6([html.I(className="bi bi-lightbulb-fill me-2",
                                    style={"color": COLORS["yellow"]}),
                             "Kesimpulan Komparasi Model"], className="fw-bold mb-3"),
                    html.Ul(
                        [
                            html.Li([html.B("ANN unggul mutlak"), " dengan R² > 99.7% di ketiga zona, sedangkan MLR mandek di ~73%."]),
                            html.Li([html.B("MLR menghasilkan prediksi negatif"), " (tidak masuk akal secara fisika) — bukti bahwa hubungan parameter bersifat non-linear."]),
                            html.Li([html.B("Random Forest"), " adalah alternatif yang baik (R² ~98%), tapi tetap tertinggal dari ANN."]),
                            html.Li([html.B("Rekomendasi:"), " Gunakan ANN sebagai model utama; MLR hanya sebagai baseline pembanding di laporan."]),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className="shadow-sm border-start border-success border-4 mb-3",
        ),
    ],
    fluid=True,
    className="px-4 py-3",
)
