from data import Data
from team import Team
from game import Game, Location
import csv

class NCAA14:
  def __init__(self, data):
    self.data = data

  def run(self):
    self.get_team_info()
    self.get_team_season_info()

  def save_bcs_rank(self):
    output = open('data/teams_ranked.csv', 'w')
    reader = csv.reader(open('data/teams.csv'))
    lines = [l for l in reader]
    output.write(lines[0][0] + ',' + lines[0][1] + "\n")
    with open('data/teams.csv') as csvfile:
      next(csvfile)
      teams = csv.DictReader(csvfile)
      csvwriter = csv.DictWriter(output, teams.fieldnames)
      csvwriter.writeheader()
      rankings = self.data.sorted_rankings()
      for team in teams:
        finder = [t for t in rankings if t.url == team['TSNA']]
        if len(finder) > 0:
          if int(team['TBPR']) == 0:
            team['TBPR'] = team['TBRK']
          else:
            team['TBPR'] = finder[0].previous_bcs_rank
          team['TBRK'] = rankings.index(finder[0]) + 1
          csvwriter.writerow(team)

  def get_win_qualities(self):
    with open('data/wqs.csv', 'w') as csvfile:
      for team in self.data.fbs_teams():
        for game in team.games:
          csvfile.write(team.name + ',' + game.opponent.name + ',' + str(game.adjusted_quality()) + "\n")

  def get_team_info(self):
    with open('data/teams.csv') as csvfile:
      next(csvfile)
      teams = csv.DictReader(csvfile)
      for team in teams:
        new_team = Team(team['TDNA'], team['TSNA'])
        new_team._id = team['TGID']
        new_team.division = 'Div FBS' if team['LGID'] == '0' else 'FCS'
        new_team.wins = int(team['TSWI'])
        new_team.losses = int(team['TSLO'])
        new_team.bcs_rank = int(team['TBRK'])
        new_team.previous_bcs_rank = int(team['TBPR'])
        new_team.games = []
        self.data.teams.append(new_team)

  def get_team_season_info(self):
    with open('data/games.csv') as csvfile:
      next(csvfile)
      games = csv.DictReader(csvfile)
      for game in games:
        home_score = int(game['GHSC'])
        away_score = int(game['GASC'])

        if home_score == 0 and away_score == 0:
          continue # game hasn't played yet

        home_team = [team for team in self.data.teams if team._id == game['GHTG']][0]
        away_team = [team for team in self.data.teams if team._id == game['GATG']][0]

        if home_team.division == 'Div FBS':
          home_team.games.append(Game(Location.home, away_team, home_score, away_score))
        else:
          home_team.games.append([])

        if away_team.division == 'Div FBS':
          away_team.games.append(Game(Location.away, home_team, away_score, home_score))
        else:
          away_team.games.append([])
