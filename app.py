import streamlit as st
from dataviz import *

df = pd.read_csv("data/fbref_data_2324_big5_291113.csv")

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
    # df['age'] = df['age'].astype(float)
    return df

all_types = ["standard", "shooting", "passing", "goal_shot_creation", "possession"]
data = {}
for type_data in all_types:
    data[type_data] = load_data("data/{}_player_season_stats.csv".format(type_data))

# def clean_league(string):
#     return " ".join(string.split()[1:])

# def clean_df(df):
#     df.drop(columns=["Matches Misc", "Matches Play", "Matches Poss", "Matches Def", "Matches Gca", "Matches Pt", "Matches Pass", "Matches St", "Matches Std"], axis=1, inplace=True)
#     df = df[df["Min"] != "Min"].reset_index(drop=True)
#     df["Comp"] = df["Comp"].apply(clean_league)
#     df = df.sort_values(by=["Comp", "Squad", "Player"])
#     cols = list(df.columns)[6:-3]
#     for col in cols:
#         # df[col] = df[col].astype(float)
#         # df[col] = df[col].apply(float)
#         df[col] = df[col].apply(lambda x: float(x) if x != 'na' else 0.001)
#     return df

# df = clean_df(df)

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image("img/logo_tr.png")
with col3:
    st.write(' ')

st.sidebar.markdown("<h1 style='text-align: center; color: white;'>{}</h1>".format("Player radarplot by Yannis R"), unsafe_allow_html=True)
st.sidebar.text("Data last updated on 02-20-24")

compare_data = data.copy()

league = st.sidebar.selectbox(
    'Select a league',
    data["standard"]["league"].unique())
for type_data in all_types:
    data[type_data] = data[type_data][data[type_data]["league"] == league] #.reset_index()
# df_league = df[df["Comp"] == league].reset_index(drop=True)

club = st.sidebar.selectbox(
    'Select a club',
    data["standard"]["team"].unique())
for type_data in all_types:
    data[type_data] = data[type_data][data[type_data]["team"] == club] #.reset_index()

# df_club = df_league[df_league["Squad"] == club].reset_index(drop=True)
# df_club = df_club[df_club["Pos"] != "GK"].reset_index(drop=True)

player = st.sidebar.selectbox(
    'Select a player',
    data["standard"]["player"].unique())
for type_data in all_types:
    data[type_data] = data[type_data][data[type_data]["player"] == player] #.reset_index()

# df_player = df_club[df_club["Player"] == player].reset_index(drop=True)

compare_champ = st.sidebar.radio("Compare with", (league, 'Big 5 Leagues'))
if compare_champ == league:
    for type_data in all_types:
        compare_data[type_data] = compare_data[type_data][compare_data[type_data]["league"] == league].reset_index()
    # df = df[df["Comp"] == league].reset_index(drop=True)

compare_percentile = st.sidebar.slider("Compare player with the top %", min_value=1, max_value=30, value=5)
ages = st.sidebar.slider('Select an age group', 15, 45, (15, 45))
minutes = st.sidebar.slider('Select a minimum number of minutes', min_value=90, max_value=1500, value=900)

if ages:
    for type_data in all_types:
        compare_data[type_data]['age'] = compare_data[type_data]['age'].str.split('-').str[0].astype(float)
        # compare_data[type_data]['age'] = compare_data[type_data]['age'].astype(float)
        compare_data[type_data] = compare_data[type_data][(compare_data[type_data].age >= ages[0]) & (compare_data[type_data].age <= ages[1])]
    
    player_already_in_compare_data = any(player in compare_data[type_data]["player"].values for type_data in all_types)

    if not player_already_in_compare_data:        
        st.sidebar.text("The chosen player is not included in this \nage category! We add him...")
        for type_data in all_types:
            # Get the data for the selected player from the original dataset
            player_data = data[type_data][data[type_data]["player"] == player]
            # Append the player's data to the comparison dataset
            compare_data[type_data] = compare_data[type_data].append(player_data, ignore_index=True)
    # df = df[(df.Age >= ages[0]) & (df.Age <= ages[1])].reset_index(drop=True)
    # if player not in df["Player"]:
    #     # st.sidebar.text("The chosen player is not included in this \nage category! We add him...")
    #     df.loc[len(df)] = df_player.loc[0, :].values.tolist()


pos_player = data["standard"]["pos"].values[0]

# st.title(df_player["Player"].values[0])
st.markdown("<h1 style='text-align: center; color: black;'>{}</h1>".format(data["standard"]["player"].values[0]), unsafe_allow_html=True)
# st.dataframe(df_player)
for type_data in all_types:
    print(type_data)
    st.pyplot(plot_radar(compare_data[type_data], data[type_data], pos_player, player, compare_percentile, False, type_data, minutes))

# st.pyplot(plot_radar(compare_data["standard"], data["standard"], pos_player, player, compare_percentile, False))

# st.pyplot(plot_radar(df, player, pos_player, standard_stats, name_mapping, player, compare_percentile))
# st.pyplot(plot_radar(df, player, pos_player, shooting_stats, name_mapping, player, compare_percentile))
# st.pyplot(plot_radar(df, player, pos_player, passing_stats, name_mapping, player, compare_percentile))
# st.pyplot(plot_radar(df, player, pos_player, creation_stats, name_mapping, player, compare_percentile))
# st.pyplot(plot_radar(df, player, pos_player, possession_stats, name_mapping, player, compare_percentile))