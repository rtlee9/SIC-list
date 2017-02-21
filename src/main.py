from os import path

import config
import scrape_sic_osha as osha
import scrape_sic_sec as sec

osha.get_sic_all(out_fname=path.join(config.path_data, 'osha_combined'))
sec.save_sic_sec(path.join(config.path_data, 'sec_combined.csv'))
