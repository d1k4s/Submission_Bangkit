import streamlit as st
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import datetime

all_data = pd.read_csv(".\Dashboard\main_data.csv")

st.header("Air Quality Analysis Data Statistic")

with st.container():
    all_data['datetime'] = pd.to_datetime(all_data['datetime'])

    # Extract minimum and maximum dates from the dataset
    min_date = all_data['datetime'].min().date()
    max_date = all_data['datetime'].max().date()
    # Date picker for start date
    start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)

    # Date picker for end date
    end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

clean_combined_df = all_data[(all_data['datetime'] >= pd.to_datetime(start_date)) & (all_data['datetime'] <= pd.to_datetime(end_date))]

st.subheader(f"Analysis from {start_date} to {end_date} at Multiple Stations")

with st.container():
    average_pm25_each_station = clean_combined_df.groupby('station')['PM2.5'].mean()
    max_pm25_station = average_pm25_each_station.idxmax()
    min_pm25_station = average_pm25_each_station.idxmin()

    plt.figure(figsize=(18, 8))
    bars = plt.bar(x=average_pm25_each_station.keys(), height=average_pm25_each_station.values)

    for bar in bars:
        if bar.get_height() == average_pm25_each_station[max_pm25_station]:
            bar.set_color('red')  # Color max red
        elif bar.get_height() == average_pm25_each_station[min_pm25_station]:
            bar.set_color('green')  # Color min green

    plt.xlabel('Stations')
    plt.ylabel('PM2.5')
    plt.title('Average PM2.5 Level per Station from 2013 to 2017')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    average_pm25_each_station = {station: pm25 for station, pm25 in average_pm25_each_station.items() if pm25 is not None}

    # Divide the six columns
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # List of all columns
    columns = [col1, col2, col3, col4, col5, col6]

    # Get the the smallest and largest 
    min_station = min(average_pm25_each_station, key=average_pm25_each_station.get)
    max_station = max(average_pm25_each_station, key=average_pm25_each_station.get)

    # Iterate over the keys and values 
    for i, (station, pm25) in enumerate(average_pm25_each_station.items()):
        # Format after the decimal point
        pm25_formatted = "{:.2f}".format(pm25)

        # Write station name 
        with columns[i % len(columns)]:
            if station == min_station:
                st.metric(label=f"{station}", value=pm25_formatted, delta="min", delta_color="normal")
            elif station == max_station:
                st.metric(label=f"{station}", value=pm25_formatted, delta="max", delta_color="inverse")
            else:
                st.metric(label=station, value=pm25_formatted)

    st.pyplot(plt)

st.subheader("Corelation between PM10 and CO")
with st.container():
    mean_PM10_monthly = clean_combined_df.groupby(['year', 'month'])['PM10'].mean()
    mean_CO_monthly = clean_combined_df.groupby(['year', 'month'])['CO'].mean()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Average PM10", value="{:.2f}".format(mean_PM10_monthly.mean()))

    with col2:
        st.metric(label="Average CO", value="{:.2f}".format(mean_CO_monthly.mean()))

    with st.container():
        plt.figure(figsize=(12, 8))
        sns.regplot(x=mean_PM10_monthly.values, y=mean_CO_monthly.values)
        plt.xlabel("PM10 levels")
        plt.ylabel("CO levels")
        st.pyplot(plt)

st.subheader("Comparison of SO2 Levels Between Rain and Dry Months")
with st.container():
    mean_SO2 = clean_combined_df.groupby(['year', 'month'])['SO2'].mean()
    mean_SO2_dict = mean_SO2.to_dict()  
    rain_month = [6,7,8]
    dry_mount = [11,12,1,2]

    dry_SO2 = {}
    rain_SO2 = {}

    for key, value in mean_SO2_dict.items():
        if key[1] in dry_mount:
            dry_SO2[key] = value
        elif key[1] in rain_month:
            rain_SO2[key] = value

    # Convert the keys to datetime objects
    dry_dates = [datetime.datetime(year, month, 1) for year, month in dry_SO2.keys()]
    rain_dates = [datetime.datetime(year, month, 1) for year, month in rain_SO2.keys()]

    # Create a new figure
    plt.figure(figsize=(16,8))

    # Plot rain_SO2 and rain_SO2
    plt.bar(rain_dates, list(rain_SO2.values()), label='Rain SO2',width=20)
    plt.bar(dry_dates, list(dry_SO2.values()), label='Dry SO2',width=20)

    # Add a legend
    plt.legend()

    st.pyplot(plt)

st.caption("Copyright (c) 2024 Dwi Nafis Mahardika")
