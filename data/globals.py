import time
import math

global max_calls
global current_calls
global last_second

max_calls = 8
current_calls = 0


last_minute = math.floor(time.time() / 60)


def isAbleCall():
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
    return False
