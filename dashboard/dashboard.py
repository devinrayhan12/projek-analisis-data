import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# --- LOAD DATA ---
day_df = pd.read_csv("dashboard/main_data.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

st.title("Bike Sharing Analysis Dashboard 🚲")

# --- SIDEBAR (FITUR INTERAKTIF) ---
st.sidebar.header("Pusat Kontrol Filter")

# --- FILTER 1: CUACA ---
st.sidebar.subheader("Filter Grafik Cuaca")
weather_list = day_df['weathersit_label'].unique()
selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca:",
    options=weather_list,
    default=weather_list
)

# --- FILTER 2: KHUSUS GRAFIK TREN ---
st.sidebar.subheader("Filter Grafik Tren")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    label='Pilih Rentang Tanggal:',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# --- PROSES FILTERING DATA ---
# Data untuk grafik cuaca (hanya difilter berdasarkan kategori cuaca)
weather_filtered_df = day_df[day_df["weathersit_label"].isin(selected_weather)]

# Data untuk grafik tren (hanya difilter berdasarkan rentang tanggal)
time_filtered_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                          (day_df["dteday"] <= str(end_date))]

# --- DISPLAY VISUALISASI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Pengaruh Cuaca Terhadap Penyewaan")
    if len(selected_weather) > 0:
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Menghitung rata-rata dari data yang difilter cuaca
        avg_weather = weather_filtered_df.groupby('weathersit_label')['cnt'].mean().reset_index()
        
        sns.barplot(
            x='weathersit_label', 
            y='cnt', 
            data=avg_weather, 
            palette='viridis',
            ax=ax,
            hue='weathersit_label',
            legend=False
        )
        ax.set_title("Rata-rata Sewa Berdasarkan Cuaca Pilihan", fontsize=15)
        st.pyplot(fig)
    else:
        st.warning("Silakan pilih minimal satu kondisi cuaca di sidebar.")

with col2:
    st.subheader("2. Tren Penyewaan Berdasarkan Waktu")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Menampilkan tren dari data yang difilter tanggal
    sns.lineplot(
        x='dteday', 
        y='cnt', 
        data=time_filtered_df, 
        ax=ax,
        color='red',
        linewidth=2
    )
    plt.xticks(rotation=45)
    ax.set_title(f"Tren dari {start_date} s/d {end_date}", fontsize=15)
    st.pyplot(fig)

st.divider()
st.caption('Copyright (c) 2024 - Devin Rayhan Putra Aswin')
