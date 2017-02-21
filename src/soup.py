from bs4 import BeautifulSoup
import urllib2

import config

def get_soup(url):
    """Return a soup object for scraping based on provided URL
    """
    page = urllib2.urlopen(url).read()
    return BeautifulSoup(page, config.html_lib)
