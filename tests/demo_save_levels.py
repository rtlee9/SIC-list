# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath(
    'scrape_sic'))
import scrape_sic_osha as scrape


fname = 'test_div_raw.pkl'
scrape.save_divisions(fname)
os.remove(fname)

url = 'https://www.osha.gov/pls/imis/sic_manual.display?id=1&tab=group'
fname = 'test_maj_raw.pkl'
scrape.save_majors(url, fname)
os.remove(fname)
