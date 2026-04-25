"""
Konfigurasi global Dashboard BI
- Tema warna Safety/Hazard
- Path data
- Metrik performa model (hardcoded dari laporan)
"""

from pathlib import Path

# ── PATH ────────────────────────────────────────────────────────────────────
# Semua data berada di dalam folder bi_dashboard/ agar self-contained
# (kompatibel dengan Render.com dan deployment lainnya)
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

DATA_MAIN_CSV = DATA_DIR / "simulasi_aloha.csv"
DATA_ROBUST_WIND = DATA_DIR / "robust_wind.csv"
DATA_ROBUST_TEMP = DATA_DIR / "robust_temp.csv"

# Gambar di-serve lewat assets/ oleh Dash (path statis, tidak perlu Path obj)
IMG_AKTUAL_VS_ANN = BASE_DIR / "assets" / "images" / "aktual_vs_ann.png"
IMG_AKTUAL_VS_MLR = BASE_DIR / "assets" / "images" / "aktual_vs_mlr.png"
IMG_LEARNING_ANN = BASE_DIR / "assets" / "images" / "kurva_learning_ann.png"
DIR_ROBUST_OUTPUT = BASE_DIR / "assets" / "images"


# ── TEMA WARNA (Safety/Hazard) ──────────────────────────────────────────────
COLORS = {
    "red":        "#DC3545",   # Zona Merah (Bahaya)
    "orange":     "#FD7E14",   # Zona Oranye (Awas)
    "yellow":     "#FFC107",   # Zona Kuning (Waspada)
    "bg":         "#F4F6F9",
    "card":       "#FFFFFF",
    "text":       "#212529",
    "muted":      "#6C757D",
    "success":    "#198754",
    "primary":    "#0D6EFD",
    "dark":       "#1F2937",
    "border":     "#E5E7EB",
}

ZONE_COLORS = {
    "Zone Red (m)":    COLORS["red"],
    "Zone orange (m)": COLORS["orange"],
    "Zone yellow (m)": COLORS["yellow"],
}

ZONE_LABELS = {
    "Zone Red (m)":    "Zona Merah (Bahaya)",
    "Zone orange (m)": "Zona Oranye (Awas)",
    "Zone yellow (m)": "Zona Kuning (Waspada)",
}

# Mapping warna model
MODEL_COLORS = {
    "MLR":           "#6C757D",   # abu-abu (baseline)
    "ANN":           "#DC3545",   # merah primer (model unggulan)
    "Random Forest": "#198754",   # hijau
}


# ── METRIK PERFORMA MODEL (dari laporan_bab4_fase4_6.md & notebook RF) ──────
# Sumber: ml_development_report/laporan_bab4_fase4_6.md & Fase3_RandomForest_claude.ipynb
MODEL_METRICS = {
    "MLR": {
        "Zona Merah":  {"MAE": 22.25, "RMSE": 27.17, "R2": 71.78},
        "Zona Oranye": {"MAE": 28.53, "RMSE": 34.73, "R2": 73.87},
        "Zona Kuning": {"MAE": 52.92, "RMSE": 64.36, "R2": 73.46},
    },
    "ANN": {
        "Zona Merah":  {"MAE": 1.82, "RMSE": 2.35, "R2": 99.79},
        "Zona Oranye": {"MAE": 2.69, "RMSE": 3.69, "R2": 99.70},
        "Zona Kuning": {"MAE": 4.51, "RMSE": 6.25, "R2": 99.75},
    },
    "Random Forest": {
        "Zona Merah":  {"MAE": 4.27,  "RMSE": 6.32,  "R2": 98.47},
        "Zona Oranye": {"MAE": 6.27,  "RMSE": 8.79,  "R2": 98.33},
        "Zona Kuning": {"MAE": 12.15, "RMSE": 17.31, "R2": 98.08},
    },
}


# ── KOLOM DATASET ───────────────────────────────────────────────────────────
COL_INPUT_X = [
    "Wind (m/s)", "Temp (C)", "Stability",
    "Rate In (kL/jam)", "T_eff (menit)", "Thickness (mm)",
]

COL_INPUT_LABEL = {
    "Wind (m/s)":       "Kecepatan Angin (m/s)",
    "Temp (C)":         "Suhu (°C)",
    "Stability":        "Stabilitas Atmosfer",
    "Rate In (kL/jam)": "Rate Pengisian (kL/jam)",
    "T_eff (menit)":    "Waktu Efektif Tumpahan (menit)",
    "Thickness (mm)":   "Ketebalan Tumpahan (mm)",
}

COL_OUTPUT_Y = ["Zone Red (m)", "Zone orange (m)", "Zone yellow (m)"]

# Mapping ordinal balik (untuk display)
STABILITY_LABELS = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F"}
STABILITY_MAP = {v: k for k, v in STABILITY_LABELS.items()}


# ── PLOTLY TEMPLATE ─────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_white"

PLOTLY_LAYOUT_DEFAULTS = dict(
    template=PLOTLY_TEMPLATE,
    font=dict(family="Inter, Segoe UI, sans-serif", size=12, color=COLORS["text"]),
    paper_bgcolor=COLORS["card"],
    plot_bgcolor=COLORS["card"],
    # Margin bawah dibuat lapang (b=95) supaya x-axis title tidak bertabrakan
    # dengan legend horizontal yang dipasang di bawah plot area.
    margin=dict(l=55, r=25, t=60, b=95),
)
