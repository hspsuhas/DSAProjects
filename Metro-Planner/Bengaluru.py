import os
from pathlib import Path
import difflib
import streamlit as st
import pandas as pd
from PIL import Image
from graph import bengaluru  # <-- keep your full, updated adjacency dict here

# -----------------------------
# Paths & Safe Image Loading
# -----------------------------
BASE_DIR = Path(__file__).parent
icon_path = BASE_DIR / "images" / "icon.png"
metro_logo_path = BASE_DIR / "images" / "namma_metro.png"
metro_map_path = BASE_DIR / "images" / "bengaluru_map.jpg"

def load_image_safe(path: Path):
    try:
        return Image.open(path)
    except Exception:
        return None

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Bengaluru Metro Planner",
    page_icon=str(icon_path) if icon_path.exists() else "🗺️",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "# Bengaluru Metro Planner \n~Suhas Prabhu",
    },
)

# -----------------------------
# Sidebar Branding
# -----------------------------
logo = load_image_safe(metro_logo_path)
if logo is not None:
    st.sidebar.image(logo, use_container_width=True)
else:
    st.sidebar.info("Logo not found. Ensure `images/namma_metro.png` is in the repo.")

st.sidebar.markdown("#### Tips")
st.sidebar.write(
    "- Start typing a station name to filter.\n"
    "- If you mistype, we’ll suggest the closest match.\n"
    "- Interchange stations are highlighted."
)

# -----------------------------
# Simple Theme Polish
# -----------------------------
st.markdown(
    """
    <style>
    .metric-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(140px, 1fr));
        gap: 8px;
        margin: 8px 0 16px 0;
    }
    .metric-box {
        background: #1f2937;
        border-radius: 12px;
        padding: 12px 14px;
        color: #fff;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    }
    .metric-box .value { font-size: 22px; font-weight: 700; }
    .metric-box .label { font-size: 12px; opacity: 0.8; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Title & Map
# -----------------------------
st.markdown(
    "<h1 style='text-align:center; color:#f8fafc;'>Bengaluru Metro Travel Planner</h1>",
    unsafe_allow_html=True,
)

city_map = load_image_safe(metro_map_path)
if city_map is not None:
    st.image(city_map, use_container_width=True)
else:
    st.warning("Map not found. Add `images/bengaluru_map.jpg` to your repo to show it here.")

st.markdown(
    "<h3 style='text-align:center; color:#f8fafc;'>Choose Your Route</h3>",
    unsafe_allow_html=True,
)

# -----------------------------
# Station Helpers
# -----------------------------
all_stations = sorted(bengaluru.keys())

def closest_station_name(user_text: str, cutoff: float = 0.65):
    """Return the closest station name for a possibly mistyped input."""
    if not user_text:
        return None
    matches = difflib.get_close_matches(user_text.upper(), all_stations, n=1, cutoff=cutoff)
    return matches[0] if matches else None

def is_interchange(station: str) -> bool:
    """Heuristic: degree >= 3 is likely an interchange."""
    # Some known interchanges might have degree==2 due to data specifics; keep a manual allow-list too.
    manual = {
        "NADAPRABHU KEMPEGOWDA STATION, MAJESTIC",
        "KRANTIVIRA SANGOLLI RAYANNA RAILWAY STATION",
        "SRI M VISVESWARAYA STATION, CENTRAL COLLEGE",
        "RASHTREEYA VIDYALAYA ROAD",
        "JAYADEVA HOSPITAL",
        "CENTRAL SILK BOARD",
    }
    deg = len(bengaluru.get(station, []))
    return deg >= 3 or station in manual

# -----------------------------
# Shortest Path (BFS)
# -----------------------------
from collections import deque

def shortest_path(graph: dict, start: str, end: str):
    """Unweighted shortest path via BFS."""
    if start == end:
        return [start]
    visited = set([start])
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        for nei in graph.get(node, []):
            if nei not in visited:
                visited.add(nei)
                new_path = path + [nei]
                if nei == end:
                    return new_path
                queue.append(new_path)
    return None

# -----------------------------
# Metrics: Distance, Time, Fare
# -----------------------------
STATION_DISTANCE_KM = 1.2    # avg spacing assumption
AVERAGE_SPEED_KMPH = 32      # typical metro average incl. dwell
MIN_DWELL_SEC = 25           # per stop average dwell time

def calc_distance_km(path):
    return max(0, (len(path) - 1)) * STATION_DISTANCE_KM

def calc_time_minutes(path):
    # run time: distance/speed + dwell_time*(stops-1)
    dist = calc_distance_km(path)
    run_minutes = (dist / AVERAGE_SPEED_KMPH) * 60.0
    dwell_minutes = max(0, (len(path) - 1)) * (MIN_DWELL_SEC / 60.0)
    return int(round(run_minutes + dwell_minutes))

def calc_fare(distance_km: float) -> int:
    # Simple slab; adjust as needed to match current BMRCL fare matrix
    if distance_km <= 2: return 10
    elif distance_km <= 5: return 15
    elif distance_km <= 10: return 25
    elif distance_km <= 15: return 35
    elif distance_km <= 20: return 45
    else: return 60

# -----------------------------
# UI Inputs (with fuzzy fix)
# -----------------------------
colA, colB = st.columns(2)
with colA:
    source = st.selectbox("Source", all_stations, index=0, key="src_select")
with colB:
    dest = st.selectbox("Destination", all_stations, index=min(1, len(all_stations)-1), key="dst_select")

st.write("Or type to auto-correct a misspelled station (optional):")
colC, colD = st.columns(2)
with colC:
    typo_src = st.text_input("Source (free text)", placeholder="e.g., majestic")
with colD:
    typo_dst = st.text_input("Destination (free text)", placeholder="e.g., rv road")

fix_btn = st.button("Auto-correct typed names")
if fix_btn:
    c_src = closest_station_name(typo_src) if typo_src else None
    c_dst = closest_station_name(typo_dst) if typo_dst else None
    if c_src:
        source = c_src
        st.success(f"Source corrected to **{source}**")
    if c_dst:
        dest = c_dst
        st.success(f"Destination corrected to **{dest}**")
    if not c_src and typo_src:
        st.warning("Couldn’t find a close match for the typed source.")
    if not c_dst and typo_dst:
        st.warning("Couldn’t find a close match for the typed destination.")

# -----------------------------
# Find & Display Routes
# -----------------------------
go = st.button("Search Route 🔎")

def style_route_df(df: pd.DataFrame):
    def row_style(row):
        station = row["Station"]
        if station == source or station == dest:
            return ["font-weight:700; background-color:#0ea5e9; color:white"] * len(row)
        if is_interchange(station):
            return ["background-color:#eab308; color:black; font-weight:600"] * len(row)
        return [""] * len(row)

    return df.style.apply(row_style, axis=1)

if go:
    if source == dest:
        st.info("Source and destination are the same. Please pick different stations.")
    else:
        path = shortest_path(bengaluru, source, dest)
        if not path:
            st.error("No route found between the selected stations. Please verify station names.")
        else:
            # Metrics
            distance_km = round(calc_distance_km(path), 2)
            time_min = calc_time_minutes(path)
            fare = calc_fare(distance_km)

            st.markdown("<div class='metric-row'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='metric-box'><div class='value'>{distance_km} km</div><div class='label'>Total Distance</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='metric-box'><div class='value'>{time_min} min</div><div class='label'>Est. Travel Time</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='metric-box'><div class='value'>₹{fare}</div><div class='label'>Est. Fare</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Build dataframes
            df_forward = pd.DataFrame({"#": range(1, len(path)+1), "Station": path})
            df_return = df_forward.iloc[::-1].reset_index(drop=True)
            df_return["#"] = range(1, len(df_return)+1)

            c1, c2 = st.columns(2)
            with c1:
                st.subheader(f"{source} → {dest}")
                st.dataframe(style_route_df(df_forward), use_container_width=True)
            with c2:
                st.subheader(f"{dest} → {source}")
                st.dataframe(style_route_df(df_return), use_container_width=True)

            # Small legend
            st.caption("🟦 start/end  •  🟨 interchange")

# -----------------------------
# Safety: Warn if images missing in repo (Cloud gotchas)
# -----------------------------
missing = []
for p in (icon_path, metro_logo_path, metro_map_path):
    if not p.exists():
        missing.append(str(p.relative_to(BASE_DIR)))
if missing:
    st.sidebar.warning(
        "Missing files in repo:\n- " + "\n- ".join(missing) +
        "\n\nCommit & push these files so Streamlit Cloud can load them."
    )
