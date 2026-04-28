import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# 1. Load Data
# Menggunakan path relatif agar aman di Streamlit Cloud
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "main_data.csv")
df = pd.read_csv(file_path)

# 2. Tambahkan Mapping (Cara 2)
# Sesuai Readme: 1: Clear, 2: Mist, 3: Light Rain, 4: Heavy Rain 
weather_mapping = {
    1: 'Clear', 
    2: 'Misty', 
    3: 'Light Rain/Snow', 
    4: 'Heavy Rain'
}

# Membuat kolom baru jika belum ada
df['weather_label'] = df['weathersit'].map(weather_mapping)

# 3. Visualisasi
st.header('Bike Sharing Analysis Dashboard 🚲')
st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='weather_label', 
    y='registered', 
    data=df, 
    palette='viridis',
    ax=ax
)

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewa (Registered)")
st.pyplot(fig)
