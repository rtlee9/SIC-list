from os import path
import pickle
import csv

import config
from type import ind_group
from soup import get_soup


# Parse full OSHA industry description into industry code, type and description
def clean_desc(full_desc):

    # OSHA descriptions are delimated by colons
    full_desc_split = full_desc.split(': ')

    # Check for errors
    if len(full_desc_split) < 2:
        # Check for case when no delimiter found
        raise Exception('No \':\' delimiter found:\n' + full_desc)
    elif len(full_desc_split) > 2:
        # If more than one delimiter found then assume latter delimiters
        # are part of the description
        new_list = []
        new_list.append(full_desc_split[0])
        new_list.append(': '.join(full_desc_split[1:]))
        full_desc_split = new_list

    # Assign full description components
    code_split = full_desc_split[0].split(' ')
    code = code_split[len(code_split) - 1]
    code_type = ' '.join(code_split[:-1])
    code_desc = full_desc_split[1]

    return [code, code_type, code_desc]


# Get the description of an industry group's parent
# OSHA industry decriptions are provided in ordered lists;
# this function identifies the parent industry group based
# on information provided by the groups preceeding it
def get_parent(running_list, i, this_type, parent_type):

    prior = running_list[i - 1]

    if clean_desc(prior.full_desc)[1] == parent_type:
        # If the type of the previous group is a parent type then set the
        # parent description to previous element's description
        parent_desc = str(prior.full_desc)
    elif clean_desc(prior.full_desc)[1] == this_type:
        # Else if the previous group is the more granular type then set the
        # parent description to previous element's parent description
        parent_desc = str(prior.parent_desc)
    else:
        # Otherwise raise a value error
        err_msg = 'Unexpected code type: ' + prior
        raise ValueError(err_msg)

    return parent_desc

# Scrape the list of divisions and major groups from the OSHA website
#   Divisions are the broadest grouping of SIC codes provided by OSHA
#   Major groups are the second broadest grouping of SIC codes provided by OSHA
def get_divisions():

    # Read site
    soup = get_soup(config.OSHA_base_url + 'sic_manual.html')

    # Find content
    container = soup.select('div#maincontain')[0]
    master_list = container.find('div').find('ol')
    all_links = master_list.find_all('a')

    # Store cleaned descriptions, from aref elements
    divisions = []
    for i in range(0, len(all_links)):

        # Store full desciption provided by site and keep the associated link
        l = all_links[i]
        full_desc = str(l.contents[0]).strip().encode("utf-8")
        link = l.get('href').encode("utf-8")

        # Get the description of the parent group
        if (i > 0) & (clean_desc(full_desc)[1] == 'Major Group'):
            parent_desc = get_parent(divisions, i, 'Major Group', 'Division')
        else:
            parent_desc = str(None)

        # Add to running list of named tuples
        divisions.append(ind_group(full_desc, parent_desc, link))

    return divisions


# Scrape the list of major groups, industry groups and SIC four-digit SIC codes
# from the OSHA website
#   Major groups are the second broadest grouping of SIC codes provided by OSHA
#   Industry groups are the third broadest grouping (least granular) of SIC
#   codes provided by OSHA
def get_major(url_ext):

    # Read site
    soup = get_soup(config.OSHA_base_url + url_ext)

    # Isolate relevant content
    container = soup.select('div#maincontain')[0]
    groups = container.find_all(['strong', 'li'])
    major_desc = str(container.find_all('h2')[0].contents[0])

    # Store cleaned descriptions, from strong and li elements
    majors = []
    for i in range(0, len(groups)):

        g = groups[i]

        # Get description of SIC and industry groups
        if g.name == 'strong':
            # Get industry group descriptions
            full_desc = g.contents[0].strip().encode("utf-8")
            link = None
        elif g.name == 'li':
            # Get four-digit SIC code descriptions
            full_desc = 'SIC4 ' + str(g.contents[0]).strip() + \
                ': ' + str(g.contents[1].contents[0]).strip()
            link = g.contents[1].get('href').encode("utf-8")
        else:
            # Otherwise raise a value error
            raise ValueError('Unexpected element type: ' + g.name)

        # Get the description of the parent group
        if (i > 0) & (clean_desc(full_desc)[1] == 'SIC4'):
            parent_desc = get_parent(majors, i, 'SIC4', 'Industry Group')
        else:
            parent_desc = major_desc

        # Add to running list of named tuples
        majors.append(ind_group(full_desc, parent_desc, link))

    return majors


# Get and append descriptions for SIC codes and industry groups for all
# major groups; links to the individual pages can be found from the manual
# landing page
def get_all_majors():

    # Get a links to more granular descriptions from the landing page
    divisions = get_divisions()

    # Find the children descriptions for each major group
    majors_all = []
    for d in divisions:
        desc = clean_desc(d.full_desc)
        if desc[1] == 'Major Group':
            majors = get_major(d.link)
            majors_all.extend(majors)

    # Return a single running list of named tuples
    return majors_all


# Save a pickled copy of the division (high-level) descriptions,
# and return the raw data
def save_divisions(fname='divisions_raw.pkl'):
    divisions = get_divisions()
    with open(fname, 'w') as f:
        pickle.dump(divisions, f)
    return divisions


# Save a pickled copy of the descriptions for children of a given major group;
# major group must be identified by a url, and return the raw data
def save_majors(url, fname='majors_raw.pkl'):
    majors = get_major(url)
    with open(fname, 'w') as f:
        pickle.dump(majors, f)
    return majors


# Save pickled copies of the descriptions for children of all major groups,
# and return a list of all saved files
def save_all_majors(fname_prepend='Maj_'):

    # Get a links to more granular descriptions from the landing page
    divisions = get_divisions()

    # Find and save the children descriptions for each major group
    file_list = []
    for d in divisions:
        desc = clean_desc(d.full_desc)
        if desc[1] == 'Major Group':
            filename = fname_prepend + desc[0] + '.pkl'
            save_majors(d.link, fname=filename)
            file_list.append(filename)

    # Return list of names of saved files
    return file_list


# Helper function: return a list of the industry code and description,
# given a full description
def clean_out(unit):
    fdesc = clean_desc(unit.full_desc)
    cd = fdesc[0]
    desc = fdesc[2]
    return [cd, desc]


# Combine all datasets into a single, wide data table
def combine_sic_all(divisions, majors_all):

    # Create combined table, long format
    combined = list(majors_all)
    combined.extend(divisions)

    # Save to dictionary for future lookup
    d_combined = {c.full_desc: c for c in combined}

    # Reshape table: long to wide
    wide = []
    for sic in combined:
        sic_fdesc = clean_desc(sic.full_desc)
        if sic_fdesc[1] == 'SIC4':

            # Find parents
            ind = d_combined[sic.parent_desc.strip()]
            maj = d_combined[ind.parent_desc.strip()]
            div = d_combined[maj.parent_desc.strip()]

            # Store cleaned codes and descriptions
            cols = clean_out(sic)
            cols.extend(clean_out(ind))
            cols.extend(clean_out(maj))
            cols.extend(clean_out(div))

            wide.append(cols)

    return wide


# Wrapper for combine_sic_all function -- save wide dataset to local machine
def get_sic_all(div_fname=None, maj_fnames=None, out_fname='osha_combined'):

    # Get divisions if file not provided
    if div_fname:
        with open(div_fname, 'rb') as f:
            divisions = pickle.load(f)
    else:
        divisions = get_divisions()

    # Get major lists if files not provided
    if maj_fnames:
        majors_all = []
        for f in maj_fnames:
            with open(f, 'rb') as f:
                majors_all.extend(pickle.load(f))
    else:
        majors_all = get_all_majors()

    wide = combine_sic_all(divisions, majors_all)

    # Save data in pickled format
    with open(out_fname + '.pkl', 'w') as f:
        pickle.dump(wide, f)

    # Save data in csv format
    with open(out_fname + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(config.OSHA_columns)
        writer.writerows(wide)

    # Return success confirmation
    return True

if __name__ == '__main__':
    get_sic_all(out_fname=path.join(config.path_data, 'osha_combined'))
