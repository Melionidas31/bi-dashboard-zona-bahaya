"""Filter sidebar global (untuk halaman Statistik & Korelasi)."""

import dash_bootstrap_components as dbc
from dash import dcc, html


def make_filter_sidebar(prefix: str):
    """Buat filter sidebar.

    Args:
        prefix: prefix unik untuk ID component (misal 'stat' atau 'korelasi')
                supaya tidak konflik antar halaman.
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(
                    [html.I(className="bi bi-funnel-fill me-2"), "Filter Data"],
                    className="mb-3 fw-bold",
                ),

                html.Label("Stabilitas Atmosfer", className="filter-label"),
                dcc.Checklist(
                    id=f"{prefix}-stability",
                    options=[{"label": "  B (Tidak Stabil)", "value": "B"},
                             {"label": "  D (Netral)", "value": "D"},
                             {"label": "  F (Sangat Stabil)", "value": "F"}],
                    value=["B", "D", "F"],
                    className="mb-3",
                    inputClassName="form-check-input me-1",
                    labelStyle={"display": "block"},
                ),

                html.Label("Kecepatan Angin (m/s)", className="filter-label"),
                dcc.RangeSlider(
                    id=f"{prefix}-wind",
                    min=1.5, max=5.0, step=0.5, value=[1.5, 5.0],
                    marks={1.5: "1.5", 3.0: "3.0", 5.0: "5.0"},
                    tooltip={"placement": "bottom", "always_visible": False},
                    className="mb-4",
                ),

                html.Label("Suhu (°C)", className="filter-label"),
                dcc.RangeSlider(
                    id=f"{prefix}-temp",
                    min=25, max=30, step=1, value=[25, 30],
                    marks={25: "25", 27: "27", 30: "30"},
                    tooltip={"placement": "bottom", "always_visible": False},
                    className="mb-4",
                ),

                html.Label("Rate Pengisian (kL/jam)", className="filter-label"),
                dcc.RangeSlider(
                    id=f"{prefix}-rate",
                    min=250, max=550, step=50, value=[250, 550],
                    marks={250: "250", 400: "400", 550: "550"},
                    tooltip={"placement": "bottom", "always_visible": False},
                    className="mb-3",
                ),

                html.Hr(),
                html.Div(
                    id=f"{prefix}-filter-info",
                    className="text-muted small text-center",
                ),
            ]
        ),
        className="shadow-sm sticky-top",
        style={"top": "70px"},
    )
