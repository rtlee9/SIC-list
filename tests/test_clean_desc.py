import pytest
from .context import scrape_sic_osha as scrape


# Test clean_desc()
class TestClass:

    def test_none(self):
        with pytest.raises(AttributeError):
            scrape.clean_desc(None)

    def test_nospace(self):
        with pytest.raises(Exception):
            scrape.clean_desc('thistaghasnospace')

    def test_multcol(self):
        mult_str = 'Industry Group 271: Newspapers: Publishing, ' + \
            'Or Publishing And Printing'
        with pytest.warns(UserWarning):
            clean = scrape.clean_desc(mult_str)
        assert clean[0] == '271'
        assert clean[1] == 'Industry Group'
        assert clean[2] == 'Newspapers: Publishing, Or Publishing And Printing'

    def test_division(self):
        clean = scrape.clean_desc(
            'Division I: Services')
        assert clean[0] == 'I'
        assert clean[1] == 'Division'
        assert clean[2] == 'Services'

    def test_major(self):
        clean = scrape.clean_desc(
            'Major Group 86: Membership Organizations')
        assert clean[0] == '86'
        assert clean[1] == 'Major Group'
        assert clean[2] == 'Membership Organizations'

    def test_industry(self):
        clean = scrape.clean_desc(
            'Industry Group 019: General Farms, Primarily Crop')
        assert clean[0] == '019'
        assert clean[1] == 'Industry Group'
        assert clean[2] == 'General Farms, Primarily Crop'
