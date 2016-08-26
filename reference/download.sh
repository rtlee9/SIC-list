#!/bin/bash

wget -O SicCodesAllLevels.xls http://www.stssamples.com/xls/SicCodesAllLevels.xls
python to_csv.py
mv ref_list.csv ../tests/
