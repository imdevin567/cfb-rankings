# This script isn't necessary for the calculations. It ranks the
# win qualities of individual games in descending order. I was
# using this to validate how accurate the win quality formula was.

import csv

win_quality = open("data/adjusted-win-qualities.csv")
wq = list(csv.reader(win_quality))
rankings = sorted(wq, key=lambda x: float(x[2]), reverse=True)
with open("data/sorted-win-qualities.csv", "w") as output_file:
	writer = csv.writer(output_file)
	writer.writerows(rankings)
