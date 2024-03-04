import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
#load dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

#cleaning day data
#convert dteday(object) menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weathersit'] = day_df['weathersit'].map({1: 'Clear/Few clouds',2:'Mist',3: 'Light Snow',4: 'Heavy Rain'})
day_df['weekday'] = pd.to_datetime(day_df['dteday']).dt.day_name()
day_df['mnth'] = pd.to_datetime(day_df['dteday']).dt.month_name()
day_df['yr'] = day_df['dteday'].dt.year

# Mengubah nama judul kolom agar terlihat jelas
day_df = day_df.rename({
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count',
    'weathersit': 'weather',
    'hum' : 'humidity'
}, axis='columns')

#cleaning hour data
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['season'] = hour_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
hour_df['weathersit'] = hour_df['weathersit'].map({1: 'Clear/Few clouds',2:'Mist',3: 'Light Snow',4: 'Heavy Rain'})
hour_df['weekday'] = pd.to_datetime(hour_df['dteday']).dt.day_name()
hour_df['mnth'] = pd.to_datetime(hour_df['dteday']).dt.month_name()
hour_df['yr'] = hour_df['dteday'].dt.year

hour_df = hour_df.rename({
    'dteday': 'dateday',
    'yr': 'year',
    'hr':'hour',
    'mnth': 'month',
    'cnt': 'count',
    'weathersit': 'weather',
    'hum' : 'humidity'
}, axis='columns')

#cretae functian 
def count_daily_rent_bike(df):
    daily_rent_bike = df.groupby(by='dateday').agg({'count': 'sum'}).reset_index()
    return daily_rent_bike

# Menyiapkan daily_casual_rent_df
def count_daily_casual_rent_bike(df):
    daily_casual_rent_bike = df.groupby(by='dateday').agg({'casual': 'sum'}).reset_index()
    return daily_casual_rent_bike

# Menyiapkan daily_registered_rent_df
def count_daily_registered_rent_bike(df):
    daily_registered_rent_bike = df.groupby(by='dateday').agg({'registered': 'sum'}).reset_index()
    return daily_registered_rent_bike

def count_season_df(df):
    count_season = df.groupby(by="season").agg({'count':'sum'
            ,'casual':'sum','registered':'sum'}).reset_index()
    return count_season

def count_year_df(df):
    count_year = df.groupby(by="year").agg({'count':'sum','casual':'sum','registered':'sum'}).reset_index()
    return count_year

def count_month_df(df):
    count_month = df.groupby(by="month").agg({'count':'sum','casual':'sum','registered':'sum'}).reset_index()
    return count_month

def count_holiday_df(df):
    count_holiday = df.groupby(by="holiday").agg({'count':'sum','casual':'sum','registered':'sum'}).reset_index()
    return count_holiday

def count_weekday_df(df):
    count_weekday = df.groupby(by="weekday").agg({'count':'sum','casual':'sum','registered':'sum'}).reset_index().sort_values(by='count', ascending=False)  
    return count_weekday

def count_workingday_df(df):
    count_workingday = df.groupby(by="workingday").agg({'count':'sum','casual':'sum','registered':'sum'}).reset_index().sort_values(by='count', ascending=False)  
    return count_workingday

def count_weather_df(df):
    count_weather = df.groupby(by="weather").agg({'count':'sum','casual':'sum','registered':'sum'}).reset_index().sort_values(by='count', ascending=False)  
    return count_weather
    
# membuat side bar 
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()
 
with st.sidebar:
    st.image('bike.jpeg')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )
main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

#ambil nilai tiap fuction untuk membuat dataframe pada day_data
daily_rent_bike=count_daily_rent_bike(main_df)
daily_casual_rent_bike=count_daily_casual_rent_bike(main_df)
daily_registered_rent_bike=count_daily_registered_rent_bike(main_df)
count_season=count_season_df(main_df)
count_year=count_year_df(main_df)
count_month=count_month_df(main_df)
count_holiday=count_holiday_df(main_df)
count_weekday=count_weekday_df(main_df)
count_workingday=count_workingday_df(main_df)
count_weather=count_weather_df(main_df)


# Membuat judul
st.header('Bike Sharing Dashboard 🚲')

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_casual_sum = daily_casual_rent_bike['casual'].sum()
    st.metric('Casual User', value=daily_casual_sum)
with col2:
    daily_registered_sum = daily_registered_rent_bike['registered'].sum()
    st.metric('Registered User', value=daily_registered_sum)

with col3:
    total_rentals_sum = daily_rent_bike['count'].sum()
    st.metric('Total User', value=total_rentals_sum)

#pertanyaan no 1
st.set_option('deprecation.showPyplotGlobalUse', False)  # Disable deprecation warning
st.write("Graph depicting the trend of bike-sharing usage between {0}, and {1}.".format(start_date, end_date))

# Plot using seaborn
fig = px.line(daily_rent_bike, x='dateday', y='count', title='Bike-Sharing Tren ({0} - {1})'.format(start_date, end_date))
fig.update_xaxes(title='date')
fig.update_yaxes(title='Total')
fig.update_layout(xaxis=dict(tickformat='%d-%m-%Y'))
st.plotly_chart(fig, use_container_width=True)

# Plot monhthly
result = day_df.resample(rule='M', on='dateday').agg({"count": "sum", "casual": "sum", "registered": "sum"})
fig = px.line(result, x=result.index.strftime('%B %Y'), y=['count', 'casual', 'registered'],
              title="Monthly Count of Bikeshare Rides",
              labels={'x': 'Month', 'y': 'Total'},
              markers=True)
st.plotly_chart(fig, use_container_width=True)

#pertanyaan no 2 use haour_data
result = hour_df.groupby(by="hour").agg({'count':'sum','casual':'sum','registered':'sum'}).reset_index()
# Plot using Plotly Express
fig = px.line(result, x='hour', y=['count', 'casual', 'registered'], 
              labels={'hour': 'Hour', 'value': 'Total Rides', 'variable': 'Type'},
              title='Hourly Bike-sharing Rides',
              markers=True)

fig.update_layout(xaxis=dict(tickmode='linear', dtick=1), 
                  yaxis_title='Total Rides')
st.plotly_chart(fig)

#no3

workingday_df = day_df.groupby(by="workingday").agg({'count':'mean', 'casual':'mean', 'registered':'mean'}).reset_index()
holiday_df = day_df.groupby(by="holiday").agg({'count':'mean', 'casual':'mean', 'registered':'mean'}).reset_index()
workingday_df['workingday'] = workingday_df['workingday'].replace({0: 'not workingday',1: 'workingday'})
holiday_df['holiday'] = holiday_df['holiday'].replace({0: 'not holiday',1:'holiday'})
# Plot for working days
fig1 = px.bar(workingday_df, x='workingday', y=['count', 'casual', 'registered'], 
              barmode='group', title='Working Day', 
              labels={'value': 'Number of Rentals', 'variable': 'Rental Type'})

# Plot for holidays
fig2 = px.bar(holiday_df, x='holiday', y=['count', 'casual', 'registered'], 
              barmode='group', title='Holiday', 
              labels={'value': 'Number of Rentals', 'variable': 'Rental Type'})

st.title('The Influence of Workdays and Holidays on Bike-Sharing (average)')
st.plotly_chart(fig1)
st.plotly_chart(fig2)


#no4 dan 5
st.title('The Influence of Season and Weather on Bike-sharing')
chart1, chart2 = st.columns((2))
with chart1:  # Gunakan beta_container untuk keluaran yang bersamaan
    st.subheader(' Season')
    fig1 = px.pie(count_season, values="count", names="season", template="plotly_dark",width=300, height=300)
    fig1.update_traces(text=count_season["season"], textposition="inside")
    st.plotly_chart(fig1)

# Chart 2: Weather
with chart2:  # Gunakan beta_container untuk keluaran yang bersamaan
    st.subheader('Weather')
    fig2 = px.pie(count_weather, values="count", names="weather", template="gridon",width=300, height=300)
    fig2.update_traces(text=count_weather["weather"], textposition="inside")
    st.plotly_chart(fig2)

#no6
x_variables = ['temp', 'atemp', 'humidity', 'windspeed']
fig = make_subplots(rows=2, cols=2, subplot_titles=[f'count vs {col.capitalize()}' for col in x_variables])
for i, col in enumerate(x_variables):
    fig.add_trace(go.Scatter(x=day_df[col], y=hour_df['count'], mode='markers', name=f'count vs {col.capitalize()}'), 
                  row=i // 2 + 1, col=i % 2 + 1)
st.title('Scatter Plots of count vs Weather Variables')
fig.update_layout(height=600, width=800)
st.plotly_chart(fig)