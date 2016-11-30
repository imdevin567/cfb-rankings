import config
from enum import Enum

class Location(Enum):
  home = 1
  away = 2
  neutral = 3

class Game:
  def __init__(self, location, opponent, team_score, opponent_score):
    self.location = location
    self.opponent = opponent
    self.team_score = team_score
    self.opponent_score = opponent_score
    self.differential = max(team_score, opponent_score) - min(team_score, opponent_score)

  def win(self):
    return self.team_score > self.opponent_score

  def raw_quality(self):
    quality = 0
    if self.win():
      quality += config.WIN_CONST
      quality += min(self.differential, config.MAX_POINT_DIFF) * config.PER_POINT_MULT
      if self.location == Location.away:
        quality += config.ROAD_WIN_ADD
    else:
      quality += config.LOSS_CONST
      quality -= min(self.differential, config.MAX_POINT_DIFF) * config.PER_POINT_MULT
      if self.location == Location.home:
        quality += config.HOME_LOSS_ADD
    return quality

  def quality(self):
    quality = self.raw_quality()
    opponent_winperc = min(max(self.opponent.winning_percentage(), config.MIN_WINPERC), config.MAX_WINPERC)
    if self.opponent.division != 'Div FBS':
      opponent_winperc = opponent_winperc * config.NON_FBS_MULT
    winperc_factor = opponent_winperc if self.win() else abs(opponent_winperc - 1)
    return quality * winperc_factor

  def adjusted_quality(self):
    quality = self.raw_quality()
    opponent_rating = min(max(self.opponent.unadjusted_rating(), config.MIN_RATING), config.MAX_RATING)
    rating_factor = opponent_rating if self.win() else abs(opponent_rating - 1)
    return quality * rating_factor
