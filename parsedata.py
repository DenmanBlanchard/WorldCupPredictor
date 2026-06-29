import json
import math
import os
import time

import requests
import tqdm
from dotenv import load_dotenv

import data.globals as glb

load_dotenv()

api_key = os.getenv("API_KEY")


def getTeams():
    with open(os.path.join(os.path.abspath("data"), "teams.json"), "w") as file:
        json.dump(getData("competitions/WC/teams?season=2026"), file, indent=4)


def getMatches(teamid):
    try:
        with open(
            os.path.join(os.path.abspath("data"), "teams", f"{teamid}.json"), "w"
        ) as file:
            json.dump(
                getData(f"teams/{teamid}/matches?season=2026&competitions=2000,"),
                file,
                indent=4,
            )
    except Exception:
        os.mkdir(os.path.join("data", "teams"))
        getMatches(teamid)


def getData(url_end="competitions", unfold_goals=False):

    url = "http://api.football-data.org/v4/"

    payload = {}
    headers = {
        "X-Auth-Token": api_key,
        **({"X-Unfold-Goals": True} if unfold_goals else {}),
    }

    has_Called = False

    while not (has_Called):
        if glb.isAbleCall():
            try:
                response = requests.request(
                    "GET", (url + url_end), headers=headers, data=payload
                )

                has_Called = True

                if response.status_code == 200:
                    if response.text:
                        return response.json()
                    else:
                        return {"Nothing"}

                else:
                    response.raise_for_status()
            except Exception as e:
                if str(e).startswith("429"):
                    print(f"\r{'Rate Limited':<{glb.columns}}", end="", flush=True)
                    time.sleep(61.0)
                    glb.last_minute = math.floor(time.time() / 60)
                    glb.current_calls = 0
                elif (
                    str(e).startswith("4")
                    or str(e).startswith("3")
                    or str(e).startswith("2")
                    or str(e).startswith("1")
                ):
                    print(e)
                    print(response.text)
                    exit()

                has_Called = False

        else:
            continue


def main_parse():
    if glb.check_internet():
        print("\nGetting team data")
        getTeams()

        print("\nGetting match data for all the teams")
        with open(os.path.join(os.path.abspath("data"), "teams.json"), "r") as file:
            teams = json.load(file)
            for team in tqdm.tqdm(
                teams["teams"],
                desc="Getting matches",
                unit="match",
                colour="blue",
            ):
                getMatches(team["id"])
    else:
        print("Internet connection failed for some reason")
