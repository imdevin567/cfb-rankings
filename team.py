import config

class Team:
  wins = 0
  losses = 0
  division = ''
  games = []
  html = None
  normalized_wq = 0
  adjusted_normalized_wq = 0

  def __init__(self, name, url):
    self.name = name
    self.url = url

  def winning_percentage(self):
    return float(self.wins) / len(self.games)

  def win_quality_avg(self):
    if self.division != 'Div FBS':
      avg = config.NON_FBS_WQ
    else:
      win_qualities = [game.quality() for game in self.games]
      avg = sum(win_qualities) / len(self.games)
    return avg

  def strength_of_schedule(self):
    win_quality_avgs = [game.opponent.normalized_wq for game in self.games]
    return sum(win_quality_avgs) / len(self.games)

  def unadjusted_rating(self):
    if self.division != 'Div FBS':
      rating = config.NON_FBS_RATING
    else:
      rating = (self.normalized_wq * config.RAW_WQ_MULT) + (self.strength_of_schedule() * config.RAW_SOS_MULT)
    return rating

  def adjusted_win_quality_avg(self):
    if self.division != 'Div FBS':
      avg = config.NON_FBS_WQ
    else:
      win_qualities = [game.adjusted_quality() for game in self.games]
      avg = sum(win_qualities) / len(self.games)
    return avg

  def adjusted_strength_of_schedule(self):
    win_quality_avgs = [game.opponent.adjusted_normalized_wq for game in self.games]
    return sum(win_quality_avgs) / len(self.games)

  def rating(self):
    return (self.adjusted_normalized_wq * config.WQ_MULT) + (self.adjusted_strength_of_schedule() * config.SOS_MULT)
