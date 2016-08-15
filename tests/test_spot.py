import os
import pandas as pd
from .context import scrape_sic_sec as scrape


class TestClass:

    # Test scrape
    out_name = 'test.csv'
    data = scrape.get_sic_sec(out_name)
    output_read = pd.read_csv(out_name)

    def test_export(self):
        assert len(self.data) - len(self.output_read) == 1

    def test_headers(self):
        assert self.data[0] == ['SIC4', 'AD_office', 'industry_title']

    def test_5122(self):
        assert self.data[300][2] == 'WHOLESALE-DRUGS, '\
                                    'PROPRIETARIES & DRUGGISTS\' SUNDRIES'

    # Clean up
    os.remove(out_name)
