import os
import sys
sys.path.insert(0, os.path.abspath(
    '/Users/Ryan/Github/SIC-list/scrape_sic'))

import scrape_sic_sec
scrape_sic_sec.get_sic_sec('test.csv')
