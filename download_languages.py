# This code updates the projects json with languages until it reaches the maximum requests limit.
# We have only 6000 requests per hour (GitHub limits)
import gzip
import json
import sys
from github import Github


# finishes our session for now and updates the file
def finalize():
    print('finished for now... writing data and exiting.')
    with open('processed_data/2015-01.json', 'w') as outfile:
        json.dump(projects, outfile)
    exit()

with open('github/config', 'r') as config_file:
    user, password = config_file.readline().split(' ')
g = Github(user, password)  # insert github user

# read the projects file
with open('processed_data/2015-01.json', 'r') as data_file:
    projects = json.load(data_file)
for repo in projects.keys():
    try:
        print("getting language for {}".format(repo))
        if 'languages' not in projects[repo]:  # get the languages for a project
            projects[repo]['languages'] = g.get_repo(int(repo)).get_languages()
    except Exception as e:
        print(e)
        if 'Maximum number of login attempts exceeded. Please try again later.' in str(e) or 'API rate limit exceeded' in str(e):
            finalize()  # we are out of requests
        else:
            projects[repo]['languages'] = {}  # no languages for this project

finalize()
