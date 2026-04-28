import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


st.header('Bike Sharing Analysis Dashboard 🚲')

# Load data 
df = pd.read_csv("dashboard/main_data.csv")

# Tampilkan grafik 
st.subheader("Penyewaan Berdasarkan Cuaca")
fig, ax = plt.subplots()
sns.barplot(x='weather_label', y='registered', data=df, ax=ax)
st.pyplot(fig)