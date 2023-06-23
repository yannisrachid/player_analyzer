import pandas as pd
import numpy as np
from mplsoccer import Radar, FontManager, grid
import matplotlib.pyplot as plt
import re
import traceback

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

standard_stats = ["Gls Std", "Ast Std", "G-PK.1 Std", "G+A-PK Std", 'PrgC Std', 'PrgP Std', 'PrgR Std']
shooting_stats = ["Gls Std", "G-PK.1 Std", "Sh/90 St", "SoT/90 St", "G/Sh St", "G/SoT St", "Dist St", "G-xG St", "np:G-xG St"]
passing_stats = ["Cmp Pass", "Att Pass", "Cmp% Pass", "PrgDist Pass", "Ast Std", "xAG Pass", "xA Pass", "KP Pass", "1/3 Pass", "PPA Pass", "CrsPA Pass", "PrgP Std"]
creation_stats = ["SCA Gca", "SCA90 Gca", "PassLive Gca", "TO Gca", "Sh Gca", "GCA Gca", "GCA90 Gca"]
possession_stats = ["Touches Poss", "Carries Poss", "PrgC Std", "CPA Poss", "Rec Poss", "PrgR Std"]

def get_player_stats(df, player, stats):
    """
    ============
    Input: 
        - df: pd.DataFrame
        - player: string
        - stats: list
    ============
    Output:
        - dict_player: dict
    ============
    Slice the dataframe with player stats of the season, and returns a dict with all stats entered in input
    ============
    """
    df_player = df[df["Player"] == player].reset_index(drop=True)
    # print(player, "played", df_player.loc[0, 'Min'], "minutes in league this season.")
    dict_player = {}
    for stat in stats:
        try:
            dict_player[stat] = df_player.loc[0, stat]
        except:
            print(stat, "unavailable in the dataframe")
    return dict_player

def get_avg_stats_by_pos(df, pos, stats, percent):
    """
    ============
    Input: 
        - df: pd.DataFrame
        - pos: string
        - stats: list
    ============
    Output:
        - dict_player: dict
    ============
    Slice the dataframe with all players stats by position of the season, and returns a dict with all avg stats entered in input
    ============
    """
    df_pos = df[(df["Pos"] == pos) & (df["Min"] >= 900)].reset_index(drop=True) #  & (df["Age"] <= 25)
    # print(round(df_pos['Min'].mean()), "average minutes played a player in league this season.")
    dict_player = {}
    for stat in stats:
        try:
            dict_player[stat] = [min(df_pos[stat]), df_pos[stat].median(), df[stat].quantile(1-(percent/100)), max(df_pos[stat]), df_pos.loc[df_pos[stat] == max(df_pos[stat]), 'Player'].iloc[0]]
        except:
            print(stat, "unavailable in the dataframe")
    return dict_player

def plot_radar(df, player, pos, stats, map_dict, player_name, percent):
    """
    """
    params = list(map(map_dict.get, stats))
    player_stats = get_player_stats(df, player, stats)
    avg_stats = get_avg_stats_by_pos(df, pos, stats, percent)
    
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
    
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25,
                                           fontproperties=robotto_bold.prop, color="black")

    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25,
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
    vars_name = re.compile(r'\((.*?)\).*$').search(code).groups()[0].replace(' ', '').split(',')

    title_axs = axs['title'].text(0.50, 0.65, vars_name[3].replace('_', ' ').title(), fontsize=35, color='black',
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

    fig.set_facecolor('#F2F2F0')
    
    return fig