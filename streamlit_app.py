import streamlit as st
import math

# Konstanta gas ideal
R = 8.314

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(layout="wide", page_title="Kalkulator Termodinamika & Konverter")

# --- Custom CSS untuk UI/UX ---
st.markdown("""
    <style>
        /* Mengatur font utama dan latar belakang gradien untuk seluruh aplikasi */
        .stApp {
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
        }
        /* Styling untuk judul utama (H1) */
        h1 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            letter-spacing: -0.05em;
            background: linear-gradient(90deg, #a78bfa, #c4b5fd); /* Gradien teks */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            color: transparent;
            text-align: center;
            font-size: 3.5rem; /* Ukuran font lebih besar */
            margin-bottom: 0.5rem;
        }
        /* Styling untuk subheader (deskripsi) */
        p.subheader {
            font-weight: 300;
            color: #a0aec0;
            text-align: center;
            font-size: 1.125rem; /* text-lg */
            margin-bottom: 2rem;
        }
        /* Padding untuk container utama */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Styling untuk semua input teks dan textarea */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #2f3a4b; /* Warna latar belakang input yang lebih gelap */
            border: 1px solid #475569; /* Border yang lebih jelas */
            color: #e2e8f0;
            padding: 0.75rem 1rem;
            border-radius: 0.625rem; /* Sudut membulat */
            transition: all 0.3s ease;
        }
        /* Efek fokus untuk input teks dan textarea */
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            border-color: #6366f1; /* Border indigo saat fokus */
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3); /* Cincin fokus */
            background-color: #3a475a; /* Sedikit lebih terang saat fokus */
        }
        /* Placeholder styling */
        input::placeholder, textarea::placeholder {
            color: #94a3b8; /* Warna placeholder yang lebih terang */
        }

        /* Styling umum untuk semua tombol */
        div.stButton > button {
            background: linear-gradient(90deg, #3b82f6, #2563eb); /* Gradien biru */
            color: white;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
            width: 100%; /* Lebar penuh */
            margin-top: 1rem; /* Jarak dari elemen di atasnya */
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
            opacity: 0.95;
        }
        /* Styling untuk kotak hasil perhitungan */
        .result-box {
            background: linear-gradient(145deg, #2d3748, #1a202c); /* Gradien untuk kotak hasil */
            border: 1px solid #475569;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            padding: 1.5rem;
            border-radius: 1rem;
            margin-top: 1.5rem;
        }
        .result-box h3 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            color: #818cf8; /* Warna indigo terang untuk judul hasil */
            font-size: 1.25rem;
            margin-bottom: 0.75rem;
            display: flex; /* Untuk menyelaraskan ikon */
            align-items: center;
        }
        .result-box p {
            color: #cbd5e1;
        }
        /* Styling untuk Selectbox Streamlit */
        .stSelectbox > div > label {
            color: #e2e8f0;
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .stSelectbox > div > div {
            background-color: #2f3a4b;
            border-radius: 0.625rem;
            border: 1px solid #475569;
            color: #e2e8f0; /* Warna teks di selectbox */
        }
        .stSelectbox > div > div:hover {
            border-color: #6366f1;
        }
        /* Styling untuk header bagian (H2) */
        .section-header {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: #e2e8f0;
            font-size: 2rem; /* Ukuran font lebih besar untuk header bagian */
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
        }
        .section-header i {
            margin-right: 0.75rem;
        }
        /* Styling untuk sub-subheader (H3) */
        .subsection-header {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: #cbd5e1;
            font-size: 1.125rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        /* Styling untuk kolom di Streamlit */
        .st-emotion-cache-1cypcdb { /* Menargetkan container kolom Streamlit */
            gap: 1.5rem; /* Menambahkan jarak antar kolom */
        }
    </style>
    <!-- Font Awesome untuk ikon -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

# --- Header Aplikasi ---
st.title("ThermoCalc Lab")
st.markdown('<p class="subheader">Kalkulator dan Konverter untuk Proses Termodinamika.</p>', unsafe_allow_html=True)

# Membagi tata letak menjadi dua kolom utama (kalkulator di kiri, konverter di kanan)
col_calc, col_conv = st.columns([1, 2]) # Mengubah nama kolom kanan

with col_calc:
    st.markdown('<h2 class="section-header"><i class="fas fa-calculator text-blue-400"></i> Kalkulator Proses</h2>', unsafe_allow_html=True)

    # Menggunakan st.session_state untuk mengelola tab aktif
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Isobarik"

    # Tombol tab kustom (simulasi)
    tab_cols = st.columns(3)
    with tab_cols[0]:
        if st.button("Isobarik", key="tab_isobaric"):
            st.session_state.active_tab = "Isobarik"
    with tab_cols[1]:
        if st.button("Isokhorik", key="tab_isochoric"):
            st.session_state.active_tab = "Isokhorik"
    with tab_cols[2]:
        if st.button("Isotermal", key="tab_isothermal"):
            st.session_state.active_tab = "Isotermal"

    # Menambahkan CSS untuk tombol tab aktif
    st.markdown(f"""
        <style>
            div.stButton > button[data-testid="stButton-primary"]:nth-child(1) {{
                background-color: {'#4f46e5' if st.session_state.active_tab == 'Isobarik' else '#2f3a4b'};
                color: {'white' if st.session_state.active_tab == 'Isobarik' else '#cbd5e1'};
                box-shadow: {'0 4px 10px rgba(79, 70, 229, 0.4)' if st.session_state.active_tab == 'Isobarik' else 'none'};
                transform: {'translateY(-2px)' if st.session_state.active_tab == 'Isobarik' else 'none'};
                border-radius: 0.75rem 0 0 0.75rem; /* Rounded top-left, bottom-left */
            }}
            div.stButton > button[data-testid="stButton-primary"]:nth-child(2) {{
                background-color: {'#4f46e5' if st.session_state.active_tab == 'Isokhorik' else '#2f3a4b'};
                color: {'white' if st.session_state.active_tab == 'Isokhorik' else '#cbd5e1'};
                box-shadow: {'0 4px 10px rgba(79, 70, 229, 0.4)' if st.session_state.active_tab == 'Isokhorik' else 'none'};
                transform: {'translateY(-2px)' if st.session_state.active_tab == 'Isokhorik' else 'none'};
                border-radius: 0;
            }}
            div.stButton > button[data-testid="stButton-primary"]:nth-child(3) {{
                background-color: {'#4f46e5' if st.session_state.active_tab == 'Isotermal' else '#2f3a4b'};
                color: {'white' if st.session_state.active_tab == 'Isotermal' else '#cbd5e1'};
                box-shadow: {'0 4px 10px rgba(79, 70, 229, 0.4)' if st.session_state.active_tab == 'Isotermal' else 'none'};
                transform: {'translateY(-2px)' if st.session_state.active_tab == 'Isotermal' else 'none'};
                border-radius: 0 0.75rem 0.75rem 0; /* Rounded top-right, bottom-right */
            }}
        </style>
    """, unsafe_allow_html=True)


    # Konten berdasarkan tab aktif
    if st.session_state.active_tab == "Isobarik":
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
                        W = p * (v2 - v1)
                        dU = 1.5 * n * R * (t2 - t1)
                        Q = W + dU
                        st.markdown(f"""
                            <div class="result-box">
                                <h3><i class="fas fa-flask mr-2"></i> Hasil Perhitungan:</h3>
                                <p>Usaha (W): <span style="font-weight: 600; color: white;">{W:.4f} J</span></p>
                                <p>Energi Dalam (ΔU): <span style="font-weight: 600; color: white;">{dU:.4f} J</span></p>
                                <p>Kalor (Q): <span style="font-weight: 600; color: white;">{Q:.4f} J</span></p>
                            </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}. Harap periksa kembali semua input.")
            else:
                st.warning("Harap masukkan semua nilai numerik yang valid untuk proses Isobarik.")

    elif st.session_state.active_tab == "Isokhorik":
        st.markdown('<p class="subsection-header">Input untuk Proses Isokhorik</p>', unsafe_allow_html=True)
        n = st.number_input("Jumlah mol (n)", min_value=0.0, format="%.4f", key="isok_n_input")
        t1 = st.number_input("Suhu Awal (T₁) dalam Kelvin", min_value=0.0, format="%.2f", key="isok_t1_input")
        t2 = st.number_input("Suhu Akhir (T₂) dalam Kelvin", min_value=0.0, format="%.2f", key="isok_t2_input")

        if st.button("Hitung Isokhorik", key="calc_isokhoric_btn"):
            if n is not None and t1 is not None and t2 is not None:
                try:
                    if t1 < 0 or t2 < 0 or n < 0:
                        st.error("Suhu dan Jumlah mol tidak boleh negatif.")
                    else:
                        W = 0
                        dU = 1.5 * n * R * (t2 - t1)
                        Q = dU
                        st.markdown(f"""
                            <div class="result-box">
                                <h3><i class="fas fa-flask mr-2"></i> Hasil Perhitungan:</h3>
                                <p>Usaha (W): <span style="font-weight: 600; color: white;">{W:.4f} J</span></p>
                                <p>Energi Dalam (ΔU): <span style="font-weight: 600; color: white;">{dU:.4f} J</span></p>
                                <p>Kalor (Q): <span style="font-weight: 600; color: white;">{Q:.4f} J</span></p>
                            </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}. Harap periksa kembali semua input.")
            else:
                st.warning("Harap masukkan semua nilai numerik yang valid untuk proses Isokhorik.")

    elif st.session_state.active_tab == "Isotermal":
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
                        W = n * R * T * math.log(v2 / v1)
                        dU = 0
                        Q = W
                        st.markdown(f"""
                            <div class="result-box">
                                <h3><i class="fas fa-flask mr-2"></i> Hasil Perhitungan:</h3>
                                <p>Usaha (W): <span style="font-weight: 600; color: white;">{W:.4f} J</span></p>
                                <p>Energi Dalam (ΔU): <span style="font-weight: 600; color: white;">{dU:.4f} J</span></p>
                                <p>Kalor (Q): <span style="font-weight: 600; color: white;">{Q:.4f} J</span></p>
                            </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}. Harap periksa kembali semua input.")
            else:
                st.warning("Harap masukkan semua nilai numerik yang valid untuk proses Isotermal.")

with col_conv: # Menggunakan kolom yang sama untuk konverter
    st.markdown('<h2 class="section-header"><i class="fas fa-exchange-alt text-green-400"></i> Konverter Satuan</h2>', unsafe_allow_html=True)

    st.markdown("### Suhu")
    col1, col2, col3 = st.columns(3)

    with col1:
        celsius = st.number_input("Celsius (°C)", format="%.2f", key="conv_celsius")
        if celsius is not None:
            fahrenheit_conv_c = (celsius * 9/5) + 32
            kelvin_conv_c = celsius + 273.15
        else:
            fahrenheit_conv_c = None
            kelvin_conv_c = None

    with col2:
        fahrenheit = st.number_input("Fahrenheit (°F)", format="%.2f", key="conv_fahrenheit")
        if fahrenheit is not None:
            celsius_conv_f = (fahrenheit - 32) * 5/9
            kelvin_conv_f = celsius_conv_f + 273.15
        else:
            celsius_conv_f = None
            kelvin_conv_f = None

    with col3:
        kelvin = st.number_input("Kelvin (K)", format="%.2f", key="conv_kelvin")
        if kelvin is not None:
            celsius_conv_k = kelvin - 273.15
            fahrenheit_conv_k = (celsius_conv_k * 9/5) + 32
        else:
            celsius_conv_k = None
            fahrenheit_conv_k = None

    # Tampilkan hasil konversi suhu di bawah input yang berubah
    if st.session_state.get('conv_celsius') != st.session_state.get('prev_celsius', None):
        if celsius is not None:
            st.info(f"Fahrenheit: {fahrenheit_conv_c:.2f} °F | Kelvin: {kelvin_conv_c:.2f} K")
        st.session_state.prev_celsius = celsius
    elif st.session_state.get('conv_fahrenheit') != st.session_state.get('prev_fahrenheit', None):
        if fahrenheit is not None:
            st.info(f"Celsius: {celsius_conv_f:.2f} °C | Kelvin: {kelvin_conv_f:.2f} K")
        st.session_state.prev_fahrenheit = fahrenheit
    elif st.session_state.get('conv_kelvin') != st.session_state.get('prev_kelvin', None):
        if kelvin is not None:
            st.info(f"Celsius: {celsius_conv_k:.2f} °C | Fahrenheit: {fahrenheit_conv_k:.2f} °F")
        st.session_state.prev_kelvin = kelvin


    st.markdown("### Tekanan")
    col4, col5, col6 = st.columns(3)

    with col4:
        atm = st.number_input("Atmosfer (atm)", format="%.5f", key="conv_atm")
        if atm is not None:
            mmhg_conv_atm = atm * 760
            pascal_conv_atm = atm * 101325
        else:
            mmhg_conv_atm = None
            pascal_conv_atm = None

    with col5:
        mmhg = st.number_input("mmHg", format="%.2f", key="conv_mmhg")
        if mmhg is not None:
            atm_conv_mmhg = mmhg / 760
            pascal_conv_mmhg = mmhg * 133.322
        else:
            atm_conv_mmhg = None
            pascal_conv_mmhg = None

    with col6:
        pascal = st.number_input("Pascal (Pa)", format="%.3e", key="conv_pascal")
        if pascal is not None:
            atm_conv_pascal = pascal / 101325
            mmhg_conv_pascal = pascal / 133.322
        else:
            atm_conv_pascal = None
            mmhg_conv_pascal = None

    # Tampilkan hasil konversi tekanan di bawah input yang berubah
    if st.session_state.get('conv_atm') != st.session_state.get('prev_atm', None):
        if atm is not None:
            st.info(f"mmHg: {mmhg_conv_atm:.2f} | Pascal: {pascal_conv_atm:.3e}")
        st.session_state.prev_atm = atm
    elif st.session_state.get('conv_mmhg') != st.session_state.get('prev_mmhg', None):
        if mmhg is not None:
            st.info(f"Atmosfer: {atm_conv_mmhg:.5f} atm | Pascal: {pascal_conv_mmhg:.3e}")
        st.session_state.prev_mmhg = mmhg
    elif st.session_state.get('conv_pascal') != st.session_state.get('prev_pascal', None):
        if pascal is not None:
            st.info(f"Atmosfer: {atm_conv_pascal:.5f} atm | mmHg: {mmhg_conv_pascal:.2f}")
        st.session_state.prev_pascal = pascal

