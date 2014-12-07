# STEP 3
# This script gets the win quality averages from each team and calculates
# strength of schedule by averaging the win quality of their opponents.
# Resulting data is saved to data/final-data.csv in the format of:
# team_name,win_quality_average,sos,final_rating

import urllib
import csv

NON_FBS_WQ = 0 # Non-FBS opponents are considered to have a win quality average of 0
WQ_MULT = 0.99 # The percentage of the total counted for win quality
SOS_MULT = 0.01 # The percentage of the total counted for strength of schedule

# List of win quality averages for FBS teams
schools_csv = open("data/adjusted-win-quality-average.csv")
schools = list(csv.reader(schools_csv))

# List of win qualities for ALL games
wins_csv = open('data/adjusted-win-qualities.csv')
wins = list(csv.reader(wins_csv))

def wq_by_team(team_name):
    wq = False
    for school in schools:
        if school[0] == team_name:
            wq = school
            break
    return wq

def wins_by_team(team_name):
    team_wins = []
    for win in wins:
        if win[0] == team_name:
            team_wins.append(win)
        else:
            continue
    return team_wins

# Normalizes win quality averages for every team on a scale of 0 to 1
def normalize(val):
    sorted_data = sorted(schools, key=lambda x: float(x[1]), reverse=True)
    normalized = (val - float(sorted_data[-1][1])) / (float(sorted_data[0][1]) - float(sorted_data[-1][1]))
    return normalized

output_file = open('data/adjusted-final-data.csv', "w")
for school in schools:
    ADJUSTED_TOTAL = 0
    TOTAL_GAMES = 0
    normalized_wq = normalize(float(school[1]))
    team_wins = wins_by_team(school[0])
    for win in team_wins:
        opp = wq_by_team(win[1])
        opp_wq = float(opp[1]) if opp else NON_FBS_WQ
        ADJUSTED_TOTAL += normalize(float(opp_wq))
        TOTAL_GAMES += 1
    final_rating = (normalized_wq * WQ_MULT) + ((ADJUSTED_TOTAL / TOTAL_GAMES) * SOS_MULT)
    output_file.write(school[0] + "," + str(round(normalized_wq,3)) + "," + str(round((ADJUSTED_TOTAL / TOTAL_GAMES),3)) + "," + str(round(final_rating,3)) + "\n")
output_file.close()
schools_csv.close()
wins_csv.close()
