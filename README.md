# Bike Sharing Analysis Dashboard 🚲

## Project Overview
Proyek ini bertujuan untuk menganalisis data penyewaan sepeda berdasarkan kondisi lingkungan seperti cuaca dan waktu. Analisis ini mencakup pola penyewaan pada hari kerja vs hari libur serta pengaruh kondisi cuaca terhadap jumlah pengguna (Registered & Casual).

## Dataset
Dataset yang digunakan adalah "Bike Sharing Dataset" dari Capital Bikeshare.

## Setup Environment - Anaconda
   ```bash
   conda create --name bike-sharing python=3.9
   conda activate bike-sharing
   pip install -r requirements.txt
   ```

## Setup Environment - Shell/Terminal
   ```bash
   mkdir proyek_analisis_data
   cd proyek_analisis_data
   pipenv install
   pipenv shell
   pip install -r requirements.txt
   ```

## Run Streamlit App
   ```bash
   streamlit run dashboard/dashboard.py
