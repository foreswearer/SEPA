import pandas as pd

dfp = pd.read_csv('../../data/properties/properties.csv', low_memory=False)

dfs = pd.read_csv('../../data/stations/stations.csv')

result = pd.merge(dfp, dfs, on='postcode')

result.to_clipboard()

