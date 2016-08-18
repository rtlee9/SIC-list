# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath(
    'scrape_sic'))
import scrape_sic_osha as scrape


fname = 'test_div_raw.pkl'
print scrape.save_divisions(fname)
os.remove(fname)

fname = 'test_maj_raw.pkl'
print scrape.save_majors(fname)
os.remove(fname)
