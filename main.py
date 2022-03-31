import time
import helper
import math

def get_data():
    difference = helper.get_difference()
    day = int(difference / helper.Data.sol)
    percentage = math.floor(int(day) / 668 * 100)
    latest = helper.recent_one()
    if str(percentage) != latest:
        return True, day, percentage
    else:
        return False, day, percentage


def tweet(day, percentage):
    if percentage == 0:
        helper.send_tweet(668, 100)
        helper.send_tweet(0, 0)
    else:
        helper.send_tweet(day,percentage)

if __name__ == "__main__":
    while True:
        moment, day, percentage = get_data()
        print(moment, day)
        if moment:
            tweet(day, percentage)
        else:
            pass

        time.sleep(500)




