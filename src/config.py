from os import path

path_src = path.dirname(path.abspath(__file__))
path_base = path.dirname(path_src)
path_data = path.join(path_base, 'data')

html_lib = 'html5lib'
OSHA_base_url = 'https://www.osha.gov/pls/imis/'
OSHA_columns = (
    'SIC4_cd', 'SIC4_desc', 'ind_cd', 'ind_desc',
    'maj_cd', 'maj_desc', 'div_cd', 'div_desc')

SEC_base_url = 'https://www.sec.gov/info/edgar/siccodes.htm'
SEC_expected_columns = ['SICCode', 'A/D \xc2\xa0Office', 'Industry Title']
SEC_columns = ['SIC4_cd', 'AD_office', 'industry_title']
