# This code takes the projects file and makes a pd.DataFrame from it

import json
import pandas as pd

with open('processed_data/2015-01.json', 'r') as data_file:
    data = json.load(data_file)

df_raw = pd.DataFrame.from_dict(data, orient='index') # make a DataFrame
df = pd.DataFrame.from_dict(df_raw['languages'].to_dict(), orient='index').sort_index(axis=1)

# df['sum bits'] = df['languages'].apply(lambda x: sum(x.values())) different method
df['Sum_Bit'] = df.sum(axis=1) # sum all bits of a project

# Normalize the bits for all languages
# norm_df = df.apply(lambda series: series[:-1]/series['Sum_Bit'], axis=1)
norm_df = df.div(df['Sum_Bit'], axis=0).drop(['Sum_Bit'], axis=1)

# Add the issue count
norm_df['Count'] = df_raw['count']
print(norm_df)
