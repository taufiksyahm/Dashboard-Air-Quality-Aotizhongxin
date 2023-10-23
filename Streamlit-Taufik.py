import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# data
data = pd.read_csv("all_data.csv")
# membuat data harian
data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
# fungsi data harian baru
def harian(df):
    datadate = df.resample(rule='D', on='date').agg({
        "date": "min",
        "PM2.5": "median",
        "TEMP": "mean"
    })   
    return datadate

# batas tanggal
min_date = data["date"].min()
max_date = data['date'].max()

# side bar kalender
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Timeframe',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# buat tanggal pilihan
main_df = data[(data["date"] >= str(start_date)) & 
                (data["date"] <= str(end_date))]

# data tanggal pilihan
datadate = harian(main_df)

# buat judul utama
st.title("Aotizhongxin Air Quality 2013-2017", anchor=False)

# buat nama
st.subheader("Taufik Syah Mauludin", anchor=False)

# buat garis pemisah
st.divider()

# buat judul 
st.header('PM2.5 Concentration')

# buat grafik PM2.5
fig = go.Figure()
fig.update_yaxes(title_text="PM2.5 (μg/m^3)")
fig.add_trace(go.Scatter(x=datadate["date"], y=datadate["PM2.5"]))
st.plotly_chart(fig, use_container_width=True)

# buat judul
st.subheader('Temperature')

# buat grafik TEMP
fig = go.Figure()
fig.update_yaxes(title_text="T (oC)")
fig.add_trace(go.Scatter(x=datadate["date"], y=datadate["TEMP"]))
st.plotly_chart(fig, use_container_width=True)

# buat musim
datadate['Musim'] = datadate['date'].dt.month.map({1: 'Winter',
                                                   2: 'Winter',
                                                   3: 'Spring',
                                                   4: 'Spring',
                                                   5: 'Spring',
                                                   6: 'Summer',
                                                   7: 'Summer',
                                                   8: 'Summer',
                                                   9: 'Autumn',
                                                   10: 'Autumn',
                                                   11: 'Autumn',
                                                   12: 'Winter'})

datapm_musim = datadate.groupby('Musim')['PM2.5'].median()
datatemp_musim = datadate.groupby('Musim')['TEMP'].mean()

# buat judul
st.header('Seasonal Analysis')

# buat grafik musim
fig = make_subplots(rows=1, cols=2)
fig.add_trace(go.Scatter(x=datapm_musim.index, y=datapm_musim, name="PM2.5"),row=1,col=1)
fig.add_trace(go.Scatter(x=datatemp_musim.index, y=datatemp_musim, name="Temperature"),row=1,col=2)
fig.update_yaxes(title_text="PM2.5 (μg/m^3)", row=1, col=1)
fig.update_yaxes(title_text="T (oC)", row=1, col=2)
st.plotly_chart(fig, use_container_width=True)

# buat data per bulan
datapm_bulan = datadate.groupby(datadate['date'].dt.month)['PM2.5'].median()
datatemp_bulan = datadate.groupby(datadate['date'].dt.month)['TEMP'].mean()

# buat judul
st.header('Monthly Analysis')

# buat grafik musim
fig = make_subplots(rows=1, cols=2)
fig.add_trace(go.Scatter(x=datapm_bulan.index, y=datapm_bulan, name="PM2.5"),row=1,col=1)
fig.add_trace(go.Scatter(x=datatemp_bulan.index, y=datatemp_bulan, name="Temperature"),row=1,col=2)
fig.update_yaxes(title_text="PM2.5 (μg/m^3)", row=1, col=1)
fig.update_yaxes(title_text="T (oC)", row=1, col=2)
st.plotly_chart(fig, use_container_width=True)