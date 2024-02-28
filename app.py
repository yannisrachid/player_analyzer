import streamlit as st
from dataviz import *

st.markdown("<h3 style='text-align: left; color: black;'>For any contact or support:</h3>", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.markdown("[![My LinkedIn profile](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/yannis-rachid-230/)")
with col2:
    st.markdown('<a href="https://www.buymeacoffee.com/yannisr" target="_blank"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=votrepseudo&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff"></a>', unsafe_allow_html=True)

@st.cache_data
def load_data(path_df):
    df = pd.read_csv(path_df, header=[0, 1], index_col=[0, 1, 2, 3])
    new_columns = [(a, b if not 'Unnamed' in b else '') for a, b in df.columns]
    df.columns = pd.MultiIndex.from_tuples(new_columns)
    df = df.reset_index()
    df = df.sort_values(by=["league", "team", "player"])
    try:
        df['age'] = df['age'].apply(lambda x: x[:2])
        df['age'] = df['age'].astype(float)
    except TypeError:
        print("Age column already in the right type")
    df = df[df["pos"] != "GK"]
    return df

all_types = ["standard", "shooting", "passing", "goal_shot_creation", "possession", "misc", "defense"]
data = {}
for type_data in all_types:
    data[type_data] = load_data("data/{}_player_season_stats.csv".format(type_data))

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image("img/logo_tr.png")
with col3:
    st.write(' ')

st.sidebar.markdown("<h1 style='text-align: center; color: white;'>{}</h1>".format("Player analyzer by Yannis R"), unsafe_allow_html=True)
st.sidebar.text("Data last updated on 02-28-2024")

compare_data = data.copy()

league = st.sidebar.selectbox(
    'Select a league',
    data["standard"]["league"].unique())
for type_data in all_types:
    data[type_data] = data[type_data][data[type_data]["league"] == league]

club = st.sidebar.selectbox(
    'Select a club',
    data["standard"]["team"].unique())
for type_data in all_types:
    data[type_data] = data[type_data][data[type_data]["team"] == club]

player = st.sidebar.selectbox(
    'Select a player',
    data["standard"]["player"].unique())
for type_data in all_types:
    data[type_data] = data[type_data][data[type_data]["player"] == player]
    
compare_champ = st.sidebar.multiselect("Compare with", compare_data["standard"]["league"].unique(), default = compare_data["standard"]["league"].unique())

if len(compare_champ) == 0:
    st.sidebar.error("Please select at least one competition.")
for type_data in all_types:
    compare_data[type_data] = compare_data[type_data][compare_data[type_data]["league"].isin(compare_champ)].reset_index()


compare_percentile = st.sidebar.slider("Compare player with the percentile", min_value=1, max_value=30, value=5)
ages = st.sidebar.slider('Select an age group', 15, 45, (15, 45))
minutes = st.sidebar.slider('Select a minimum number of minutes', min_value=90, max_value=1500, value=900)

per_90 = st.sidebar.checkbox("Aggregate per 90", value=False)

if ages:
    for type_data in all_types:
        compare_data[type_data]['age'] = compare_data[type_data]['age'].str.split('-').str[0].astype(float)
        compare_data[type_data] = compare_data[type_data][(compare_data[type_data].age >= ages[0]) & (compare_data[type_data].age <= ages[1])]
    
    player_already_in_compare_data = any(player in compare_data[type_data]["player"].values for type_data in all_types)

    if not player_already_in_compare_data:        
        st.sidebar.text("The chosen player is not included in\nthis selected filtering! We add him...")
        for type_data in all_types:
            player_data = data[type_data][data[type_data]["player"] == player]
            compare_data[type_data] = pd.concat([compare_data[type_data], player_data], ignore_index=True)

pos_player = data["standard"]["pos"].values[0]

st.markdown("<h1 style='text-align: center; color: black;'>{}</h1>".format(data["standard"]["player"].values[0]), unsafe_allow_html=True)

for type_data in all_types:
    st.pyplot(plot_radar(compare_data[type_data], data[type_data], pos_player, player, compare_percentile, per_90, type_data, minutes))
