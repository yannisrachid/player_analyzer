import pandas as pd
import numpy as np
from mplsoccer import Radar, FontManager, grid
import matplotlib.pyplot as plt
import re
import traceback
from radar_chart import Radar

# Display all columns of pandas DataFrames
pd.set_option('display.max_columns', None)

URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-Regular.ttf')
serif_regular = FontManager(URL1)
URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-ExtraLight.ttf')
serif_extra_light = FontManager(URL2)
URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
        'RubikMonoOne-Regular.ttf')
rubik_regular = FontManager(URL3)
URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
robotto_thin = FontManager(URL4)
URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')
robotto_bold = FontManager(URL5)

name_mapping = {
    "Gls Std": "Goals",
    "Ast Std": "Assists",
    "G-PK.1 Std": "Goals np /90",
    "G+A-PK Std": "Goals+Assists np /90", 
    "PrgC Std": "Prg Carries", 
    "PrgP Std": "Prg Passes", 
    "PrgR Std": "Prg Passes Received",
    "Sh/90 St": "Shots /90",
    "SoT/90 St": "Shots on target /90",
    "G/Sh St": "Goals per shot", 
    "G/SoT St": "Goals per shot on target",
    "Dist St": "Avg shot distance",
    "G-xG St": "Goals - xGoal",
    "np:G-xG St": "np Goals - ngxGoal",
    "Cmp Pass": "Completed", 
    "Att Pass": "Attempted", 
    "Cmp% Pass": "% Completed", 
    "PrgDist Pass": "Progressive Distance", 
    "xAG Pass": "xAssistedGoal", 
    "xA Pass": "xAssist", 
    "KP Pass": "Key Passes", 
    "1/3 Pass": "Passes in final 1/3", 
    "PPA Pass": "Passes in box", 
    "Crs Pass": "Crosses", 
    "CrsPA Pass": "Crosses in box",
    "SCA Gca": "Shot-Creating Action", 
    "SCA90 Gca": "Shot-Creating Action /90",
    "PassLive Gca": "PassLive to Goal", 
    "TO Gca": "TakeOns to Shot", 
    "Sh Gca": "Shots", 
    "GCA Gca": "Goal-Creating Action", 
    "GCA90 Gca": "Goal-Creating Action /90",
    "Touches Poss": "Touches", 
    "Carries Poss": "Carries", 
    "CPA Poss": "Carries in box", 
    "Rec Poss": "Passes received"
}

# standard_stats = ["Gls Std", "Ast Std", "G-PK.1 Std", "G+A-PK Std", 'PrgC Std', 'PrgP Std', 'PrgR Std']
# shooting_stats = ["Gls Std", "G-PK.1 Std", "Sh/90 St", "SoT/90 St", "G/Sh St", "G/SoT St", "Dist St", "G-xG St", "np:G-xG St"]
# passing_stats = ["Cmp Pass", "Att Pass", "Cmp% Pass", "PrgDist Pass", "Ast Std", "xAG Pass", "xA Pass", "KP Pass", "1/3 Pass", "PPA Pass", "CrsPA Pass", "PrgP Std"]
# creation_stats = ["SCA Gca", "SCA90 Gca", "PassLive Gca", "TO Gca", "Sh Gca", "GCA Gca", "GCA90 Gca"]
# possession_stats = ["Touches Poss", "Carries Poss", "PrgC Std", "CPA Poss", "Rec Poss", "PrgR Std"]

def data_prep_compare_by_type(df, type_data, pos, minutes, per90):
    # df = df[(df["pos"] == pos) & (df["Playing Time"]["Min"] >= 900)]
    per_match = minutes / 90
    
    if type_data == "standard":
        df = df[(df["pos"] == pos) & (df["Playing Time"]["90s"] >= per_match)]
        df = df[["player", "Playing Time", "Performance", "Expected"]].droplevel(0, axis=1)
        df = df.rename(columns={'': 'player'})
        df = df.drop(columns=['MP', 'Starts', "Min"])
        
    elif type_data == "shooting":
        df = df[(df["pos"] == pos) & (df["90s"] >= per_match)]
        df = df[["player", "90s", "Standard", "Expected"]].droplevel(0, axis=1)
        df = df.drop(columns=['Sh/90', 'SoT/90'])
        df.columns = ["player", "90s"] + df.columns[2:].tolist()
        
    elif type_data == "passing":
        df = df[(df["pos"] == pos) & (df["90s"] >= per_match)]
        selected_columns = ["player", "90s", "Total", "Short", "Medium", "Long", "Ast", "xAG", "Expected", "KP", "1/3", "PPA", "CrsPA", "PrgP"]
        df = df[selected_columns]
        prefixes = df.columns.get_level_values(0)
        df.columns = prefixes + '_' + df.columns.get_level_values(1)
        df.columns = [col_name.split("_")[0] if col_name.split("_")[1] == "" else col_name for col_name in df.columns]
        
    elif type_data == "goal_shot_creation":
        df = df[(df["pos"] == pos) & (df["90s"] >= per_match)]
        selected_columns = ["player", "90s", "SCA", "SCA Types", "GCA", "GCA Types"]
        df = df[selected_columns]
        prefixes = df.columns.get_level_values(0)
        df.columns = prefixes + '_' + df.columns.get_level_values(1)
        df.columns = [col_name.split("_")[1] if col_name.split("_")[0] in ["SCA", "GCA"] else col_name.replace(" Types", "") for col_name in df.columns]
        df = df.drop(columns=['SCA90', 'GCA90'])
        df = df.rename(columns={'player_': 'player', '90s_': '90s'})
        
    elif type_data == "possession":
        df = df[(df["pos"] == pos) & (df["90s"] >= per_match)]
        df = df[["player", "90s", "Touches", "Take-Ons", "Carries", "Receiving"]].droplevel(0, axis=1)
        df.columns = ["player", "90s"] + df.columns[2:].tolist()
        
    elif type_data == "misc":
        df = df[(df["pos"] == pos) & (df["90s"] >= per_match)]
        selected_columns = ["player", "90s", "Performance", "Aerial Duels"]
        df = df[selected_columns]
        prefixes = df.columns.get_level_values(0)
        df.columns = prefixes + '_' + df.columns.get_level_values(1)
        df.columns = [col_name.split("_")[1] if col_name.split("_")[0] == "Performance" else col_name.replace("_", " ") for col_name in df.columns]
        df = df.rename(columns={'player ': 'player', '90s ': '90s'})
        df = df.drop(columns=["OG", "PKcon", "2CrdY"])
        
    elif type_data == "defense":
        df = df[(df["pos"] == pos) & (df["90s"] >= per_match)]
        selected_columns = ["player", "90s", "Tackles", "Challenges", "Blocks", "Int", "Tkl+Int", "Clr", "Err"]
        df = df[selected_columns]
        prefixes = df.columns.get_level_values(0)
        df.columns = prefixes + '_' + df.columns.get_level_values(1)
        df.columns = [col_name.split("_")[0] if col_name.split("_")[1] == "" else col_name for col_name in df.columns]
        df.columns = [col_name.split("_")[1] if (col_name.split("_")[0] != "Challenges" and "_" in col_name) else col_name.replace("_", " ") for col_name in df.columns]
    
    if per90:
        filtered_columns = [col for col in df.columns if ('%' not in col) and ('/' not in col or col == '1/3')]
        df = df[filtered_columns]
        for col in df.columns[2:].tolist():
            df[col] = df[col] / df["90s"]
            
    df = df.drop(columns=["90s"])
        
    return df


def data_prep_player_by_type(df, type_data, per90):
    # df = df[(df["pos"] == pos) & (df["Playing Time"]["Min"] >= 900)]
    
    if type_data == "standard":
        df = df[["player", "Playing Time", "Performance", "Expected"]].droplevel(0, axis=1)
        df = df.rename(columns={'': 'player'})
        df = df.drop(columns=['MP', 'Starts', "Min"])
        
    elif type_data == "shooting":
        df = df[["player", "90s", "Standard", "Expected"]].droplevel(0, axis=1)
        df = df.drop(columns=['Sh/90', 'SoT/90'])
        df.columns = ["player", "90s"] + df.columns[2:].tolist()
        
    elif type_data == "passing":
        selected_columns = ["player", "90s", "Total", "Short", "Medium", "Long", "Ast", "xAG", "Expected", "KP", "1/3", "PPA", "CrsPA", "PrgP"]
        df = df[selected_columns]
        prefixes = df.columns.get_level_values(0)
        df.columns = prefixes + '_' + df.columns.get_level_values(1)
        df.columns = [col_name.split("_")[0] if col_name.split("_")[1] == "" else col_name for col_name in df.columns]
        
    elif type_data == "goal_shot_creation":
        selected_columns = ["player", "90s", "SCA", "SCA Types", "GCA", "GCA Types"]
        df = df[selected_columns]
        prefixes = df.columns.get_level_values(0)
        df.columns = prefixes + '_' + df.columns.get_level_values(1)
        df.columns = [col_name.split("_")[1] if col_name.split("_")[0] in ["SCA", "GCA"] else col_name.replace(" Types", "") for col_name in df.columns]
        df = df.drop(columns=['SCA90', 'GCA90'])
        df = df.rename(columns={'player_': 'player', '90s_': '90s'})
        
    elif type_data == "possession":
        df = df[["player", "90s", "Touches", "Take-Ons", "Carries", "Receiving"]].droplevel(0, axis=1)
        df.columns = ["player", "90s"] + df.columns[2:].tolist()
        
    elif type_data == "misc":
        selected_columns = ["player", "90s", "Performance", "Aerial Duels"]
        df = df[selected_columns]
        prefixes = df.columns.get_level_values(0)
        df.columns = prefixes + '_' + df.columns.get_level_values(1)
        df.columns = [col_name.split("_")[1] if col_name.split("_")[0] == "Performance" else col_name.replace("_", " ") for col_name in df.columns]
        df = df.rename(columns={'player ': 'player', '90s ': '90s'})
        df = df.drop(columns=["OG", "PKcon", "2CrdY"])
        
    elif type_data == "defense":
        selected_columns = ["player", "90s", "Tackles", "Challenges", "Blocks", "Int", "Tkl+Int", "Clr", "Err"]
        df = df[selected_columns]
        prefixes = df.columns.get_level_values(0)
        df.columns = prefixes + '_' + df.columns.get_level_values(1)
        df.columns = [col_name.split("_")[0] if col_name.split("_")[1] == "" else col_name for col_name in df.columns]
        df.columns = [col_name.split("_")[1] if (col_name.split("_")[0] != "Challenges" and "_" in col_name) else col_name.replace("_", " ") for col_name in df.columns]
    
    if per90:
        filtered_columns = [col for col in df.columns if ('%' not in col) and ('/' not in col or col == '1/3')]
        df = df[filtered_columns]
        for col in df.columns[2:].tolist():
            df[col] = df[col] / df["90s"]
            
    df = df.drop(columns=["90s"])
    
    return df

def get_avg_stats_by_pos(df, type_data, pos, percent, minutes, per90):
    """
    ============
    Input: 
        - df: pd.DataFrame
        - pos: string
        - percent: int
        - per90: bool
    ============
    Output:
        - dict_player: dict
    ============
    Slice the dataframe with all players stats by position of the season, and returns a dict with all avg stats entered in input
    ============
    """
    # df_pos = df[(df["Pos"] == pos) & (df["Min"] >= 900)].reset_index(drop=True) #  & (df["Age"] <= 25)
    # print(round(df_pos['Min'].mean()), "average minutes played a player in league this season.")
    df_pos = data_prep_compare_by_type(df, type_data, pos, minutes, per90)
    stats = list(df_pos.columns)
    if "player" in stats:
        stats.remove("player")
    dict_player = {}
    for stat in stats:
        dict_player[stat] = [min(df_pos[stat]), df_pos[stat].median(), df_pos[stat].quantile(1-(percent/100)), max(df_pos[stat]), df_pos.loc[df_pos[stat] == max(df_pos[stat]), 'player'].iloc[0]]
    return dict_player

def get_player_stats(df, type_data, per90):
    """
    ============
    Input: 
        - df: pd.DataFrame
        - per90: bool
    ============
    Output:
        - dict_player: dict
    ============
    Slice the dataframe with player stats of the season, and returns a dict with all stats entered in input
    ============
    """
    df = data_prep_player_by_type(df, type_data, per90).reset_index()
    # print(player, "played", df_player.loc[0, 'Min'], "minutes in league this season.")
    stats = list(df.columns)
    if "index" in stats:
        stats.remove("index")
    if "player" in stats:
        stats.remove("player")
    dict_player = {}
    for stat in stats:
        dict_player[stat] = df.loc[0, stat]
    return dict_player

def plot_radar(df, df_player, pos, player_name, percent, per90, type_data, minutes):
    """
    """
    avg_stats = get_avg_stats_by_pos(df, type_data, pos, percent, minutes, per90)
    stats = list(avg_stats.keys())

    params = stats
    player_stats = get_player_stats(df_player, type_data, per90)

    # The lower and upper boundaries for the statistics
    low =  [val[0] for val in list(avg_stats.values())]
    top_5 = [val[2] for val in list(avg_stats.values())]
    high = [val[3] for val in list(avg_stats.values())]
    high_name = [val[4] for val in list(avg_stats.values())]
    avg = [val[1] for val in list(avg_stats.values())]
    player = list(player_stats.values())
    
    radar = Radar(params, low, high,
              # lower_is_better=lower_is_better,
              # whether to round any of the labels to integers instead of decimal places
              round_int=[False]*len(params),
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)
    
    # creating the figure using the grid function from mplsoccer:
    fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                    title_space=0, endnote_space=0, grid_key='radar', axis=False)

    # plot radar
    radar.setup_axis(ax=axs['radar'], facecolor="#F2F2F0")  # format axis as a radar
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#97cbfa', edgecolor='black')

    radar1, vertices1 = radar.draw_radar_solid(player, ax=axs['radar'],
                                               kwargs={'facecolor': '#aa65b2',
                                                       'alpha': 0.6,
                                                       'edgecolor': '#216352',
                                                       'lw': 3})

    radar2, vertices2 = radar.draw_radar_solid(avg, ax=axs['radar'],
                                               kwargs={'facecolor': '#66d8ba',
                                                       'alpha': 0.6,
                                                       'edgecolor': '#216352',
                                                       'lw': 3})
    
    radar3, vertices3 = radar.draw_radar_solid(top_5, ax=axs['radar'],
                                               kwargs={'facecolor': '#697cd4',
                                                       'alpha': 0.6,
                                                       'edgecolor': '#222b54',
                                                       'lw': 3})

    # radar1, radar2, radar3, vertices1, vertices2, vertices3 = radar_output

    if len(params) > 15:
        labels_size = 12
        param_labels_size = 16
    else:
        labels_size = 25
        param_labels_size = 25
    
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=labels_size,
                                           fontproperties=robotto_bold.prop, color="black")

    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=param_labels_size,
                                           fontproperties=robotto_bold.prop, color="black")
    
    max_labels = radar.draw_under_param_labels(text_list=high_name, ax=axs['radar'], fontsize=12,
                                           fontproperties=robotto_bold.prop, color="#FF5D00")

    axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                         c='#aa65b2', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
    axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                         c='#66d8ba', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
    axs['radar'].scatter(vertices3[:, 0], vertices3[:, 1],
                         c='#697cd4', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)

    # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
    # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
    # endnote_text = axs['endnote'].text(0.99, 0.5, 'Data: FBRef / Creator: Intelligence Football Performance', fontsize=15,
                                       # fontproperties=serif_regular.prop, ha='right', va='center', color="white")
    
    stack = traceback.extract_stack()
    filename, lineno, function_name, code = stack[-2]
    # vars_name = re.compile(r'\((.*?)\).*$').search(code).groups()[0].replace(' ', '').split(',')

    title_axs = axs['title'].text(0.50, 0.65, "{} Stats".format(type_data).replace("_", " ").title(), fontsize=35, color='black',
                                    fontproperties=robotto_bold.prop, ha='center', va='center')
    
    leader = axs["radar"].text(-7, -4, "Leader", fontsize=25, color='#FF5D00',
                                    fontproperties=robotto_bold.prop, ha='left', va='center')
    player = axs['radar'].text(-7, -4.5, player_name, fontsize=25, color='#aa65b2',
                                    fontproperties=robotto_bold.prop, ha='left', va='center')
    top_5 = axs['radar'].text(-7, -5, 'Top {}%'.format(percent), fontsize=25,
                                fontproperties=robotto_bold.prop,
                                ha='left', va='center', color='#697cd4')
    median = axs['radar'].text(-7, -5.5, 'Median', fontsize=25,
                                    fontproperties=robotto_bold.prop,
                                    ha='left', va='center', color='#66d8ba')
    
    signing = axs['radar'].text(-0.75, 0, '@Yannis R', fontsize=20,
                                    fontproperties=robotto_bold.prop,
                                    ha='left', va='center', color='#DEDEDE')
    data_source = axs['radar'].text(5, -5.5, 'Data: FBRef', fontsize=20,
                                    fontproperties=robotto_bold.prop,
                                    ha='left', va='center', color='#000000')

    fig.set_facecolor('#F2F2F0')
    
    return fig