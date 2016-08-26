from .context import scrape_sic_osha as scrape


# Test get_divisions()
class TestClass:

    divisions = scrape.get_divisions()
    url = 'sic_manual.display?id=1&tab=group'
    major = scrape.get_major(url)

    def test_forestry(self):
        cleaned = scrape.clean_out(self.divisions[4])
        assert isinstance(cleaned, list)
        assert cleaned[0] == '08'
        assert cleaned[1] == 'Forestry'

    def test_dfirst(self):
        cleaned = scrape.clean_out(self.divisions[0])
        assert isinstance(cleaned, list)
        assert cleaned[0] == 'A'
        assert cleaned[1] == 'Agriculture, Forestry, And Fishing'

    def test_dlast(self):
        cleaned = scrape.clean_out(self.divisions[len(self.divisions) - 1])
        assert isinstance(cleaned, list)
        assert cleaned[0] == '99'
        assert cleaned[1] == 'Nonclassifiable Establishments'

    def test_grapes(self):
        cleaned = scrape.clean_out(self.major[16])
        assert isinstance(cleaned, list)
        assert cleaned[0] == '0172'
        assert cleaned[1] == 'Grapes'

    def test_mfirst(self):
        cleaned = scrape.clean_out(self.major[0])
        assert isinstance(cleaned, list)
        assert cleaned[0] == '011'
        assert cleaned[1] == 'Cash Grains'

    def test_mlast(self):
        cleaned = scrape.clean_out(self.major[len(self.major) - 1])
        assert isinstance(cleaned, list)
        assert cleaned[0] == '0191'
        assert cleaned[1] == 'General Farms, Primarily Crop'
