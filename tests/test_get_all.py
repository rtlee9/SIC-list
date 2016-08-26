from .context import scrape_sic_osha as scrape
import pandas as pd
import pickle


# Test get_divisions()
class TestClass:

    filename = 'test'
    success = scrape.get_sic_all(out_fname=filename)
    with open(filename + '.pkl', 'rb') as f:
        out_pick = pickle.load(f)
    out_csv = pd.read_csv(filename + '.csv')

    def test_script_success(self):
        assert self.success

    def files_found(self):
        assert self.out_pick is not None
        assert self.out_csv is not None

    def test_equal_len(self):
        assert len(self.out_pick) == len(self.out_csv)

    def test_first(self):

        assert self.out_pick[0] == [
            '0111',
            'Wheat',
            '011',
            'Cash Grains',
            '01',
            'Agricultural Production Crops',
            'A',
            'Agriculture, Forestry, And Fishing']

        assert list(self.out_csv.iloc[0]) == [
            111,
            'Wheat',
            11,
            'Cash Grains',
            1,
            'Agricultural Production Crops',
            'A',
            'Agriculture, Forestry, And Fishing']

    def test_5812(self):

        assert self.out_pick[749] == [
            '5812',
            'Eating Places',
            '581',
            'Eating And Drinking Places',
            '58',
            'Eating And Drinking Places',
            'G',
            'Retail Trade']

        assert list(self.out_csv[self.out_csv.SIC4_cd == 5812].iloc[0]) == [
            5812,
            'Eating Places',
            581,
            'Eating And Drinking Places',
            58,
            'Eating And Drinking Places',
            'G',
            'Retail Trade']

    def test_last(self):

        assert self.out_pick[len(self.out_pick) - 1] == [
            '9999',
            'Nonclassifiable Establishments',
            '999',
            'Nonclassifiable Establishments',
            '99',
            'Nonclassifiable Establishments',
            'J',
            'Public Administration']

        assert list(self.out_csv.iloc[len(self.out_csv) - 1]) == [
            9999,
            'Nonclassifiable Establishments',
            999,
            'Nonclassifiable Establishments',
            99,
            'Nonclassifiable Establishments',
            'J',
            'Public Administration']
