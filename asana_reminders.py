import base64
import datetime
import json
import os
import urllib
import urllib2

workspace_id = os.environ['ASANA_WORKSPACE_ID']
thirty_days_ago = datetime.datetime.now() - datetime.timedelta(30)
yesterday = datetime.datetime.now() - datetime.timedelta(1)
modified_since_param = (datetime.datetime.now() - datetime.timedelta(90)).strftime('%Y-%m-%dT00:00:00Z')
basic_auth = 'Basic ' + base64.b64encode(os.environ['ASANA_API_KEY'] + ':')

overdue_comment_text = 'This is a friendly (automated) reminder that this task is past its due date. Please update it so that others have a better sense of when it\'ll will be complete. Thanks!'
stale_comment_text = 'This is a friendly (automated) reminder that this task is getting stale. Please update it if it\'s still prioritized. Or kill it, that\'s cool too. Thanks!'


def data_for(path):
    request = urllib2.Request('https://app.asana.com/api/1.0' + path)
    request.add_header('Authorization', basic_auth)
    return json.load(urllib2.urlopen(request))['data']


def comment_on_task(task_id, comment_text):
    data = urllib.urlencode({'text': comment_text})
    request = urllib2.Request('https://app.asana.com/api/1.0/tasks/' + str(task_id) + '/stories', data)
    request.add_header('Authorization', basic_auth)
    return urllib2.urlopen(request)

users = data_for('/users')

for user in users:
    tasks = data_for('/tasks?workspace=' + workspace_id + '&assignee=' + str(user['id']) + '&modified_since=' + modified_since_param)
    i = 0
    for task in tasks:
        print '{}/{} tasks for {}'.format(i, len(tasks), user['name'])

        task_data = data_for('/tasks/' + str(task['id']))
        stories = data_for('/tasks/' + str(task['id']) + '/stories')

        if 'due_on' in task_data and task_data['due_on'] is not None and task_data['completed'] is not True:
            due_date = datetime.datetime.strptime(task_data['due_on'], '%Y-%m-%d')
            if due_date < yesterday:
                comment_on_task(task['id'], overdue_comment_text)
                print 'overdue; commented'

        if len(stories) > 0 and datetime.datetime.strptime(stories[-1]['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') < thirty_days_ago and task_data['completed'] is not True:
            comment_on_task(task['id'], stale_comment_text)
            print 'stale; commented'

        i += 1

print 'done!'
