# STEP 2
# The meat of the calculation. This script iterates over each game for
# each team. ONLY GAMES THAT HAVE BEEN PLAYED ARE INCLUDED, NO FUTURE GAMES.
# Resulting data for individual games is saved to data/win-qualities.csv in the format of:
# team_name,opponent,win_quality
# Resulting data for total win quality per team is saved to data/win-quality-average.csv in the format of:
# team_name,win_quality_average

import urllib
import csv
import re
from bs4 import BeautifulSoup

LOSS_CONST = -1 # Value of a standard loss
WIN_CONST = 1 # Value of a standard win
ROAD_WIN_ADD = 0.07 # Bonus for road win
HOME_LOSS_ADD = -0.07 # Penalty for home loss
PER_POINT_MULT = 0.01 # Value of each point in point differential
NON_FBS_RATING = 0.005 # Factor to multiply Non-FBS winning percentages by
MAX_POINT_DIFF = 28 # Maximum point differential

# List of records for each team
schools_csv = open("data/final-data.csv")
schools = list(csv.reader(schools_csv))

def rating_by_team(team_name):
    rating = False
    for team in schools:
        if team_name in team:
            rating = team
            break
    return rating

wq_output_file = open('data/adjusted-win-qualities.csv',"w")
wq_total_file = open('data/adjusted-win-quality-average.csv', "w")
for school in schools:
    WINQUALITY_TOTAL = 0
    num_games = 0

    # Still no damn API
    sock = urllib.urlopen("http://www.ncaa.com/schools/" + school[0] + "/football")
    html = sock.read()
    soup = BeautifulSoup(html) # mmm, soup
    div = soup.find("div", {"id": "tabs-1"})
    if not div:
        continue
    table = soup.find("table")
    if not table:
        continue
    rows = table.find_all("tr")
    if not rows:
        continue
    for row in rows:
        cells = row.find_all("td")
        if not cells or not cells[1] or not cells[2] or not cells[2].string: # Game hasn't played yet
            continue
        if "W" not in cells[2].string and "L" not in cells[2].string: # NCAA.com likes to stick an asterisk here for title games
            continue
        WINQUALITY = 0
        opponent_url = ""
        opponent_record = []
        opponent_rating = 0
        rating_factor = opponent_rating
        result = cells[2].string.split(" ")
        score = re.findall("\d+", result[1])

        # I don't always use ternaries, but when I do, they're long as hell.
        point_diff = (float(score[0]) - float(score[1])) if (float(score[0]) - float(score[1])) <= MAX_POINT_DIFF else MAX_POINT_DIFF
        win = False
        home_or_away = ""

        if len(cells[1].contents) > 1 and cells[1].contents[0].strip() == "@":
            home_or_away = "AWAY"
            opponent_url = cells[1].contents[1]['href'].split("/")
        elif len(cells[1].contents) > 1 and cells[1].contents[0].strip() == "vs.":
            home_or_away = "NEUTRAL"
            opponent_url = cells[1].contents[1]['href'].split("/")
        else:
            home_or_away = "HOME"
            opponent_url = cells[1].contents[0]['href'].split("/")

        if result[0] == "W":
            win = True

        if win:
            WINQUALITY += WIN_CONST
            WINQUALITY += (point_diff * PER_POINT_MULT)
            if home_or_away == "AWAY":
                WINQUALITY += ROAD_WIN_ADD
        else:
            WINQUALITY += LOSS_CONST
            WINQUALITY -= (point_diff * PER_POINT_MULT)
            if home_or_away == "HOME":
                WINQUALITY += HOME_LOSS_ADD

        opponent = opponent_url[2]
        opponent_record = rating_by_team(opponent)
        opponent_rating = float(opponent_record[3]) if opponent_record else NON_FBS_RATING
        rating_factor = opponent_rating if win else abs(opponent_rating - 1)

        WINQUALITY = WINQUALITY * rating_factor
        WINQUALITY_TOTAL += WINQUALITY
        num_games += 1
        wq_output_file.write(school[0] + "," + opponent + "," + str(WINQUALITY) + "\n")
    wq_total_file.write(school[0] + "," + str(WINQUALITY_TOTAL / num_games) + "\n")
wq_output_file.close()
schools_csv.close()