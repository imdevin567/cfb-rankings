from scraper import Scraper
from data import Data

d = Data()
#d.clear()
s = Scraper(d, True)
s.run()
d.save()
d.normalize_wq()
d.normalize_adjusted_wq()

for team in d.sorted_rankings():
  print(team.name + ': ' + str(team.adjusted_normalized_wq) + ',' + str(team.adjusted_strength_of_schedule()) + ',' + str(team.rating()))
