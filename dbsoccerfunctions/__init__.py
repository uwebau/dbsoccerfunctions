import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
plt.style.use('ggplot')
# import datetime


def readDB(path):
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    df_Matches = pd.read_sql('SELECT * FROM Match', conn)
    df_Countries = pd.read_sql('SELECT * FROM Country', conn)
    df_Leagues = pd.read_sql('SELECT * FROM League', conn)
    df_Teams = pd.read_sql('SELECT * FROM Team', conn)
    df_MarketValue = pd.read_sql('SELECT * FROM MarketValue', conn)
    conn.close()
    return df_Matches, df_Countries, df_Leagues, df_Teams, df_MarketValue


def readDB2(path):
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    df_Matches = pd.read_sql('SELECT * FROM Match', conn)
    df_Countries = pd.read_sql('SELECT * FROM Country', conn)
    df_Leagues = pd.read_sql('SELECT * FROM League', conn)
    df_Teams = pd.read_sql('SELECT * FROM Team', conn)
    conn.close()
    return df_Matches, df_Countries, df_Leagues, df_Teams


def getTable(df_Matches, league_id, season, stages):
    df_table = pd.DataFrame()
    teams = df_Matches.loc[(df_Matches['season'] == season) &
                           (df_Matches['league_id'] ==
                            league_id)].home_team_id.unique()

    for team in teams:
        df_Matches_home = df_Matches[(df_Matches['league_id'] == league_id) &
                                     (df_Matches['season'] == season) &
                                     (df_Matches['stage'].isin(stages)) &
                                     (df_Matches['home_team_id'] == team)]

        df_Matches_away = df_Matches[(df_Matches['league_id'] == league_id) &
                                     (df_Matches['season'] == season) &
                                     (df_Matches['stage'].isin(stages)) &
                                     (df_Matches['away_team_id'] == team)]
    
        home_matches = len(df_Matches_home)
        home_wins = len(df_Matches_home[(df_Matches_home['FTR'] == 'H')])
        home_draws = len(df_Matches_home[(df_Matches_home['FTR'] == 'D')])
        home_losses = len(df_Matches_home[(df_Matches_home['FTR'] == 'A')])
        home_goals_shot = sum(df_Matches_home.FTHG)
        home_goals_received = sum(df_Matches_home.FTAG)
        home_goals_difference = home_goals_shot - home_goals_received
        home_points = home_wins*3 + home_draws
    
        away_matches = len(df_Matches_away)
        away_wins = len(df_Matches_away[(df_Matches_away['FTR'] == 'A')])
        away_draws = len(df_Matches_away[(df_Matches_away['FTR'] == 'D')])
        away_losses = len(df_Matches_away[(df_Matches_away['FTR'] == 'H')])
        away_goals_shot = sum(df_Matches_away.FTAG)
        away_goals_received = sum(df_Matches_away.FTHG)
        away_goals_difference = away_goals_shot - away_goals_received
        away_points = away_wins*3 + away_draws
    
        total_matches = home_matches + away_matches
        total_wins = home_wins + away_wins
        total_losses = home_losses + away_losses
        total_draws = home_draws + away_draws
        total_goals_shot = home_goals_shot + away_goals_shot
        total_goals_received = home_goals_received + away_goals_received
        total_goals_difference = total_goals_shot - total_goals_received
        total_points = home_points + away_points
     
        if 'HS' in df_Matches.columns:
            if ((not df_Matches_home[['HS', 'AS']].isnull().values.any()) and
                (not df_Matches_away[['HS', 'AS']].isnull().values.any())):
                home_shots_shot = sum(df_Matches_home.HS)
                home_shots_received = sum(df_Matches_home.AS)
                home_shots_difference = home_shots_shot - home_shots_received
                away_shots_shot = sum(df_Matches_away.AS)
                away_shots_received = sum(df_Matches_away.HS)
                away_shots_difference = away_shots_shot - away_shots_received
                total_shots_shot = home_shots_shot + away_shots_shot
                total_shots_received = (home_shots_received
                                        + away_shots_received)
                total_shots_difference = (total_shots_shot
                                          - total_shots_received)
        if (('HS' not in df_Matches.columns) or
            (df_Matches_home[['HS', 'AS']].isnull().values.any()) or
            (df_Matches_away[['HS', 'AS']].isnull().values.any())):
            home_shots_shot = float('NaN')
            home_shots_received = float('NaN')
            home_shots_difference = float('NaN')
            away_shots_shot = float('NaN')
            away_shots_received = float('NaN')
            away_shots_difference = float('NaN')
            total_shots_shot = float('NaN')
            total_shots_received = float('NaN')
            total_shots_difference = float('NaN')

        if 'HST' in df_Matches.columns:
            if ((not df_Matches_home[['HST', 'AST']].isnull().values.any()) and
                (not df_Matches_away[['HST', 'AST']].isnull().values.any())):
                home_shotsTarget_shot = sum(df_Matches_home.HST)
                home_shotsTarget_received = sum(df_Matches_home.AST)
                home_shotsTarget_difference = (home_shotsTarget_shot
                                               - home_shotsTarget_received)
                away_shotsTarget_shot = sum(df_Matches_away.AST)
                away_shotsTarget_received = sum(df_Matches_away.HST)
                away_shotsTarget_difference = (away_shotsTarget_shot
                                               - away_shotsTarget_received)
                total_shotsTarget_shot = (home_shotsTarget_shot
                                          + away_shotsTarget_shot)
                total_shotsTarget_received = (home_shotsTarget_received
                                              + away_shotsTarget_received)
                total_shotsTarget_difference = (total_shotsTarget_shot
                                                - total_shotsTarget_received)
        if (('HST' not in df_Matches.columns) or
            (df_Matches_home[['HST', 'AST']].isnull().values.any()) or
            (df_Matches_away[['HST', 'AST']].isnull().values.any())):
            home_shotsTarget_shot = float('NaN')
            home_shotsTarget_received = float('NaN')
            home_shotsTarget_difference = float('NaN')
            away_shotsTarget_shot = float('NaN')
            away_shotsTarget_received = float('NaN')
            away_shotsTarget_difference = float('NaN')
            total_shotsTarget_shot = float('NaN')
            total_shotsTarget_received = float('NaN')
            total_shotsTarget_difference = float('NaN')

        if 'HC' in df_Matches.columns:
            if ((not df_Matches_home[['HC', 'AC']].isnull().values.any()) and
                (not df_Matches_away[['HC', 'AC']].isnull().values.any())):
                home_corners_shot = sum(df_Matches_home.HC)
                home_corners_received = sum(df_Matches_home.AC)
                home_corners_difference = (home_corners_shot
                                           - home_corners_received)
                away_corners_shot = sum(df_Matches_away.AC)
                away_corners_received = sum(df_Matches_away.HC)
                away_corners_difference = (away_corners_shot
                                           - away_corners_received)
                total_corners_shot = home_corners_shot + away_corners_shot
                total_corners_received = (home_corners_received
                                          + away_corners_received)
                total_corners_difference = (total_corners_shot
                                            - total_corners_received)
        if (('HC' not in df_Matches.columns) or
            (df_Matches_home[['HC', 'AC']].isnull().values.any()) or
            (df_Matches_away[['HC', 'AC']].isnull().values.any())):
            home_corners_shot = float('NaN')
            home_corners_received = float('NaN')
            home_corners_difference = float('NaN')
            away_corners_shot = float('NaN')
            away_corners_received = float('NaN')
            away_corners_difference = float('NaN')
            total_corners_shot = float('NaN')
            total_corners_received = float('NaN')
            total_corners_difference = float('NaN')

        if 'HF' in df_Matches.columns:
            if ((not df_Matches_home[['HF', 'AF']].isnull().values.any()) and
                (not df_Matches_away[['HF', 'AF']].isnull().values.any())):
                home_fouls_commit = sum(df_Matches_home.HF)
                home_fouls_received = sum(df_Matches_home.AF)
                home_fouls_difference = home_fouls_commit - home_fouls_received
                away_fouls_commit = sum(df_Matches_away.AF)
                away_fouls_received = sum(df_Matches_away.HF)
                away_fouls_difference = away_fouls_commit - away_fouls_received
                total_fouls_commit = home_fouls_commit + away_fouls_commit
                total_fouls_received = (home_fouls_received
                                        + away_fouls_received)
                total_fouls_difference = (total_fouls_commit
                                          - total_fouls_received)
        if (('HF' not in df_Matches.columns) or
            (df_Matches_home[['HF', 'AF']].isnull().values.any()) or
            (df_Matches_away[['HF', 'AF']].isnull().values.any())):
            home_fouls_commit = float('NaN')
            home_fouls_received = float('NaN')
            home_fouls_difference = float('NaN')
            away_fouls_commit = float('NaN')
            away_fouls_received = float('NaN')
            away_fouls_difference = float('NaN')
            total_fouls_commit = float('NaN')
            total_fouls_received = float('NaN')
            total_fouls_difference = float('NaN')

        if 'HO' in df_Matches.columns:
            if ((not df_Matches_home[['HO', 'AO']].isnull().values.any()) and
                (not df_Matches_away[['HO', 'AO']].isnull().values.any())):    
                home_offside_commit = sum(df_Matches_home.HO)
                home_offside_received = sum(df_Matches_home.AO)
                home_offside_difference = (home_offside_commit
                                           - home_offside_received)
                away_offside_commit = sum(df_Matches_away.AO)
                away_offside_received = sum(df_Matches_away.HO)
                away_offside_difference = (away_offside_commit
                                           - away_offside_received)
                total_offside_commit = (home_offside_commit
                                        + away_offside_commit)
                total_offside_received = (home_offside_received
                                          + away_offside_received)
                total_offside_difference = (total_offside_commit
                                            - total_offside_received)
        if (('HO' not in df_Matches.columns) or
            (df_Matches_home[['HO', 'AO']].isnull().values.any()) or
            (df_Matches_away[['HO', 'AO']].isnull().values.any())):
            home_offside_commit = float('NaN')
            home_offside_received = float('NaN')
            home_offside_difference = float('NaN')
            away_offside_commit = float('NaN')
            away_offside_received = float('NaN')
            away_offside_difference = float('NaN')
            total_offside_commit = float('NaN')
            total_offside_received = float('NaN')
            total_offside_difference = float('NaN')

        if 'HY' in df_Matches.columns:
            if ((not df_Matches_home[['HY', 'AY']].isnull().values.any()) and
                (not df_Matches_away[['HY', 'AY']].isnull().values.any())):
                home_yellow_booked = sum(df_Matches_home.HY)
                home_yellow_opponent = sum(df_Matches_home.AY)
                home_yellow_difference = (home_yellow_booked
                                          - home_yellow_opponent)
                away_yellow_booked = sum(df_Matches_away.AY)
                away_yellow_opponent = sum(df_Matches_away.HY)
                away_yellow_difference = (away_yellow_booked
                                          - away_yellow_opponent)
                total_yellow_booked = home_yellow_booked - away_yellow_booked
                total_yellow_opponent = (home_yellow_opponent
                                         + away_yellow_opponent)
                total_yellow_difference = (total_yellow_booked
                                           - total_yellow_opponent)
        if (('HY' not in df_Matches.columns) or
            (df_Matches_home[['HY', 'AY']].isnull().values.any()) or
            (df_Matches_away[['HY', 'AY']].isnull().values.any())):
            home_yellow_booked = float('NaN')
            home_yellow_opponent = float('NaN')
            home_yellow_difference = float('NaN')
            away_yellow_booked = float('NaN')
            away_yellow_opponent = float('NaN')
            away_yellow_difference = float('NaN')
            total_yellow_booked = float('NaN')
            total_yellow_opponent = float('NaN')
            total_yellow_difference = float('NaN')

        if 'HR' in df_Matches.columns:
            if ((not df_Matches_home[['HR', 'AR']].isnull().values.any()) and
                (not df_Matches_away[['HR', 'AR']].isnull().values.any())):
                home_red_booked = sum(df_Matches_home.HR)
                home_red_opponent = sum(df_Matches_home.AR)
                home_red_difference = home_red_booked - home_red_opponent
                away_red_booked = sum(df_Matches_away.AR)
                away_red_opponent = sum(df_Matches_away.HR)
                away_red_difference = away_red_booked - away_red_opponent
                total_red_booked = home_red_booked + away_red_booked
                total_red_opponent = home_red_opponent - away_red_opponent
                total_red_difference = total_red_booked - total_red_opponent
        if (('HR' not in df_Matches.columns) or
            (df_Matches_home[['HR', 'AR']].isnull().values.any()) or
            (df_Matches_away[['HR', 'AR']].isnull().values.any())):
            home_red_booked = float('NaN')
            home_red_opponent = float('NaN')
            home_red_difference = float('NaN')
            away_red_booked = float('NaN')
            away_red_opponent = float('NaN')
            away_red_difference = float('NaN')
            total_red_booked = float('NaN')
            total_red_opponent = float('NaN')
            total_red_difference = float('NaN')  
    
        df = pd.DataFrame({'league_id': [league_id],
                           'season': [season],
                           'team_id': [team],
                           'home_matches': [home_matches],
                           'home_wins': [home_wins],
                           'home_draws': [home_draws],
                           'home_losses': [home_losses],
                           'home_points': [home_points],
                           'home_goals_shot': [home_goals_shot],
                           'home_goals_received': [home_goals_received],
                           'home_goals_difference': [home_goals_difference],
                           'home_shots_shot': [home_shots_shot],
                           'home_shots_received': [home_shots_received],
                           'home_shots_difference': [home_shots_difference],
                           'home_shotsTarget_shot': [home_shotsTarget_shot],
                           'home_shotsTarget_received': [home_shotsTarget_received],
                           'home_shotsTarget_difference': [home_shotsTarget_difference],
                           'home_corners_shot': [home_corners_shot],
                           'home_corners_received': [home_corners_received],
                           'home_corners_difference': [home_corners_difference],
                           'home_fouls_commit': [home_fouls_commit],
                           'home_fouls_received': [home_fouls_received],
                           'home_fouls_difference': [home_fouls_difference],
                           'home_offside_commit': [home_offside_commit],
                           'home_offside_received': [home_offside_received],
                           'home_offside_difference': [home_offside_difference],
                           'home_yellow_booked': [home_yellow_booked],
                           'home_yellow_opponent': [home_yellow_opponent],
                           'home_yellow_difference': [home_yellow_difference],
                           'home_red_booked': [home_red_booked],
                           'home_red_opponent': [home_red_opponent],
                           'home_red_difference': [home_red_difference],
                           'away_matches': [away_matches],
                           'away_wins': [away_wins],
                           'away_draws': [away_draws],
                           'away_losses': [away_losses],
                           'away_points': [away_points],
                           'away_goals_shot': [away_goals_shot],
                           'away_goals_received': [away_goals_received],
                           'away_goals_difference': [away_goals_difference],
                           'away_shots_shot': [away_shots_shot],
                           'away_shots_received': [away_shots_received],
                           'away_shots_difference': [away_shots_difference],
                           'away_shotsTarget_shot': [away_shotsTarget_shot],
                           'away_shotsTarget_received':
                               [away_shotsTarget_received],
                           'away_shotsTarget_difference':
                               [away_shotsTarget_difference],
                           'away_corners_shot': [away_corners_shot],
                           'away_corners_received': [away_corners_received],
                           'away_corners_difference':
                               [away_corners_difference],
                           'away_fouls_commit': [away_fouls_commit],
                           'away_fouls_received': [away_fouls_received],
                           'away_fouls_difference': [away_fouls_difference],
                           'away_offside_commit': [away_offside_commit],
                           'away_offside_received': [away_offside_received],
                           'away_offside_difference':
                               [away_offside_difference],
                           'away_yellow_booked': [away_yellow_booked],
                           'away_yellow_opponent': [away_yellow_opponent],
                           'away_yellow_difference': [away_yellow_difference],
                           'away_red_booked': [away_red_booked],
                           'away_red_opponent': [away_red_opponent],
                           'away_red_difference': [away_red_difference],
                           'total_matches': [total_matches],
                           'total_wins': [total_wins],
                           'total_draws': [total_draws],
                           'total_losses': [total_losses],
                           'total_points': [total_points],
                           'total_goals_shot': [total_goals_shot],
                           'total_goals_received': [total_goals_received],
                           'total_goals_difference': [total_goals_difference],
                           'total_shots_shot': [total_shots_shot],
                           'total_shots_received': [total_shots_received],
                           'total_shots_difference': [total_shots_difference],
                           'total_shotsTarget_shot': [total_shotsTarget_shot],
                           'total_shotsTarget_received':
                               [total_shotsTarget_received],
                           'total_shotsTarget_difference':
                               [total_shotsTarget_difference],
                           'total_corners_shot': [total_corners_shot],
                           'total_corners_received': [total_corners_received],
                           'total_corners_difference':
                               [total_corners_difference],
                           'total_fouls_commit': [total_fouls_commit],
                           'total_fouls_received': [total_fouls_received],
                           'total_fouls_difference': [total_fouls_difference],
                           'total_offside_commit': [total_offside_commit],
                           'total_offside_received': [total_offside_received],
                           'total_offside_difference':
                               [total_offside_difference],
                           'total_yellow_booked': [total_yellow_booked],
                           'total_yellow_opponent': [total_yellow_opponent],
                           'total_yellow_difference':
                               [total_yellow_difference],
                           'total_red_booked': [total_red_booked],
                           'total_red_opponent': [total_red_opponent],
                           'total_red_difference': [total_red_difference]
                           })
        df_table = df_table.append(df, ignore_index=True)
    df_table.dropna(axis=1, how='any', inplace=True)
    df_table.sort_values(['total_points',
                          'total_goals_difference'],
                         ascending=[0, 0], inplace=True)
    df_table['Position'] = list(range(1, len(teams)+1))
    if 'total_shotsTarget_shot' in df_table.columns:
        df_table['total_goal_efficiency'] = df_table['total_goals_shot']/df_table['total_shotsTarget_shot']
    if 'total_shotsTarget_received' in df_table.columns:
        df_table['total_block_efficiency'] = df_table['total_goals_received']/df_table['total_shotsTarget_received']

    return df_table


def getMeanGoals(df_Matches: 'Match database', *,
             goal_type: "choices: 'home', 'away', total'(default), 'diff'"='total',
             conf_intervall: 'default = 0.95'=0.95):
    goal_types = ('home', 'away', 'total', 'diff')
    no_matches = len(df_Matches)
    t_critical = -stats.t.ppf(q=(1-conf_intervall)/2, df=no_matches)
    if goal_type not in goal_types:
        return False
    if goal_type == goal_types[0]:
        goals = df_Matches['FTHG']
    if goal_type == goal_types[1]:
        goals = df_Matches['FTAG']
    if goal_type == goal_types[2]:
        goals = df_Matches['FTHG']+df_Matches['FTAG']
    if goal_type == goal_types[3]:
        goals = df_Matches['FTHG']-df_Matches['FTAG']
    goals_mean = goals.mean()
    goals_std = goals.std()
    goals_margin_of_error = t_critical * goals_std / math.sqrt(no_matches)
    goals_conf_low = goals_mean - goals_margin_of_error
    goals_conf_high = goals_mean + goals_margin_of_error
    df = pd.DataFrame({'goals_mean': [goals_mean],
                       'goals_std': [goals_std],
                       'goals_errormargin': [goals_margin_of_error],
                       'goals_conf_low': [goals_conf_low],
                       'goals_conf_high': [goals_conf_high]})
    return df


# get mean goals distinguished by season, country and tier and
# goalType (home, away, total, diff)
def GetDFMeanGoalsSeason(df_Matches, goal_types=('home', 'away', 'total',
                                                 'diff')):
    country_ids = df_Matches.country_id.unique()
    min_tiers = float('NaN')
    for country_id in country_ids:
        min_tiers = min([len(df_Matches[df_Matches['country_id'] ==
                                        country_id].tier.unique()), min_tiers])
    tiers = tuple(range(1, 1+min_tiers))
    df_Goals = pd.DataFrame()
    for country_id in country_ids:
        for tier in tiers:
            seasons = df_Matches.loc[(df_Matches.country_id ==
                                     country_id) & (df_Matches.tier ==
                                     tier)].season.unique()
            for season in seasons:
                for goal_type in goal_types:
                    df = getMeanGoals(df_Matches.loc[
                            (df_Matches.country_id == country_id) &
                            (df_Matches.tier == tier) &
                            (df_Matches.season == season)],
                            goal_type=goal_type, conf_intervall=0.95)
                    df['season'] = season
                    df['country_id'] = country_id
                    df['tier'] = tier
                    df['goal_type'] = goal_type
                    df_Goals = df_Goals.append(df, ignore_index=True)
    return df_Goals


# get mean goals distinguished by season, country, tier, stage and
# goalType (home, away, total, diff)
def GetDFMeanGoalsStage(df_Matches, goal_types=('home', 'away', 'total',
                                                'diff')):
    country_ids = df_Matches.country_id.unique()
    min_tiers = float('NaN')
    for country_id in country_ids:
        min_tiers = min([len(df_Matches[df_Matches['country_id'] ==
                                        country_id].tier.unique()), min_tiers])
    tiers = tuple(range(1, 1+min_tiers))
    df_Goals = pd.DataFrame()
    for country_id in country_ids:
        for tier in tiers:
            seasons = df_Matches.loc[(df_Matches.country_id ==
                                     country_id) & (df_Matches.tier ==
                                     tier)].season.unique()
            for season in seasons:
                stages = df_Matches.loc[(df_Matches.country_id ==
                                        country_id) & (df_Matches.tier ==
                                        tier) & (df_Matches.season ==
                                        season)].stage.unique()
                for stage in stages:
                    for goal_type in goal_types:
                        df = getMeanGoals(df_Matches.loc[
                                (df_Matches.country_id == country_id) &
                                (df_Matches.tier == tier) &
                                (df_Matches.season == season) &
                                (df_Matches.stage == stage)],
                                goal_type=goal_type, conf_intervall=0.95)
                        df['season'] = season
                        df['stage'] = stage
                        df['country_id'] = country_id
                        df['tier'] = tier
                        df['goal_type'] = goal_type
                        df_Goals = df_Goals.append(df, ignore_index=True)
    return df_Goals


def addCountryName(df, df_Countries):
    df['country_name'] = ''
    for i, row in enumerate(df.itertuples()):
        df.loc[i, 'country_name'] = df_Countries['country'].loc[
                df_Countries['id'] == row.country_id].iloc[0]
    return df


def getResultShare(df_Matches: 'Match database', *,
                   result: "choices: 'H', 'A', D'(default)'"='D',
                   conf_intervall: 'default = 0.95'=0.95):
    no_matches = len(df_Matches)
    t_critical = -stats.t.ppf(q=(1-conf_intervall)/2, df=no_matches)
    count = len(df_Matches.loc[df_Matches.FTR == result])
    share = count/no_matches
    margin_of_error = t_critical * math.sqrt(share * (1-share) / no_matches)
    conf_low = share - margin_of_error
    conf_high = share + margin_of_error
    df = pd.DataFrame({'share': [share],
                       'margin_of_error': [margin_of_error],
                       'conf_low': [conf_low],
                       'conf_high': [conf_high]})
    return df


def GetDFResultShare(df_Matches, results=('H', 'A', 'D')):
    country_ids = df_Matches.country_id.unique()
    min_tiers = float('NaN')
    for country_id in country_ids:
        min_tiers = min([len(df_Matches[df_Matches['country_id'] ==
                                        country_id].tier.unique()), min_tiers])
    tiers = tuple(range(1, 1+min_tiers))
    df_Results = pd.DataFrame()
    for country_id in country_ids:
        for tier in tiers:
            seasons = df_Matches.loc[(df_Matches.country_id ==
                                     country_id) & (df_Matches.tier ==
                                     tier)].season.unique()
            for season in seasons:
                for result in results:
                    df = getResultShare(df_Matches.loc[
                            (df_Matches.country_id == country_id) &
                            (df_Matches.tier == tier) &
                            (df_Matches.season == season)],
                            result=result, conf_intervall=0.95)
                    df['season'] = season
                    df['country_id'] = country_id
                    df['tier'] = tier
                    df['result'] = result
                    df_Results = df_Results.append(df, ignore_index=True)
    return df_Results


def getMatchesTeam(df_Matches, season, team_id):
    df_MatchesTeam = pd.DataFrame()
    if team_id not in df_Matches.home_team_id.unique():
        return df_MatchesTeam
    league_id = df_Matches.league_id.loc[(df_Matches.season == season) &
                                         (df_Matches.home_team_id == team_id)].unique()
    league_id = league_id[0]
    stages = df_Matches.loc[(df_Matches.season == season) &
                            (df_Matches.league_id == league_id)].stage.unique()
    for i, stage in enumerate(stages):
        df_TableStage = getTable(df_Matches, league_id, season, stages[i:i+1])
        df_TableStage['stage'] = stage
        df_MatchesTeam = df_MatchesTeam.append(df_TableStage.loc[df_TableStage.team_id == team_id],
                                               ignore_index=True)
    df_MatchesTeam['match_location'] = df_MatchesTeam['home_matches']\
                                       - df_MatchesTeam['away_matches']
    colNamesAway = df_MatchesTeam.columns[df_MatchesTeam.columns.str.contains(pat='away')]
    colNamesHome = df_MatchesTeam.columns[df_MatchesTeam.columns.str.contains(pat='home')]
    df_MatchesTeam.drop(colNamesAway, axis=1, inplace=True)
    df_MatchesTeam.drop(colNamesHome, axis=1, inplace=True)
    return df_MatchesTeam, league_id

def getMatchesTeam2(df_Matches, season, team_id):
    df_MatchesTeam = pd.DataFrame()
    if team_id not in df_Matches.home_team_id.unique():
        return df_MatchesTeam
    league_id = df_Matches.league_id.loc[(df_Matches.season == season) &
                                         (df_Matches.home_team_id == team_id)].unique()
    league_id = league_id[0]
    stages = df_Matches.loc[(df_Matches.season == season) &
                            (df_Matches.league_id == league_id)].stage.unique()
    df_MatchesTeam = df_Matches.loc[(df_Matches.home_team_id == team_id) |
                                    (df_Matches.away_team_id == team_id)]
    df_MatchesTeam = df_MatchesTeam.loc[(df_MatchesTeam.season == season) &
                                        (df_MatchesTeam.league_id == league_id)]
    df_MatchesTeam.loc[:,'stage'] = stages
    df_MatchesTeam['match_location'] = 0
    df_MatchesTeam.loc[df_MatchesTeam.home_team_id == team_id,
                       'match_location'] = 1
    df_MatchesTeam.loc[df_MatchesTeam.away_team_id == team_id,
                       'match_location'] = -1
    df_MatchesTeam['goals_difference'] = (df_MatchesTeam.FTHG-df_MatchesTeam.FTAG)*df_MatchesTeam.match_location
    df_MatchesTeam['shots_difference'] = (df_MatchesTeam.HS-df_MatchesTeam.AS)*df_MatchesTeam.match_location
    df_MatchesTeam['shotsTarget_difference'] = (df_MatchesTeam.HST-df_MatchesTeam.AST)*df_MatchesTeam.match_location
    
    df_MatchesTeam['goals_shot'] = 0
    df_MatchesTeam['shots_shot'] = 0
    df_MatchesTeam['shotsTarget_shot'] = 0
    
    df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'goals_shot'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'FTHG']
    df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'goals_shot'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'FTAG']
    
    df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'shots_shot'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'HS']
    df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'shots_shot'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'AS']
    
    df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'shotsTarget_shot'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'HST']
    df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'shotsTarget_shot'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'AST']
    
    df_MatchesTeam['goals_received'] = 0
    df_MatchesTeam['shots_received'] = 0
    df_MatchesTeam['shotsTarget_received'] = 0
    
    df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'goals_received'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'FTAG']
    df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'goals_received'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'FTHG']
    
    df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'shots_received'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'AS']
    df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'shots_received'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'HS']
    
    df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'shotsTarget_received'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == 1, 'AST']
    df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'shotsTarget_received'] = df_MatchesTeam.loc[df_MatchesTeam.match_location == -1, 'HST']
    
    df_MatchesTeam['team_id'] = team_id
    
    
    columns = ['id', 'team_id', 'date', 'match_location', 'stage',
               'league_id', 'season', 'tier', 'country_id', 'goals_difference',
               'shots_difference', 'shotsTarget_difference', 'goals_shot',
               'shots_shot', 'shotsTarget_shot', 'goals_received',
               'shots_received', 'shotsTarget_received']
    df_MatchesTeam = df_MatchesTeam.loc[:, columns]
    return df_MatchesTeam, league_id


def getHomeAdvantage(df_Matches, season, league_id):
    df_stats = df_Matches.loc[(df_Matches.season == season) &
                              (df_Matches.league_id == league_id)].describe()
    goals = df_stats.loc['mean', 'FTHG'] - df_stats.loc['mean', 'FTAG']
    if 'HST' in df_stats.columns:
        shotsTarget = df_stats.loc['mean', 'HST'] - df_stats.loc['mean', 'AST']
    if 'HST' not in df_stats.columns:
        shotsTarget = float('NaN')

    if 'HS' in df_stats.columns:
        shots = df_stats.loc['mean', 'HS'] - df_stats.loc['mean', 'AS']
    if 'HS' not in df_stats.columns:
        shots = float('NaN')

    df = pd.DataFrame({'league_id': [league_id],
                       'season': [season],
                       'goals': [goals],
                       'shotsTarget': [shotsTarget],
                       'shots': [shots]
                       })
    df.dropna(axis=1, how='any', inplace=True)
    return df


def getMatchesTeamNeutral(df_Matches, season, team_id):
    df, league_id = getMatchesTeam2(df_Matches, season, team_id)
    df_HomeAdv = getHomeAdvantage(df_Matches, season, league_id)
    df_Neutral = df.copy()

    df_Neutral.loc[:,'goals_difference'] = df.loc[:,'goals_difference']-df_HomeAdv.loc[0,'goals']*df.loc[:,'match_location']
    df_Neutral.loc[:,'shots_difference'] = df.loc[:,'shots_difference']-df_HomeAdv.loc[0,'shots']*df.loc[:,'match_location']
    df_Neutral.loc[:,'shotsTarget_difference'] = df.loc[:,'shotsTarget_difference']-df_HomeAdv.loc[0,'shotsTarget']*df.loc[:,'match_location']

    df_Neutral.loc[:,'goals_shot'] = df.loc[:,'goals_shot']-df_HomeAdv.loc[0,'goals']*df.loc[:,'match_location']/2
    df_Neutral.loc[:,'shots_shot'] = df.loc[:,'shots_shot']-df_HomeAdv.loc[0,'shots']*df.loc[:,'match_location']/2
    df_Neutral.loc[:,'shotsTarget_shot'] = df.loc[:,'shotsTarget_shot']-df_HomeAdv.loc[0,'shotsTarget']*df.loc[:,'match_location']/2

    df_Neutral.loc[:,'goals_received'] = df.loc[:,'goals_received']+df_HomeAdv.loc[0,'goals']*df.loc[:,'match_location']/2
    df_Neutral.loc[:,'shots_received'] = df.loc[:,'shots_received']+df_HomeAdv.loc[0,'shots']*df.loc[:,'match_location']/2
    df_Neutral.loc[:,'shotsTarget_received'] = df.loc[:,'shotsTarget_received']+df_HomeAdv.loc[0,'shotsTarget']*df.loc[:,'match_location']/2
    return df, df_Neutral, df_HomeAdv

