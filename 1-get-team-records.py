# STEP 1
# This script grabs the record of each team in the data/schools.json file
# strength of schedule by averaging the win quality of their opponents.
# Resulting data is saved to data/team-records.csv in the format of:
# team_name,division,wins,losses

import urllib
import json
import re
from bs4 import BeautifulSoup

schools_json = open("data/schools.json")
schools = json.load(schools_json)
with open('data/team-records.csv',"w") as output_file:
    for school in schools:
        # Scrape the data from NCAA.com because there aren't any free APIs for this damn data
        sock = urllib.urlopen("http://www.ncaa.com/schools/" + school["url"] + "/football")
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
        rows.reverse() # Reverse to get the record after the last played game
        for row in rows:
            cells = row.find_all("td")
            if not cells or not cells[3] or not cells[3].string: # Game hasn't played yet
                continue
            record = re.findall("\d+", cells[3].string)
            wins = record[0]
            losses = record[1]
            break
        li = soup.find("li", {"class": "school-info"})
        division = li.contents[1].string.strip()
        output_file.write(school["url"] + "," + division + "," + wins + "," + losses + "\n")
    schools_json.close()
