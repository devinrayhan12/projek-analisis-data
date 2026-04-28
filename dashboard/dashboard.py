import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page config
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# --- LOAD DATA ---
day_df = pd.read_csv("dashboard/main_data.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Tambahkan kolom bantuan untuk filter
day_df['year'] = day_df['dteday'].dt.year
day_df['month'] = day_df['dteday'].dt.month_name()

# --- SIDEBAR (FILTER BERJENJANG) ---
st.sidebar.header("Filter Eksplorasi")

# 1. Pilih Tahun
year_options = day_df['year'].unique()
selected_year = st.sidebar.selectbox("Pilih Tahun", options=year_options)

# 2. Pilih Bulan (Berdasarkan Tahun yang dipilih)
month_options = day_df[day_df['year'] == selected_year]['month'].unique()
selected_month = st.sidebar.selectbox("Pilih Bulan", options=month_options)

# 3. Pilih Rentang Tanggal (Berdasarkan Tahun & Bulan yang dipilih)
filtered_by_month_df = day_df[(day_df['year'] == selected_year) & (day_df['month'] == selected_month)]
min_date = filtered_by_month_df["dteday"].min()
max_date = filtered_by_month_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Tanggal di Bulan Terpilih',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# --- FILTER DATA AKHIR ---
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# --- DASHBOARD DISPLAY ---
st.title("Bike Sharing Analysis Dashboard 🚲")
st.markdown(f"Menampilkan data: **{selected_month} {selected_year}** ({start_date} s/d {end_date})")

col1, col2 = st.columns(2)

# Visualisasi 1: Cuaca
with col1:
    st.subheader("Rata-rata Sewa Berdasarkan Cuaca")
    weather_rent = main_df.groupby('weathersit_label')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='weathersit_label', 
        y='cnt', 
        data=weather_rent, 
        palette='Blues_r',
        ax=ax,
        hue='weathersit_label',
        legend=False
    )
    st.pyplot(fig)

# Visualisasi 2: Tren Harian
with col2:
    st.subheader("Tren Penyewaan Harian")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        x='dteday', 
        y='cnt', 
        data=main_df, 
        ax=ax,
        marker='o'
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.divider()
st.caption('Copyright (c) 2024 - Devin Rayhan Putra Aswin')
