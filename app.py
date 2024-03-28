import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
# from geocode import update_data

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

csv = "data.csv"
# update_data()


# main
st.title("Kyoto Tachibana SHS Band Travel Map")

# data = pd.DataFrame(
#    np.random.randn(10, 2) / [99999, 99999] + [34.9321689, 135.7785686],
#    columns=['lat', 'lon'])

data = pd.read_csv(csv)
data.dropna(inplace=True)

# ICON_URL = "https://img.icons8.com/plasticine/100/000000/marker.png"
# ICON_URL = "https://static-00.iconduck.com/assets.00/tangerine-emoji-478x512-gkxeysdm.png"
ICON_URL = "https://static-00.iconduck.com/assets.00/tangerine-emoji-512x510-bjsdm1qw.png"




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



# add embedded youtube
html_youtube_embed = '# <iframe width="560" height="315" src="https://www.youtube.com/embed/ZVJ3Ho83Ksg?si=eF5jUW3EJhXulnzo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',


tooltip = {
   "html": "<b>Event Name:</b> {event_name} <br/> <b>Date:</b> {date} <br/>" + f"{html_youtube_embed}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}

# st.dataframe(data)


st.pydeck_chart(pdk.Deck(
    map_style='road',
    initial_view_state=pdk.ViewState(
        latitude=34.9321689,
        longitude=135.7785686,
        zoom=15,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            type="IconLayer",
            data=data,
            get_icon="icon_data",
            get_size=4,
            size_scale=4,
            get_position=["lon", "lat"],
            pickable=True,
        )

    ],
    tooltip=tooltip
))


