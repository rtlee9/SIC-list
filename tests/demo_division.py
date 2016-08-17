# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath(
    'scrape_sic'))
import scrape_sic_osha as scrape

divisions = scrape.get_divisions()

for d in divisions:
    print str(d.parent_desc) + d.full_desc
