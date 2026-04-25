"""Reusable KPI card dengan border-left berwarna."""

import dash_bootstrap_components as dbc
from dash import html

from config import COLORS


def make_kpi_card(title: str, value: str, unit: str = "", color: str = COLORS["primary"],
                  icon: str = "bi-bar-chart-fill", subtitle: str = ""):
    """Buat satu KPI card.

    Args:
        title:    judul kecil di atas
        value:    angka utama
        unit:     satuan (m, %, dll)
        color:    warna accent border-left
        icon:     bootstrap icon class
        subtitle: keterangan kecil di bawah
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(title, className="kpi-title"),
                                html.Div(
                                    [
                                        html.Span(value, className="kpi-value"),
                                        html.Span(unit, className="kpi-unit ms-1"),
                                    ]
                                ),
                                html.Div(subtitle, className="kpi-subtitle") if subtitle else None,
                            ],
                            className="flex-grow-1",
                        ),
                        html.Div(
                            html.I(className=f"bi {icon}", style={"fontSize": "2rem", "color": color, "opacity": 0.7}),
                            className="ms-2",
                        ),
                    ],
                    className="d-flex align-items-center justify-content-between",
                ),
            ],
        ),
        className="kpi-card shadow-sm h-100",
        style={"borderLeft": f"4px solid {color}"},
    )
