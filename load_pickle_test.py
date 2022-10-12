import os
import pandas as pd
import pickle
from fuzzywuzzy import process, fuzz

pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('expand_frame_repr', False)


def find_sure_bets(df):
    keys = df.keys()
    ko = [k for k in keys if "Odds" in k]
    arb = (1/df[ko]).sum(axis=1)
    m = arb < 1
    return df[m]


def get_betting_amounts(df, stake, rounding=5):
    # rounding to nearest 1, 5, 0.1 etc
    keys = df.keys()
    keys_o = [k for k in keys if "Odds" in k]
    n_k = len(keys_o)
    names_s = {keys_o[i]: "Stake" + str(i+1) for i in range(n_k)}
    names_p = {keys_o[i]: "Profit" + str(i+1) for i in range(n_k)}
    arbitrages = (1 / df[keys_o]).sum(axis=1)
    odds = df[keys_o]
    stakes = stake*(1 / odds).div(arbitrages, axis=0).rename(columns=names_s)
    stakes = rounding * (stakes / rounding).round(0)
    profits = odds.mul(stakes.values).rename(columns=names_p) - stake
    df = df.join(stakes).join(profits)

    return df


threshold = 90
sport = "football"
webb = "bethard"
path = "/home/per/Desktop/pythonProject/arbitrage_betting/" + sport + "/"

II = 0

for file_name in sorted(os.listdir(path)):    # Remove sorted
    if file_name.endswith(sport):
        read_test = pickle.load(open(path + file_name, 'rb'))
        if II == 0:
            df1 = read_test
            keys = df1.keys()
            odds_keys = [k for k in keys if "Odds" in k]
            webb_keys = [k for k in keys if "Webb" in k]
        elif II == 1:
            teams = ["Nah", "SaintEtienne Monaco", "CKK", "Brentford Tottenham"]
            odds1 = [1,100, 137,-1]
            odds2 = [0,9, 1337, 9]
            odds3 = [0,999, 0,11]
            webb = "LOL.com"
            dict_gambling = {"Games": teams, "Odds1": odds1, "Odds2": odds2, "Odds3": odds3, "Webb1": webb,
                             "Webb2": webb, "Webb3": webb}
            df2 = pd.DataFrame.from_dict(dict_gambling)

            # Comparing strings of dataframes
            dfm = df1.copy()
            dfm[["Matches", "Score"]] = dfm["Games"].apply(
                lambda x: process.extractOne(x, teams, scorer=fuzz.token_set_ratio)).apply(pd.Series)
            dfm = pd.merge(dfm, df2, left_on="Matches", right_on="Games")
            m1 = dfm["Score"] >= threshold   # Mask for matching strings
            m2 = ~df2["Games"].isin(dfm["Matches"])
            n = len(odds_keys)
            for i in range(n):
                ko = odds_keys[i]
                kw = webb_keys[i]
                ox = dfm.loc[m1, ko + "_x"]
                oy = dfm.loc[m1, ko + "_y"]
                wx = dfm.loc[m1, kw + "_x"]
                wy = dfm.loc[m1, kw + "_y"]
                b = ox >= oy
                df1.loc[m1, ko] = b*ox + ~b*oy
                df1.loc[m1, kw] = b*wx + ~b*wy

            df1 = pd.concat([df1, pd.DataFrame.from_records(df2[m2])])

        II += 1

dfsb = find_sure_bets(df1)
print(get_betting_amounts(dfsb, 100))