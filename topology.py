import requests
requests.packages.urllib3.disable_warnings()
import json
import os
import time
import redis

url = "https://10.10.2.25:8443/oauth2/token"

payload = {'grant_type': 'password', 'username': 'group1', 'password': 'Group1'}
#payload = {'grant_type': 'password', 'username': 'admin', 'password': 'northstar123'}
response = requests.post (url, data=payload, auth=('group1','Group1'), verify=False)
#response = requests.post (url, data=payload, auth=('admin','northstar123'), verify=False)
json_data = json.loads(response.text)
authHeader= {"Authorization":"{token_type} {access_token}".format(**json_data)}
while(1):
    r = requests.get('https://10.10.2.25:8443/NorthStar/API/v1/tenant/1/topology/1', headers=authHeader, verify=False)

    f = open('temp.json', 'wb')
    #print json.dumps(r.json(), indent=4, separators=(',', ': '))
    f.write(json.dumps(r.json(), indent=4, separators=(',', ': ')))
    f.close();

    json_data = open('temp.json')
    json_decoded = json.load(json_data)
    f.close()
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

    # store traffic utilization to links
    r = redis.StrictRedis(host='10.10.4.252', port=6379, db=0)
    # r.lrange is list
    dict = {}
    #with open('a.json', 'w') as outfile2:
    traffic1 = r.lrange('tampa:ge-1/0/2:traffic statistics', 0, 0)[0]
    traffic1_decoded = json.loads(traffic1)
    dict[traffic1_decoded.get('router_id') + '_' + traffic1_decoded.get('interface_address')]=int(traffic1_decoded.get('stats')[0].get('output-bps')[0].get('data'))
    #key: router_id + interface_id

    traffic2 = r.lrange('tampa:ge-1/0/1:traffic statistics', 0, 0)[0]
    traffic2_decoded = json.loads(traffic2)
    dict[traffic2_decoded.get('router_id') + '_' + traffic2_decoded.get('interface_address')]=float(traffic2_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic3 = r.lrange('tampa:ge-1/0/0:traffic statistics', 0, 0)[0]
    traffic3_decoded = json.loads(traffic3)
    dict[traffic3_decoded.get('router_id') + '_' + traffic3_decoded.get('interface_address')]=float(traffic3_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic4 = r.lrange('dallas:ge-1/0/0:traffic statistics', 0, 0)[0]
    traffic4_decoded = json.loads(traffic4)
    dict[traffic4_decoded.get('router_id') + '_' + traffic4_decoded.get('interface_address')]=float(traffic4_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic5 = r.lrange('dallas:ge-1/0/1:traffic statistics', 0, 0)[0]
    traffic5_decoded = json.loads(traffic5)
    dict[traffic5_decoded.get('router_id') + '_' + traffic5_decoded.get('interface_address')]=float(traffic5_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic6 = r.lrange('dallas:ge-1/0/2:traffic statistics', 0, 0)[0]
    traffic6_decoded = json.loads(traffic6)
    dict[traffic6_decoded.get('router_id') + '_' + traffic6_decoded.get('interface_address')]=float(traffic6_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic7 = r.lrange('dallas:ge-1/0/3:traffic statistics', 0, 0)[0]
    traffic7_decoded = json.loads(traffic7)
    dict[traffic7_decoded.get('router_id') + '_' + traffic7_decoded.get('interface_address')]=float(traffic7_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic8 = r.lrange('dallas:ge-1/0/4:traffic statistics', 0, 0)[0]
    traffic8_decoded = json.loads(traffic8)
    dict[traffic8_decoded.get('router_id') + '_' + traffic8_decoded.get('interface_address')]=float(traffic8_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic9 = r.lrange('houston:ge-0/1/0:traffic statistics', 0, 0)[0]
    traffic9_decoded = json.loads(traffic9)
    dict[traffic9_decoded.get('router_id') + '_' + traffic9_decoded.get('interface_address')]=float(traffic9_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic10 = r.lrange('houston:ge-0/1/1:traffic statistics', 0, 0)[0]
    traffic10_decoded = json.loads(traffic10)
    dict[traffic10_decoded.get('router_id') + '_' + traffic10_decoded.get('interface_address')]=float(traffic10_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic11 = r.lrange('houston:ge-0/1/2:traffic statistics', 0, 0)[0]
    traffic11_decoded = json.loads(traffic11)
    dict[traffic11_decoded.get('router_id') + '_' + traffic11_decoded.get('interface_address')]=float(traffic11_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic12 = r.lrange('houston:ge-0/1/3:traffic statistics', 0, 0)[0]
    traffic12_decoded = json.loads(traffic12)
    dict[traffic12_decoded.get('router_id') + '_' + traffic12_decoded.get('interface_address')]=float(traffic12_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic13 = r.lrange('chicago:ge-1/0/4:traffic statistics', 0, 0)[0]
    traffic13_decoded = json.loads(traffic13)
    dict[traffic13_decoded.get('router_id') + '_' + traffic13_decoded.get('interface_address')]=float(traffic13_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic14 = r.lrange('chicago:ge-1/0/3:traffic statistics', 0, 0)[0]
    traffic14_decoded = json.loads(traffic14)
    dict[traffic14_decoded.get('router_id') + '_' + traffic14_decoded.get('interface_address')]=float(traffic14_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic15 = r.lrange('chicago:ge-1/0/2:traffic statistics', 0, 0)[0]
    traffic15_decoded = json.loads(traffic15)
    dict[traffic15_decoded.get('router_id') + '_' + traffic15_decoded.get('interface_address')]=float(traffic15_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic16 = r.lrange('chicago:ge-1/0/1:traffic statistics', 0, 0)[0]
    traffic16_decoded = json.loads(traffic16)
    dict[traffic16_decoded.get('router_id') + '_' + traffic16_decoded.get('interface_address')]=float(traffic16_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic17 = r.lrange('los angeles:ge-0/1/0:traffic statistics', 0, 0)[0]
    traffic17_decoded = json.loads(traffic17)
    dict[traffic17_decoded.get('router_id') + '_' + traffic17_decoded.get('interface_address')]=float(traffic17_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic18 = r.lrange('los angeles:ge-0/1/1:traffic statistics', 0, 0)[0]
    traffic18_decoded = json.loads(traffic18)
    dict[traffic18_decoded.get('router_id') + '_' + traffic18_decoded.get('interface_address')]=float(traffic18_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic19 = r.lrange('los angeles:ge-0/1/2:traffic statistics', 0, 0)[0]
    traffic19_decoded = json.loads(traffic19)
    dict[traffic19_decoded.get('router_id') + '_' + traffic19_decoded.get('interface_address')]=float(traffic19_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic20 = r.lrange('san francisco:ge-1/0/0:traffic statistics', 0, 0)[0]
    traffic20_decoded = json.loads(traffic20)
    dict[traffic20_decoded.get('router_id') + '_' + traffic20_decoded.get('interface_address')]=int(traffic20_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic21 = r.lrange('san francisco:ge-1/0/1:traffic statistics', 0, 0)[0]
    traffic21_decoded = json.loads(traffic21)
    dict[traffic21_decoded.get('router_id') + '_' + traffic21_decoded.get('interface_address')]=int(traffic21_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic22 = r.lrange('san francisco:ge-1/0/3:traffic statistics', 0, 0)[0]
    traffic22_decoded = json.loads(traffic22)
    dict[traffic22_decoded.get('router_id') + '_' + traffic22_decoded.get('interface_address')]=int(traffic22_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic23 = r.lrange('new york:ge-1/0/3:traffic statistics', 0, 0)[0]
    traffic23_decoded = json.loads(traffic23)
    dict[traffic23_decoded.get('router_id') + '_' + traffic23_decoded.get('interface_address')]=float(traffic23_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic24 = r.lrange('new york:ge-1/0/5:traffic statistics', 0, 0)[0]
    traffic24_decoded = json.loads(traffic24)
    dict[traffic24_decoded.get('router_id') + '_' + traffic24_decoded.get('interface_address')]=float(traffic24_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic25 = r.lrange('new york:ge-1/0/7:traffic statistics', 0, 0)[0]
    traffic25_decoded = json.loads(traffic25)
    dict[traffic25_decoded.get('router_id') + '_' + traffic25_decoded.get('interface_address')]=float(traffic25_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic26 = r.lrange('miami:ge-0/1/2:traffic statistics', 0, 0)[0]
    traffic26_decoded = json.loads(traffic26)
    dict[traffic26_decoded.get('router_id') + '_' + traffic26_decoded.get('interface_address')]=float(traffic26_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic27 = r.lrange('miami:ge-1/3/0:traffic statistics', 0, 0)[0]
    traffic27_decoded = json.loads(traffic27)
    dict[traffic27_decoded.get('router_id') + '_' + traffic27_decoded.get('interface_address')]=float(traffic27_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic28 = r.lrange('miami:ge-0/1/3:traffic statistics', 0, 0)[0]
    traffic28_decoded = json.loads(traffic28)
    dict[traffic28_decoded.get('router_id') + '_' + traffic28_decoded.get('interface_address')]=float(traffic28_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic29 = r.lrange('miami:ge-0/1/0:traffic statistics', 0, 0)[0]
    traffic29_decoded = json.loads(traffic29)
    dict[traffic29_decoded.get('router_id') + '_' + traffic29_decoded.get('interface_address')]=float(traffic29_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    traffic30 = r.lrange('miami:ge-0/1/1:traffic statistics', 0, 0)[0]
    traffic30_decoded = json.loads(traffic30)
    dict[traffic30_decoded.get('router_id') + '_' + traffic30_decoded.get('interface_address')]= float(traffic30_decoded.get('stats')[0].get('output-bps')[0].get('data'))/8000000000

    for link_key in json_decoded.get('links'): # each key is a dict
        link_key.setdefault('source', link_key.get('endA').get('node').get('name'))
        link_key.setdefault('target', link_key.get('endZ').get('node').get('name'))
        #link_key.setdefault('type', link_key.get('operationalStatus'))
        link_key.setdefault('cost', 1)
        # define a dict in json
        link_key['properties'] = {'type':link_key.get('operationalStatus'), 'source to target':dict.get(str(link_key.get('endA').get('node').get('name'))+ '_' + str(link_key.get('endA').get('ipv4Address').get('address'))), 'target to source':dict.get(str(link_key.get('endZ').get('node').get('name'))+ '_' + str(link_key.get('endZ').get('ipv4Address').get('address')))}
        del link_key['name']
        del link_key['endZ']
        del link_key['topoObjectType']
        del link_key['endA']
        del link_key['operationalStatus']
        del link_key['topologyIndex']
        del link_key['linkIndex']

    # write to json
    with open('topology.json', 'wb') as outfile:
        #json.dump(json_decoded, outfile, indent=4)
        json.dump(json_decoded, outfile, indent = 4)
    outfile.close()
    os.remove('temp.json')
    time.sleep(10)

#print dict
#json.dump(traffic_decoded, outfile2, indent = 4)