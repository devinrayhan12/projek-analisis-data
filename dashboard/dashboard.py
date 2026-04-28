import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page config
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# --- LOAD DATA ---
# Untuk filter jam, pastikan kamu menggunakan dataset 'hour.csv' yang sudah dibersihkan
# Di sini saya asumsikan main_data_hour.csv adalah data tingkat per jam
hour_df = pd.read_csv("dashboard/main_data_hour.csv") 
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.title("Bike Sharing Analysis Dashboard 🚲")

# --- SIDEBAR (FITUR INTERAKTIF JAM) ---
st.sidebar.header("Filter Spesifik")

# 1. Pilih Tanggal
selected_date = st.sidebar.date_input(
    label='Pilih Tanggal:',
    min_value=hour_df["dteday"].min(),
    max_value=hour_df["dteday"].max(),
    value=hour_df["dteday"].min()
)

# 2. Filter Rentang Jam (Slider)
# User bisa menggeser untuk memilih jam, misal dari jam 7 sampai jam 19
min_hour = int(hour_df['hr'].min())
max_hour = int(hour_df['hr'].max())

start_hour, end_hour = st.sidebar.slider(
    'Pilih Rentang Jam:',
    min_value=min_hour,
    max_value=max_hour,
    value=(7, 17) # Default: jam 7 pagi sampai 5 sore
)

# --- PROSES FILTERING DATA ---
# Filter berdasarkan tanggal DAN rentang jam
filtered_hour_df = hour_df[
    (hour_df["dteday"] == pd.to_datetime(selected_date)) & 
    (hour_df["hr"] >= start_hour) & 
    (hour_df["hr"] <= end_hour)
]

# --- DISPLAY VISUALISASI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Tren Jam pada {selected_date}")
    if not filtered_hour_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(
            x='hr', 
            y='cnt', 
            data=filtered_hour_df, 
            marker='o', 
            linewidth=2,
            color='blue',
            ax=ax
        )
        ax.set_xticks(range(start_hour, end_hour + 1))
        ax.set_xlabel("Jam (Hour)")
        ax.set_ylabel("Jumlah Sewa")
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk kombinasi tanggal dan jam ini.")

with col2:
    st.subheader("Statistik Singkat")
    if not filtered_hour_df.empty:
        total_sewa = filtered_hour_df['cnt'].sum()
        rata_sewa = filtered_hour_df['cnt'].mean()
        jam_puncak = filtered_hour_df.loc[filtered_hour_df['cnt'].idxmax(), 'hr']
        
        st.metric("Total Penyewaan", f"{total_sewa} unit")
        st.metric("Rata-rata per Jam", f"{rata_sewa:.2f} unit")
        st.metric("Jam Paling Ramai", f"Pukul {jam_puncak}:00")
    else:
        st.write("Data kosong.")

st.divider()
st.caption('Copyright (c) 2024 - Proyek Analisis Data Bike Sharing')
