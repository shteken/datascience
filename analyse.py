# This code takes the projects file and makes a pd.DataFrame from it

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

with open('processed_data/2015-01.json', 'r') as data_file:
    data = json.load(data_file)

df_raw = pd.DataFrame.from_dict(data, orient='index') # make a DataFrame
df = pd.DataFrame.from_dict(df_raw['languages'].to_dict(), orient='index').sort_index(axis=1)

# df['sum bits'] = df['languages'].apply(lambda x: sum(x.values())) different method
df['Sum_Bit'] = df.sum(axis=1) # sum all bits of a project

# Normalize the bits for all languages
# norm_df = df.apply(lambda series: series[:-1]/series['Sum_Bit'], axis=1)
norm_df = 100*df.div(df['Sum_Bit'], axis=0).drop(['Sum_Bit'], axis=1)

# Add the issue count
norm_df['Count'] = df_raw['count']
norm_df.loc['Popularity'] = norm_df.count()
norm_df.sort_values(by='Popularity', axis=1, inplace=True, ascending=False)
norm_df.drop(['Popularity'], inplace=True)
# print(list(norm_df.columns))
# print(norm_df.iloc[:, :10])

#df_piechart = norm_df.multiply(norm_df['Count'], axis=1)
issues_contrib = norm_df.apply(lambda x: x['Count']*x, axis=1).mean()
# print(issues_contrib)


plt.style.use('seaborn-colorblind')
labels = list(map(lambda p: '{}%-{}%'.format(int(p[0]), int(p[1])), zip(np.linspace(0, 90, 10), np.linspace(10, 100, 10))))

def group_language_data(language):
    view = norm_df[[language, 'Count']].dropna() #.groupby(by=['Python'], by=binner).mean('Count')
    groups = view.groupby(pd.cut(view[language], np.linspace(0, 100, 11)))
    return groups.mean()['Count']


def python_ruby():
    python = group_language_data('Python')
    ruby = group_language_data('Ruby')
    plt.figure()
    plt.xticks(np.arange(10), labels, rotation=45)
    plt.bar(left=np.arange(10)-0.175, height=python.values, width=0.35, label='Python', color='#92e5e1')
    plt.bar(left=np.arange(10)+0.175, height=ruby.values, width=0.35, label='Ruby', color='#e592b3')
    plt.ylim(bottom=0, top=25)
    plt.legend()
    plt.ylabel('Number of Issues per Repository')
    plt.xlabel('Percentage of Language in Repository')
    plt.tight_layout()
    plt.savefig('python-ruby-bars.png', transparent=True)
    plt.figure()
    plt.axes(aspect=1)
    plt.pie(x=issues_contrib[['Python', 'Ruby']], colors=['#92e5e1','#e592b3'], labels=['Python', 'Ruby'], autopct='%1.1f%%')
    plt.savefig('python-ruby-pie.png', transparent=True)

def java_csharp_objectivec():
    java = group_language_data('Java')
    csharp = group_language_data('C#')
    objectivec = group_language_data('Objective-C')
    plt.figure()
    plt.xticks(np.arange(10), labels, rotation=45)
    plt.bar(left=np.arange(10)-0.2, height=java.values, width=0.2, label='Java', color='#c592e5')
    plt.bar(left=np.arange(10), height=objectivec.values, width=0.2, label='Objective-C', color='#92e5e1')
    plt.bar(left=np.arange(10)+0.2, height=csharp.values, width=0.2, label='C#', color='#e592b3')
    plt.ylim(bottom=0, top=25)
    plt.legend()
    plt.ylabel('Number of Issues per Repository')
    plt.xlabel('Percentage of Language in Repository')
    plt.tight_layout()
    plt.savefig('java-csharp-objectivec-bar.png', transparent=True)
    plt.figure()
    plt.axes(aspect=1)
    plt.pie(x=issues_contrib[['Java', 'C#', 'Objective-C']], colors=['#c592e5', '#e592b3', '#92e5e1'], labels=['Java', 'C#', 'Objective-C'], autopct='%1.1f%%')
    plt.savefig('java-csharp-objectivec-pie.png', transparent=True)

python_ruby()
java_csharp_objectivec()
