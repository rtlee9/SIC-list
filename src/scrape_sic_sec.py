from os import path
import csv
import warnings

import config
from soup import get_soup


def get_sic_sec():
    """Scrape SIC codes from SEC website
    """

    # Setup
    soup = get_soup(config.SEC_base_url)
    table = soup.find_all('table')[3]

    # Convert HTML to nested list
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip().replace('  ', ' ') for ele in cols]
        if (len(cols) > 1):
            data.append([ele.encode('utf-8') for ele in cols if ele])

    # Clean headers
    if data[0] != config.SEC_expected_columns:
        warnings.warn(
            'Warning: column names have changed in URL ' + config.SEC_base_url)
    data[0] = config.SEC_columns

    return data


def save_sic_sec(out_fname='sec_combined.csv'):
    """Save scraped SIC codes to local machine
    """
    data = get_sic_sec()
    with open(out_fname, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(data)
    return data

if __name__ == '__main__':
    save_sic_sec(path.join(config.path_data, 'sec_combined.csv'))
