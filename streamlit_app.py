import streamlit as st
import math

# Konstanta gas ideal
R = 8.314

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="ThermoCalc Lab")

# --- Custom CSS untuk UI/UX ---
st.markdown("""
    <style>
        /* Definisi keyframes untuk animasi latar belakang */
        @keyframes background-pan {
            0% {
                background-position: 0% 0%;
            }
            100% {
                background-position: 100% 100%;
            }
        }

        /* Mengatur font utama dan latar belakang gradien untuk seluruh aplikasi */
        .stApp {
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); /* Gradien gelap yang kaya */
            color: #e2e8f0; /* Warna teks default */
            font-family: 'Inter', sans-serif;
            /* Menambahkan efek latar belakang abstrak */
            background-image: radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%),
                                 radial-gradient(at 50% 100%, hsla(225,39%,30%,1) 0, transparent 50%),
                                 radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
            background-attachment: fixed;
            background-size: 200% 200%; /* Ukuran latar belakang lebih besar dari viewport */
            animation: background-pan 30s linear infinite alternate; /* Animasi latar belakang */
        }

        /* Styling untuk judul utama (H1) */
        h1 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            letter-spacing: -0.05em;
            background: linear-gradient(90deg, #a78bfa, #c4b5fd); /* Gradien teks ungu-biru */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            color: transparent;
            text-align: center;
            font-size: 4rem; /* Ukuran font lebih besar */
            margin-bottom: 0.5rem;
            text-shadow: 0 0 15px rgba(167, 139, 250, 0.4); /* Efek glow pada teks */
        }
        /* Styling untuk subheader (deskripsi) */
        p.subheader {
            font-weight: 300;
            color: #a0aec0;
            text-align: center;
            font-size: 1.25rem; /* text-xl */
            margin-bottom: 3rem;
            text-shadow: 0 0 5px rgba(160, 174, 192, 0.2);
        }
        /* Padding untuk container utama */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 1200px; /* Batasi lebar untuk tampilan yang lebih baik */
        }

        /* Styling untuk semua input teks dan textarea */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: rgba(47, 58, 75, 0.6); /* Transparan lembut */
            border: 1px solid rgba(71, 85, 105, 0.8); /* Border yang lebih jelas */
            color: #e2e8f0;
            padding: 0.8rem 1.2rem; /* Padding sedikit lebih besar */
            border-radius: 0.75rem; /* Sudut lebih membulat */
            transition: all 0.3s ease;
            backdrop-filter: blur(5px); /* Efek blur glassmorphism */
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2); /* Bayangan lembut */
        }
        /* Efek fokus untuk input teks dan textarea */
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            border-color: #6366f1; /* Border indigo saat fokus */
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.4), 0 0 20px rgba(99, 102, 241, 0.3); /* Cincin fokus + glow */
            background-color: rgba(58, 71, 90, 0.7); /* Sedikit lebih terang saat fokus */
            outline: none; /* Hapus outline default browser */
        }
        /* Placeholder styling */
        input::placeholder, textarea::placeholder {
            color: #94a3b8; /* Warna placeholder yang lebih terang */
            opacity: 0.8;
        }

        /* Styling umum untuk semua tombol */
        div.stButton > button {
            background: linear-gradient(90deg, #3b82f6, #2563eb); /* Gradien biru yang kuat */
            color: white;
            font-weight: 700; /* Lebih tebal */
            padding: 0.9rem 1.8rem; /* Padding lebih besar */
            border-radius: 0.75rem;
            box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4); /* Bayangan lebih dalam */
            transition: all 0.3s ease;
            width: 100%; /* Lebar penuh */
            margin-top: 1.5rem; /* Jarak dari elemen di atasnya */
            border: none; /* Hapus border default */
            position: relative;
            overflow: hidden;
        }
        div.stButton > button:hover {
            transform: translateY(-3px); /* Terangkat lebih tinggi */
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5); /* Bayangan lebih besar */
            opacity: 1;
            background: linear-gradient(90deg, #2563eb, #3b82f6); /* Balik gradien saat hover */
        }
        div.stButton > button:active {
            transform: translateY(0); /* Efek tekan */
            box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
        }
        /* Efek kilauan pada tombol saat hover */
        div.stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.2);
            transform: skewX(-30deg);
            transition: all 0.7s ease;
        }
        div.stButton > button:hover::before {
            left: 100%;
        }

        /* Styling khusus untuk tombol tab (Isobarik, Isokhorik, Isotermal) */
        div.stButton > button[data-testid^="stButton-primary"]:nth-child(1),
        div.stButton > button[data-testid^="stButton-primary"]:nth-child(2),
        div.stButton > button[data-testid^="stButton-primary"]:nth-child(3) {
            background: rgba(47, 58, 75, 0.6); /* Latar belakang transparan untuk tab non-aktif */
            color: #cbd5e1;
            box-shadow: none;
            transform: none;
            margin-top: 0;
            border: 1px solid rgba(71, 85, 105, 0.8);
            transition: all 0.3s ease;
            padding: 0.75rem 1rem; /* Sesuaikan padding agar tidak terlalu besar */
            font-weight: 500;
        }
        div.stButton > button[data-testid^="stButton-primary"]:nth-child(1):hover,
        div.stButton > button[data-testid^="stButton-primary"]:nth-child(2):hover,
        div.stButton > button[data-testid^="stButton-primary"]:nth-child(3):hover {
            background: rgba(58, 71, 90, 0.7); /* Sedikit lebih terang saat hover */
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            transform: translateY(-1px);
        }

        /* Styling untuk kotak hasil perhitungan */
        .result-box {
            background: rgba(45, 55, 72, 0.7); /* Transparan lembut */
            border: 1px solid rgba(71, 85, 105, 0.8);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
            padding: 2rem; /* Padding lebih besar */
            border-radius: 1rem; /* Sudut lebih membulat */
            margin-top: 2rem; /* Jarak lebih besar */
            backdrop-filter: blur(8px); /* Efek blur glassmorphism yang lebih kuat */
        }
        .result-box h3 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: #818cf8; /* Warna indigo terang untuk judul hasil */
            font-size: 1.5rem; /* Ukuran font lebih besar */
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            text-shadow: 0 0 10px rgba(129, 140, 248, 0.3);
        }
        .result-box p {
            color: #cbd5e1;
            font-size: 1.1rem; /* Ukuran font sedikit lebih besar */
            line-height: 1.8;
        }
        .result-box p span {
            color: #e2e8f0; /* Warna teks hasil yang lebih menonjol */
            font-weight: 700;
        }

        /* Styling untuk Selectbox Streamlit */
        .stSelectbox > div > label {
            color: #e2e8f0;
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .stSelectbox > div > div {
            background-color: rgba(47, 58, 75, 0.6); /* Transparan lembut */
            border-radius: 0.625rem;
            border: 1px solid rgba(71, 85, 105, 0.8);
            color: #e2e8f0;
            backdrop-filter: blur(5px);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        .stSelectbox > div > div:hover {
            border-color: #6366f1;
        }
        /* Styling untuk header bagian (H2) */
        .section-header {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: #e2e8f0;
            font-size: 2.2rem; /* Ukuran font lebih besar untuk header bagian */
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            text-shadow: 0 0 10px rgba(226, 232, 240, 0.2);
        }
        .section-header i {
            margin-right: 1rem; /* Jarak ikon lebih besar */
            font-size: 1.8rem;
            color: #6366f1; /* Warna ikon yang lebih konsisten */
        }
        /* Styling untuk sub-subheader (H3) */
        .subsection-header {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: #cbd5e1;
            font-size: 1.25rem; /* Ukuran font lebih besar */
            margin-top: 2rem;
            margin-bottom: 1.2rem;
        }
        /* Styling untuk kolom di Streamlit */
        .st-emotion-cache-1cypcdb { /* Menargetkan container kolom Streamlit */
            gap: 2rem; /* Menambahkan jarak antar kolom */
        }
        /* Card-like containers for the main sections */
        .st-emotion-cache-fg4pbf { /* Ini adalah div utama yang membungkus kolom di Streamlit */
            background: rgba(30, 41, 59, 0.7); /* Latar belakang semi-transparan untuk seluruh area konten */
            border-radius: 1.5rem; /* Sudut yang sangat membulat */
            padding: 2.5rem; /* Padding yang lebih besar */
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4); /* Bayangan yang lebih menonjol */
            backdrop-filter: blur(10px); /* Efek blur glassmorphism utama */
            border: 1px solid rgba(71, 85, 105, 0.6); /* Border lembut */
        }
        /* Mengatur ulang padding untuk input number agar tidak terlalu lebar */
        .stNumberInput > label + div > div {
            padding: 0; /* Hapus padding default */
        }
        .stNumberInput input {
            padding: 0.75rem 1rem !important; /* Terapkan padding kustom */
        }

    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

# --- Header Aplikasi ---
st.title("ThermoCalc Lab")
st.markdown('<p class="subheader">Kalkulator dan Konverter untuk Perhitungan Termodinamika.</p>', unsafe_allow_html=True)

# Membagi tata letak menjadi dua kolom utama (kalkulator di kiri, konverter di kanan)
col_calc, col_conv = st.columns([1, 2]) # Mengubah nama kolom kanan

with col_calc:
    st.markdown('<h2 class="section-header"><i class="fas fa-calculator text-blue-400"></i> Kalkulator Termodinamika</h2>', unsafe_allow_html=True)

    # Menggunakan st.session_state untuk mengelola tab aktif
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Isobarik"

    # Tombol tab kustom (simulasi)
    tab_cols = st.columns(3)
    with tab_cols[0]:
        # Tambahkan kelas 'active' secara dinamis untuk styling
        button_class = "tab-btn active" if st.session_state.active_tab == "Isobarik" else "tab-btn"
        if st.button("Isobarik", key="tab_isobaric"):
            st.session_state.active_tab = "Isobarik"
    with tab_cols[1]:
        button_class = "tab-btn active" if st.session_state.active_tab == "Isokhorik" else "tab-btn"
        if st.button("Isokhorik", key="tab_isochoric"):
            st.session_state.active_tab = "Isokhorik"
    with tab_cols[2]:
        button_class = "tab-btn active" if st.session_state.active_tab == "Isotermal" else "tab-btn"
        if st.button("Isotermal", key="tab_isothermal"):
            st.session_state.active_tab = "Isotermal"

    # Menambahkan CSS untuk tombol tab aktif (diperbarui agar lebih dinamis)
    st.markdown(f"""
        <style>
            /* Mengatur ulang gaya tombol stButton untuk tab */
            div.stButton > button[data-testid^="stButton-primary"] {{
                background: rgba(47, 58, 75, 0.6); /* Latar belakang transparan untuk tab non-aktif */
                color: #cbd5e1;
                box-shadow: none;
                transform: none;
                margin-top: 0;
                border: 1px solid rgba(71, 85, 105, 0.8);
                transition: all 0.3s ease;
                padding: 0.75rem 1rem; /* Sesuaikan padding agar tidak terlalu besar */
                font-weight: 500;
            }}
            div.stButton > button[data-testid^="stButton-primary"]:hover {{
                background: rgba(58, 71, 90, 0.7); /* Sedikit lebih terang saat hover */
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                transform: translateY(-1px);
            }}
            /* Gaya untuk tab aktif */
            div.stButton > button[data-testid="stButton-primary"][key="tab_isobaric"] {{
                background-color: {'#4f46e5' if st.session_state.active_tab == 'Isobarik' else 'rgba(47, 58, 75, 0.6)'};
                color: {'white' if st.session_state.active_tab == 'Isobarik' else '#cbd5e1'};
                box-shadow: {'0 4px 10px rgba(79, 70, 229, 0.4)' if st.session_state.active_tab == 'Isobarik' else 'none'};
                transform: {'translateY(-2px)' if st.session_state.active_tab == 'Isobarik' else 'none'};
                border-radius: 0.75rem 0 0 0.75rem; /* Rounded top-left, bottom-left */
            }}
            div.stButton > button[data-testid="stButton-primary"][key="tab_isochoric"] {{
                background-color: {'#4f46e5' if st.session_state.active_tab == 'Isokhorik' else 'rgba(47, 58, 75, 0.6)'};
                color: {'white' if st.session_state.active_tab == 'Isokhorik' else '#cbd5e1'};
                box-shadow: {'0 4px 10px rgba(79, 70, 229, 0.4)' if st.session_state.active_tab == 'Isokhorik' else 'none'};
                transform: {'translateY(-2px)' if st.session_state.active_tab == 'Isokhorik' else 'none'};
                border-radius: 0;
            }}
            div.stButton > button[data-testid="stButton-primary"][key="tab_isothermal"] {{
                background-color: {'#4f46e5' if st.session_state.active_tab == 'Isotermal' else 'rgba(47, 58, 75, 0.6)'};
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

    # --- Volume Converter ---
    st.markdown("### Volume")
    col7, col8, col9 = st.columns(3)

    with col7:
        cm_cubed = st.number_input("Cubic Centimeters (cm³)", format="%.2f", key="conv_cm_cubed")
        if cm_cubed is not None:
            m_cubed_conv_cm = cm_cubed * 1e-6
            dm_cubed_conv_cm = cm_cubed * 1e-3
        else:
            m_cubed_conv_cm = None
            dm_cubed_conv_cm = None

    with col8:
        m_cubed = st.number_input("Cubic Meters (m³)", format="%.4f", key="conv_m_cubed")
        if m_cubed is not None:
            cm_cubed_conv_m = m_cubed * 1e6
            dm_cubed_conv_m = m_cubed * 1e3
        else:
            cm_cubed_conv_m = None
            dm_cubed_conv_m = None

    with col9:
        dm_cubed = st.number_input("Cubic Decimeters (dm³)", format="%.2f", key="conv_dm_cubed")
        if dm_cubed is not None:
            cm_cubed_conv_dm = dm_cubed * 1e3
            m_cubed_conv_dm = dm_cubed * 1e-3
        else:
            cm_cubed_conv_dm = None
            m_cubed_conv_dm = None

    # Display volume conversion results dynamically
    if st.session_state.get('conv_cm_cubed') != st.session_state.get('prev_cm_cubed', None):
        if cm_cubed is not None:
            st.info(f"Cubic Meters: {m_cubed_conv_cm:.6f} m³ | Cubic Decimeters: {dm_cubed_conv_cm:.4f} dm³")
        st.session_state.prev_cm_cubed = cm_cubed
    elif st.session_state.get('conv_m_cubed') != st.session_state.get('prev_m_cubed', None):
        if m_cubed is not None:
            st.info(f"Cubic Centimeters: {cm_cubed_conv_m:.2f} cm³ | Cubic Decimeters: {dm_cubed_conv_m:.4f} dm³")
        st.session_state.prev_m_cubed = m_cubed
    elif st.session_state.get('conv_dm_cubed') != st.session_state.get('prev_dm_cubed', None):
        if dm_cubed is not None:
            st.info(f"Cubic Centimeters: {cm_cubed_conv_dm:.2f} cm³ | Cubic Meters: {m_cubed_conv_dm:.6f} m³")
        st.session_state.prev_dm_cubed = dm_cubed