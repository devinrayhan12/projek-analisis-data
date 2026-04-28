import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


st.header('Bike Sharing Analysis Dashboard 🚲')

# Load data 
df = pd.read_csv("dashboard/main_data.csv")

if 'weather_label' not in df.columns:
    weather_mapping = {1: 'Clear', 2: 'Misty', 3: 'Light Rain/Snow', 4: 'Heavy Rain'} [cite: 19, 20]
    df['weather_label'] = df['weathersit'].map(weather_mapping) [cite: 19, 20]
  
# Tampilkan grafik 
st.subheader("Penyewaan Berdasarkan Cuaca")
fig, ax = plt.subplots()
sns.barplot(x='weather_label', y='registered', data=df, ax=ax)
st.pyplot(fig)
