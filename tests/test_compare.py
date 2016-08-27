from __future__ import division
from .context import scrape_sic_osha as scrape_osha
from .context import scrape_sic_sec as scrape_sec
import pandas as pd
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Read OSHA data
osha_fname = 'osha_combined.csv'
try:
    osha = pd.read_csv(osha_fname)
except IOError:
    scrape_osha.get_sic_all()
    osha = pd.read_csv(osha_fname)
len(osha)

# Read SEC data
sec_fname = 'sec_combined.csv'
try:
    sec = pd.read_csv(sec_fname)
except IOError:
    scrape_sec.save_sic_sec()
    sec = pd.read_csv(sec_fname)
len(sec)

# Read benchmark data
benchmark = pd.read_csv('tests/ref_list.csv')
benchmark.columns = ['SIC4_cd', 'SIC4_desciption']
benchmark_osha = pd.read_csv('tests/ref_osha_combined.csv')
benchmark_sec = pd.read_csv('tests/ref_sec_combined.csv')


# Test get_divisions()
class TestClass:

    def test_compare_osha_sec(self):

        # Merge OSHA and SEC data
        inner = osha.merge(sec, how='inner', on='SIC4_cd')
        len(inner)
        osha_desc = list(inner.SIC4_desc.str.lower().str.strip())
        sec_desc = list(inner.industry_title.str.lower().str.strip())

        match = []
        for i in range(0, len(inner)):
            match_ind = sec_desc[i] == osha_desc[i]
            if not(match_ind):

                tokens_taged = nltk.pos_tag(nltk.word_tokenize(osha_desc[i]))
                sec_words = [word[0] for word in nltk.pos_tag(
                    nltk.word_tokenize(sec_desc[i]))]

                word_matches = [word[0] in sec_words for word in tokens_taged
                                if word[1] != 'CC']
                match_rate = sum(word_matches) / len(word_matches)
                if match_rate > 0.3:
                    match_ind = True
            match.append(match_ind)

        assert sum(match) / len(inner) > .98

    def test_compare_osha_benchmark(self):

        # Merge OSHA and benchmark data
        inner = osha.merge(benchmark, how='inner', on='SIC4_cd')
        len(inner)
        osha_desc = list(inner.SIC4_desc.str.lower().str.strip())
        benchmark_desc = list(inner.SIC4_desciption.str.lower().str.strip())

        match = []
        for i in range(0, len(inner)):
            match_ind = benchmark_desc[i] == osha_desc[i]
            if not(match_ind):

                tokens_taged = nltk.pos_tag(
                    nltk.word_tokenize(benchmark_desc[i]))
                osha_words = [word[0] for word in nltk.pos_tag(
                    nltk.word_tokenize(osha_desc[i]))]

                word_matches = [word[0] in osha_words for word
                                in tokens_taged if word[1] != 'CC']
                match_rate = sum(word_matches) / len(word_matches)
                if match_rate > 0.3:
                    match_ind = True
            match.append(match_ind)

        assert sum(match) / len(inner) > .98

    def test_compare_orig(self):
        assert osha.equals(benchmark_osha)
        assert sec.equals(benchmark_sec)
