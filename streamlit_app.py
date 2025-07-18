# Jalankan aplikasi dengan perintah `streamlit run filename.py`

import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu

# --- Konstanta Global ---
R = 8.314 # Konstanta gas ideal

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="ThermoCalc Lab",
    page_icon="🧪", # Menggunakan emoji sebagai ikon halaman
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Define Color Palettes (Tema Neon Gelap) ---
# Variabel CSS untuk Tema Neon Gelap
DARK_THEME_COLORS = {
    "bg_primary": "#1a1a2e", # Warna latar belakang utama yang lebih gelap
    "bg_secondary": "#0f0f1c", # Warna latar belakang elemen sekunder
    "bg_card": "#1f1f3a", # Latar belakang card/container
    "bg_sidebar": "#1a1a2e", # Latar belakang sidebar
    "bg_active_sidebar_item": "#007bff", # Warna biru cerah untuk item sidebar aktif (sesuai option_menu default)
    "bg_hover_sidebar_item": "#2a2a4a", # Warna hover sidebar

    "text_primary": "#e0e0e0", # Warna teks utama
    "text_secondary": "#bbbbbb", # Warna teks sekunder
    "text_subheader": "#a0aec0", # Warna untuk subheader
    "text_neon_blue": "#00bcd4", # Neon Blue
    "text_neon_purple": "#9c27b0", # Neon Purple
    "text_neon_green": "#00e676", # Neon Green
    "text_neon_red": "#ff1744", # Neon Red
    "text_success": "#00e676", # Warna teks untuk st.success

    "border_color": "#3a3a5e", # Warna border umum
    "border_neon_blue": "#00bcd4",
    "border_neon_purple": "#9c27b0",

    "button_bg": "#007bff", # Biru cerah untuk tombol utama
    "button_hover_bg": "#0056b3",
    "button_text": "white",
    "button_shadow": "rgba(0, 123, 255, 0.4)",

    "input_bg": "#2a2a4a", # Latar belakang input
    "input_border": "#4a4a6e",
    "input_focus_border": "#00bcd4", # Neon blue focus
    "input_placeholder": "#888888",

    "header_gradient_start": "#00bcd4", # Neon blue
    "header_gradient_end": "#9c27b0", # Neon purple

    "plot_line_isobaric": "#00bcd4", # Neon blue
    "plot_line_isochoric": "#00e676", # Neon green
    "plot_line_isothermal": "#ff1744", # Neon red
    "plot_point_color": "#ffeb3b", # Neon yellow
    "plot_text_color": "#e0e0e0",
    "plot_grid_color": "#4a4a6e",
    "plot_title_color": "#00bcd4",
    "plot_legend_bg": "#1f1f3a",
    "plot_legend_border": "#4a4a6e",
    "plot_legend_text": "#e0e0e0",
}

current_theme = DARK_THEME_COLORS # Kita hanya pakai tema gelap/neon sekarang

# --- Custom CSS untuk UI/UX Baru ---
st.markdown(f"""
    <style>
        /* Definisi keyframes untuk animasi latar belakang */
        @keyframes background-pan {{
            0% {{
                background-position: 0% 0%;
            }}
            100% {{
                background-position: 100% 100%;
            }}
        }}

        /* Mengatur font utama dan latar belakang gradien untuk seluruh aplikasi */
        .stApp {{
            background: linear-gradient(135deg, {current_theme["bg_primary"]} 0%, {current_theme["bg_secondary"]} 100%);
            color: {current_theme["text_primary"]};
            font-family: 'Inter', sans-serif;
            background-image: radial-gradient(at 0% 0%, rgba(0,255,255,0.1) 0, transparent 50%),
                              radial-gradient(at 50% 100%, rgba(156,39,176,0.1) 0, transparent 50%),
                              radial-gradient(at 100% 0%, rgba(255,87,34,0.1) 0, transparent 50%);
            background-attachment: fixed;
            background-size: 200% 200%;
            animation: background-pan 30s linear infinite alternate;
        }}

        /* Styling untuk judul utama (H1) */
        h1 {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            letter-spacing: -0.05em;
            background: linear-gradient(90deg, {current_theme["header_gradient_start"]}, {current_theme["header_gradient_end"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            color: transparent;
            text-align: center;
            font-size: 4rem;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 20px rgba(0, 188, 212, 0.6); /* Neon glow */
        }}
        /* Styling untuk subheader (deskripsi) */
        p.subheader {{
            font-weight: 300;
            color: {current_theme["text_subheader"]};
            text-align: center;
            font-size: 1.25rem;
            margin-bottom: 3rem;
            text-shadow: 0 0 5px rgba(187, 187, 187, 0.2);
        }}
        /* Padding untuk container utama */
        .block-container {{
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }}

        /* Styling untuk semua input teks dan textarea */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea,
        .stNumberInput > div > label + div > div > input {{ /* Target input number juga */
            background-color: {current_theme["input_bg"]};
            border: 1px solid {current_theme["input_border"]};
            color: {current_theme["text_primary"]};
            padding: 0.8rem 1.2rem;
            border-radius: 0.5rem; /* Lebih tajam */
            transition: all 0.2s ease-in-out;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }}
        /* Efek fokus untuk input teks dan textarea */
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > label + div > div > input:focus {{
            border-color: {current_theme["input_focus_border"]};
            box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.4), 0 0 15px rgba(0, 188, 212, 0.3); /* Neon glow focus */
            background-color: {current_theme["input_bg"]}; /* Tetap sama saat fokus */
            outline: none;
        }}
        /* Placeholder styling */
        input::placeholder, textarea::placeholder {{
            color: {current_theme["input_placeholder"]};
            opacity: 0.7;
        }}

        /* Styling umum untuk semua tombol */
        div.stButton > button {{
            background: {current_theme["button_bg"]};
            color: {current_theme["button_text"]};
            font-weight: 600;
            padding: 0.8rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 3px 10px {current_theme["button_shadow"]};
            transition: all 0.2s ease-in-out;
            width: 100%;
            margin-top: 1rem;
            border: none;
            position: relative;
            overflow: hidden;
        }}
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px {current_theme["button_shadow"]};
            opacity: 0.9;
        }}
        div.stButton > button:active {{
            transform: translateY(0);
            box-shadow: 0 1px 5px {current_theme["button_shadow"]};
        }}
        /* Efek kilauan pada tombol saat hover */
        div.stButton > button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.2);
            transform: skewX(-30deg);
            transition: all 0.7s ease;
        }}
        div.stButton > button:hover::before {{
            left: 100%;
        }}

        /* Styling khusus untuk tombol tab (Isobarik, Isokhorik, Isotermal) */
        /* Tombol tab ini akan diatur di halaman masing-masing untuk aktif/tidak aktif */
        div.stButton > button[data-testid^="stButton-primary"] {{ /* Target semua tombol Streamlit */
            background: {current_theme["bg_secondary"]}; /* Latar belakang yang lebih gelap untuk tombol non-aktif */
            color: {current_theme["text_secondary"]};
            border: 1px solid {current_theme["border_color"]};
            box-shadow: none;
            transform: none;
            margin-top: 0.5rem;
            transition: all 0.2s ease-in-out;
            padding: 0.75rem 1rem;
            font-weight: 500;
            border-radius: 0.5rem;
        }}
        div.stButton > button[data-testid^="stButton-primary"]:hover {{
            background: {current_theme["bg_card"]}; /* Sedikit lebih terang saat hover */
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
            transform: translateY(-1px);
        }}

        /* Styling untuk kotak hasil perhitungan */
        .result-box {{
            background: {current_theme["bg_card"]};
            border: 1px solid {current_theme["border_color"]};
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
            padding: 1.5rem;
            border-radius: 0.75rem;
            margin-top: 1.5rem;
        }}
        .result-box h3 {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: {current_theme["text_neon_blue"]}; /* Neon blue untuk judul hasil */
            font-size: 1.4rem;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: center;
            text-shadow: 0 0 10px rgba(0, 188, 212, 0.4);
        }}
        .result-box p {{
            color: {current_theme["text_secondary"]};
            font-size: 1rem;
            line-height: 1.6;
        }}
        .result-box p span {{
            color: {current_theme["text_primary"]};
            font-weight: 700;
        }}

        /* Styling untuk Selectbox Streamlit */
        .stSelectbox > div > label {{
            color: {current_theme["text_primary"]};
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        .stSelectbox > div > div {{
            background-color: {current_theme["input_bg"]};
            border-radius: 0.5rem;
            border: 1px solid {current_theme["input_border"]};
            color: {current_theme["text_primary"]};
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }}
        .stSelectbox > div > div:hover {{
            border-color: {current_theme["input_focus_border"]};
        }}
        /* Styling untuk header bagian (H2) */
        .section-header {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: {current_theme["text_primary"]};
            font-size: 2rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            text-shadow: 0 0 10px rgba(224, 224, 224, 0.2);
        }}
        .section-header i {{
            margin-right: 0.8rem;
            font-size: 1.6rem;
            color: {current_theme["text_neon_blue"]}; /* Neon blue untuk ikon header */
        }}
        /* Styling untuk sub-subheader (H3) */
        .subsection-header {{
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: {current_theme["text_primary"]};
            font-size: 1.15rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }}
        /* Styling untuk kolom di Streamlit */
        .st-emotion-cache-1cypcdb {{
            gap: 1.5rem;
        }}
        /* Card-like containers for the main sections */
        .st-emotion-cache-fg4pbf {{ /* Ini adalah div utama yang membungkus kolom di Streamlit */
            background: {current_theme["bg_card"]};
            border-radius: 0.75rem; /* Lebih tajam */
            padding: 2rem;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
            border: 1px solid {current_theme["border_color"]};
        }}
        /* Mengatur ulang padding untuk input number agar tidak terlalu lebar */
        .stNumberInput > label + div > div {{
            padding: 0;
        }}
        .stNumberInput input {{
            padding: 0.75rem 1rem !important;
        }}
        /* Styling untuk kotak info (st.info) */
        .stAlert.stAlert--info {{
            background-color: rgba(0, 188, 212, 0.1); /* Neon blue transparan */
            color: {current_theme["text_neon_blue"]};
            border-left: 5px solid {current_theme["border_neon_blue"]};
            border-radius: 0.5rem;
            padding: 1rem;
            margin-top: 1rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        /* Styling untuk kotak error (st.error) */
        .stAlert.stAlert--error {{
            background-color: rgba(255, 23, 68, 0.1); /* Neon red transparan */
            color: {current_theme["text_neon_red"]};
            border-left: 5px solid {current_theme["text_neon_red"]};
            border-radius: 0.5rem;
            padding: 1rem;
            margin-top: 1rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        /* Styling untuk kotak warning (st.warning) */
        .stAlert.stAlert--warning {{
            background-color: rgba(255, 235, 59, 0.1); /* Neon yellow transparan */
            color: {current_theme["plot_point_color"]};
            border-left: 5px solid {current_theme["plot_point_color"]};
            border-radius: 0.5rem;
            padding: 1rem;
            margin-top: 1rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}

        /* Sidebar Styling */
        .stSidebar {{
            background-color: {current_theme["bg_sidebar"]};
            padding-top: 2rem;
            border-right: 1px solid {current_theme["border_color"]};
            box-shadow: 5px 0 15px rgba(0, 0, 0, 0.3);
        }}
        /* Sembunyikan daftar halaman default Streamlit */
        .st-emotion-cache-10q0tfy {{ /* Ini adalah class untuk div yang membungkus daftar halaman default */
            display: none;
        }}
        /* Sembunyikan label radio default "Pilih Halaman:" */
        .stSidebar .stRadio > label {{
            display: none;
        }}
        /* Buat radio button vertikal */
        .stSidebar .stRadio div[role="radiogroup"] {{
            flex-direction: column;
        }}
        /* Styling untuk setiap item radio (tombol navigasi) */
        .stSidebar .stRadio div[role="radiogroup"] label {{
            width: 100%;
            margin-bottom: 0.5rem;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            color: {current_theme["text_primary"]};
            font-weight: 500;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
            display: flex;
            align-items: center;
            background-color: {current_theme["bg_secondary"]}; /* Default background for inactive items */
            border: 1px solid {current_theme["border_color"]};
        }}
        /* Efek hover untuk item navigasi */
        .stSidebar .stRadio div[role="radiogroup"] label:hover {{
            background-color: {current_theme["bg_hover_sidebar_item"]};
            color: {current_theme["text_neon_blue"]};
        }}
        /* Gaya untuk item navigasi yang aktif */
        .stSidebar .stRadio div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] {{
            background-color: {current_theme["bg_active_sidebar_item"]};
            color: {current_theme["button_text"]};
            box-shadow: 0 2px 10px rgba(0, 123, 255, 0.4);
            border-color: {current_theme["bg_active_sidebar_item"]};
        }}
        /* Sembunyikan titik radio button default */
        .stSidebar .stRadio div[role="radiogroup"] label span svg {{
            display: none;
        }}
        .stSidebar .stRadio div[role="radiogroup"] label span {{
            background-color: transparent !important;
            border: none !important;
        }}
        /* Styling untuk teks di dalam label radio */
        .stSidebar .stRadio div[role="radiogroup"] label p {{
            font-size: 1.1rem;
            margin: 0;
            flex-grow: 1; /* Agar teks mengisi ruang */
        }}
        /* Styling untuk ikon di dalam label radio (jika ada) */
        .stSidebar .stRadio div[role="radiogroup"] label i {{
            margin-right: 0.75rem;
            font-size: 1.2rem;
            color: inherit; /* Warisi warna dari parent label */
        }}
        /* Styling untuk judul sidebar */
        .sidebar-header {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: {current_theme["text_neon_blue"]};
            font-size: 1.8rem;
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid {current_theme["border_color"]};
            text-shadow: 0 0 10px rgba(0, 188, 212, 0.3);
        }}
        /* Mengatur ulang padding atas untuk konten utama */
        .main .block-container {{
            padding-top: 1rem; /* Kurangi padding atas di konten utama */
        }}
        /* Sidebar header */
        .sidebar-header {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: {current_theme["text_neon_blue"]};
            font-size: 1.8rem;
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid {current_theme["border_color"]};
            text-shadow: 0 0 10px rgba(0, 188, 212, 0.3);
        }}
        /* Streamlit Tabs styling (for Tentang Aplikasi page) */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 1rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid {current_theme["border_color"]};
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 3rem;
            background-color: {current_theme["bg_secondary"]};
            border-radius: 0.5rem 0.5rem 0 0;
            padding: 0 1.5rem;
            color: {current_theme["text_secondary"]};
            font-weight: 500;
            font-size: 1.05rem;
            transition: all 0.2s ease-in-out;
            border: 1px solid {current_theme["border_color"]};
            border-bottom: none;
            margin-bottom: -1px; /* Overlap border */
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: {current_theme["bg_card"]};
            color: {current_theme["text_primary"]};
        }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background-color: {current_theme["bg_card"]};
            color: {current_theme["text_neon_blue"]};
            border-bottom: 3px solid {current_theme["border_neon_blue"]}; /* Garis bawah neon */
            font-weight: 600;
            box-shadow: 0 -2px 10px rgba(0, 188, 212, 0.2);
        }}
        .stTabs [data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] p {{
            font-size: 1.05rem; /* Ukuran font teks tab */
            color: inherit; /* Warisi warna dari parent tab */
        }}
        /* Styling untuk konten di dalam tab */
        .stTabs .stMarkdown {{
            background-color: {current_theme["bg_card"]};
            border: 1px solid {current_theme["border_color"]};
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }}
        /* Styling untuk tabel di markdown (jika ada) */
        .stMarkdown table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        .stMarkdown th, .stMarkdown td {{
            border: 1px solid {current_theme["border_color"]};
            padding: 0.8rem;
            text-align: left;
            color: {current_theme["text_secondary"]};
        }}
        .stMarkdown th {{
            background-color: {current_theme["bg_secondary"]};
            color: {current_theme["text_neon_blue"]};
            font-weight: 600;
        }}
        .stMarkdown tr:nth-child(even) {{
            background-color: rgba(0,0,0,0.1);
        }}
        .stMarkdown a {{
            color: {current_theme["text_neon_blue"]};
            text-decoration: none;
        }}
        .stMarkdown a:hover {{
            text-decoration: underline;
        }}

        /* HOME PAGE SPECIFIC STYLES */
        .home-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 3rem;
            background: {current_theme["bg_card"]};
            border-radius: 1rem;
            border: 1px solid {current_theme["border_color"]};
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        }}
        .home-title {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 3rem;
            color: {current_theme["text_neon_blue"]};
            margin-bottom: 1rem;
            text-shadow: 0 0 15px rgba(0, 188, 212, 0.5);
        }}
        .home-subtitle {{
            font-size: 1.2rem;
            color: {current_theme["text_secondary"]};
            margin-bottom: 2rem;
        }}
        .home-illustration {{
            width: 250px;
            height: 250px;
            background-color: {current_theme["bg_secondary"]};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            border: 3px solid {current_theme["border_neon_blue"]};
            box-shadow: 0 0 20px rgba(0, 188, 212, 0.4);
        }}
        .home-illustration i {{
            font-size: 120px;
            color: {current_theme["text_neon_blue"]};
            text-shadow: 0 0 10px rgba(0, 188, 212, 0.6);
        }}
        .home-description {{
            font-size: 1rem;
            color: {current_theme["text_secondary"]};
            line-height: 1.6;
            max-width: 800px;
        }}
        .home-description strong {{
            color: {current_theme["text_neon_blue"]};
        }}
        .team-section {{
            margin-top: 3rem;
            text-align: left;
            width: 100%;
            max-width: 600px;
        }}
        .team-section h3 {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            color: {current_theme["text_neon_purple"]};
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            text-shadow: 0 0 10px rgba(156, 39, 176, 0.4);
        }}
        .team-section ul {{
            list-style: none;
            padding-left: 0;
        }}
        .team-section li {{
            font-size: 1.1rem;
            color: {current_theme["text_primary"]};
            margin-bottom: 0.5rem;
        }}
        .team-section li span {{
            font-weight: 600;
            color: {current_theme["text_neon_blue"]};
        }}

    </style>
    <!-- Font Awesome untuk ikon -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

# --- Inisialisasi Session State untuk Plot Data (Global) ---
if 'plot_data' not in st.session_state:
    st.session_state.plot_data = None
if 'plot_title' not in st.session_state:
    st.session_state.plot_title = None

# --- Fungsi-fungsi Perhitungan Termodinamika ---
def calculate_isobaric(p, v1, v2, n, t1, t2):
    W = p * (v2 - v1)
    dU = 1.5 * n * R * (t2 - t1)
    Q = W + dU
    return W, dU, Q

def calculate_isochoric(n, t1, t2):
    W = 0
    dU = 1.5 * n * R * (t2 - t1)
    Q = dU
    return W, dU, Q

def calculate_isothermal(n, T, v1, v2):
    W = n * R * T * math.log(v2 / v1)
    dU = 0
    Q = W
    return W, dU, Q

# --- Sidebar Navigasi (Menggunakan streamlit_option_menu) ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">MENU</div>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, # Sembunyikan judul menu default
        options=["Beranda", "Kalkulator Termodinamika", "Konverter Satuan", "Visualisasi Proses", "Tentang Aplikasi"],
        icons=["house-door", "calculator", "arrow-left-right", "graph-up", "info-circle"], # Bootstrap icons atau custom
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": current_theme["bg_sidebar"]},
            "icon": {"color": current_theme["text_neon_blue"], "font-size": "1.2rem"},
            "nav-link": {
                "font-size": "1.1rem",
                "text-align": "left",
                "margin": "0px",
                "padding": "0.75rem 1rem",
                "border-radius": "0.5rem",
                "color": current_theme["text_primary"],
                "background-color": current_theme["bg_secondary"],
                "border": f"1px solid {current_theme['border_color']}",
                "--hover-color": current_theme["bg_hover_sidebar_item"],
            },
            "nav-link-selected": {
                "background-color": current_theme["bg_active_sidebar_item"],
                "color": current_theme["button_text"],
                "box-shadow": f"0 2px 10px {current_theme['button_shadow']}",
                "border-color": current_theme["bg_active_sidebar_item"],
            },
        }
    )

# --- Konten Halaman Berdasarkan Pilihan Sidebar ---

if selected == "Beranda":
    st.markdown('<div class="home-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="home-title">SELAMAT DATANG</h2>', unsafe_allow_html=True)
    st.markdown('<p class="home-subtitle">Di ThermoCalc Lab</p>', unsafe_allow_html=True)
    st.markdown('<div class="home-illustration"><i class="fas fa-flask"></i></div>', unsafe_allow_html=True)
    st.markdown("""
        <p class="home-description">
            <strong>ThermoCalc Lab</strong> adalah alat online gratis yang dirancang untuk memudahkan Anda dalam memahami dan menghitung proses termodinamika. Aplikasi ini menyediakan kalkulator interaktif untuk berbagai proses, konverter satuan, dan visualisasi grafik P-V untuk membantu Anda memvisualisasikan konsep.
            Silakan pilih metode perhitungan atau alat yang sesuai dari menu di samping, kemudian ikuti perintah yang ditampilkan di layar!
        </p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="team-section">', unsafe_allow_html=True)
    st.markdown('<h3>DIBUAT OLEH:</h3>', unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li><span>KELOMPOK 12 (1C - ANALISIS KIMIA)</span></li>
            <li>1. Bagus Inayatullah Pramudana Herman (2460342)</li>
            <li>2. Ihtiathus Syar'iyah (2460387)</li>
            <li>3. Nafisa Alya Rahma (2460451)</li>
            <li>4.  Riko Putra Pamungkas (2460499)</li>
            <li>5. Zayyum Adji Lubis (2460546)</li>
        </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Kalkulator Termodinamika":
    st.markdown('<h2 class="section-header"><i class="fas fa-calculator"></i> Kalkulator Termodinamika</h2>', unsafe_allow_html=True)

    # Menggunakan st.session_state untuk mengelola tab aktif
    if 'active_tab_calc' not in st.session_state:
        st.session_state.active_tab_calc = "Isobarik"

    # Tombol tab kustom (simulasi)
    tab_cols = st.columns(3)
    with tab_cols[0]:
        if st.button("Isobarik", key="tab_isobaric_calc"):
            st.session_state.active_tab_calc = "Isobarik"
    with tab_cols[1]:
        if st.button("Isokhorik", key="tab_isochoric_calc"):
            st.session_state.active_tab_calc = "Isokhorik"
    with tab_cols[2]:
        if st.button("Isotermal", key="tab_isothermal_calc"):
            st.session_state.active_tab_calc = "Isotermal"

    # Menambahkan CSS untuk tombol tab aktif (diperbarui agar lebih dinamis)
    st.markdown(f"""
        <style>
            /* Mengatur ulang gaya tombol stButton untuk tab */
            div.stButton > button[data-testid^="stButton-primary"] {{
                background: {current_theme["bg_secondary"]}; /* Latar belakang yang lebih gelap untuk tombol non-aktif */
                color: {current_theme["text_secondary"]};
                box-shadow: none;
                transform: none;
                margin-top: 0;
                border: 1px solid {current_theme["border_color"]};
                transition: all 0.2s ease-in-out;
                padding: 0.75rem 1rem;
                font-weight: 500;
                border-radius: 0.5rem;
            }}
            div.stButton > button[data-testid^="stButton-primary"]:hover {{
                background: {current_theme["bg_card"]}; /* Sedikit lebih terang saat hover */
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }}
            /* Gaya untuk tab aktif */
            div.stButton > button[data-testid="stButton-primary"][key="tab_isobaric_calc"] {{
                background-color: {current_theme["bg_active_sidebar_item"] if st.session_state.active_tab_calc == 'Isobarik' else current_theme["bg_secondary"]};
                color: {current_theme["button_text"] if st.session_state.active_tab_calc == 'Isobarik' else current_theme["text_secondary"]};
                box-shadow: {'0 4px 10px rgba(0, 123, 255, 0.4)' if st.session_state.active_tab_calc == 'Isobarik' else 'none'};
                transform: {'translateY(-2px)' if st.session_state.active_tab_calc == 'Isobarik' else 'none'};
                border-radius: 0.5rem 0.5rem 0 0; /* Rounded top only */
            }}
            div.stButton > button[data-testid="stButton-primary"][key="tab_isochoric_calc"] {{
                background-color: {current_theme["bg_active_sidebar_item"] if st.session_state.active_tab_calc == 'Isokhorik' else current_theme["bg_secondary"]};
                color: {current_theme["button_text"] if st.session_state.active_tab_calc == 'Isokhorik' else current_theme["text_secondary"]};
                box-shadow: {'0 4px 10px rgba(0, 123, 255, 0.4)' if st.session_state.active_tab_calc == 'Isokhorik' else 'none'};
                transform: {'translateY(-2px)' if st.session_state.active_tab_calc == 'Isokhorik' else 'none'};
                border-radius: 0.5rem 0.5rem 0 0;
            }}
            div.stButton > button[data-testid="stButton-primary"][key="tab_isothermal_calc"] {{
                background-color: {current_theme["bg_active_sidebar_item"] if st.session_state.active_tab_calc == 'Isotermal' else current_theme["bg_secondary"]};
                color: {current_theme["button_text"] if st.session_state.active_tab_calc == 'Isotermal' else current_theme["text_secondary"]};
                box-shadow: {'0 4px 10px rgba(0, 123, 255, 0.4)' if st.session_state.active_tab_calc == 'Isotermal' else 'none'};
                transform: {'translateY(-2px)' if st.session_state.active_tab_calc == 'Isotermal' else 'none'};
                border-radius: 0.5rem 0.5rem 0 0;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Konten berdasarkan tab aktif
    if st.session_state.active_tab_calc == "Isobarik":
        st.markdown('<p class="subsection-header">Input untuk Proses Isobarik</p>', unsafe_allow_html=True)
        p = st.number_input("Tekanan (p) dalam Pascal", min_value=0.0, format="%.2f", key="iso_p_input")
        v1 = st.number_input("Volume Awal (V₁) dalam m³", min_value=0.0, format="%.4f", key="iso_v1_input")
        v2 = st.number_input("Volume Akhir (V₂) dalam m³", min_value=0.0, format="%.4f", key="iso_v2_input")
        n = st.number_input("Jumlah mol (n)", min_value=0.0, format="%.4f", key="iso_n_input")
        t1 = st.number_input("Suhu Awal (T₁) dalam Kelvin", min_value=0.0, format="%.2f", key="iso_t1_input")
        t2 = st.number_input("Suhu Akhir (T₂) dalam Kelvin", min_value=0.0, format="%.2f", key="iso_t2_input")

        if st.button("Hitung Isobarik", key="calc_isobaric_btn"):
            if p is not None and v1 is not None and v2 is not None and n is not None and t1 is not None and t2 is not None:
                try:
                    if v1 < 0 or v2 < 0 or t1 < 0 or t2 < 0 or n < 0:
                        st.error("Volume, Suhu, dan Jumlah mol tidak boleh negatif.")
                    else:
                        W, dU, Q = calculate_isobaric(p, v1, v2, n, t1, t2)
                        st.markdown(f"""
                            <div class="result-box">
                                <h3><i class="fas fa-flask mr-2"></i> Hasil Perhitungan:</h3>
                                <p>Usaha (W): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{W:.4f} J</span></p>
                                <p>Energi Dalam (ΔU): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{dU:.4f} J</span></p>
                                <p>Kalor (Q): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{Q:.4f} J</span></p>
                            </div>
                        """, unsafe_allow_html=True)
                        # Simpan data untuk plot di session state global
                        st.session_state.plot_data = {
                            'type': 'isobaric',
                            'p': p,
                            'v1': v1,
                            'v2': v2,
                            'n': n,
                            't1': t1,
                            't2': t2
                        }
                        st.session_state.plot_title = f"Grafik P-V Proses Isobarik (P={p:.2f} Pa)"
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}. Harap periksa kembali semua input.")
            else:
                st.warning("Harap masukkan semua nilai numerik yang valid untuk proses Isobarik.")

    elif st.session_state.active_tab_calc == "Isokhorik":
        st.markdown('<p class="subsection-header">Input untuk Proses Isokhorik</p>', unsafe_allow_html=True)
        n = st.number_input("Jumlah mol (n)", min_value=0.0, format="%.4f", key="isok_n_input")
        t1 = st.number_input("Suhu Awal (T₁) dalam Kelvin", min_value=0.0, format="%.2f", key="isok_t1_input")
        t2 = st.number_input("Suhu Akhir (T₂) dalam Kelvin", min_value=0.0, format="%.2f", key="isok_t2_input")
        v_const = st.number_input("Volume Konstan (V) dalam m³", min_value=0.0, format="%.4f", key="isok_v_const_input")

        if st.button("Hitung Isokhorik", key="calc_isokhoric_btn"):
            if n is not None and t1 is not None and t2 is not None and v_const is not None:
                try:
                    if t1 < 0 or t2 < 0 or n < 0 or v_const <= 0:
                        st.error("Suhu, Jumlah mol tidak boleh negatif, dan Volume harus positif.")
                    else:
                        W, dU, Q = calculate_isochoric(n, t1, t2)
                        st.markdown(f"""
                            <div class="result-box">
                                <h3><i class="fas fa-flask mr-2"></i> Hasil Perhitungan:</h3>
                                <p>Usaha (W): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{W:.4f} J</span></p>
                                <p>Energi Dalam (ΔU): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{dU:.4f} J</span></p>
                                <p>Kalor (Q): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{Q:.4f} J</span></p>
                            </div>
                        """, unsafe_allow_html=True)
                        # Simpan data untuk plot
                        st.session_state.plot_data = {
                            'type': 'isochoric',
                            'n': n,
                            't1': t1,
                            't2': t2,
                            'v_const': v_const
                        }
                        st.session_state.plot_title = f"Grafik P-V Proses Isokhorik (V={v_const:.2f} m³)"
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}. Harap periksa kembali semua input.")
            else:
                st.warning("Harap masukkan semua nilai numerik yang valid untuk proses Isokhorik.")

    elif st.session_state.active_tab_calc == "Isotermal":
        st.markdown('<p class="subsection-header">Input untuk Proses Isotermal</p>', unsafe_allow_html=True)
        n = st.number_input("Jumlah mol (n)", min_value=0.0, format="%.4f", key="isot_n_input")
        T = st.number_input("Suhu (T) dalam Kelvin", min_value=0.0, format="%.2f", key="isot_t_input")
        v1 = st.number_input("Volume Awal (V₁) dalam m³", min_value=0.0, format="%.4f", key="isot_v1_input")
        v2 = st.number_input("Volume Akhir (V₂) dalam m³", min_value=0.0, format="%.4f", key="isot_v2_input")

        if st.button("Hitung Isotermal", key="calc_isotermal_btn"):
            if n is not None and T is not None and v1 is not None and v2 is not None:
                try:
                    if v1 <= 0 or v2 <= 0 or T <= 0 or n < 0:
                        st.error("Volume dan Suhu harus positif, Jumlah mol tidak boleh negatif.")
                    else:
                        W, dU, Q = calculate_isothermal(n, T, v1, v2)
                        st.markdown(f"""
                            <div class="result-box">
                                <h3><i class="fas fa-flask mr-2"></i> Hasil Perhitungan:</h3>
                                <p>Usaha (W): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{W:.4f} J</span></p>
                                <p>Energi Dalam (ΔU): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{dU:.4f} J</span></p>
                                <p>Kalor (Q): <span style="font-weight: 600; color: {current_theme["text_primary"]};">{Q:.4f} J</span></p>
                            </div>
                        """, unsafe_allow_html=True)
                        # Simpan data untuk plot
                        st.session_state.plot_data = {
                            'type': 'isothermal',
                            'n': n,
                            'T': T,
                            'v1': v1,
                            'v2': v2
                        }
                        st.session_state.plot_title = f"Grafik P-V Proses Isotermal (T={T:.2f} K)"
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}. Harap periksa kembali semua input.")
            else:
                st.warning("Harap masukkan semua nilai numerik yang valid untuk proses Isotermal.")

elif selected == "Konverter Satuan":
    st.markdown('<h2 class="section-header"><i class="fas fa-exchange-alt"></i> Konverter Satuan</h2>', unsafe_allow_html=True)

    st.markdown('<p class="subsection-header">Suhu</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        celsius = st.number_input("Celsius (°C)", format="%.2f", key="conv_celsius")
        if 'prev_celsius' not in st.session_state: st.session_state.prev_celsius = None
        if celsius is not None and celsius != st.session_state.prev_celsius:
            fahrenheit_conv_c = (celsius * 9/5) + 32
            kelvin_conv_c = celsius + 273.15
            st.info(f"Fahrenheit: {fahrenheit_conv_c:.2f} °F | Kelvin: {kelvin_conv_c:.2f} K")
        st.session_state.prev_celsius = celsius

    with col2:
        fahrenheit = st.number_input("Fahrenheit (°F)", format="%.2f", key="conv_fahrenheit")
        if 'prev_fahrenheit' not in st.session_state: st.session_state.prev_fahrenheit = None
        if fahrenheit is not None and fahrenheit != st.session_state.prev_fahrenheit:
            celsius_conv_f = (fahrenheit - 32) * 5/9
            kelvin_conv_f = celsius_conv_f + 273.15
            st.info(f"Celsius: {celsius_conv_f:.2f} °C | Kelvin: {kelvin_conv_f:.2f} K")
        st.session_state.prev_fahrenheit = fahrenheit

    with col3:
        kelvin = st.number_input("Kelvin (K)", format="%.2f", key="conv_kelvin")
        if 'prev_kelvin' not in st.session_state: st.session_state.prev_kelvin = None
        if kelvin is not None and kelvin != st.session_state.prev_kelvin:
            celsius_conv_k = kelvin - 273.15
            fahrenheit_conv_k = (celsius_conv_k * 9/5) + 32
            st.info(f"Celsius: {celsius_conv_k:.2f} °C | Fahrenheit: {fahrenheit_conv_k:.2f} °F")
        st.session_state.prev_kelvin = kelvin

    st.markdown('<p class="subsection-header">Tekanan</p>', unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)

    with col4:
        atm = st.number_input("Atmosfer (atm)", format="%.5f", key="conv_atm")
        if 'prev_atm' not in st.session_state: st.session_state.prev_atm = None
        if atm is not None and atm != st.session_state.prev_atm:
            mmhg_conv_atm = atm * 760
            pascal_conv_atm = atm * 101325
            st.info(f"mmHg: {mmhg_conv_atm:.2f} | Pascal: {pascal_conv_atm:.3e}")
        st.session_state.prev_atm = atm

    with col5:
        mmhg = st.number_input("mmHg", format="%.2f", key="conv_mmhg")
        if 'prev_mmhg' not in st.session_state: st.session_state.prev_mmhg = None
        if mmhg is not None and mmhg != st.session_state.prev_mmhg:
            atm_conv_mmhg = mmhg / 760
            pascal_conv_mmhg = mmhg * 133.322
            st.info(f"Atmosfer: {atm_conv_mmhg:.5f} atm | Pascal: {pascal_conv_mmhg:.3e}")
        st.session_state.prev_mmhg = mmhg

    with col6:
        pascal = st.number_input("Pascal (Pa)", format="%.3e", key="conv_pascal")
        if 'prev_pascal' not in st.session_state: st.session_state.prev_pascal = None
        if pascal is not None and pascal != st.session_state.prev_pascal:
            atm_conv_pascal = pascal / 101325
            mmhg_conv_pascal = pascal / 133.322
            st.info(f"Atmosfer: {atm_conv_pascal:.5f} atm | mmHg: {mmhg_conv_pascal:.2f}")
        st.session_state.prev_pascal = pascal

    # --- Bagian Konverter Volume Baru ---
    st.markdown('<p class="subsection-header">Volume</p>', unsafe_allow_html=True)
    col_vol1, col_vol2, col_vol3 = st.columns(3)

    with col_vol1:
        mm_kubik = st.number_input("Milimeter Kubik (mm³)", format="%.4f", key="conv_mm_kubik")
        if 'prev_mm_kubik' not in st.session_state: st.session_state.prev_mm_kubik = None
        if mm_kubik is not None and mm_kubik != st.session_state.prev_mm_kubik:
            cm_kubik_mm = mm_kubik / 1000
            m_kubik_mm = mm_kubik / 1_000_000_000
            st.info(f"cm³: {cm_kubik_mm:.4f} | m³: {m_kubik_mm:.9f}")
        st.session_state.prev_mm_kubik = mm_kubik

    with col_vol2:
        cm_kubik = st.number_input("Sentimeter Kubik (cm³)", format="%.4f", key="conv_cm_kubik")
        if 'prev_cm_kubik' not in st.session_state: st.session_state.prev_cm_kubik = None
        if cm_kubik is not None and cm_kubik != st.session_state.prev_cm_kubik:
            mm_kubik_cm = cm_kubik * 1000
            m_kubik_cm = cm_kubik / 1_000_000
            st.info(f"mm³: {mm_kubik_cm:.4f} | m³: {m_kubik_cm:.9f}")
        st.session_state.prev_cm_kubik = cm_kubik

    with col_vol3:
        m_kubik = st.number_input("Meter Kubik (m³)", format="%.9f", key="conv_m_kubik")
        if 'prev_m_kubik' not in st.session_state: st.session_state.prev_m_kubik = None
        if m_kubik is not None and m_kubik != st.session_state.prev_m_kubik:
            mm_kubik_m = m_kubik * 1_000_000_000
            cm_kubik_m = m_kubik * 1_000_000
            st.info(f"mm³: {mm_kubik_m:.4f} | cm³: {cm_kubik_m:.4f}")
        st.session_state.prev_m_kubik = m_kubik


elif selected == "Visualisasi Proses":
    st.markdown('<h2 class="section-header"><i class="fas fa-chart-line"></i> Visualisasi Proses Termodinamika</h2>', unsafe_allow_html=True)

    if st.session_state.plot_data:
        plot_type = st.session_state.plot_data['type']
        
        # Gaya plot Matplotlib (menggunakan warna hardcoded yang sesuai dengan tema neon gelap)
        plt.style.use('dark_background')
        text_color = current_theme["plot_text_color"]
        grid_color = current_theme["plot_grid_color"]
        title_color = current_theme["plot_title_color"]
        legend_facecolor = current_theme["plot_legend_bg"]
        legend_edgecolor = current_theme["plot_legend_border"]
        legend_labelcolor = current_theme["plot_legend_text"]

        line_isobaric_color = current_theme["plot_line_isobaric"]
        line_isochoric_color = current_theme["plot_line_isochoric"]
        line_isothermal_color = current_theme["plot_line_isothermal"]
        point_color = current_theme["plot_point_color"]

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.set_xlabel('Volume (m³)', color=text_color)
        ax.set_ylabel('Tekanan (Pa)', color=text_color)
        ax.set_title(st.session_state.plot_title, color=title_color)
        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        ax.spines['bottom'].set_color(grid_color)
        ax.spines['top'].set_color(grid_color)
        ax.spines['right'].set_color(grid_color)
        ax.spines['left'].set_color(grid_color)
        ax.grid(True, linestyle='--', alpha=0.5, color=grid_color)

        if plot_type == 'isobaric':
            p = st.session_state.plot_data['p']
            v1 = st.session_state.plot_data['v1']
            v2 = st.session_state.plot_data['v2']
            
            if v1 == v2:
                v_plot = np.array([v1 * 0.9, v1 * 1.1])
                p_plot = np.array([p, p])
            else:
                v_plot = np.linspace(min(v1, v2), max(v1, v2), 100)
                p_plot = np.full_like(v_plot, p)

            ax.plot(v_plot, p_plot, label='Isobarik', color=line_isobaric_color, linewidth=3)
            ax.plot([v1, v2], [p, p], 'o', color=point_color, markersize=8, zorder=5)
            ax.annotate('State 1', (v1, p), textcoords="offset points", xytext=(-15,-15), ha='center', color=text_color)
            ax.annotate('State 2', (v2, p), textcoords="offset points", xytext=(15,-15), ha='center', color=text_color)
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)

        elif plot_type == 'isochoric':
            n = st.session_state.plot_data['n']
            t1 = st.session_state.plot_data['t1']
            t2 = st.session_state.plot_data['t2']
            v_const = st.session_state.plot_data['v_const']

            p1 = (n * R * t1) / v_const
            p2 = (n * R * t2) / v_const

            p_plot = np.linspace(min(p1, p2), max(p1, p2), 100)
            v_plot = np.full_like(p_plot, v_const)

            ax.plot(v_plot, p_plot, label='Isokhorik', color=line_isochoric_color, linewidth=3)
            ax.plot([v_const, v_const], [p1, p2], 'o', color=point_color, markersize=8, zorder=5)
            ax.annotate('State 1', (v_const, p1), textcoords="offset points", xytext=(15,-15), ha='center', color=text_color)
            ax.annotate('State 2', (v_const, p2), textcoords="offset points", xytext=(15,15), ha='center', color=text_color)
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)

        elif plot_type == 'isothermal':
            n = st.session_state.plot_data['n']
            T = st.session_state.plot_data['T']
            v1 = st.session_state.plot_data['v1']
            v2 = st.session_state.plot_data['v2']

            v_range = np.linspace(min(v1, v2, 0.1), max(v1, v2) * 1.5, 100)
            p_range = (n * R * T) / v_range

            valid_indices = v_range > 0
            v_range = v_range[valid_indices]
            p_range = p_range[valid_indices]

            ax.plot(v_range, p_range, label='Isotermal', color=line_isothermal_color, linewidth=3)
            
            p1 = (n * R * T) / v1
            p2 = (n * R * T) / v2
            ax.plot([v1, v2], [p1, p2], 'o', color=point_color, markersize=8, zorder=5)
            ax.annotate('State 1', (v1, p1), textcoords="offset points", xytext=(-15,-15), ha='center', color=text_color)
            ax.annotate('State 2', (v2, p2), textcoords="offset points", xytext=(15,-15), ha='center', color=text_color)
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=0)

        ax.legend(facecolor=legend_facecolor, edgecolor=legend_edgecolor, labelcolor=legend_labelcolor)
        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("Lakukan perhitungan di kalkulator untuk melihat grafik P-V.")

elif selected == "Tentang Aplikasi":
    st.markdown('<h2 class="section-header"><i class="fas fa-info-circle"></i> Tentang Aplikasi</h2>', unsafe_allow_html=True)

    tab_materi, tab_cara, tab_contoh, tab_kontak = st.tabs(["Materi", "Cara Penggunaan", "Contoh Soal", "Kontak"])

    with tab_materi:
        st.markdown('<h3>Apa itu Termodinamika?</h3>', unsafe_allow_html=True)
        st.markdown("""
            <p>Termodinamika adalah cabang fisika yang mempelajari hubungan antara panas, kerja, dan energi. Ini menjelaskan bagaimana energi diubah dari satu bentuk ke bentuk lain dan bagaimana hal itu mempengaruhi materi.</p>
            <h3>Hukum-hukum Termodinamika:</h3>
            <ul>
                <li><strong>Hukum Termodinamika Nol:</strong> Jika dua sistem berada dalam kesetimbangan termal dengan sistem ketiga, maka mereka berada dalam kesetimbangan termal satu sama lain.</li>
                <li><strong>Hukum Termodinamika Pertama:</strong> Energi tidak dapat diciptakan atau dimusnahkan dalam proses biasa; ia hanya dapat berubah bentuk. (Konservasi Energi)</li>
                <li><strong>Hukum Termodinamika Kedua:</strong> Entropi total dari sistem terisolasi hanya dapat meningkat dari waktu ke waktu, atau tetap konstan dalam proses reversibel.</li>
                <li><strong>Hukum Termodinamika Ketiga:</strong> Saat suhu sistem mendekati nol absolut, entropi sistem mendekati nilai minimum konstan.</li>
            </ul>
        """, unsafe_allow_html=True)

    with tab_cara:
        st.markdown('<h3>Cara Menggunakan ThermoCalc Lab:</h3>', unsafe_allow_html=True)
        st.markdown("""
            <p>Aplikasi ini dirancang untuk kemudahan penggunaan. Ikuti langkah-langkah berikut:</p>
            <ol>
                <li><strong>Navigasi:</strong> Gunakan menu di sisi kiri (sidebar) untuk berpindah antara Kalkulator Termodinamika, Konverter Satuan, Visualisasi Proses, dan halaman ini.</li>
                <li><strong>Kalkulator Termodinamika:</strong>
                    <ul>
                        <li>Pilih jenis proses (Isobarik, Isokhorik, atau Isotermal) dari tab di bagian atas.</li>
                        <li>Masukkan nilai-nilai yang diperlukan pada kolom input.</li>
                        <li>Klik tombol "Hitung" untuk mendapatkan hasil Usaha (W), Perubahan Energi Dalam (ΔU), dan Kalor (Q).</li>
                    </ul>
                </li>
                <li><strong>Konverter Satuan:</strong>
                    <ul>
                        <li>Masukkan nilai pada salah satu kolom input (misalnya Celsius untuk suhu, atau Atmosfer untuk tekanan).</li>
                        <li>Aplikasi akan secara otomatis menampilkan hasil konversi ke satuan lain yang relevan di bawahnya.</li>
                    </ul>
                </li>
                <li><strong>Visualisasi Proses:</strong>
                    <ul>
                        <li>Setelah melakukan perhitungan di "Kalkulator Termodinamika", buka halaman "Visualisasi Proses".</li>
                        <li>Grafik P-V dari proses terakhir yang Anda hitung akan ditampilkan secara otomatis.</li>
                    </ul>
                </li>
            </ol>
        """, unsafe_allow_html=True)

    with tab_contoh:
        st.markdown('<h3>Contoh Soal:</h3>', unsafe_allow_html=True)
        st.markdown("""
            <h4>Contoh Soal 1: Proses Isobarik</h4>
            <p>Suatu gas ideal mengalami proses isobarik pada tekanan konstan <b>10^5 Pa</b>. Volume gas berubah dari <b>0.1 m^3</b> menjadi <b>0.3 m^3</b>. Jika jumlah mol gas adalah <b>1 mol</b> dan suhu awal <b>300 K</b>, suhu akhir <b>900 K</b>, hitung Usaha (W), Perubahan Energi Dalam (ΔU), dan Kalor (Q).</p>
            <p><strong>Diketahui:</strong></p>
            <ul>
                <li>P  = 10^5 Pa</li>
                <li>V1 = 0.1 m^3</li>
                <li>V2 = 0.3 m^3</li>
                <li>n  = 1 mol</li>
                <li>T1 = 300 K</li>
                <li>T2 = 900 K</li>
                <li>R  = 8.314 J/mol·K</li>
            </ul>
            <p><strong>Penyelesaian (menggunakan kalkulator):</strong></p>
            <ol>
                <li>Pilih tab "Isobarik" di Kalkulator Termodinamika.</li>
                <li>Masukkan nilai-nilai yang diketahui.</li>
                <li>Klik "Hitung Isobarik".</li>
                 <li>Dan hasil akan muncul.</li>
                
            </ol>
        """, unsafe_allow_html=True)

    with tab_kontak:
        st.markdown('<h3>Hubungi Kami</h3>', unsafe_allow_html=True)
        st.markdown("""
            <p>Silakan tinggalkan pesan Anda. Kami akan berusaha merespons sesegera mungkin.</p>
            <form action="https://formsubmit.co/ajizayum@gmail.com" method="POST">
     <input type="text" name="name" required>
     <input type="email" name="email" required>
     <p type="text" name="name";type="email" name="email">
     <!DOCTYPE html>
<html>
<head>
<title>Form Pesan</title>
<style>
  /* Basic styling for the entire page to match the dark background */
  body {
    background-color: #1a1a2e; /* Dark blue-ish background */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh; /* Make sure it takes full viewport height */
    margin: 0;
    font-family: sans-serif; /* A common sans-serif font */
    color: white; /* Default text color for the main message */
  }

  .container {
    text-align: center;
    padding: 20px;
    /* You can add more styling here for the container if needed */
  }

  /* Styling for the main message text */
  p {
    font-size: 1.2em; /* Slightly larger text */
    margin-bottom: 20px; /* Space below the message */
  }

  /* Styling for the input fields (the two smaller boxes) and textarea (the larger box) */
  input[type="text"],
  textarea {
    background-color: #333333; /* Dark grey background for the boxes */
    border: 1px solid #555555; /* Subtle border */
    color: white; /* Color of the text the user types */
    padding: 10px; /* Internal spacing */
    border-radius: 5px; /* Slightly rounded corners */
    font-size: 1em; /* Standard font size inside the boxes */
    width: 300px; /* Fixed width for the boxes, adjust as needed */
    box-sizing: border-box; /* Ensures padding and border are included in the width */
  }

  /* Specific styling for the textarea (the larger message box) */
  textarea {
    height: 100px; /* Height for the multi-line message box */
    resize: vertical; /* Allows the user to resize vertically */
    margin-top: 20px; /* Space above the textarea */
  }

  /* Styling for the placeholder text (the faded text inside the boxes) */
  /* This is the key part to make the text "pudar" (faded) */
  input::placeholder,
  textarea::placeholder {
    color: #a0a0a0; /* Light grey color for faded effect */
    opacity: 0.8; /* Makes the text slightly transparent */
  }

  /* Styling for the group of two input boxes */
  .input-group {
    display: flex; /* Use flexbox to put them side-by-side */
    gap: 20px; /* Space between the two input boxes */
    margin-top: 20px; /* Space above this group */
    justify-content: center; /* Center the boxes horizontally */
  }

  .input-group input {
    flex: 1; /* Makes each input take equal space within the group */
  }

</style>
</head>
<body>

<div class="container">
  <p>Silakan tinggalkan pesan Anda. Kami akan berusaha merespons sesegera mungkin.</p>

  <div class="input-group">
    <input type="text" placeholder="Nama Anda"> <input type="text" placeholder="Email Anda"> </div>

  <textarea placeholder="Tulis pesan Anda di sini..."></textarea> </div>

</body>
</html>
     </p>
     <button type="submit">Send</button>
</form>
            <p style="margin-top: 2rem; color: {current_theme["text_secondary"]};">
                Anda juga bisa menghubungi kami melalui GitHub: <a href="https://github.com/zayyum-a-l" target="_blank">Profil GitHub Kami</a>
            </p>
        """, unsafe_allow_html=True)
