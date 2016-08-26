from bs4 import BeautifulSoup
import urllib2
from collections import namedtuple
import pickle
import csv

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


def get_all_majors():
    divisions = get_divisions()
    majors_all = []
    for d in divisions:
        desc = clean_desc(d.full_desc)
        if desc[1] == 'Major Group':
            majors = get_major(d.link)
            majors_all.extend(majors)
    return majors_all


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


def get_sic_all(div_fname=None, maj_fnames=None, out_fname='osha_combined'):

    # Get divisions if file not provided
    if div_fname:
        divisions = pickle.load(open(div_fname, 'rb'))
    else:
        divisions = get_divisions()

    # Get major lists if files not provided
    if maj_fnames:
        majors_all = []
        for f in maj_fnames:
            majors_all.extend(pickle.load(open(f, 'rb')))
    else:
        majors_all = get_all_majors()

    combined = list(majors_all)
    combined.extend(divisions)
    d_combined = {c.full_desc: c for c in combined}

    sic = [c for c in combined if clean_desc(c.full_desc)[1] == 'SIC4']
    wide = []
    for sic in combined:
        sic_fdesc = clean_desc(sic.full_desc)
        if sic_fdesc[1] == 'SIC4':

            # Clean SIC4
            SIC4_cd = sic_fdesc[0]
            SIC4_desc = sic_fdesc[2]

            # Clean industry
            ind = d_combined[sic.parent_desc.strip()]
            ind_fdesc = clean_desc(ind.full_desc)
            ind_cd = ind_fdesc[0]
            ind_desc = ind_fdesc[2]

            # Clean major
            maj = d_combined[ind.parent_desc.strip()]
            maj_fdesc = clean_desc(maj.full_desc)
            maj_cd = maj_fdesc[0]
            maj_desc = maj_fdesc[2]

            # Clean division
            div = d_combined[maj.parent_desc.strip()]
            div_fdesc = clean_desc(div.full_desc)
            div_cd = div_fdesc[0]
            div_desc = div_fdesc[2]

            wide.append((SIC4_cd, SIC4_desc, ind_cd, ind_desc,
                         maj_cd, maj_desc, div_cd, div_desc))

            # Save data
            with open(out_fname + '.pkl', 'w') as f:
                pickle.dump(wide, f)

            with open(out_fname + '.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow((
                    'SIC4_cd', 'SIC4_desc', 'ind_cd', 'ind_desc',
                    'maj_cd', 'maj_desc', 'div_cd', 'div_desc'))
                writer.writerows(wide)

    return True

get_sic_all()
