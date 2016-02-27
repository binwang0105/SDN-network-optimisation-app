import requests
requests.packages.urllib3.disable_warnings()
import json
import os

url = "https://10.10.2.25:8443/oauth2/token"

payload = {'grant_type': 'password', 'username': 'group1', 'password': 'Group1'}
#payload = {'grant_type': 'password', 'username': 'admin', 'password': 'northstar123'}
response = requests.post (url, data=payload, auth=('group1','Group1'), verify=False)
#response = requests.post (url, data=payload, auth=('admin','northstar123'), verify=False)
json_data = json.loads(response.text)
authHeader= {"Authorization":"{token_type} {access_token}".format(**json_data)}

r = requests.get('https://10.10.2.25:8443/NorthStar/API/v1/tenant/1/topology/1', headers=authHeader, verify=False)

f = open('temp.json', 'wb')
#print json.dumps(r.json(), indent=4, separators=(',', ': '))
f.write(json.dumps(r.json(), indent=4, separators=(',', ': ')))
f.close();

json_data = open('temp.json')
json_decoded = json.load(json_data)

#add a key value pair
json_decoded['type'] = 'Network Topology'
json_decoded['label'] = 'NorthStar Visualizer'
json_decoded['version'] = '1.0.0.0 by Team1'
json_decoded['protocol'] = 'OSPF'

for node_key in json_decoded.get('nodes'): # each key is a dict
    node_key.setdefault('id', node_key.get('name'))
    node_key.setdefault('label', node_key.get('hostName'))
    node_key.setdefault('hostname', node_key.get('topologyIndex'))
    del node_key['nodeIndex']
    del node_key['layer']
    del node_key['hostName']
    del node_key['name']
    del node_key['AutonomousSystem']
    del node_key['topoObjectType']
    del node_key['topologyIndex']
    del node_key['protocols']
    del node_key['topology']

for link_key in json_decoded.get('links'): # each key is a dict
    link_key.setdefault('source', link_key.get('endA').get('node').get('name'))
    link_key.setdefault('target', link_key.get('endZ').get('node').get('name'))
    #link_key.setdefault('type', link_key.get('operationalStatus'))
    link_key.setdefault('cost', 1)
    # define a dict in json
    link_key['Property'] = {'type':link_key.get('operationalStatus')}
    del link_key['name']
    del link_key['endZ']
    del link_key['topoObjectType']
    del link_key['endA']
    del link_key['operationalStatus']
    del link_key['topologyIndex']
    del link_key['linkIndex']

# write to json
with open('topology.json', 'w') as outfile:
    #json.dump(json_decoded, outfile, indent=4)
    json.dump(json_decoded, outfile, indent = 4)

os.remove('temp.json')