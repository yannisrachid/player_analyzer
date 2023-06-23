import streamlit as st
from dataviz import *

df = pd.read_csv("data/fbref_data_2223_big5.csv")

def clean_league(string):
    return " ".join(string.split()[1:])

def clean_df(df):
    df.drop(columns=["Matches Misc", "Matches Play", "Matches Poss", "Matches Def", "Matches Gca", "Matches Pt", "Matches Pass", "Matches St", "Matches Std"], axis=1, inplace=True)
    df = df[df["Min"] != "Min"].reset_index(drop=True)
    df["Comp"] = df["Comp"].apply(clean_league)
    df = df.sort_values(by=["Comp", "Squad", "Player"])
    cols = list(df.columns)[6:-3]
    for col in cols:
        df[col] = df[col].astype(float)
    return df

df = clean_df(df)

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image("img/logo_tr.png")
with col3:
    st.write(' ')

st.sidebar.markdown("<h1 style='text-align: center; color: white;'>{}</h1>".format("Player radarplot by IFP"), unsafe_allow_html=True)

league = st.sidebar.selectbox(
    'Select a league',
    df["Comp"].unique())
df_league = df[df["Comp"] == league].reset_index(drop=True)

club = st.sidebar.selectbox(
    'Select a club',
    df_league["Squad"].unique())
df_club = df_league[df_league["Squad"] == club].reset_index(drop=True)
df_club = df_club[df_club["Pos"] != "GK"].reset_index(drop=True)

player = st.sidebar.selectbox(
    'Select a player',
    df_club["Player"].unique())
df_player = df_club[df_club["Player"] == player].reset_index(drop=True)

compare_champ = st.sidebar.radio("Compare with", (league, 'Big 5 Leagues'))
if compare_champ == league:
    df = df[df["Comp"] == league].reset_index(drop=True)

compare_percentile = st.sidebar.slider("Compare player with the top %", min_value=1, max_value=30, value=5)

ages = st.sidebar.slider('Select an age group', 15, 45, (15, 45))
if ages:
    df = df[(df.Age >= ages[0]) & (df.Age <= ages[1])].reset_index(drop=True)
    if player not in df["Player"]:
        # st.sidebar.text("The chosen player is not included in this \nage category! We add him...")
        df.loc[len(df)] = df_player.loc[0, :].values.tolist()


pos_player = df_player["Pos"].values[0]
# st.title(df_player["Player"].values[0])
st.markdown("<h1 style='text-align: center; color: black;'>{}</h1>".format(df_player["Player"].values[0]), unsafe_allow_html=True)
# st.dataframe(df_player)

st.pyplot(plot_radar(df, player, pos_player, standard_stats, name_mapping, player, compare_percentile))
st.pyplot(plot_radar(df, player, pos_player, shooting_stats, name_mapping, player, compare_percentile))
st.pyplot(plot_radar(df, player, pos_player, passing_stats, name_mapping, player, compare_percentile))
st.pyplot(plot_radar(df, player, pos_player, creation_stats, name_mapping, player, compare_percentile))
st.pyplot(plot_radar(df, player, pos_player, possession_stats, name_mapping, player, compare_percentile))