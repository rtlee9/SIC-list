# Import packages
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(
    'scrape_sic'))
import scrape_sic_sec

# Test scrape
fname = 'test.csv'
test_scrape = scrape_sic_sec.save_sic_sec(fname)
output_read = pd.read_csv(fname)
print len(test_scrape) - len(output_read.index)

# Convert to dataframe
df = pd.DataFrame(test_scrape)
df.columns = df.iloc[0]
print list(df.columns.values)

# Clean up
os.remove('test.csv')
print 'Test completed\n'
