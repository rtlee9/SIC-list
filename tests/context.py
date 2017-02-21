import sys
from os import path
sys.path.insert(0, path.join(path.dirname(path.dirname(__file__)), 'src'))

import scrape_sic_sec
import scrape_sic_osha
path_test = path.dirname(path.abspath(__file__))
