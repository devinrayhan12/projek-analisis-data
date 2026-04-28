import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page config agar tampilan lebih profesional
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# --- LOAD DATA ---
# Pastikan main_data.csv adalah hasil gabungan day.csv dan hour.csv yang sudah bersih
day_df = pd.read_csv("dashboard/main_data.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# --- SIDEBAR (FITUR INTERAKTIF) ---
st.sidebar.header("Filter Eksplorasi")

# Widget Interaktif 1: Filter Rentang Tanggal
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    label='Pilih Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter Data Utama berdasarkan tanggal
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# --- DASHBOARD HEADER ---
st.title("Bike Sharing Analysis Dashboard 🚲")
st.markdown(f"Menampilkan data dari **{start_date}** hingga **{end_date}**")

# --- VISUALISASI DATA ---
col1, col2 = st.columns(2)

# Visualisasi 1: Pertanyaan Bisnis tentang Jam (Gunakan pola per jam)
with col2:
    st.subheader("2. Pola Penyewaan Berdasarkan Jam")
    
    # Contoh visualisasi tren harian sebagai pengganti jika data jam tidak di-merge:
    daily_rent = main_df.groupby('dteday')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.lineplot(
        x='dteday',       
        y='cnt', 
        data=daily_rent, 
        ax=ax,
        color='#1f77b4',
        linewidth=2
    )
    ax.set_title("Tren Penyewaan Harian", fontsize=15)
    ax.set_xlabel(None)
    ax.set_ylabel("Total Sewa")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write("Grafik ini membantu memantau lonjakan penyewaan pada rentang waktu yang dipilih.")
    
# Visualisasi 2: Pertanyaan Bisnis tentang Cuaca
with col1:
    st.subheader("1. Pengaruh Cuaca terhadap Penyewaan")
    # Menghitung rata-rata berdasarkan data yang sudah terfilter
    weather_rent = main_df.groupby('weathersit_label')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(
        x='weathersit_label', 
        y='cnt', 
        data=weather_rent, 
        palette='Blues_r',
        ax=ax,
        hue='weathersit_label',
        legend=False
    )
    ax.set_title("Rata-rata Penyewaan per Kondisi Cuaca", fontsize=15)
    ax.set_xlabel(None)
    ax.set_ylabel("Rata-rata Jumlah Sewa")
    st.pyplot(fig)
    st.write("Grafik ini menunjukkan bagaimana kondisi cuaca mempengaruhi minat pengguna untuk bersepeda.")

st.divider()
