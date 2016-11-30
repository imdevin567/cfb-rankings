#!/usr/bin/env python3

from scraper import Scraper
from ncaa14 import NCAA14
from data import Data
from tabulate import tabulate

def calculator(data, engine):
  engine.run()
  data.normalize_wq()
  data.normalize_adjusted_wq()

  rankings = data.sorted_rankings(25)
  vals = [[i+1]+[str(val) for k, val in team] for i, team in enumerate(rankings)]
  keys = [[k for k, val in team] for team in rankings][0]
  keys.insert(0, 'Ranking')
  print(tabulate(vals, headers=keys, floatfmt='.3f'))
  return data.sorted_rankings()

def scraper(use_cache):
  data = Data()
  calculator(data, Scraper(data, use_cache))

def ncaa14():
  data = Data()
  ncaa = NCAA14(data)
  calc = calculator(data, ncaa)
  vals = [[i+1]+[str(val) for k, val in team] for i, team in enumerate(calc)]
  keys = [[k for k, val in team] for team in calc][0]
  print(tabulate(vals, headers=keys, floatfmt='.3f'))
  #ncaa.save_bcs_rank()
  ncaa.get_win_qualities()

#ncaa14()
scraper(False)
#scraper(True)
