# Import packages
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(
    '/Users/Ryan/Github/SIC-list/scrape_sic'))
import scrape_sic_sec

# Test scrape
test_scrape = scrape_sic_sec.get_sic_sec('test.csv')
output_read = pd.read_csv('test.csv')
print len(test_scrape) - len(output_read.index)

# Convert to dataframe
df = pd.DataFrame(test_scrape)
df.columns = df.iloc[0]
print list(df.columns.values)

# Clean up
os.remove('test.csv')
print 'Test completed\n'
