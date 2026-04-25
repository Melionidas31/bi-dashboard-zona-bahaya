"""
Loader data untuk Dashboard BI
- Cached agar tidak re-read setiap callback
- Membaca CSV utama dan data robustness
"""

from functools import lru_cache
import pandas as pd

from config import (
    DATA_MAIN_CSV,
    DATA_ROBUST_WIND,
    DATA_ROBUST_TEMP,
    STABILITY_MAP,
)


@lru_cache(maxsize=1)
def load_main_dataset() -> pd.DataFrame:
    """Memuat dataset simulasi ALOHA utama (1.215 baris).

    Stability dipertahankan sebagai huruf (A-F) untuk display BI,
    tetapi juga ditambahkan kolom 'Stability_Num' untuk perhitungan korelasi.
    """
    df = pd.read_csv(DATA_MAIN_CSV, sep=";", encoding="latin1")

    # Normalisasi nama kolom (handle simbol derajat)
    expected_cols = [
        "No", "Wind (m/s)", "Temp (C)", "Stability",
        "Rate In (kL/jam)", "Rate in (m3/s)", "T_eff (menit)",
        "Thickness (mm)", "Volume (m3)", "Area(m2)",
        "Zone Red (m)", "Zone orange (m)", "Zone yellow (m)",
    ]
    if len(df.columns) == len(expected_cols):
        df.columns = expected_cols

    # Tambah kolom numerik untuk Stability (untuk korelasi)
    df["Stability_Num"] = df["Stability"].map(STABILITY_MAP)

    return df


@lru_cache(maxsize=1)
def load_robustness_wind() -> pd.DataFrame:
    """Data uji robustness variasi kecepatan angin.

    File memiliki 2 baris header info (skip), header sebenarnya di baris ke-3.
    """
    df = pd.read_csv(DATA_ROBUST_WIND, sep=";", encoding="latin1", skiprows=2)
    df.columns = [c.strip() for c in df.columns]
    return df.sort_values("Wind (m/s)").reset_index(drop=True)


@lru_cache(maxsize=1)
def load_robustness_temp() -> pd.DataFrame:
    """Data uji robustness variasi suhu."""
    df = pd.read_csv(DATA_ROBUST_TEMP, sep=";", encoding="latin1", skiprows=2)
    df.columns = [c.strip() for c in df.columns]
    return df.sort_values("Temp (C)").reset_index(drop=True)


def filter_dataset(df: pd.DataFrame,
                   stability: list = None,
                   wind_range: tuple = None,
                   temp_range: tuple = None,
                   rate_range: tuple = None) -> pd.DataFrame:
    """Apply filter sidebar ke dataset."""
    out = df.copy()
    if stability:
        out = out[out["Stability"].isin(stability)]
    if wind_range:
        out = out[(out["Wind (m/s)"] >= wind_range[0]) & (out["Wind (m/s)"] <= wind_range[1])]
    if temp_range:
        out = out[(out["Temp (C)"] >= temp_range[0]) & (out["Temp (C)"] <= temp_range[1])]
    if rate_range:
        out = out[(out["Rate In (kL/jam)"] >= rate_range[0]) & (out["Rate In (kL/jam)"] <= rate_range[1])]
    return out
