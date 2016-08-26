# SIC codes for download -- open source edition

[![Build Status](https://travis-ci.org/rtlee9/SIC-list.svg?branch=master)](https://travis-ci.org/rtlee9/SIC-list)
[![Coverage Status](https://coveralls.io/repos/github/rtlee9/SIC-list/badge.svg?branch=)](https://coveralls.io/github/rtlee9/SIC-list?branch=)
[![Code Climate](https://codeclimate.com/github/rtlee9/SIC-list/badges/gpa.svg)](https://codeclimate.com/github/rtlee9/SIC-list)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/rtlee9/SIC-list/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/rtlee9/SIC-list/?branch=master)
[![license](https://img.shields.io/badge/license-Apache_License-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/download/releases/2.7/)

The Standard Industrial Classification (SIC) is a system used to classify businesses by their primary business activity, or industry. The SIC system was created in the 1930's and has since been [replaced](https://www.census.gov/eos/www/naics/faqs/faqs.html#q8) as the industry classification system for Federal statistical agencies; however, it is still widely used by many businesses and by some government agencies.

## Authoritative sources

SIC codes were once maintained and assigned by the US government. I've found that only two government agencies currently publish a list of SIC codes and descriptions:

| Source | Version | Use case |
| ------ | ------- | -------- |
| [Occupational Safety & Health Administration (OSHA)](https://www.osha.gov/pls/imis/sic_manual.html) | 1987 SIC manual | Unknown |
| [U.S. Securities and Exchange Commission (SEC)](https://www.sec.gov/info/edgar/siccodes.htm) | No version provided, but the SEC website indicates the webpage was last modified January 25, 2015 | Used in [EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch.html) electronic filings |

The SIC codes that are provided by the SEC appear to align with those provided by OSHA upon an initial (and non-comprehensive) comparison; however, OSHA's SIC manual is more comprehensive -- it contains many more SIC codes than does the SEC's list.

## Other sources

There are a number of online sources that provide SIC codes and descriptions, though I've found none that provide all of the following:
* The source of their data
* Their code, if relevant
* Machine readable data

Taken together, these are important for assessing data quality and reliability. The purpose of this repository is to provide SIC codes in adherence with these standards.

## Usage

The latest data can be found in the root directory. To refresh:

1. Install Python 2.7
1. Install python requirements: `$ pip install -r requirements.txt`
1. Import package `scrape_sic`
1. Call `scrape_sic.scrape_sic_sec(output_file)` where `output_file` is the name of the csv file to be saved

## License
[Apache License 2.0](http://choosealicense.com/licenses/apache-2.0/)
