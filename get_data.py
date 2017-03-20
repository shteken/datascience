from github import Github
import json

with open('github/config', 'r') as config_file:
    user, password = config_file.readline().split(' ')
g = Github(user, password)  # insert github user

raw_data = {}  # our data
last_repo_id = None

try:
    with open('status', 'r') as inputfile:
        since_id = int(inputfile.readline())  # check if we already started the programm
except:
        since_id = 28677545  # first repository in 2015
try:
    for repo in g.get_repos(since=since_id):
        raw_data[repo.full_name] = {
            'languages': repo.get_languages(),
            'issue_url': repo.get_issues(state='all')._getLastPageUrl(),  # we need this URL for future analysis
            'id': repo.id,
            'created_at': repo.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(repo.id)
        last_repo_id = repo.id
except Exception as err:
    print(err)
finally:
    with open('output{}.json'.format(since_id), 'w') as outfile:
        json.dump(raw_data, outfile)  # save the data we collected
    with open('status', 'w') as outfile:
        outfile.write(str(last_repo_id))  # save our last seen repository
