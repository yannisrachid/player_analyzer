import soccerdata as sd
import pandas as pd

import logging

def load_data():
    fbref = sd.FBref(leagues=['Big 5 European Leagues Combined'], seasons=['2324'])
    fbref.read_schedule(force_cache=True)

    all_types = ["standard", "shooting", "passing", "passing_types", "goal_shot_creation", "defense", "possession", "playing_time", "misc", "keeper", "keeper_adv"]

    for type_stat in all_types:
        df_stats = fbref.read_player_season_stats(stat_type=type_stat)
        df_stats.to_csv("data/{}_player_season_stats.csv".format(type_stat))
        logging.info("{} stats successfully loaded".format(type_stat))


if __name__=="__main__":
    load_data()