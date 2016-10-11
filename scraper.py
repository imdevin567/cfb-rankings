from data import Data
from team import Team
from game import Game, Location
from urllib.request import build_opener
import urllib.error
import concurrent.futures
import json
import re
from bs4 import BeautifulSoup

class Scraper:
  def __init__(self, data, from_cache=False):
    self.from_cache = from_cache
    self.data = data
    teams_json = open('data/schools.json')
    for team in json.load(teams_json):
      self.data.teams.append(Team(team['name'], team['url']))

  def run(self):
    self.get_team_pages()
    self.get_team_season_info()
    #with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
    #  future_to_team = {executor.submit(self.get_team_season_info, team): team for team in filter(self.has_html_page, self.data.teams)}
    #  for future in concurrent.futures.as_completed(future_to_team):
    #    new_teams.append(future.result())

  def has_html_page(self, team):
    return team.html is not None

  def get_team_pages(self):
    if self.from_cache:
      for team in self.data.teams:
        team.html = self.data.db[team.url]
        print('Using cache for ' + team.name)
    else:
      #with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
      for team in self.data.teams:
        if team.url == 'uab':
          continue
        # Scrape the data from NCAA.com because there aren't any free APIs for this damn data
        opener = build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
          sock = opener.open("http://www.ncaa.com/schools/" + team.url + "/football")
        except (urllib.error.HTTPError):
          print('404 for ' + team.name)
          continue
        team.html = sock.read()
        print('Retrieved data for ' + team.name)
      self.data.save()

  def get_team_season_info(self):
    for team in filter(self.has_html_page, self.data.teams):
      team.games = []
      print('Calculating season info for ' + team.name)
      soup = BeautifulSoup(team.html, 'html.parser') # mmm, soup
      div = soup.find("div", {"id": "tabs-1"})
      if not div:
        continue
      table = soup.find("table")
      if not table:
        continue
      rows = table.find_all("tr")
      if not rows:
        continue

      li = soup.find("li", {"class": "school-info"})
      team.division = li.contents[1].string.strip()

      for row in rows:
        cells = row.find_all("td")
        if not cells or not cells[3] or not cells[3].string: # Game hasn't played yet
          continue
        if "W" not in cells[2].string and "L" not in cells[2].string: # NCAA.com likes to stick an asterisk here for title games
          continue
        # Save team record
        record = re.findall("\d+", cells[3].string)
        team.wins = record[0]
        team.losses = record[1]

        if team.division == 'Div FBS':
          # Handle win/loss to know which score is for this team
          result = cells[2].string.split(" ")
          score = re.findall("\d+", result[1])
          win = result[0] == "W"
          team_score = 0
          opp_score = 0
          if win:
            team_score = float(score[0])
            opp_score = float(score[1])
          else:
            team_score = float(score[1])
            opp_score = float(score[0])

          # Handle location of game and opponent
          location = 0
          opponent = ""
          if len(cells[1].contents) > 1 and cells[1].contents[0].strip() == "@":
            location = Location.away
            opponent_data = cells[1].contents[1]['href'].split("/")
          elif len(cells[1].contents) > 1 and cells[1].contents[0].strip() == "vs.":
            location = Location.neutral
            opponent_data = cells[1].contents[1]['href'].split("/")
          else:
            location = Location.home
            opponent_data = cells[1].contents[0]['href'].split("/")

          opponent = [team for team in self.data.teams if team.url == opponent_data[2]][0]

          # Create new instance of game
          game = Game(location, opponent, team_score, opp_score)
          team.games.append(game)
        else:
          team.games.append([])
