# extract projects and issues_count from all events
import gzip
import json

projects = {}
for day in range(1,32):
    if day < 10:
        day = '0{}'.format(day)
    print('Start day {}'.format(day))
    for hour in range(0, 24):
        with gzip.open('data/2015-01-{}-{}.json.gz'.format(day, hour), 'rb') as f:
            for line in iter(f.readline, b''):
                event = json.loads(line)
                if (event['type'] == 'IssuesEvent') and (event['payload']['action'] == 'opened'):
                    if event['repo']['id'] not in projects:
                        projects[event['repo']['id']] = {'count': 1}
                    else:
                        projects[event['repo']['id']]['count'] += 1
print('done with issues')

with open('processed_data/2015-01.json', 'w') as outfile:
    json.dump(projects, outfile)
