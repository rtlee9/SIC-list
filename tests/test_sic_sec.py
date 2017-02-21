# Test SEC scraping functions
from os import remove, path
import pandas as pd

from .context import scrape_sic_sec as scrape
from .context import path_test


class TestClass:

    out_name = path.join(path_test, 'test.csv')
    data = scrape.save_sic_sec(out_name)
    output_read = pd.read_csv(out_name)
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]

    def test_export(self):
        assert len(self.data) - len(self.output_read) == 1

    def test_headers(self):
        assert self.data[0] == ['SIC4_cd', 'AD_office', 'industry_title']

    def test_df_headers(self):
        assert list(self.df.columns.values) == \
            ['SIC4_cd', 'AD_office', 'industry_title']

    def test_5122(self):
        assert self.df[pd.to_numeric(
            self.df.SIC4_cd, errors='coerce') == 8071].\
            industry_title.iloc[0] == 'SERVICES-MEDICAL LABORATORIES'

    def test_0800(self):
        assert self.df[pd.to_numeric(
            self.df.SIC4_cd, errors='coerce') == 800].\
            industry_title.iloc[0] == 'FORESTRY'

    def test_3540(self):
        assert self.df[pd.to_numeric(
            self.df.SIC4_cd, errors='coerce') == 3540].\
            industry_title.iloc[0] == 'METALWORKG MACHINERY & EQUIPMENT'

    # Clean up
    remove(out_name)
