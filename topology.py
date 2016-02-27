import requests
requests.packages.urllib3.disable_warnings()
import json

url = "https://10.10.2.25:8443/oauth2/token"

payload = {'grant_type': 'password', 'username': 'group1', 'password': 'Group1'}
#payload = {'grant_type': 'password', 'username': 'admin', 'password': 'northstar123'}
response = requests.post (url, data=payload, auth=('group1','Group1'), verify=False)
#response = requests.post (url, data=payload, auth=('admin','northstar123'), verify=False)
json_data = json.loads(response.text)
authHeader= {"Authorization":"{token_type} {access_token}".format(**json_data)}

r = requests.get('https://10.10.2.25:8443/NorthStar/API/v1/tenant/1/topology/1', headers=authHeader, verify=False)

f = open('poker_face.json', 'wb')
#print json.dumps(r.json(), indent=4, separators=(',', ': '))
f.write(json.dumps(r.json(), indent=4, separators=(',', ': ')))
f.close();