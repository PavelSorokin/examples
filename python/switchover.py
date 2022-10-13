import requests
import sys
import json
from datetime import datetime, timedelta


def is_leader():
    url_address = 'test-patroni-n3.isb:8008'
    health = requests.get('http://'+url_address+'/cluster')
    health_json = json.dumps(health.json())
    patroni = json.loads(health_json)
    for node in patroni['members']:
        if node['role'] == 'leader':
            return node['name']

time = datetime.now().astimezone()+timedelta(seconds=20)
time_iso = time.replace(microsecond=0).isoformat()
parser = sys.argv
node_leader = is_leader()
node_candidate = 'node3'
#if node_leader == node_candidate:
#    print(node_leader + ' is leader, switchover is not')
#    quit()
url_address = 'test-patroni-n3.isb:8008'
health = requests.get('http://'+url_address+'/health')
health_json = json.dumps(health.json())
patroni = json.loads(health_json)
data = '{{"leader":"{0}","candidate":"{1}","scheduled_at":"{2}"}}'.format(node_leader, node_candidate, time_iso)


if patroni['role'] == 'replica' and patroni['state'] == 'running':
    response = requests.post('http://'+url_address+'/switchover', data = data)
    print(response.text, response.status_code)
    if response.status_code == 202:
        print ('change master at ' + time_iso)
elif patroni['role'] == 'master' and patroni['state'] == 'running':
    print (url_address + ' master')
else:
    print ('role:',patroni['role'])
    print ('state:',patroni['state'])


