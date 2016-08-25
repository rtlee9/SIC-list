import os
from .context import scrape_sic_osha as scrape


class TestClass:

    def test_unamed(self):
        file_list = scrape.save_all_majors()
        assert all([os.path.isfile(s) for s in file_list])
        assert all([s.split('_')[0] == 'Maj' for s in file_list])
        assert all([os.remove(s) is None for s in file_list])

    def test_named(self):
        file_list = scrape.save_all_majors('test_')
        assert all([s.split('_')[0] == 'test' for s in file_list])
        assert all([os.path.isfile(s) for s in file_list])
        assert all([os.remove(s) is None for s in file_list])
