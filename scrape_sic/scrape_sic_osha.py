from bs4 import BeautifulSoup
import urllib2
from collections import namedtuple
import pickle

ind_group = namedtuple('ind_group', [
    'full_desc', 'parent_desc', 'link'])


def clean_desc(full_desc):
    full_desc_split = full_desc.split(': ')
    if len(full_desc_split) < 2:
        raise Exception('No \':\' delimiter found:\n' + full_desc)
    elif len(full_desc_split) > 2:
        new_list = []
        new_list.append(full_desc_split[0])
        new_list.append(': '.join(full_desc_split[1:]))
        full_desc_split = new_list

    code_split = full_desc_split[0].split(' ')
    code = code_split[len(code_split) - 1]
    code_type = ' '.join(code_split[:-1])
    code_desc = full_desc_split[1]

    return [code, code_type, code_desc]


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
    for i in range(0, len(all_links)):
        l = all_links[i]
        full_desc = str(l.contents[0]).strip()
        link = l.get('href')

        if (i > 0) & (clean_desc(full_desc)[1] == 'Major Group'):
            prior = divisions[i - 1]
            if clean_desc(prior.full_desc)[1] == 'Division':
                parent_desc = str(prior.full_desc)
            elif clean_desc(prior.full_desc)[1] == 'Major Group':
                parent_desc = str(prior.parent_desc)
            else:
                raise ValueError('Unexpected code type')
        else:
            parent_desc = str(None)
        divisions.append(ind_group(full_desc, parent_desc, link))

    return divisions


def get_major(url_ext):

    # Read site
    url = 'https://www.osha.gov/pls/imis/' + url_ext
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'html5lib')

    # Find content
    container = soup.select('div#maincontain')[0]
    groups = container.find_all(['strong', 'li'])
    major_desc = str(container.find_all('h2')[0].contents[0])

    majors = []
    for i in range(0, len(groups)):

        g = groups[i]

        # Get description
        if g.name == 'strong':
            full_desc = g.contents[0].strip()
            link = None
        elif g.name == 'li':
            full_desc = 'SIC4 ' + str(g.contents[0]).strip() + \
                ': ' + str(g.contents[1].contents[0]).strip()
            link = g.contents[1].get('href')
        else:
            raise ValueError('Unexpected element type: ' + g.name)

        # Get parent element
        if (i > 0) & (clean_desc(full_desc)[1] == 'SIC4'):
            prior = majors[i - 1]
            if clean_desc(prior.full_desc)[1] == 'Industry Group':
                parent_desc = str(prior.full_desc)
            elif clean_desc(prior.full_desc)[1] == 'SIC4':
                parent_desc = str(prior.parent_desc)
            else:
                err_msg = 'Unexpected code type: ' + prior
                raise ValueError(err_msg)
        else:
            parent_desc = major_desc

        # Save to named tuple
        majors.append(ind_group(full_desc, parent_desc, link))

    return majors


def save_divisions(fname='divisions_raw.pkl'):
    divisions = get_divisions()
    with open(fname, 'w') as f:
        pickle.dump(divisions, f)
    return divisions


def save_majors(url, fname='majors_raw.pkl'):
    majors = get_major(url)
    with open(fname, 'w') as f:
        pickle.dump(majors, f)
    return majors


def save_all_majors(fname_prepend='Maj_'):
    divisions = get_divisions()
    file_list = []
    for d in divisions:
        desc = clean_desc(d.full_desc)
        if desc[1] == 'Major Group':
            filename = fname_prepend + desc[0] + '.pkl'
            save_majors(d.link, fname=filename)
            file_list.append(filename)
    return file_list
