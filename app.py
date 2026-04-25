"""
Dashboard BI — Prediksi Zona Bahaya Dispersi Uap Bahan Bakar
Tugas Akhir M. Zaki Ramdhan (NIM 102222050)

Menjalankan:
    cd bi_dashboard
    pip install -r requirements.txt
    python app.py

Buka: http://localhost:8050
"""

import dash
from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

from components.navbar import make_navbar


app = Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
    title="Dashboard BI — Prediksi Zona Bahaya",
    suppress_callback_exceptions=True,
    update_title=None,
)

app.layout = html.Div(
    [
        make_navbar(),
        html.Main(
            page_container,
            className="bi-main-content",
        ),
        html.Footer(
            dbc.Container(
                [
                    html.Hr(className="my-2"),
                    html.Div(
                        [
                            html.Span("Dashboard BI Tugas Akhir © 2026 — M. Zaki Ramdhan (NIM 102222050)",
                                      className="text-muted small"),
                            html.Span(" | Dibangun dengan Plotly Dash",
                                      className="text-muted small"),
                        ],
                        className="text-center py-3",
                    ),
                ],
                fluid=True,
            ),
            className="bi-footer mt-4",
        ),
    ],
    className="bi-app",
)


server = app.server  # ekspos Flask server untuk gunicorn (Render.com)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    debug = os.environ.get("RENDER") is None  # debug=False di Render
    print("=" * 70)
    print(" DASHBOARD BI — PREDIKSI ZONA BAHAYA DISPERSI UAP BAHAN BAKAR")
    print(f" Buka di browser: http://localhost:{port}")
    print(" Tekan CTRL+C untuk menghentikan server")
    print("=" * 70)
    app.run(debug=debug, host="0.0.0.0", port=port)
