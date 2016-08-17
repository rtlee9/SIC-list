from bs4 import BeautifulSoup
import urllib2
from collections import namedtuple

ind_group = namedtuple('ind_group', [
    'full_desc', 'parent_desc', 'link'])


def clean_desc(full_desc):
    full_desc_split = full_desc.split(': ')
    code_split = full_desc_split.split(' ')
    code = code_split[len(code_split) - 1]
    code_type = ' '.join(code_split[len(code_split) - 1])
    return [code, code_type]


def get_divisions():

    # Setup
    url = 'https://www.osha.gov/pls/imis/sic_manual.html'
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html5lib')

    # Find content
    container = soup.select('div#maincontain')[0]
    master_list = container.find('div').find('ol')
    all_links = master_list.find_all('a')

    # Store cleaned aref elements
    divisions = []
    for i in range(1, len(all_links) - 1):
        l = all_links[i]
        full_desc = str(l.contents[0])
        link = l.get('href')

        if (i > 0) & (full_desc.split(' ')[0] == 'Major'):
            prior_desc = str(all_links[i - 1].contents[0])
            if prior_desc.split(' ')[0] == 'Division':
                parent_desc = str(all_links[i - 1].contents[0])
            elif prior_desc.split(' ')[0] == 'Major':
                parent_desc = divisions[i - 2].parent_desc
            else:
                raise ValueError('Unexpected code type')
        else:
            parent_desc = None
        divisions.append(ind_group(full_desc, parent_desc, link))

    return divisions
