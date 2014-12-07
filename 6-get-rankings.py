# STEP 4
# This script re-orders the final data to reflect rankings.
# The key can be changed to order by win quality or strength of schedule as well.
# Resulting data is saved to data/rankings.csv in descending order in the format of:
# team_name,win_quality_average,sos,final_rating

import csv

win_quality = open("data/adjusted-final-data.csv")
wq = list(csv.reader(win_quality))

# The key for x in the lambda can be changed to rank by different values
# 1 = Win Quality Average
# 2 = Strength of Schedule
# 3 = Final Rating
rankings = sorted(wq, key=lambda x: float(x[3]), reverse=True)
with open("data/rankings.csv", "w") as output_file:
	writer = csv.writer(output_file)
	writer.writerows(rankings)
