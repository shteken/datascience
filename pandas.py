import json
import pandas as pd

with open('processed_data/2015-01.json', 'r') as data_file:
    data = json.load(data_file)
print(data)

df_raw = pd.DataFrame.from_dict(data, orient='index').dropna()
print(df_raw)
# df['sum bits'] = df['languages'].apply(lambda x: sum(x.values()))
print(df_raw['languages'].to_dict())
df = pd.DataFrame.from_dict(df_raw['languages'].to_dict(), orient='index').sort_index(axis=1)
df['Sum_Bit'] = df.sum(axis=1)
# norm_df = df.apply(lambda series: series[:-1]/series['Sum_Bit'], axis=1)
norm_df = df.div(df['Sum_Bit'], axis=0).drop(['Sum_Bit'], axis=1)
norm_df['Count'] = df_raw['count']
print(norm_df)
