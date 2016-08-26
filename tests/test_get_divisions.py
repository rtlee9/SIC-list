from .context import scrape_sic_osha as scrape


# Test get_divisions()
class TestClass:

    divisions = scrape.get_divisions()

    def test_len(self):
        assert len(self.divisions) > 1

    def test_forestry(self):
        assert self.divisions[4].full_desc == \
            'Major Group 08: Forestry'
        assert self.divisions[4].parent_desc == \
            'Division A: Agriculture, Forestry, And Fishing'

    def test_first(self):
        assert self.divisions[0].full_desc == \
            'Division A: Agriculture, Forestry, And Fishing'
        assert self.divisions[0].parent_desc == \
            'None'

    def test_last(self):
        assert self.divisions[len(self.divisions) - 1].full_desc == \
            'Major Group 99: Nonclassifiable Establishments'
        assert self.divisions[len(self.divisions) - 1].parent_desc == \
            'Division J: Public Administration'
