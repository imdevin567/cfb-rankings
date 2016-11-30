from team import Team
from game import Game
import shelve

class Data:
  teams = []
  db = shelve.open('data/db', flag='c', protocol=None, writeback=False)

  def fbs_teams(self):
    return [team for team in self.teams if team.division == 'Div FBS']

  def sorted_win_qualities(self):
    return sorted(self.fbs_teams(), key=lambda x: x.win_quality_avg(), reverse=True)

  def sorted_adjusted_win_qualities(self):
    return sorted(self.fbs_teams(), key=lambda x: x.adjusted_win_quality_avg(), reverse=True)

  def normalize_wq(self):
    sorted_data = self.sorted_win_qualities()
    for team in self.fbs_teams():
      team.normalized_wq = (team.win_quality_avg() - sorted_data[-1].win_quality_avg()) / (sorted_data[0].win_quality_avg() - sorted_data[-1].win_quality_avg())

  def normalize_adjusted_wq(self):
    sorted_data = self.sorted_adjusted_win_qualities()
    for team in self.fbs_teams():
      team.adjusted_normalized_wq = (team.adjusted_win_quality_avg() - sorted_data[-1].adjusted_win_quality_avg()) / (sorted_data[0].adjusted_win_quality_avg() - sorted_data[-1].adjusted_win_quality_avg())

  def sorted_rankings(self, limit=None):
    if limit is None:
      data = sorted(self.fbs_teams(), key=lambda x: x.rating(), reverse=True)
    else:
      data = sorted(self.fbs_teams(), key=lambda x: x.rating(), reverse=True)[:limit]
    return data

  # Cache methods
  def clear(self):
    for team in self.teams:
      del self.db[team.url]

  def save(self):
    for team in self.teams:
      self.db[team.url] = team.html

  def close_db(self):
    self.db.close()
