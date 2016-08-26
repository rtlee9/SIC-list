from .context import scrape_sic_osha as scrape


# Test get_divisions()
class TestClass:

    divisions = scrape.get_divisions()
    url = 'sic_manual.display?id=1&tab=group'
    major = scrape.get_major(url)

    def test_forestry(self):
        test_unit = scrape.ind_group(
            full_desc='Major Group 08: Forestry',
            parent_desc='Division A: Agriculture, Forestry, And Fishing',
            link='sic_manual.display?id=4&tab=group')
        cleaned = scrape.clean_out(test_unit)
        assert isinstance(cleaned, list)
        assert cleaned[0] == '08'
        assert cleaned[1] == 'Forestry'

    def test_dfirst(self):
        test_unit = scrape.ind_group(
            full_desc='Division A: Agriculture, Forestry, And Fishing',
            parent_desc='None', link='sic_manual.display?id=1&tab=division')
        cleaned = scrape.clean_out(test_unit)
        assert isinstance(cleaned, list)
        assert cleaned[0] == 'A'
        assert cleaned[1] == 'Agriculture, Forestry, And Fishing'

    def test_dlast(self):
        test_unit = scrape.ind_group(
            full_desc='Major Group 99: Nonclassifiable Establishments',
            parent_desc='Division J: Public Administration',
            link='sic_manual.display?id=82&tab=group')
        cleaned = scrape.clean_out(test_unit)
        assert isinstance(cleaned, list)
        assert cleaned[0] == '99'
        assert cleaned[1] == 'Nonclassifiable Establishments'

    def test_grapes(self):
        test_unit = scrape.ind_group(
            full_desc='SIC4 0172: Grapes',
            parent_desc='Industry Group 017: Fruits And Tree Nuts',
            link='sic_manual.display?id=322&tab=description')
        cleaned = scrape.clean_out(test_unit)
        assert isinstance(cleaned, list)
        assert cleaned[0] == '0172'
        assert cleaned[1] == 'Grapes'

    def test_mfirst(self):
        test_unit = scrape.ind_group(
            full_desc='Industry Group 011: Cash Grains',
            parent_desc='Major Group 01: Agricultural Production Crops',
            link=None)
        cleaned = scrape.clean_out(test_unit)
        assert isinstance(cleaned, list)
        assert cleaned[0] == '011'
        assert cleaned[1] == 'Cash Grains'

    def test_mlast(self):
        test_unit = scrape.ind_group(
            full_desc='SIC4 0191: General Farms, Primarily Crop',
            parent_desc='Industry Group 019: General Farms, Primarily Crop',
            link='sic_manual.display?id=329&tab=description')
        cleaned = scrape.clean_out(test_unit)
        assert isinstance(cleaned, list)
        assert cleaned[0] == '0191'
        assert cleaned[1] == 'General Farms, Primarily Crop'
