import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import datetime
sns.set(style='dark')

day_df = pd.read_csv("dashboard/day.csv")
hour_df= pd.read_csv("dashboard/hour.csv")

day_df['season'] = day_df['season'].replace({1:'springer', 2:'summer', 3:'fall', 4:'winter'})
day_df['yr'] = day_df['yr'].replace({0: '2011', 1:'2012'})
day_df['holiday'] = day_df['holiday'].replace({0: 'Holiday', 1:'non-Holiday'})
day_df['weekday'] = day_df['weekday'].replace({0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'})
day_df['workingday'] = day_df['workingday'].replace({0: 'Workingday', 1:'Weekend nor holiday'})

hour_df['season'] = hour_df['season'].replace({1:'springer', 2:'summer', 3:'fall', 4:'winter'})
hour_df['yr'] = hour_df['yr'].replace({0: '2011', 1:'2012'})
hour_df['holiday'] = hour_df['holiday'].replace({0: 'Holiday', 1:'non-Holiday'})
hour_df['weekday'] = hour_df['weekday'].replace({0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'})
hour_df['workingday'] = hour_df['workingday'].replace({0: 'Workingday', 1:'Weekend nor holiday'})

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://asset-2.tstatic.net/jakarta/foto/bank/images/Jejeran-sepeda-yang-disewakan-mengunakan-aplikasi-GOWES-2.jpg")
    
    # Tentang Kami
    st.subheader("About Us")
    st.write("Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return back has become automatic. Through these systems, user is able to easily rent a bike from a particular position and return back at another position. Currently, there are about over 500 bike-sharing programs around the world which is composed of over 500 thousands bicycles. Today, there exists great interest in these systems due to their important role in traffic, environmental and health issues.")
    st.subheader("Tentang Kami")
    st.write("Sistem berbagi sepeda adalah generasi baru dari persewaan sepeda tradisional di mana seluruh proses mulai dari keanggotaan, penyewaan, dan pengembalian menjadi otomatis. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari posisi tertentu dan kembali lagi ke posisi lain. Saat ini, terdapat lebih dari 500 program berbagi sepeda di seluruh dunia yang mencakup lebih dari 500 ribu sepeda. Saat ini, terdapat minat yang besar terhadap sistem ini karena peran pentingnya dalam masalah lalu lintas, lingkungan dan kesehatan.")

st.header('🚲DASHBOARD BIKE SHARING SYSTEM🚲')

st.subheader('Daily Orders')

hourly_date = st.date_input(
        label='Pilih Tanggal (2011-2012)',
        value = datetime.date(2011, 1, 1)
)
date = hour_df[(hour_df["dteday"] == str(hourly_date))]

hourly_day = hour_df[hour_df["dteday"] == str(hourly_date)]
#tanggalnya dapat diganti untuk melihat perubahan per hari

col1, col2 = st.columns(2)
 
with col1:
    day_total = hourly_day["cnt"].sum()
    st.metric("Total Sepeda yang Disewakan", value=day_total)
 
with col2:
    jam_tertinggi = hourly_day.loc[hourly_day["cnt"] == hourly_day["cnt"].max(), "hr"].iloc[0] 
    st.metric("Jam dengan Penyewaan Tertinggi", value=str(jam_tertinggi) + " WIB")

plt.figure(figsize=(10, 5))
plt.bar(
    hourly_day["hr"],
    hourly_day["cnt"],
    color="#72BCD4",
    edgecolor="black",  # Warna tepi batang
    linewidth=2,  # Ketebalan tepi batang
)
plt.title("Total Peminjaman per Jam", loc="center", fontsize=20)
plt.xlabel("Jam", fontsize=12)
plt.ylabel("Jumlah Peminjaman", fontsize=12)
plt.xticks(hourly_day["hr"], fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(plt)


st.subheader('Daily Recap')

day_weekday = day_df.groupby("weekday")["cnt"].sum().reset_index(name="jumlah_persewaan")
day_order_mapping = {"Sunday": 0,"Monday": 1,"Tuesday": 2,"Wednesday": 3,"Thursday": 4,"Friday": 5,"Saturday": 6,}
day_weekday["weekday_order"] = day_weekday["weekday"].map(day_order_mapping)
day_weekday = day_weekday.sort_values(by="weekday_order")
day_weekday = day_weekday.drop("weekday_order", axis=1)

col1, col2 = st.columns(2)
 
with col1:
    day_weekday_max_rentals = day_weekday.loc[day_weekday['jumlah_persewaan'].idxmax()]
    st.metric("Hari Dengan Jumlah Penyewaan Tertinggi:", day_weekday_max_rentals['weekday'])
 
with col2:
    day_max_rentals = day_weekday.loc[day_weekday['jumlah_persewaan'].idxmax()]
    st.metric("Dengan Jumlah Penyewaan Sebesar:", day_max_rentals['jumlah_persewaan'])

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(day_weekday["weekday"], day_weekday["jumlah_persewaan"], marker='o', linestyle='-', color='b')
ax.set_xlabel("Hari Kerja/Libur")
ax.set_ylabel("Jumlah Persewaan")
ax.set_title("Persebaran Persewaan Per Hari Kerja/Libur")

st.pyplot(fig)

st.subheader('Relationship between Number of Bicycle Users and Temperature')
coefficients = np.polyfit(day_df["temp"], day_df["cnt"], 1)
regression_line = np.polyval(coefficients, day_df["temp"])
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(day_df["temp"], day_df["cnt"], label="Data")
ax.plot(day_df["temp"], regression_line, color="red", label="Regresi Linear")
ax.set_xlabel("Temperatur")
ax.set_ylabel("Jumlah Pengguna Sepeda")
ax.set_title("Hubungan antara Jumlah Pengguna Sepeda dan Temperatur")
ax.legend()
st.pyplot(fig)

st.write("Interpretasi:")
st.write("1. Hubungan positif: Ada hubungan positif antara temperatur dan jumlah pengguna sepeda. Semakin tinggi temperatur, semakin banyak pengguna sepeda.")
st.write("2. Korelasi sedang: Korelasi antara temperatur dan jumlah pengguna sepeda tidak terlalu kuat. Ada banyak faktor lain yang mempengaruhi jumlah pengguna sepeda, seperti cuaca, hari libur, dan acara khusus.")
st.write("3. Variabilitas: Ada banyak variabilitas dalam jumlah pengguna sepeda untuk setiap temperatur. Hal ini menunjukkan bahwa faktor lain selain temperatur juga mempengaruhi jumlah pengguna sepeda.")
