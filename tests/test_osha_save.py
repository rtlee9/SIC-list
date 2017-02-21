# Test save_divisions() and save_majors() functions
from os import path, remove

from .context import scrape_sic_osha as scrape
from .context import path_test


class TestClass:

    def test_save_div(self):
        test_fname = path.join(path_test, 'test_div.pkl')
        assert scrape.save_divisions(test_fname)
        assert path.isfile(test_fname)
        remove(test_fname)
        assert not(path.isfile(test_fname))

    def test_save_maj(self):
        url = 'sic_manual.display?id=1&tab=group'
        test_fname = path.join(path_test, 'test_maj.pkl')
        assert scrape.save_majors(url, test_fname)
        assert path.isfile(test_fname)
        remove(test_fname)
        assert not(path.isfile(test_fname))
