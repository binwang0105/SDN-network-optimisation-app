import json

json_data = open('topology.json')
json_decoded = json.load(json_data)

#add a key value pair
json_decoded['type'] = 'Network Topology'
json_decoded['label'] = 'NorthStar Visualization Panal'
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

#json_decoded.get('nodes').setdefault(id, default=5)
#key.get('topologyIndex')
#modify a key value pair
#json_decoded['nodes'] = 'A7'

for link_key in json_decoded.get('links'): # each key is a dict

    link_key.setdefault('source', link_key.get('endA').get('node').get('name'))
    link_key.setdefault('target', link_key.get('endZ').get('node').get('name'))
    link_key.setdefault('cost', 1)
    link_key['Property'] = {"age":25}
    del link_key['name']
    del link_key['endZ']
    del link_key['topoObjectType']
    del link_key['endA']
    del link_key['operationalStatus']
    del link_key['topologyIndex']
    del link_key['linkIndex']

    #print type(link_key.get('endZ').get('node')) #dict
    #print link_key.get('endZ') #dict
    #link_key.setdefault('source', link_key.get('name'))
    #link_key.setdefault('target', link_key.get('hostName'))
    #  link_key.setdefault('hostname', link_key.get('topologyIndex'))

# write to json
with open('postTopology.json', 'w') as outfile:
#json.dump(json_decoded, outfile, indent=4)
    json.dump(json_decoded, outfile, indent = 4)




