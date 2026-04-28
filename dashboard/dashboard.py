import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# 1. Load Data
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load main_data (untuk harian/cuaca)
df = pd.read_csv(os.path.join(current_dir, "main_data.csv"))

# --- TAMBAHAN: Load data jam (untuk grafik pola jam) ---
# Jika Anda punya hour.csv di folder data, panggil di sini
# Atau gunakan main_data jika sudah mencakup data jam
df_hour = df 

# 2. Judul Dashboard
st.header('Bike Sharing Analysis Dashboard 🚲')

# 3. BAGIAN METRIC (Tulis di sini)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Registered", f"{df['registered'].sum():,}")
with col2:
    st.metric("Total Casual", f"{df['casual'].sum():,}")
with col3:
    st.metric("Total Pinjaman", f"{df['cnt'].sum():,}")

# 4. Grafik 1: Cuaca (Yang sudah Anda buat)
st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")
weather_mapping = {1: 'Clear', 2: 'Misty', 3: 'Light Rain/Snow', 4: 'Heavy Rain'}
df['weather_label'] = df['weathersit'].map(weather_mapping)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='weather_label', y='registered', data=df, ax=ax)
st.pyplot(fig)

# 5. BAGIAN POLA JAM (Tulis di sini)
if 'hr' in df_hour.columns:
    st.subheader("Pola Penyewaan per Jam")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    # 'workingday' di mapping agar lebih jelas (1: Working Day, 0: Holiday)
    sns.lineplot(data=df_hour, x='hr', y='cnt', hue='workingday', ax=ax2)
    st.pyplot(fig2)

# 6. PENJELASAN (Tulis di paling bawah)
st.write("Dashboard ini menunjukkan pengaruh cuaca terhadap jumlah penyewa sepeda. Cuaca cerah (Clear) memiliki tingkat penyewaan tertinggi dibandingkan cuaca hujan/salju.")
