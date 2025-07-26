# THERMOCALC LAB PROJECT

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
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Palet Warna (Tema Neon Gelap dan Terang) ---
DARK_THEME_COLORS = {
    "bg_primary": "#1a1a2e",
    "bg_secondary": "#0f0f1c",
    "bg_card": "#1f1f3a",
    "bg_sidebar": "#1a1a2e",
    "bg_active_sidebar_item": "#007bff",
    "bg_hover_sidebar_item": "#2a2a4a",
    "text_primary": "#e0e0e0",
    "text_secondary": "#bbbbbb",
    "text_subheader": "#a0aec0",
    "text_neon_blue": "#00bcd4",
    "text_neon_purple": "#9c27b0",
    "border_color": "#3a3a5e",
    "border_neon_blue": "#00bcd4",
    "button_bg": "#007bff",
    "button_text": "white",
    "button_shadow": "rgba(0, 123, 255, 0.4)",
    "input_bg": "#2a2a4a",
    "input_border": "#4a4a6e",
    "input_focus_border": "#00bcd4",
    "header_gradient_start": "#00bcd4",
    "header_gradient_end": "#9c27b0",
    "plot_line_isobaric": "#00bcd4",
    "plot_line_isochoric": "#00e676",
    "plot_line_isothermal": "#ff1744",
    "plot_point_color": "#ffeb3b",
    "plot_text_color": "#e0e0e0",
    "plot_grid_color": "#4a4a6e",
    "plot_title_color": "#00bcd4",
    "plot_legend_bg": "#1f1f3a",
}

LIGHT_THEME_COLORS = DARK_THEME_COLORS # Untuk saat ini, kita gunakan tema gelap sebagai basis

# --- Inisialisasi Session State ---
if 'theme' not in st.session_state:
    st.session_state.theme = "Gelap" # Default ke tema gelap
if 'plot_data' not in st.session_state:
    st.session_state.plot_data = None
if 'plot_title' not in st.session_state:
    st.session_state.plot_title = None

current_theme = DARK_THEME_COLORS

# --- Custom CSS ---
st.markdown(f"""
    <style>
        /* General styling */
        .stApp {{
            background: linear-gradient(135deg, {current_theme["bg_primary"]} 0%, {current_theme["bg_secondary"]} 100%);
            color: {current_theme["text_primary"]};
            font-family: 'Inter', sans-serif;
        }}
        .block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }}
        h1 {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            background: linear-gradient(90deg, {current_theme["header_gradient_start"]}, {current_theme["header_gradient_end"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
        }}
        .section-header {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: {current_theme["text_primary"]};
            font-size: 2rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            border-bottom: 2px solid {current_theme["border_neon_blue"]};
            padding-bottom: 0.5rem;
        }}
        .section-header i {{
            margin-right: 1rem;
            font-size: 1.8rem;
            color: {current_theme["text_neon_blue"]};
        }}
        .subsection-header {{
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: {current_theme["text_primary"]};
            font-size: 1.25rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }}
        /* Input, Selectbox, and Button Styling */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea,
        .stNumberInput > div > label + div > div > input,
        .stSelectbox > div > div {{
            background-color: {current_theme["input_bg"]};
            border: 1px solid {current_theme["input_border"]};
            color: {current_theme["text_primary"]};
            border-radius: 0.5rem;
            transition: all 0.2s ease-in-out;
        }}
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > label + div > div > input:focus,
        .stSelectbox > div > div:hover {{
            border-color: {current_theme["input_focus_border"]};
            box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.4);
        }}
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
        }}
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px {current_theme["button_shadow"]};
            opacity: 0.9;
        }}
        /* Result Box */
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
            color: {current_theme["text_neon_blue"]};
            font-size: 1.4rem;
        }}
        .result-box span {{
            color: {current_theme["plot_point_color"]};
            font-weight: bold;
        }}
        /* Sidebar Styling */
        .stSidebar {{
            background-color: {current_theme["bg_sidebar"]};
            border-right: 1px solid {current_theme["border_color"]};
        }}
        .sidebar-header {{
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: {current_theme["text_neon_blue"]};
            font-size: 1.8rem;
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid {current_theme["border_color"]};
        }}
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {{ border-bottom: 1px solid {current_theme["border_color"]}; }}
        .stTabs [data-baseweb="tab"] {{ background-color: {current_theme["bg_secondary"]}; }}
        .stTabs [data-baseweb="tab"]:hover {{ background-color: {current_theme["bg_card"]}; color: {current_theme["text_primary"]}; }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background-color: {current_theme["bg_card"]};
            color: {current_theme["text_neon_blue"]};
            border-bottom: 3px solid {current_theme["border_neon_blue"]};
        }}
        .stMarkdown a {{ color: {current_theme["text_neon_blue"]}; text-decoration: none; }}
        .stMarkdown a:hover {{ text-decoration: underline; }}
        .stMarkdown hr {{ border-top: 1px solid {current_theme["border_color"]}; }}
        /* Contact Form Specific Styling */
        form.contact-form {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin-top: 1rem;
        }}
        form.contact-form input, form.contact-form textarea {{
            background-color: {current_theme["input_bg"]};
            border: 1px solid {current_theme["input_border"]};
            color: {current_theme["text_primary"]};
            padding: 0.8rem 1.2rem;
            border-radius: 0.5rem;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
        }}
        form.contact-form input::placeholder, form.contact-form textarea::placeholder {{
             color: #888;
        }}
        form.contact-form input:focus, form.contact-form textarea:focus {{
            border-color: {current_theme["input_focus_border"]};
            box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.4);
            outline: none;
        }}
        form.contact-form button {{
            background: {current_theme["button_bg"]};
            color: {current_theme["button_text"]};
            font-weight: 600;
            padding: 0.8rem 1.5rem;
            border-radius: 0.5rem;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            width: auto;
            align-self: flex-start;
        }}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

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
    if v1 <= 0 or v2 <= 0:
        return float('nan'), float('nan'), float('nan')
    W = n * R * T * math.log(v2 / v1)
    dU = 0
    Q = W
    return W, dU, Q

# --- Sidebar Navigasi ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">MENU</div>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Beranda", "Kalkulator Termodinamika", "Konverter Satuan", "Visualisasi Proses", "Tentang Aplikasi"],
        icons=["house-door", "calculator", "arrow-left-right", "graph-up", "info-circle"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": current_theme["bg_sidebar"]},
            "icon": {"color": current_theme["text_neon_blue"], "font-size": "1.2rem"},
            "nav-link": {
                "font-size": "1.1rem", "text-align": "left", "margin": "0px",
                "padding": "0.75rem 1rem", "border-radius": "0.5rem",
                "color": current_theme["text_primary"], "background-color": current_theme["bg_secondary"],
                "border": f"1px solid {current_theme['border_color']}",
                "--hover-color": current_theme["bg_hover_sidebar_item"],
            },
            "nav-link-selected": {
                "background-color": current_theme["bg_active_sidebar_item"],
                "color": current_theme["button_text"],
            },
        }
    )

# --- Konten Halaman ---

if selected == "Beranda":
    st.markdown("<h1>ThermoCalc Lab</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p style="text-align: center; font-size: 1.25rem; color: #a0aec0; margin-bottom: 2rem;">
            Kalkulator Termodinamika, Konverter Satuan, dan Visualisasi dalam Satu Aplikasi
        </p>
    """, unsafe_allow_html=True)

    # --- UPDATED: Changed the GIF link to a more reliable one ---
    st.markdown("""
        <p style="text-align: center; max-width: 800px; margin: auto; line-height: 1.6;">
            <strong>ThermoCalc Lab</strong> adalah alat online gratis yang dirancang untuk memudahkan Anda dalam memahami dan menghitung proses termodinamika. Aplikasi ini menyediakan kalkulator interaktif, konverter satuan, dan visualisasi grafik P-V.
            <br><br>
            Silakan pilih alat yang sesuai dari menu di samping untuk memulai!
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: 4rem; text-align: center;">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: {current_theme["text_neon_purple"]};">DIBUAT OLEH: KELOMPOK 12 (1C - ANALISIS KIMIA)</h3>', unsafe_allow_html=True)
    st.markdown("""
        <ul style="list-style: none; padding: 0; display: inline-block; text-align: left;">
            <li>1. Bagus Inayatullah Pramudana Herman (2460342)</li>
            <li>2. Ihtiathus Syar'iyah (2460387)</li>
            <li>3. Nafisa Alya Rahma (2460451)</li>
            <li>4. Riko Putra Pamungkas (2460499)</li>
            <li>5. Zayyum Adji Lubis (2460546)</li>
        </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


elif selected == "Kalkulator Termodinamika":
    st.markdown('<h2 class="section-header"><i class="fas fa-calculator"></i> Kalkulator Termodinamika</h2>', unsafe_allow_html=True)

    process_type = st.selectbox(
        "Pilih Jenis Proses Termodinamika:",
        ("Isobarik", "Isokhorik", "Isotermal")
    )

    st.markdown(f'<div class="subsection-header">Input untuk Proses {process_type}</div>', unsafe_allow_html=True)
    
    with st.container():
        if process_type == "Isobarik":
            p = st.number_input("Tekanan (p) dalam Pascal", min_value=0.0, format="%.2f")
            v1 = st.number_input("Volume Awal (V₁) dalam m³", min_value=0.0, format="%.4f")
            v2 = st.number_input("Volume Akhir (V₂) dalam m³", min_value=0.0, format="%.4f")
            n = st.number_input("Jumlah mol (n)", min_value=0.0, format="%.4f")
            t1 = st.number_input("Suhu Awal (T₁) dalam Kelvin", min_value=0.0, format="%.2f")
            t2 = st.number_input("Suhu Akhir (T₂) dalam Kelvin", min_value=0.0, format="%.2f")

            if st.button("Hitung Isobarik"):
                W, dU, Q = calculate_isobaric(p, v1, v2, n, t1, t2)
                st.markdown(f'<div class="result-box"><h3>Hasil Perhitungan:</h3><p>Usaha (W): <span>{W:.4f} J</span></p><p>Energi Dalam (ΔU): <span>{dU:.4f} J</span></p><p>Kalor (Q): <span>{Q:.4f} J</span></p></div>', unsafe_allow_html=True)
                st.session_state.plot_data = {'type': 'isobaric', 'p': p, 'v1': v1, 'v2': v2}
                st.session_state.plot_title = f"Grafik P-V Proses Isobarik (P={p:.2f} Pa)"

        elif process_type == "Isokhorik":
            n = st.number_input("Jumlah mol (n)", min_value=0.0, format="%.4f")
            t1 = st.number_input("Suhu Awal (T₁) dalam Kelvin", min_value=0.0, format="%.2f")
            t2 = st.number_input("Suhu Akhir (T₂) dalam Kelvin", min_value=0.0, format="%.2f")
            v_const = st.number_input("Volume Konstan (V) dalam m³", min_value=0.01, format="%.4f")

            if st.button("Hitung Isokhorik"):
                W, dU, Q = calculate_isochoric(n, t1, t2)
                st.markdown(f'<div class="result-box"><h3>Hasil Perhitungan:</h3><p>Usaha (W): <span>{W:.4f} J</span></p><p>Energi Dalam (ΔU): <span>{dU:.4f} J</span></p><p>Kalor (Q): <span>{Q:.4f} J</span></p></div>', unsafe_allow_html=True)
                st.session_state.plot_data = {'type': 'isochoric', 'n': n, 't1': t1, 't2': t2, 'v_const': v_const}
                st.session_state.plot_title = f"Grafik P-V Proses Isokhorik (V={v_const:.2f} m³)"

        elif process_type == "Isotermal":
            n = st.number_input("Jumlah mol (n)", min_value=0.0, format="%.4f")
            T = st.number_input("Suhu (T) dalam Kelvin", min_value=0.01, format="%.2f")
            v1 = st.number_input("Volume Awal (V₁) dalam m³", min_value=0.01, format="%.4f")
            v2 = st.number_input("Volume Akhir (V₂) dalam m³", min_value=0.01, format="%.4f")

            if st.button("Hitung Isotermal"):
                W, dU, Q = calculate_isothermal(n, T, v1, v2)
                st.markdown(f'<div class="result-box"><h3>Hasil Perhitungan:</h3><p>Usaha (W): <span>{W:.4f} J</span></p><p>Energi Dalam (ΔU): <span>{dU:.4f} J</span></p><p>Kalor (Q): <span>{Q:.4f} J</span></p></div>', unsafe_allow_html=True)
                st.session_state.plot_data = {'type': 'isothermal', 'n': n, 'T': T, 'v1': v1, 'v2': v2}
                st.session_state.plot_title = f"Grafik P-V Proses Isotermal (T={T:.2f} K)"

elif selected == "Konverter Satuan":
    st.markdown('<h2 class="section-header"><i class="fas fa-exchange-alt"></i> Konverter Satuan</h2>', unsafe_allow_html=True)

    category = st.selectbox("Pilih Kategori Konversi:", ["Suhu", "Tekanan", "Volume"])

    if category == "Suhu":
        units = ("Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)")
        col1, col2 = st.columns(2)
        from_unit = col1.selectbox("Dari", units, index=0)
        to_unit = col2.selectbox("Ke", units, index=1)
        value = st.number_input(f"Masukkan nilai dalam {from_unit}", format="%.2f")

        if st.button("Konversi Suhu"):
            if from_unit == to_unit:
                result = value
            else:
                k = 0
                if from_unit == "Celsius (°C)": k = value + 273.15
                elif from_unit == "Fahrenheit (°F)": k = (value - 32) * 5/9 + 273.15
                elif from_unit == "Kelvin (K)": k = value

                if to_unit == "Celsius (°C)": result = k - 273.15
                elif to_unit == "Fahrenheit (°F)": result = (k - 273.15) * 9/5 + 32
                elif to_unit == "Kelvin (K)": result = k
            
            st.success(f"**Hasil:** {value:.2f} {from_unit} = **{result:.2f} {to_unit}**")

    elif category == "Tekanan":
        units = ("Pascal (Pa)", "Atmosfer (atm)", "mmHg")
        factors = {"Pascal (Pa)": 1.0, "Atmosfer (atm)": 101325.0, "mmHg": 133.322}
        
        col1, col2 = st.columns(2)
        from_unit = col1.selectbox("Dari", units, index=1)
        to_unit = col2.selectbox("Ke", units, index=0)
        value = st.number_input(f"Masukkan nilai dalam {from_unit}", format="%.5f")

        if st.button("Konversi Tekanan"):
            pascal = value * factors[from_unit]
            result = pascal / factors[to_unit]
            st.success(f"**Hasil:** {value:.5f} {from_unit} = **{result:.5f} {to_unit}**")

    elif category == "Volume":
        units = ("Meter Kubik (m³)", "Sentimeter Kubik (cm³)", "Milimeter Kubik (mm³)")
        factors = {"Meter Kubik (m³)": 1.0, "Sentimeter Kubik (cm³)": 1e-6, "Milimeter Kubik (mm³)": 1e-9}

        col1, col2 = st.columns(2)
        from_unit = col1.selectbox("Dari", units, index=0)
        to_unit = col2.selectbox("Ke", units, index=1)
        value = st.number_input(f"Masukkan nilai dalam {from_unit}", format="%.9f")

        if st.button("Konversi Volume"):
            m3 = value * factors[from_unit]
            result = m3 / factors[to_unit]
            st.success(f"**Hasil:** {value:.9f} {from_unit} = **{result:.9f} {to_unit}**")


elif selected == "Visualisasi Proses":
    st.markdown('<h2 class="section-header"><i class="fas fa-chart-line"></i> Visualisasi Proses Termodinamika</h2>', unsafe_allow_html=True)

    if st.session_state.plot_data:
        plot_type = st.session_state.plot_data['type']
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_facecolor(current_theme["bg_card"])
        fig.patch.set_facecolor(current_theme["bg_card"])

        ax.set_xlabel('Volume (m³)', color=current_theme["plot_text_color"])
        ax.set_ylabel('Tekanan (Pa)', color=current_theme["plot_text_color"])
        ax.set_title(st.session_state.plot_title, color=current_theme["plot_title_color"])
        ax.tick_params(axis='x', colors=current_theme["plot_text_color"])
        ax.tick_params(axis='y', colors=current_theme["plot_text_color"])
        ax.grid(True, linestyle='--', alpha=0.5, color=current_theme["plot_grid_color"])

        if plot_type == 'isobaric':
            p, v1, v2 = st.session_state.plot_data['p'], st.session_state.plot_data['v1'], st.session_state.plot_data['v2']
            v_plot = np.linspace(min(v1, v2), max(v1, v2), 100)
            p_plot = np.full_like(v_plot, p)
            ax.plot(v_plot, p_plot, label='Isobarik', color=current_theme["plot_line_isobaric"], linewidth=3)
            ax.plot([v1, v2], [p, p], 'o', color=current_theme["plot_point_color"], markersize=8)

        elif plot_type == 'isochoric':
            n, t1, t2, v_const = st.session_state.plot_data['n'], st.session_state.plot_data['t1'], st.session_state.plot_data['t2'], st.session_state.plot_data['v_const']
            if v_const > 0:
                p1, p2 = (n * R * t1) / v_const, (n * R * t2) / v_const
                p_plot = np.linspace(min(p1, p2), max(p1, p2), 100)
                v_plot = np.full_like(p_plot, v_const)
                ax.plot(v_plot, p_plot, label='Isokhorik', color=current_theme["plot_line_isochoric"], linewidth=3)
                ax.plot([v_const, v_const], [p1, p2], 'o', color=current_theme["plot_point_color"], markersize=8)

        elif plot_type == 'isothermal':
            n, T, v1, v2 = st.session_state.plot_data['n'], st.session_state.plot_data['T'], st.session_state.plot_data['v1'], st.session_state.plot_data['v2']
            if v1 > 0 and v2 > 0 and T > 0:
                v_range = np.linspace(min(v1, v2) * 0.8, max(v1, v2) * 1.2, 200)
                p_range = (n * R * T) / v_range
                ax.plot(v_range, p_range, label='Isotermal', color=current_theme["plot_line_isothermal"], linewidth=3)
                p1, p2 = (n * R * T) / v1, (n * R * T) / v2
                ax.plot([v1, v2], [p1, p2], 'o', color=current_theme["plot_point_color"], markersize=8)

        ax.legend(facecolor=current_theme["plot_legend_bg"])
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("Lakukan perhitungan di kalkulator terlebih dahulu untuk melihat grafik P-V dari proses yang dihitung.")

elif selected == "Tentang Aplikasi":
    st.markdown('<h2 class="section-header"><i class="fas fa-info-circle"></i> Tentang Aplikasi</h2>', unsafe_allow_html=True)
    tab_materi, tab_cara, tab_contoh, tab_kontak = st.tabs(["Materi", "Cara Penggunaan", "Contoh Soal", "Kontak"])

    with tab_materi:
        st.markdown('<h3>Dasar-dasar Termodinamika</h3>', unsafe_allow_html=True)
        st.markdown("""
            Termodinamika adalah cabang fisika yang mempelajari hubungan antara **panas, kerja, dan energi**. Ini menjelaskan bagaimana energi diubah dari satu bentuk ke bentuk lain dan bagaimana hal itu mempengaruhi materi. Konsep-konsep ini sangat penting dalam kimia, teknik, dan ilmu-ilmu fisika lainnya.
            <h4>Hukum-hukum Fundamental Termodinamika:</h4>
            <ul>
                <li><strong>Hukum Awal (Zeroth Law):</strong> Jika dua sistem berada dalam kesetimbangan termal dengan sistem ketiga, maka mereka berada dalam kesetimbangan termal satu sama lain.</li>
                <li><strong>Hukum Pertama:</strong> Energi tidak dapat diciptakan atau dimusnahkan. Perubahan energi dalam (ΔU) suatu sistem sama dengan kalor (Q) yang ditambahkan ke sistem dikurangi kerja (W) yang dilakukan oleh sistem.</li>
            </ul>
            """, unsafe_allow_html=True)
        st.latex(r'''\Delta U = Q - W''')
        st.markdown("""
            <ul>
                <li><strong>Hukum Kedua:</strong> Entropi total dari sistem terisolasi cenderung meningkat seiring waktu, mencapai nilai maksimum.</li>
                <li><strong>Hukum Ketiga:</strong> Entropi sistem mendekati nilai minimum konstan saat suhu mendekati nol absolut.</li>
            </ul>
            <hr>
            <h3>Proses-Proses Termodinamika</h3>
            <p>Aplikasi ini fokus pada tiga proses fundamental untuk gas ideal:</p>
            
            <h4>1. Proses Isobarik (Tekanan Konstan)</h4>
            <p>Proses isobarik terjadi pada tekanan konstan (ΔP = 0). Ketika gas memuai atau menyusut pada tekanan konstan, kerja dilakukan. Secara historis, studi tentang hubungan volume dan suhu pada tekanan konstan oleh <strong>Joseph Louis Gay-Lussac</strong> pada awal abad ke-19 menjadi dasar bagi pemahaman proses ini.</p>
            <ul>
                <li><strong>Usaha (W):</strong> Kerja yang dilakukan oleh gas adalah hasil kali tekanan dengan perubahan volume.</li>
            </ul>
            """, unsafe_allow_html=True)
        st.latex(r'''W = P \cdot (V_2 - V_1) = P \Delta V''')
        st.markdown("""
            <ul>
                <li><strong>Perubahan Energi Dalam (ΔU):</strong> Untuk gas ideal monoatomik, perubahan energi dalam tergantung pada perubahan suhu.</li>
            </ul>
            """, unsafe_allow_html=True)
        st.latex(r'''\Delta U = \frac{3}{2} n R (T_2 - T_1) = \frac{3}{2} n R \Delta T''')
        st.markdown("""
            <ul>
                <li><strong>Kalor (Q):</strong> Menurut Hukum Pertama Termodinamika, kalor yang ditransfer sama dengan jumlah kerja dan perubahan energi dalam.</li>
            </ul>
            """, unsafe_allow_html=True)
        st.latex(r'''Q = \Delta U + W''')

        st.markdown("""
            <h4>2. Proses Isokhorik (Volume Konstan)</h4>
            <p>Proses isokhorik terjadi pada volume konstan (ΔV = 0). Karena tidak ada perubahan volume, tidak ada kerja yang dilakukan oleh atau pada sistem. Penyelidikan oleh <strong>Guillaume Amontons</strong> pada abad ke-17 yang menunjukkan hubungan antara tekanan dan suhu pada volume konstan merupakan cikal bakal dari konsep ini.</p>
            <ul><li><strong>Usaha (W):</strong> Karena tidak ada perubahan volume (ΔV = 0), maka tidak ada kerja yang dilakukan.</li></ul>
            """, unsafe_allow_html=True)
        st.latex(r'''W = 0''')
        st.markdown("""
            <ul><li><strong>Perubahan Energi Dalam (ΔU) & Kalor (Q):</strong> Karena kerja adalah nol, semua kalor yang ditransfer digunakan untuk mengubah energi dalam sistem.</li></ul>
            """, unsafe_allow_html=True)
        st.latex(r'''Q = \Delta U = \frac{3}{2} n R \Delta T''')

        st.markdown("""
            <h4>3. Proses Isotermal (Suhu Konstan)</h4>
            <p>Proses isotermal terjadi pada suhu konstan (ΔT = 0). Hubungan terbalik antara tekanan dan volume pada suhu konstan pertama kali dijelaskan oleh <strong>Robert Boyle</strong> pada abad ke-17 (Hukum Boyle). Karena suhu konstan, energi dalam gas ideal juga konstan.</p>
            <ul><li><strong>Perubahan Energi Dalam (ΔU):</strong> Karena suhu tidak berubah (ΔT = 0), energi dalam sistem tetap konstan.</li></ul>
            """, unsafe_allow_html=True)
        st.latex(r'''\Delta U = 0''')
        st.markdown("""
            <ul><li><strong>Usaha (W) & Kalor (Q):</strong> Berdasarkan Hukum Pertama, karena ΔU = 0, semua kalor yang ditransfer diubah menjadi kerja. Kerja dihitung menggunakan integral.</li></ul>
            """, unsafe_allow_html=True)
        st.latex(r'''Q = W = n R T \ln\left(\frac{V_2}{V_1}\right)''')
        
        st.markdown("""
            <hr>
            <h4>Sumber</h4>
            <ul>
                <li>Serway, R. A., & Jewett, J. W. (2014). <em>Physics for Scientists and Engineers with Modern Physics.</em> Cengage Learning.</li>
                <li>Atkins, P., & de Paula, J. (2014). <em>Atkins' Physical Chemistry.</em> Oxford University Press.</li>
                <li>Khan Academy. (n.d.). <em>Thermodynamics.</em> Diakses dari <a href="https://www.khanacademy.org/science/physics/thermodynamics" target="_blank">khanacademy.org</a></li>
            </ul>
        """, unsafe_allow_html=True)

    with tab_cara:
        st.markdown('<h3>Cara Menggunakan ThermoCalc Lab:</h3>', unsafe_allow_html=True)
        st.markdown("""
            <ol>
                <li><strong>Navigasi:</strong> Gunakan menu di sisi kiri untuk berpindah antar halaman.</li>
                <li><strong>Kalkulator Termodinamika:</strong>
                    <ul>
                        <li>Gunakan dropdown untuk memilih jenis proses (Isobarik, Isokhorik, atau Isotermal).</li>
                        <li>Masukkan nilai yang diperlukan pada kolom input yang muncul.</li>
                        <li>Klik tombol "Hitung" untuk melihat hasilnya.</li>
                    </ul>
                </li>
                <li><strong>Konverter Satuan:</strong>
                    <ul>
                        <li>Pilih kategori (Suhu, Tekanan, Volume).</li>
                        <li>Pilih satuan asal ("Dari") dan satuan tujuan ("Ke").</li>
                        <li>Masukkan nilai yang ingin dikonversi dan klik tombol "Konversi".</li>
                    </ul>
                </li>
                <li><strong>Visualisasi Proses:</strong>
                    <ul>
                        <li>Halaman ini akan otomatis menampilkan grafik P-V dari perhitungan terakhir yang Anda lakukan di halaman "Kalkulator Termodinamika".</li>
                    </ul>
                </li>
            </ol>
        """, unsafe_allow_html=True)

    with tab_contoh:
        st.markdown('<h3>Contoh Soal: Proses Isobarik</h3>', unsafe_allow_html=True)
        st.markdown("""
            <p>Suatu gas ideal mengalami proses isobarik pada tekanan konstan <b>100,000 Pa</b>. Volume gas berubah dari <b>0.1 m³</b> menjadi <b>0.3 m³</b>. Jika jumlah mol gas adalah <b>1 mol</b>, suhu awal <b>300 K</b>, dan suhu akhir <b>900 K</b>, hitunglah W, ΔU, dan Q.</p>
            <p><strong>Penyelesaian menggunakan kalkulator:</strong></p>
            <ol>
                <li>Buka halaman "Kalkulator Termodinamika".</li>
                <li>Pilih "Isobarik" dari dropdown.</li>
                <li>Masukkan nilai-nilai: P = 100000, V₁ = 0.1, V₂ = 0.3, n = 1, T₁ = 300, T₂ = 900.</li>
                <li>Klik "Hitung Isobarik", dan hasilnya akan langsung muncul.</li>
            </ol>
        """, unsafe_allow_html=True)

    with tab_kontak:
        st.markdown('<h3>Hubungi Kami</h3>', unsafe_allow_html=True)
        st.markdown(f"""
            <p>Punya pertanyaan atau masukan? Silakan tinggalkan pesan Anda.</p>
            <form class="contact-form" action="https://formsubmit.co/ajizayum@gmail.com" method="POST">
                 <input type="email" name="email" placeholder="Email Anda" required>
                 <textarea name="message" placeholder="Pesan Anda" required rows="4"></textarea>
                 <button type="submit">Kirim</button>
            </form>
            <p style="margin-top: 2rem; color: {current_theme["text_secondary"]};">
                Anda juga bisa menemukan kami di GitHub: <a href="https://github.com/zayyum-a-l" target="_blank">Profil GitHub Kami</a>
            </p>
        """, unsafe_allow_html=True)
