import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import datetime
# from geocode import update_data

# page config
st.set_page_config("🗺️ KT Travel Map", page_icon="🍊", layout="wide", initial_sidebar_state="collapsed")

# reduce top margin
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)


# Add custom CSS to hide the GitHub icon
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# init data
csv = "data.csv"
data = pd.read_csv(csv)
data.dropna(inplace=True)
data['timestamp'] = pd.to_datetime(data.date, format='mixed')
ICON_URL = "https://static-00.iconduck.com/assets.00/tangerine-emoji-512x510-bjsdm1qw.png"

df_expedition = pd.read_csv("expeditions.csv")

# custom map icon
icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": ICON_URL,
    "width": 128,
    "height": 128,
    "anchorY": 128,
}
data["icon_data"] = None
for i in data.index:
    data["icon_data"][i] = icon_data


# tooltips
# add embedded youtube, this is a proof of concept
html_youtube_embed = '# <iframe width="560" height="315" src="https://www.youtube.com/embed/ZVJ3Ho83Ksg?si=eF5jUW3EJhXulnzo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
tooltip = {
   "html": """
   <b>Event Name:</b> {event_name} <br/> 
   <b>Date:</b> {date} <br/>
   <b>Location:</b> {location} <br/>
   """,
#    + f"{html_youtube_embed}", # disabled until we have a better database

   "style": {
        "backgroundColor": "black",
        "color": "white"
   }
}

# side bar
# st.sidebar.markdown("## About")
# st.sidebar.write("This is a fan-made project. Data is acquired from https://kyototachibanashsbandunofficialfanblog.wordpress.com/")

st.sidebar.markdown("## Options")






# main
st.title("Kyoto Tachibana SHS Band Travel Map")
st.markdown("### BETA - Some data may be inaccurate")


# date range setting
date_range = data['timestamp'].min().to_pydatetime(), data['timestamp'].max().to_pydatetime()

# showing max date range compresses more recent events to a short window
if st.sidebar.checkbox("Hide events before 2012"):
    date_range = datetime.strptime("20120101", "%Y%m%d"), data['timestamp'].max().to_pydatetime()


# c1, c2, c3, c4, c5 = st.columns(5)
# c1.checkbox('114')
# c2.checkbox('115')
# c3.checkbox('116')
# c4.checkbox('117')
# c5.checkbox('118')





# select data by time
start_date, end_date = st.slider(
    'Select date range',
    # options=data['timestamp'],
    value=date_range,
    format="MM/DD/YY",
    )
mask = (data['timestamp'] >= start_date) & (data['timestamp'] <= end_date)
df_selected = data.loc[mask]



# school centered
# backup ini view
initial_view_state=pdk.ViewState(
    latitude=34.9321689,
    longitude=135.7785686,
    zoom=5,
    pitch=0,
)

# good view, but breaks if slider selected range with no data
if len(df_selected) != 0:
    initial_view_state = pdk.data_utils.viewport_helpers.compute_view(df_selected[['lon', 'lat']])
else:
    st.info("ℹ    There is no event in your selected date range. Try again with a wider selection")


icon_layer = pdk.Layer(
                    type="IconLayer",
                    data=df_selected,
                    get_icon="icon_data",
                    get_size=4,
                    size_scale=4,
                    get_position=["lon", "lat"],
                    pickable=True,
                )

layers = [icon_layer]

# Specify a deck.gl ArcLayer
if st.sidebar.checkbox("Show Expedition Arcs"):
    arc_layer = pdk.Layer(
                            "GreatCircleLayer",
                            data=df_expedition,
                            # greatCircle=True,
                            get_stroke_width=12,
                            # get_width="S000 * 2",
                            # getHeight=0.5,
                            get_source_position=["lon", "lat"],
                            get_target_position=["lon_dest", "lat_dest"],
                            # get_tilt=-45,
                            get_source_color=[0, 255, 0, 255],
                            get_target_color=[240, 100, 0, 255],
                            pickable=True,
                            auto_highlight=True,
                        )
    layers = [icon_layer, arc_layer]

# map object
chart = pdk.Deck(
    map_style='light',
    map_provider ="carto",
    initial_view_state=initial_view_state,
    layers=layers,
    tooltip=tooltip,
    # tooltip=True,
    )

chart.picking_radius = 10
st.components.v1.html(chart.to_html(as_string=True), height=700) 



