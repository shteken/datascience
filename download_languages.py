# usage: python github/download_relevant_data.py <day> - parse all issue of given day

import gzip
import json
import sys
from github import Github


def finalize():
    print('finished for now... writing data and exiting.')
    with open('processed_data/2015-01.json', 'w') as outfile:
        json.dump(projects, outfile)
    exit()

with open('github/config', 'r') as config_file:
    user, password = config_file.readline().split(' ')
g = Github(user, password)  # insert github user

with open('processed_data/2015-01.json', 'r') as data_file:
    projects = json.load(data_file)
for repo in projects.keys():
    try:
        print("getting language for {}".format(repo))
        if 'languages' not in projects[repo]:
            projects[repo]['languages'] = g.get_repo(int(repo)).get_languages()
    except Exception as e:
        if str(e)[0:3] == '403':
            finalize()
        else:
            projects[repo]['languages'] = {}
        print(e)

finalize()
