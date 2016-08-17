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
    for i in range(0, len(all_links) - 1):
        l = all_links[i]
        full_desc = str(l.contents[0])
        link = l.get('href')

        print i
        if (i > 0) & (full_desc.split(' ')[0] == 'Major'):
            prior = divisions[i - 1]
            print prior
            if prior.full_desc.split(' ')[0] == 'Division':
                parent_desc = str(prior.full_desc)
            elif prior.full_desc.split(' ')[0] == 'Major':
                parent_desc = str(prior.parent_desc)
            else:
                raise ValueError('Unexpected code type')
        else:
            parent_desc = str(None)
        divisions.append(ind_group(full_desc, parent_desc, link))

    return divisions


def get_major(relative_links=False):

    # Setup
    base_url = 'https://www.osha.gov/pls/imis/'
    url_ext = 'https://www.osha.gov/pls/imis/sic_manual.display?id=1&tab=group'
    if relative_links:
        url = base_url + url_ext
    elif ~relative_links:
        url = url_ext
    else:
        raise ValueError('Unexpcted data type relative_links')

    # Read site
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html5lib')

    # Find content
    container = soup.select('div#maincontain')[0]
    groups = container.find_all(['strong', 'li'])

    majors = []
    for i in range(0, len(groups) - 1):

        g = groups[i]

        # Get description
        if g.name == 'strong':
            full_desc = g.contents[0]
            link = None
        elif g.name == 'li':
            full_desc = 'SIC4 ' + str(g.contents[0]).strip() + \
                ': ' + str(g.contents[1].contents[0])
            link = g.contents[1].get('href')
        else:
            raise ValueError('Unexpected element type: ' + g.name)

        # Get parent element
        if (i > 0) & (full_desc.split(' ')[0] == 'SIC4'):
            prior = majors[i - 1]
            if prior.full_desc.split(' ')[0] == 'Industry':
                parent_desc = str(prior.full_desc)
            elif prior.full_desc.split(' ')[0] == 'SIC4':
                parent_desc = str(prior.parent_desc)
            else:
                err_msg = 'Unexpected code type: ' + prior
                raise ValueError(err_msg)
        else:
            parent_desc = str(None)

        # Save to named tuple
        majors.append(ind_group(full_desc, parent_desc, link))

    return majors
