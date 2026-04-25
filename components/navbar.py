"""Top navigation bar — bertema Safety/Hazard."""

import dash_bootstrap_components as dbc
from dash import html

from config import COLORS


def make_navbar():
    nav_items = [
        dbc.NavItem(dbc.NavLink("Beranda", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Statistik Deskriptif", href="/statistik", active="exact")),
        dbc.NavItem(dbc.NavLink("Analisis Korelasi", href="/korelasi", active="exact")),
        dbc.NavItem(dbc.NavLink("Perbandingan Model", href="/model", active="exact")),
        dbc.NavItem(dbc.NavLink("Analisis Robustness", href="/robustness", active="exact")),
    ]

    return dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.I(className="bi bi-shield-exclamation me-2",
                                           style={"fontSize": "1.5rem", "color": COLORS["yellow"]}),
                                    html.Div(
                                        [
                                            html.Span("Dashboard BI",
                                                      style={"fontWeight": "700", "fontSize": "1.05rem",
                                                             "color": "white", "letterSpacing": "0.3px"}),
                                            html.Br(),
                                            html.Span("Prediksi Zona Bahaya Dispersi Uap Bahan Bakar",
                                                      style={"fontSize": "0.72rem",
                                                             "color": "rgba(255,255,255,0.7)"}),
                                        ],
                                        className="d-inline-block align-middle",
                                    ),
                                ],
                                className="d-flex align-items-center",
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                    className="g-0 flex-grow-1",
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(nav_items, className="ms-auto", navbar=True, pills=True),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color=COLORS["dark"],
        dark=True,
        sticky="top",
        className="shadow-sm mb-0",
    )
