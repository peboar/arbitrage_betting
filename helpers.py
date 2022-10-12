from unidecode import unidecode
from fuzzywuzzy import fuzz
import pandas as pd
import pickle

def eng_to_swe(sport):
    """
    Translates sports and nation to swedish
    :param sport: english string
    :return: swedish string
    """
    sport = sport.lower()
    sports = {'football': 'fotboll',
              'tennis': 'tennis',
              'ice hockey': 'ishockey',
              'england': 'england',
              'germany': 'tyskland',
              'spain': 'spanien',
              'france': 'frankrike',
              'netherlands': 'nederländerna',
              'sweden': 'sverige',
              'italy': 'italien'}

    return sports[sport]


def get_number_of_odds(sport):
    if sport == "football":
        return 3
    if sport == "tennis":
        return 2


def simple_name(n):
    """
    Simplifies string
    """
    n = unidecode(n)
    n = n.replace('\n', ' ')
    n = n.replace('Draw', '')
    n = n.replace('Oavgjort', '')
    n = ''.join([i for i in n if i.isalpha() or i == ' ' or i == '/'])
    n = n.replace(' / ', '/')
    return n.strip()


def game_string(*event):
    """
    Returns event of odds
    """
    simple_event = []
    for name in event:
        simple_event.append(simple_name(name))
    return " ".join(simple_event)


def odds_2_float(o):
    """"
    Converts string of odds to float
    """
    return float(o.strip())


def game_odds(*odds):
    """
    Converts list of strings to list of floats
    """
    return [odds_2_float(o) for o in odds]


def save_frame(*args):
    """
    Saves dataframe of match odds. Only winner and loser is supported currently.
    3 args: filename, games, odds
    4 args: path, filename, games, odds
    """
    if len(args) == 4:
        filename, games, odds, webb = args
        n = len(odds)
        m = len(odds[0])
    else:
        raise TypeError('save_frame takes 3 arguments')

    wd = {"Webb" + str(i + 1): n * [webb] for i in range(m)}
    od = {"Odds" + str(j + 1): [odds[i][j] for i in range(n)] for j in range(m)}
    df = pd.DataFrame.from_dict({"Games": games, **od, **wd})
    df = df.apply(lambda x: x.strip() if isinstance(x, str) else x)  # Remove trailing whitespaces

    with open(filename, 'wb') as file:
        pickle.dump(df, file)
