import requests

params = {}
headers = {'x-api-key' : 'f1534989-ffbf-42b0-9b23-49a832c874c0'}
r = requests.get('https://api.dbaas.intel.com' + '/v1/dataservices', params=params, headers=headers, verify='chainfile.pem')
print(r.json())
