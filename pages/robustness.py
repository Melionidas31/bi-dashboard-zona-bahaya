"""Halaman 5 — Analisis Robustness & Sensitivitas."""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from config import COLORS, ZONE_COLORS, ZONE_LABELS, COL_OUTPUT_Y, PLOTLY_LAYOUT_DEFAULTS
from data_loader import load_robustness_wind, load_robustness_temp

dash.register_page(__name__, path="/robustness", name="Robustness", title="Analisis Robustness — BI Dashboard")


df_wind = load_robustness_wind()
df_temp = load_robustness_temp()


# ── CHART: Sensitivity vs Wind ──────────────────────────────────────────────
def chart_sensitivity_wind():
    fig = go.Figure()
    for col in COL_OUTPUT_Y:
        fig.add_trace(go.Scatter(
            x=df_wind["Wind (m/s)"], y=df_wind[col],
            mode="lines+markers",
            name=ZONE_LABELS[col],
            line=dict(color=ZONE_COLORS[col], width=3),
            marker=dict(size=8, line=dict(color="white", width=1.5)),
            hovertemplate=f"<b>{ZONE_LABELS[col]}</b><br>Wind: %{{x}} m/s<br>Prediksi: %{{y:.1f}} m<extra></extra>",
        ))

    # Garis vertikal di range training (1.5–5.0)
    fig.add_vrect(
        x0=1.5, x1=5.0,
        fillcolor=COLORS["success"], opacity=0.08,
        line=dict(width=0),
        annotation_text="Range Training (In-Distribution)",
        annotation_position="top left",
        annotation_font=dict(size=10, color=COLORS["success"]),
    )

    fig.update_layout(
        title=dict(text="Sensitivitas Model terhadap Variasi Kecepatan Angin",
                   font=dict(size=14, color=COLORS["text"])),
        xaxis_title="Kecepatan Angin (m/s)",
        yaxis_title="Prediksi Jarak Zona (meter)",
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5),
        height=420,
        hovermode="x unified",
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── CHART: Sensitivity vs Temp ──────────────────────────────────────────────
def chart_sensitivity_temp():
    fig = go.Figure()
    for col in COL_OUTPUT_Y:
        fig.add_trace(go.Scatter(
            x=df_temp["Temp (C)"], y=df_temp[col],
            mode="lines+markers",
            name=ZONE_LABELS[col],
            line=dict(color=ZONE_COLORS[col], width=3),
            marker=dict(size=8, line=dict(color="white", width=1.5)),
            hovertemplate=f"<b>{ZONE_LABELS[col]}</b><br>Temp: %{{x}} °C<br>Prediksi: %{{y:.1f}} m<extra></extra>",
        ))

    fig.add_vrect(
        x0=25, x1=30,
        fillcolor=COLORS["success"], opacity=0.08,
        line=dict(width=0),
        annotation_text="Range Training (In-Distribution)",
        annotation_position="top left",
        annotation_font=dict(size=10, color=COLORS["success"]),
    )

    fig.update_layout(
        title=dict(text="Sensitivitas Model terhadap Variasi Suhu",
                   font=dict(size=14, color=COLORS["text"])),
        xaxis_title="Suhu (°C)",
        yaxis_title="Prediksi Jarak Zona (meter)",
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5),
        height=420,
        hovermode="x unified",
        **PLOTLY_LAYOUT_DEFAULTS,
    )
    return fig


# ── KOMPONEN GAMBAR ────────────────────────────────────────────────────────
def _image_card(src: str, title: str, subtitle: str = "", icon: str = "bi-image"):
    return dbc.Card(
        [
            dbc.CardHeader([html.I(className=f"bi {icon} me-2"),
                            html.Span(title, style={"fontWeight": "600"})]),
            dbc.CardBody(
                [
                    html.Img(src=src, className="img-fluid rounded mx-auto d-block"),
                    html.P(subtitle, className="text-muted small mt-3 mb-0 text-center")
                    if subtitle else None,
                ]
            ),
        ],
        className="shadow-sm h-100",
    )


# ── LAYOUT ──────────────────────────────────────────────────────────────────
layout = dbc.Container(
    [
        html.Div(
            [
                html.H3("Analisis Robustness Model", className="page-title"),
                html.P(
                    "Pengujian seberapa stabil prediksi model ketika input divariasikan, termasuk skenario di luar "
                    "rentang training (Out-of-Distribution).",
                    className="page-subtitle",
                ),
            ],
            className="mb-4",
        ),

        # Sensitivity charts (interactive)
        html.H5([html.I(className="bi bi-sliders me-2"), "Sensitivity Analysis"],
                className="fw-bold mb-3"),

        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(
                    dcc.Graph(figure=chart_sensitivity_wind(), config={"displayModeBar": False})),
                    className="shadow-sm h-100"), md=12, lg=6, className="mb-3"),
                dbc.Col(dbc.Card(dbc.CardBody(
                    dcc.Graph(figure=chart_sensitivity_temp(), config={"displayModeBar": False})),
                    className="shadow-sm h-100"), md=12, lg=6, className="mb-3"),
            ],
            className="g-3",
        ),

        # Insight singkat
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6([html.I(className="bi bi-info-circle-fill me-2",
                                    style={"color": COLORS["primary"]}),
                             "Cara Membaca Sensitivity Chart"], className="fw-bold mb-3"),
                    html.P(
                        ["Area hijau adalah ", html.B("rentang training"), " (In-Distribution). "
                         "Di luar area ini, model masuk zona ", html.B("Out-of-Distribution (OOD)"),
                         " — prediksi cenderung kurang akurat. Garis horizontal datar menandakan model gagal "
                         "menangkap variasi parameter (kasus OOD ekstrim)."],
                        className="mb-0",
                    ),
                ]
            ),
            className="shadow-sm border-start border-primary border-4 mb-4",
        ),

        # Heatmap MAE ID vs OOD
        html.H5([html.I(className="bi bi-grid-3x3-gap-fill me-2"),
                 "Perbandingan Error: In-Distribution vs Out-of-Distribution"],
                className="fw-bold mb-3"),

        dbc.Row(
            [
                dbc.Col(_image_card(
                    "/assets/images/heatmap_mae_id.png",
                    "Heatmap MAE — In-Distribution (ID)",
                    "Error model di rentang training. Semakin gelap = error semakin besar.",
                    icon="bi-grid-3x3-gap"),
                    md=12, lg=6, className="mb-3"),
                dbc.Col(_image_card(
                    "/assets/images/heatmap_mae_ood.png",
                    "Heatmap MAE — Out-of-Distribution (OOD)",
                    "Error saat input ekstrim. Memperlihatkan limit ekstrapolasi model.",
                    icon="bi-grid-3x3-gap"),
                    md=12, lg=6, className="mb-3"),
            ],
            className="g-3",
        ),

        # Scatter ANN/MLR vs ALOHA
        html.H5([html.I(className="bi bi-scatter-chart me-2"),
                 "Akurasi Prediksi Model vs Simulasi ALOHA"],
                className="fw-bold mb-3"),

        dbc.Row(
            [
                dbc.Col(_image_card(
                    "/assets/images/scatter_ann_vs_aloha.png",
                    "ANN vs ALOHA — Korelasi Sangat Kuat",
                    "Titik berhimpit dengan garis ideal Y=X (R² ≈ 99.7%)",
                    icon="bi-check-circle"),
                    md=12, lg=6, className="mb-3"),
                dbc.Col(_image_card(
                    "/assets/images/scatter_mlr_vs_aloha.png",
                    "MLR vs ALOHA — Penyebaran Lebar",
                    "Banyak titik menyimpang jauh; bahkan terdapat prediksi bernilai negatif",
                    icon="bi-x-circle"),
                    md=12, lg=6, className="mb-3"),
            ],
            className="g-3",
        ),

        # Degradasi & MPE
        dbc.Row(
            [
                dbc.Col(_image_card(
                    "/assets/images/degradasi_ood_ratio.png",
                    "Rasio Degradasi Akurasi (OOD vs ID)",
                    "Berapa kali lipat error meningkat saat model menerima input di luar training",
                    icon="bi-graph-down"),
                    md=12, lg=6, className="mb-3"),
                dbc.Col(_image_card(
                    "/assets/images/mpe_comparison.png",
                    "Mean Percentage Error (MPE) — Komparasi Model",
                    "Persentase kesalahan rata-rata: ANN secara konsisten paling presisi",
                    icon="bi-percent"),
                    md=12, lg=6, className="mb-3"),
            ],
            className="g-3",
        ),

        # Kesimpulan
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6([html.I(className="bi bi-shield-check me-2",
                                    style={"color": COLORS["success"]}),
                             "Kesimpulan Robustness"], className="fw-bold mb-3"),
                    html.Ul(
                        [
                            html.Li([html.B("ANN robust di dalam range training"),
                                     " — error tetap kecil (< 5 m) di seluruh skenario ID."]),
                            html.Li([html.B("Degradasi OOD wajar"),
                                     " — error meningkat signifikan jika input keluar dari rentang training; ini batasan inherent semua model ML."]),
                            html.Li([html.B("Implikasi praktis:"),
                                     " jangan gunakan model untuk skenario di luar batas (Wind > 5 m/s, Temp > 30°C, dll) tanpa retraining."]),
                            html.Li([html.B("MLR tidak robust"),
                                     " bahkan di range training — error baseline sudah tinggi."]),
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
