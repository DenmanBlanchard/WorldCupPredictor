import json
import os

import pandas as pd

from parsedata import main_parse


def getWins(teamid, matchday):

    with open(
        os.path.join(os.path.abspath("data\\teams"), f"{teamid}.json"), "r"
    ) as file:
        matches = json.load(file)
        df = pd.DataFrame.from_dict(matches["matches"])

        print(df)


def main_analyze(api_key):
    main_parse()
    getWins()
