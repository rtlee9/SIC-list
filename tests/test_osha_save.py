from .context import scrape_sic_osha as scrape
import os


class TestClass:

    def test_save_div(self):
        assert scrape.save_divisions()
        assert os.path.isfile('divisions_raw.pkl')
        test_fname = 'test_div.pkl'
        assert scrape.save_divisions(test_fname)
        assert os.path.isfile(test_fname)
        os.remove(test_fname)
        assert not(os.path.isfile(test_fname))

    def test_save_maj(self):
        url = 'https://www.osha.gov/pls/imis/sic_manual.display?id=1&tab=group'
        assert scrape.save_majors(url)
        assert os.path.isfile('majors_raw.pkl')
        test_fname = 'test_maj.pkl'
        assert scrape.save_majors(url, test_fname)
        assert os.path.isfile(test_fname)
        os.remove(test_fname)
        assert not(os.path.isfile(test_fname))
