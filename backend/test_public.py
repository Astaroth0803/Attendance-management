import urllib.request
import json
req = urllib.request.Request(
    'http://127.0.0.1:8000/api/public/beneficiaries/?org=ciudad-jardin-las-mananitas',
    data=json.dumps({'first_name': 'Test', 'last_name': 'User', 'dob': '2000-01-01', 'sex': 'M', 'sector': 'Test Sector'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
try:
    res = urllib.request.urlopen(req)
    print(res.read())
except urllib.error.HTTPError as e:
    print(e.read())
