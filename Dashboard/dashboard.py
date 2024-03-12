import streamlit as st
import pandas as pd
import matplotlib.pylab as plt
import datetime

all_records = pd.read_csv("Dashboard/main_data.csv")

st.header("Air Quality Analysis Data Statistic")

with st.container():
    all_records['timestamp'] = pd.to_datetime(all_records['datetime'])

    # Extract minimum and maximum timestamps from the dataset
    min_timestamp = all_records['timestamp'].min().date()
    max_timestamp = all_records['timestamp'].max().date()
    # Date picker for start date
    start_timestamp = st.date_input("Start Date", min_value=min_timestamp, max_value=max_timestamp, value=min_timestamp)

    # Date picker for end date
    end_timestamp = st.date_input("End Date", min_value=min_timestamp, max_value=max_timestamp, value=max_timestamp)

clean_data = all_records[(all_records['timestamp'] >= pd.to_datetime(start_timestamp)) & (all_records['timestamp'] <= pd.to_datetime(end_timestamp))]

st.subheader(f"Analysis from {start_timestamp} to {end_timestamp} at Multiple Locations")

with st.container():
    average_pm25_each_location = clean_data.groupby('station')['PM2.5'].mean()
    max_pm25_location = average_pm25_each_location.idxmax()
    min_pm25_location = average_pm25_each_location.idxmin()

    plt.figure(figsize=(12, 6))
    bars = plt.bar(x=average_pm25_each_location.keys(), height=average_pm25_each_location.values)

    for bar in bars:
        if bar.get_height() == average_pm25_each_location[max_pm25_location]:
            bar.set_color('red')  # Color max red
        elif bar.get_height() == average_pm25_each_location[min_pm25_location]:
            bar.set_color('green')  # Color min green

    plt.xlabel('Locations')
    plt.ylabel('PM2.5')
    plt.title('Average PM2.5 Level per Location from 2013 to 2017')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    average_pm25_each_location = {location: pm25 for location, pm25 in average_pm25_each_location.items() if pm25 is not None}

    # Divide the six sections
    sec1, sec2, sec3, sec4, sec5, sec6 = st.columns(6)

    # List of all sections
    sections = [sec1, sec2, sec3, sec4, sec5, sec6]

    # Get the the smallest and largest 
    min_location = min(average_pm25_each_location, key=average_pm25_each_location.get)
    max_location = max(average_pm25_each_location, key=average_pm25_each_location.get)

    # Iterate over the keys and values 
    for i, (location, pm25) in enumerate(average_pm25_each_location.items()):
        # Format after the decimal point
        pm25_formatted = "{:.2f}".format(pm25)

        # Write location name 
        with sections[i % len(sections)]:
            if location == min_location:
                st.metric(label=f"{location}", value=pm25_formatted, delta="min", delta_color="normal")
            elif location == max_location:
                st.metric(label=f"{location}", value=pm25_formatted, delta="max", delta_color="inverse")
            else:
                st.metric(label=location, value=pm25_formatted)

    st.pyplot(plt)

 
st.subheader("Comparison of NO2 Levels Each Months")
with st.container():
    mean_natrium_dioxide = clean_data.groupby(['year', 'month'])['NO2'].mean()
    mean_natrium_dioxide_dict = mean_natrium_dioxide.to_dict()  
    rain_months = [1, 2, 3, 4, 5, 6]
    dry_months = [7, 8, 9, 10, 11, 12]

    dry_NO2_levels = {}
    rain_NO2_levels = {}

    for key, value in mean_natrium_dioxide_dict.items():
        if key[1] in dry_months:
            dry_NO2_levels[key] = value
        elif key[1] in rain_months:
            rain_NO2_levels[key] = value

    # Convert the keys to datetime objects
    dry_dates = [datetime.datetime(year, month, 1) for year, month in dry_NO2_levels.keys()]
    rain_dates = [datetime.datetime(year, month, 1) for year, month in rain_NO2_levels.keys()]

    # Create a new figure
    plt.figure(figsize=(12, 6))

    # Plot rain_SO2_levels and dry_SO2_levels
    plt.bar(rain_dates, list(rain_NO2_levels.values()), label='Rain NO2', width=20)
    plt.bar(dry_dates, list(dry_NO2_levels.values()), label='Dry NO2', width=20)
    plt.xticks(rotation=45, ha='right')

    # Add a legend
    plt.legend()

    st.pyplot(plt)

st.caption("Copyright (c) 2024 Dwi Nafis Mahardika")
