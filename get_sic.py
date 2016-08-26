import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join('scrape_sic')))
import scrape_sic_osha as osha
import scrape_sic_sec as sec

osha.get_sic_all()
sec.save_sic_sec()
