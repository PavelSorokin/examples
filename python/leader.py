import requests
import sys
import json

def is_leader():
    url_address = 'test-patroni-n3.isb:8008'
    health = requests.get('http://'+url_address+'/cluster')
    health_json = json.dumps(health.json())
    patroni = json.loads(health_json)
    for node in patroni['members']:
        if node['role'] == 'leader':
            return node['name']

node_leader = is_leader()
print(node_leader)
