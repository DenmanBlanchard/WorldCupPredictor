import requests
import pandas
import json
import os
import time
import math

import data.globals as glb 

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

def getData(url_end = "competitions"):
    
    url = "http://api.football-data.org/v4/"

    payload = {}
    headers = {
        "X-Auth-Token": api_key,
    }

    has_Called = False

    while not(has_Called):
        if glb.isAbleCall():
            try:
                response = requests.request("GET", (url + url_end), headers=headers, data=payload)

                has_Called = True

                if response.status_code == 200:
                    if response.text:
                        return response.text
                    else:
                        return {"Nothing"}

                else:
                    response.raise_for_status()
            except Exception as e:
                if str(e).startswith("429"):
                    print("Rate Limited")
                    time.sleep(61.0)
                    glb.last_minute = math.floor(time.time() / 60)
                    glb.current_calls = 0

                has_Called = False

        else:
            continue


def main_parse():
    for i in range (20):
        getData("competitions/WC/matches")
        print("Got data")
    
