import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import warnings


st.set_page_config(
    page_title="Estimasi Harga Laptop Bekas",
    layout="wide",
)

st.title("Mr. Komputer", text_alignment='center')
st.subheader("Solusi Cerdas Tentukan Harga Jual Laptop Anda!!!", text_alignment='center')


# Variabel Fuzzy
harga_baru = ctrl.Antecedent(np.arange(3, 31, 1), 'harga_baru')
kondisi = ctrl.Antecedent(np.arange(0, 101, 1), 'kondisi')
performa = ctrl.Antecedent(np.arange(0, 101, 1), 'performa')
umur = ctrl.Antecedent(np.arange(0, 11, 1), 'umur')
permintaan = ctrl.Antecedent(np.arange(0, 101, 1), 'permintaan')
persentase = ctrl.Consequent(np.arange(10, 101, 1), 'persentase')

# Himpunan Fuzzy untuk Harga Baru (Rp.)
harga_baru['murah'] = fuzz.trimf(harga_baru.universe, [3, 3, 12])
harga_baru['menengah'] = fuzz.trimf(harga_baru.universe, [8, 16, 24])
harga_baru['premium'] = fuzz.trimf(harga_baru.universe, [20, 30, 30])

# Himpunan Fuzzy untuk Kondisi (%)
kondisi['buruk'] = fuzz.trimf(kondisi.universe, [0, 0, 45])
kondisi['sedang'] = fuzz.trimf(kondisi.universe, [35, 60, 85])
kondisi['baik'] = fuzz.trimf(kondisi.universe, [75, 100, 100])

# Himpunan Fuzzy untuk Performa (%)
performa['rendah'] = fuzz.trimf(performa.universe, [0, 0, 45])
performa['sedang'] = fuzz.trimf(performa.universe, [35, 60, 85])
performa['tinggi'] = fuzz.trimf(performa.universe, [75, 100, 100])

# Himpunan Fuzzy untuk Umur Laptop (tahun)
umur['baru'] = fuzz.trimf(umur.universe, [0, 0, 3])
umur['sedang'] = fuzz.trimf(umur.universe, [2, 5, 8])
umur['lama'] = fuzz.trimf(umur.universe, [6, 10, 10])

# Himpunan Fuzzy untuk Permintaan Pasar
permintaan['rendah'] = fuzz.trimf(permintaan.universe, [0, 0, 45])
permintaan['sedang'] = fuzz.trimf(permintaan.universe, [35, 60, 85])
permintaan['tinggi'] = fuzz.trimf(permintaan.universe, [75, 100, 100])

# Persentase Retensi Nilai (10-100%)
persentase['rendah'] = fuzz.trimf(persentase.universe, [10, 10, 45])
persentase['sedang'] = fuzz.trimf(persentase.universe, [35, 60, 85])
persentase['tinggi'] = fuzz.trimf(persentase.universe, [75, 100, 100])


# Knowledge
rules = [
    # Jika laptop premium
    ctrl.Rule(harga_baru['premium'] & kondisi['baik'] & performa['tinggi'], persentase['tinggi']),
    ctrl.Rule(harga_baru['premium'] & kondisi['baik'] & umur['baru'], persentase['tinggi']),
    ctrl.Rule(harga_baru['premium'] & permintaan['tinggi'], persentase['tinggi']),
    ctrl.Rule(harga_baru['premium'] & kondisi['sedang'], persentase['sedang']),

    # Laptop kelas menengah
    ctrl.Rule(harga_baru['menengah'] & kondisi['baik'] & umur['baru'], persentase['tinggi']),
    ctrl.Rule(harga_baru['menengah'] & kondisi['baik'] & performa['sedang'], persentase['sedang']),
    ctrl.Rule(harga_baru['menengah'] & umur['sedang'], persentase['sedang']),
    ctrl.Rule(harga_baru['menengah'] & kondisi['buruk'], persentase['rendah']),

    # Laptop kelas entry-level
    ctrl.Rule(harga_baru['murah'] & umur['lama'], persentase['rendah']),
    ctrl.Rule(harga_baru['murah'] & kondisi['baik'] & performa['tinggi'], persentase['sedang']),
    ctrl.Rule(harga_baru['murah'] & performa['rendah'], persentase['rendah']),

    # Rule Umum yang dominan
    ctrl.Rule(kondisi['buruk'], persentase['rendah']),
    ctrl.Rule(umur['lama'], persentase['rendah']),
    ctrl.Rule(performa['tinggi'] & permintaan['tinggi'], persentase['tinggi']),
    ctrl.Rule(performa['rendah'], persentase['rendah']),
    ctrl.Rule(kondisi['sedang'] & performa['sedang'], persentase['sedang']),
    ctrl.Rule(kondisi['baik'] & umur['sedang'], persentase['sedang']),
    ctrl.Rule(umur['baru'] & kondisi['baik'], persentase['tinggi']),
    ctrl.Rule(permintaan['rendah'], persentase['rendah']),
    ctrl.Rule(permintaan['tinggi'] & kondisi['baik'], persentase['tinggi']),
]

# Inference Engine menggunakan Mamdani
system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)


# UI Streamlit
st.markdown("Masukkan Spesifikasi Laptop", text_alignment='center')
col1, col2 = st.columns(2)

with col1:
    nilai_harga_baru = st.slider("💰 Harga Baru Saat Dibeli (Juta Rupiah)", 3, 30, 12, help="Berapa harga laptop ini ketika dibeli dalam kondisi baru?")
    nilai_kondisi = st.slider("✨ Kondisi Fisik (%)", 0, 100, 80, help="0: Sangat buruk/rusak, 100: Mulus seperti baru")
    nilai_performa = st.slider("🚀 Performa Saat Ini (%)", 0, 100, 75, help="0: Sangat lambat/sering hang, 100: Sangat cepat/responsif")

with col2:
    nilai_umur = st.slider("📅 Umur Laptop (Tahun)", 0, 10, 3, help="Berapa tahun laptop sudah digunakan?")
    nilai_permintaan = st.slider("📈 Permintaan Pasar (%)", 0, 100, 70, help="Apakah laptop ini sedang banyak dicari orang?")


# Compute hasil input
if st.button("Hitung Harga Jual", use_container_width=True, type="primary"):

    sim.input['harga_baru'] = nilai_harga_baru
    sim.input['kondisi'] = nilai_kondisi
    sim.input['performa'] = nilai_performa
    sim.input['umur'] = nilai_umur
    sim.input['permintaan'] = nilai_permintaan

    sim.compute()

    persentase_out = sim.output['persentase']
    
    # Harga Jual = Harga Baru * (Persentase / 100)
    hasil = (persentase_out / 100.0) * nilai_harga_baru

    # Interpretasi

    if persentase_out < 40:
        kategori = "Rendah - Depresiasi Tinggi"
        warna = "#FF4B4B" # Red
    elif persentase_out < 75:
        kategori = "Sedang - Depresiasi Wajar"
        warna = "#FFA500" # Orange
    else:
        kategori = "Tinggi - Retensi Nilai Baik"
        warna = "#00CC96" # Green

    st.markdown("---")
    st.subheader("Hasil Estimasi")
    
    st.success(f"### Rp {hasil:.2f} Juta")
    st.info(f"Persentase Retensi Nilai: **{persentase_out:.1f}%** dari harga awal ({kategori})")

    
    # Grafik Himpunan Fuzzy dari Consequent (Persentase)
    st.markdown("### Visualisasi Membership Function (Persentase)")
    
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        persentase.universe,
        persentase['rendah'].mf,
        label='Rendah',
        color='#FF4B4B'
    )

    ax.plot(
        persentase.universe,
        persentase['sedang'].mf,
        label='Sedang',
        color='#FFA500'
    )

    ax.plot(
        persentase.universe,
        persentase['tinggi'].mf,
        label='Tinggi',
        color='#00CC96'
    )

    ax.axvline(
        x=persentase_out,
        color='#00C9FF',
        linestyle='--',
        linewidth=2,
        label=f'Hasil = {persentase_out:.1f}%'
    )

    ax.set_title("Membership Function Persentase Harga Jual")
    ax.set_xlabel("Persentase (%)")
    ax.set_ylabel("Derajat Keanggotaan")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

    # =================================================
    # VIEW STYLE SKFUZZY (DIPERBAIKI)
    # =================================================

    st.markdown("### Visualisasi Fuzzy Output ")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        persentase.view(sim=sim)
        
    fig2 = plt.gcf()
    st.pyplot(fig2)
    plt.close(fig2)