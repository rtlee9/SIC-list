from bs4 import BeautifulSoup
import urllib2
import csv
import warnings


def get_sic_sec():

    # Setup
    url = 'https://www.sec.gov/info/edgar/siccodes.htm'
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'lxml')
    table = soup.find_all('table')[3]

    # Convert HTML to nested list
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip().replace('  ', ' ') for ele in cols]
        if (len(cols) > 1):
            data.append([ele.encode('utf-8') for ele in cols if ele])

    # Clean headers
    if data[0] != ['SICCode', 'A/D \xc2\xa0Office', 'Industry Title']:
        warnings.warn('Warning: column names have changed in ULR ' + url)
    data[0] = ['SIC4', 'AD_office', 'industry_title']

    return data


def save_sic_sec(out_fname):
    data = get_sic_sec()
    with open(out_fname, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(data)
    return data
