import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="MLB OPS Leaderboard", layout="wide")
st.title("⚾ 2024 MLB OPS Leaderboard")
st.write("This app pulls live MLB data using the public MLB Stats API and ranks players by OPS.")

# Step 1: Get the data from the API
@st.cache_data(show_spinner=True)
def load_data():
    url = "https://statsapi.mlb.com/api/v1/stats"
    params = {
        "stats": "season",
        "group": "hitting",
        "gameType": "R",
        "season": "2024",
        "playerPool": "all"
    }
    response = requests.get(url, params=params)
    data = response.json()
    player_stats = data['stats'][0]['splits']

    rows = []
    for player in player_stats:
        row = player['stat']
        row['name'] = player['player']['fullName']
        rows.append(row)

    df = pd.DataFrame(rows)
    df['ops'] = pd.to_numeric(df['ops'], errors='coerce')
    df['avg'] = pd.to_numeric(df['avg'], errors='coerce')
    df['obp'] = pd.to_numeric(df['obp'], errors='coerce')
    df['slg'] = pd.to_numeric(df['slg'], errors='coerce')
    df = df[df['ops'].notna()]
    return df

df = load_data()

# Step 2: Filter players with at least 50 plate appearances
df = df[df['plateAppearances'].astype(float) > 50]

# Step 3: Sort and display
st.subheader("Top Hitters by OPS (min. 50 PA)")
st.dataframe(
    df[['name', 'avg', 'obp', 'slg', 'ops', 'plateAppearances']].sort_values(by='ops', ascending=False).reset_index(drop=True),
    use_container_width=True
)