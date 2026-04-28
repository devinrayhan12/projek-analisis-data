import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page config
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# --- LOAD DATA ---
# PENTING: Gunakan data per jam (hour) agar bisa menampilkan perbandingan jam
df = pd.read_csv("dashboard/main_data_hour.csv") 
df['dteday'] = pd.to_datetime(df['dteday'])
if 'weathersit_label' not in df.columns:
    weather_map = {
        1: 'Clear',
        2: 'Misty',
        3: 'Light Rain/Snow',
        4: 'Heavy Rain/Snow'
    }
    df['weathersit_label'] = df['weathersit'].map(weather_map)
df['year'] = df['dteday'].dt.year
df['month'] = df['dteday'].dt.month_name()

# Menambahkan label untuk kategori hari agar mudah dibaca di legenda
df['day_type'] = df['workingday'].apply(lambda x: 'Working Day' if x == 1 else 'Holiday/Weekend')

# --- SIDEBAR (FILTER BERJENJANG) ---
st.sidebar.header("Filter Eksplorasi")

# 1. Pilih Tahun
year_options = df['year'].unique()
selected_year = st.sidebar.selectbox("Pilih Tahun", options=year_options)

# 2. Pilih Bulan
month_options = df[df['year'] == selected_year]['month'].unique()
selected_month = st.sidebar.selectbox("Pilih Bulan", options=month_options)

# 3. Pilih Rentang Tanggal
filtered_month_df = df[(df['year'] == selected_year) & (df['month'] == selected_month)]
min_date = filtered_month_df["dteday"].min()
max_date = filtered_month_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Tanggal',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# --- FILTER DATA AKHIR ---
main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

# --- DASHBOARD DISPLAY ---
st.title("Bike Sharing Analysis Dashboard 🚲")
st.markdown(f"Menampilkan data: **{selected_month} {selected_year}**")

col1, col2 = st.columns(2)

# Visualisasi 1: Cuaca (Bar Chart)
with col1:
    st.subheader("1. Rata-rata Sewa Berdasarkan Cuaca")
    weather_rent = main_df.groupby('weathersit_label')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(x='weathersit_label', y='cnt', data=weather_rent, palette='Blues_r', ax=ax, hue='weathersit_label', legend=False)
    st.pyplot(fig)

# Visualisasi 2: Perbandingan Jam (Line Chart - INI PERBAIKAN REVISI)
with col2:
    st.subheader("2. Perbandingan Jam Lonjakan: Hari Kerja vs Libur")
    
    # Kelompokkan data berdasarkan jam dan tipe hari
    hourly_compare = main_df.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.lineplot(
        data=hourly_compare, 
        x='hr', 
        y='cnt', 
        hue='day_type', # Ini elemen "Comparison" yang diminta reviewer
        marker='o',
        ax=ax
    )
    ax.set_title("Pola Jam Kerja vs Hari Libur", fontsize=12)
    ax.set_xlabel("Jam (Hour)")
    ax.set_ylabel("Rata-rata Sewa")
    ax.set_xticks(range(0, 24))
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

st.write("**Analisis:** Terlihat perbedaan kontras di mana hari kerja memiliki dua puncak (pagi & sore), sedangkan hari libur cenderung melonjak di tengah hari.")

st.divider()
st.caption('Copyright (c) 2024 - Devin Rayhan Putra Aswin')
