import json
import os

import pandas as pd

startElo = 10000
eloDF = pd.DataFrame(columns=["id", "elo"])


def updateTeamElo(team1id, team2id=0, wld=0, init=False):
    if init:
        eloDF.loc[len(eloDF)] = [team1id, startElo]
    else:
        match wld:
            case 0:  # They won
                t1EloDF = eloDF[eloDF["id"] == team1id]
                t2EloDF = eloDF[eloDF["id"] == team2id]

                if t1EloDF.iat[0, 1] > t2EloDF.iat[0, 1]:
                    eloDF.loc[eloDF.iloc[:, 0] == team1id, "elo"] = (
                        t1EloDF.iat[0, 1] + 100
                    )
                elif t1EloDF.iat[0, 1] == t2EloDF.iat[0, 1]:
                    eloDF.loc[eloDF.iloc[:, 0] == team1id, "elo"] = t1EloDF.iat[
                        0, 1
                    ] + (t2EloDF.iat[0, 1] / 2)
                elif t1EloDF.iat[0, 1] < t2EloDF.iat[0, 1]:
                    eloDF.loc[eloDF.iloc[:, 0] == team1id, "elo"] = t1EloDF.iat[
                        0, 1
                    ] + ((t2EloDF.iat[0, 1] / 4) * 3)
                else:
                    raise ValueError

            case 1:  # They lost
                t1EloDF = eloDF[eloDF["id"] == team1id]
                t2EloDF = eloDF[eloDF["id"] == team2id]

                if t1EloDF.iat[0, 1] < t2EloDF.iat[0, 1]:
                    eloDF.loc[eloDF.iloc[:, 0] == team1id, "elo"] = (
                        t1EloDF.iat[0, 1] - 100
                    )
                elif t1EloDF.iat[0, 1] == t2EloDF.iat[0, 1]:
                    eloDF.loc[eloDF.iloc[:, 0] == team1id, "elo"] = t1EloDF.iat[
                        0, 1
                    ] - (t2EloDF.iat[0, 1] / 4)
                elif t1EloDF.iat[0, 1] > t2EloDF.iat[0, 1]:
                    eloDF.loc[eloDF.iloc[:, 0] == team1id, "elo"] = t1EloDF.iat[
                        0, 1
                    ] - (((t2EloDF.iat[0, 1] / 4) * 3) / 2)
                else:
                    raise ValueError

            case 2:  # They drew
                pass


def updateElo(teamid, matchday):

    with open(
        os.path.join(os.path.abspath("data"), "teams", f"{teamid}.json"), "r"
    ) as file:
        matches = json.load(file)

        for match in matches["matches"]:
            if match["matchday"] == matchday:
                if match["status"] == "FINISHED":
                    match match["score"]["winner"]:
                        case "AWAY_TEAM":
                            if match["awayTeam"]["id"] == teamid:
                                updateTeamElo(teamid, match["homeTeam"]["id"], 0)
                            else:
                                updateTeamElo(teamid, match["homeTeam"]["id"], 1)
                        case "HOME_TEAM":
                            if match["homeTeam"]["id"] == teamid:
                                updateTeamElo(teamid, match["awayTeam"]["id"], 0)
                            else:
                                updateTeamElo(teamid, match["awayTeam"]["id"], 1)
                        case "DRAW":
                            updateTeamElo(
                                match["awayTeam"]["id"], match["homeTeam"]["id"], 2
                            )
                else:
                    pass


def main_analyze(api_key):
    # main_parse()
    with open(os.path.join(os.path.abspath("data"), "teams.json"), "r") as file:
        teams = json.load(file)
        # Initialize elo
        for team in teams["teams"]:
            updateTeamElo(team["id"], init=True)

        # Update elo
        for team in teams["teams"]:
            for matchday in range(teams["season"]["currentMatchday"] - 1):
                updateElo(team["id"], matchday + 1)

        print(eloDF)
