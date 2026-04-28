import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set konfigurasi halaman (opsional agar tampilan lebih luas)
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# 1. Load Data
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "main_data.csv")

# Membaca data
df = pd.read_csv(file_path)

# 2. Judul 
st.title('Bike Sharing Analysis Dashboard ')
st.markdown("---")

# 3. Menampilkan Metric Utama
st.subheader("Ringkasan Data")
col1, col2, col3 = st.columns(3)

with col1:
    total_registered = df['registered'].sum()
    st.metric("Total User Terdaftar", value=f"{total_registered:,}")

with col2:
    total_casual = df['casual'].sum()
    st.metric("Total User Kasual", value=f"{total_casual:,}")

with col3:
    total_all = df['cnt'].sum()
    st.metric("Total Semua Peminjaman", value=f"{total_all:,}")

st.markdown("---")

# 4. Visualisasi 
st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")


if 'weather_label' not in df.columns:
    weather_mapping = {
        1: 'Clear', 
        2: 'Misty', 
        3: 'Light Rain/Snow', 
        4: 'Heavy Rain'
    }
    df['weather_label'] = df['weathersit'].map(weather_mapping)


weather_colors = {
    'Clear': '#ffcc00',          
    'Misty': '#99adc1',          
    'Light Rain/Snow': '#3366cc', 
    'Heavy Rain': '#1a1a1a'       
}

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='weather_label', 
    y='cnt', 
    data=df, 
    palette=weather_colors,
    hue='weather_label',
    legend=False,
    ax=ax
)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Total Penyewaan")
st.pyplot(fig)


if 'hr' in df.columns:
    st.markdown("---")
    st.subheader("Pola Penyewaan per Jam (Hari Kerja vs Libur)")
    
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.lineplot(
        data=df, 
        x='hr', 
        y='cnt', 
        hue='workingday', 
        marker='o', 
        ax=ax2
    )
    ax2.set_xlabel("Jam (0-23)")
    ax2.set_ylabel("Jumlah Peminjaman")

    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles, ['Hari Libur', 'Hari Kerja'], title='Tipe Hari')
    
    st.pyplot(fig2)


st.markdown("---")
st.write("**Kesimpulan:**")
st.write(
    "Berdasarkan data di atas, kondisi cuaca yang cerah (Clear) memiliki tingkat penyewaan sepeda yang "
    "paling tinggi. Hal ini dikarenakan faktor keamanan dan kenyamanan pengguna saat berkendara. "
    
)
