import streamlit as st
from graph import bengaluru
import pandas as pd
from PIL import Image
import os

# Get absolute base directory of the current script
BASE_DIR = os.path.dirname(__file__)

# Build absolute paths for images
icon_path = os.path.join(BASE_DIR, "images", "icon.png")
metro_logo_path = os.path.join(BASE_DIR, "images", "namma_metro.png")
metro_map_path = os.path.join(BASE_DIR, "images", "bengaluru_map.jpg")

# Page configuration
st.set_page_config(
    page_title="Metro Planner",
    page_icon=icon_path,
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Bengaluru Metro Planner \n~Suhas Prabhu"
    }
)

# Sidebar logo
st.sidebar.image(metro_logo_path)

# Stations list from the graph
stations = bengaluru.keys()

# Title
st.markdown(
    "<h1 style='text-align: center; color: white;'>Bengaluru Metro Travel Planner</h1>",
    unsafe_allow_html=True
)

# Main metro map
metro_map = Image.open(metro_map_path)
st.image(metro_map)

st.markdown(
    "<h2 style='text-align: center; color: white;'>Enter Station Names</h2>",
    unsafe_allow_html=True
)

# Adjust spacing for select boxes and text areas
st.markdown(
    """
    <style>
    [data-baseweb="select"] {
        margin-top: -30px;
    }
    [data-baseweb="textarea"] {
        margin-top: -30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Source and Destination selectors
st.write("### Source")
source = st.selectbox("Source", stations)
st.write("### Destination")
dest = st.selectbox("Destination", stations)

# DFS function to find shortest path
def dfs(bengaluru, s, e, minlength=-1, path=[]):
    path = path + [s]
    if s == e:
        return path
    if s not in bengaluru:
        return None
    shortest = None
    for node in bengaluru[s]:
        if node not in path:
            if minlength == -1 or len(path) < (minlength - 1):
                new = dfs(bengaluru, node, e, minlength, path)
                if new:
                    if not shortest or len(new) < len(shortest):
                        shortest = new
                        minlength = len(new)
    return shortest

start = source
end = dest

# Search button
button1 = st.button('Search Route')

if st.session_state.get('button') != True:
    st.session_state['button'] = button1

if st.session_state['button'] == True:
    path = dfs(bengaluru, start, end)
    output = pd.DataFrame({"Station Name": path})
    output.index += 1
    st.write(f"#### {start} to {end} Route : ")
    st.write(output)

    if st.button('Return Route'):
        path.reverse()
        output2 = pd.DataFrame({"Station Name": path})
        output2.index += 1
        st.write(f"#### {end} to {start} Route : ")
        st.write(output2)
        st.session_state['button'] = False
