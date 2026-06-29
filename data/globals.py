import math
import os
import time
import platform
import tqdm

global max_calls
global current_calls
global last_second
global columns
global lines

max_calls = 8
current_calls = 0

columns, lines = os.get_terminal_size()


last_minute = math.floor(time.time() / 60)


def isAbleCall(tqdm=False):
    
    rateCheck = checkRate()

    if rateCheck:
        return True

    return False


def checkRate():
    global current_calls, last_minute

    now = math.floor(time.time() / 60)

    # If we've moved to a new minute, reset the counter
    if now != last_minute:
        last_minute = now
        current_calls = 0

    if current_calls < max_calls:
        current_calls += 1
        return True

    # reached max calls for this minute
    sleep_time = (math.floor(time.time()) - (last_minute * 60)) + 1

    first_string = f"Waiting for {sleep_time} seconds"
    second_string = f"Getting data / Continuing. Waited for {sleep_time} seconds"

    if not tqdm:
        print(
            f"\r{first_string:<{columns}}",
            end="",
            flush=True,
        )
        time.sleep((math.floor(time.time()) - (last_minute * 60)) + 1)
        print(
            f"\r{second_string:<{columns}}",
            end="",
            flush=True,
        )
    else:
        time.sleep((math.floor(time.time()) - (last_minute * 60)) + 1)

    return False


def check_internet():

    current_os = platform.system().lower()

    if current_os == "windows":
        command = "ping -n 1 -w 1000 1.1.1.1 > nul 2>&1"

    else:
        command = "ping -c 1 -W 1000 1.1.1.1 /dev/null 2>&1"

    response = os.system(command)

    return response == 0
