# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath(
    'scrape_sic'))
import scrape_sic_osha as scrape

url = 'https://www.osha.gov/pls/imis/sic_manual.display?id=1&tab=group'
majors = scrape.get_major(url)
for m in majors:
    print (m.parent_desc) + (m.full_desc)
print len(majors)
