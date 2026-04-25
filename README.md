# Dashboard BI — Prediksi Zona Bahaya Dispersi Uap Bahan Bakar

Dashboard Business Intelligence untuk Tugas Akhir
**M. Zaki Ramdhan — NIM 102222050**

Dibuat dengan **Plotly Dash** + **Bootstrap 5** dengan tema *Safety/Hazard*.

---

## Fitur Dashboard

5 Halaman utama:

1. **Beranda** — Ringkasan eksekutif dengan KPI cards & chart utama
2. **Statistik Deskriptif** — Distribusi parameter input & target zona (interaktif dengan filter)
3. **Analisis Korelasi** — Heatmap & scatter matrix antar variabel
4. **Perbandingan Model** — MLR vs ANN vs Random Forest (MAE/RMSE/R²)
5. **Analisis Robustness** — Sensitivitas model & analisis OOD

Filter global pada halaman 2 & 3:
- Stabilitas atmosfer (B/D/F)
- Range kecepatan angin
- Range suhu
- Range rate pengisian

---

## Cara Menjalankan

### 1. Install dependencies

```bash
cd bi_dashboard
pip install -r requirements.txt
```

### 2. Jalankan dashboard

```bash
python app.py
```

### 3. Buka browser

```
http://localhost:8050
```

---

## Struktur Folder

```
bi_dashboard/
├── app.py                      # Entry point Dash
├── config.py                   # Tema, warna, metrik model
├── data_loader.py              # Loader CSV (cached)
├── requirements.txt            # Dependencies
├── README.md
│
├── assets/
│   ├── style.css               # Custom CSS hazard theme
│   └── images/                 # Chart hasil eksperimen (PNG)
│
├── pages/
│   ├── overview.py             # Halaman 1
│   ├── descriptive.py          # Halaman 2
│   ├── correlation.py          # Halaman 3
│   ├── model_comparison.py     # Halaman 4
│   └── robustness.py           # Halaman 5
│
└── components/
    ├── navbar.py               # Top navbar
    ├── sidebar.py              # Filter sidebar
    └── kpi_card.py             # KPI card component
```

---

## Sumber Data

Dashboard ini hanya **membaca** (read-only) file dari folder utama tugas akhir:

| File | Kegunaan |
|---|---|
| `../SIMULASI TUGAS AKHIR FIX.csv` | Dataset utama 1.215 skenario |
| `../tes robust/Hasil_Uji_Robust_wind.csv` | Sensitivity wind |
| `../tes robust/Hasil_Uji_Robust_temp.csv` | Sensitivity temp |
| `assets/images/*.png` | Chart hasil pre-generated |

Tidak ada model ML yang di-load — dashboard ini ringan & cepat.

---

## Tema Visual

Mengikuti warna semantik zona bahaya:

| Warna | Hex | Penggunaan |
|---|---|---|
| Merah | `#DC3545` | Zona Merah / accent utama |
| Oranye | `#FD7E14` | Zona Oranye |
| Kuning | `#FFC107` | Zona Kuning / highlight |
| Hijau | `#198754` | Indikator akurat / aman |
| Abu | `#6C757D` | Baseline / neutral |

---

## Catatan

- Dashboard ini **terpisah** dari `dashboard_app/` (Flask app yang melakukan prediksi). Keduanya bisa berjalan paralel di port berbeda (5000 vs 8050).
- Untuk mengganti port, edit baris terakhir di `app.py`.
- Filter sidebar di-cache via `@lru_cache` agar performant.
