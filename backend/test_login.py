import urllib.request
import json
import base64

try:
    req = urllib.request.Request('http://127.0.0.1:8000/api/token/', data=json.dumps({'username': 'superadmin', 'password': 'admin123'}).encode('utf-8'), headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read())
    token = data['access']
    
    payload = json.loads(base64.urlsafe_b64decode(token.split('.')[1] + '==').decode('utf-8'))
    user_id = payload['user_id']
    print('User ID in token:', user_id)
    
    req2 = urllib.request.Request(f'http://127.0.0.1:8000/api/users/{user_id}/', headers={'Authorization': f'Bearer {token}'})
    res2 = urllib.request.urlopen(req2)
    print(res2.getcode())
    print(res2.read())
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code)
    print('Response body:', e.read().decode('utf-8'))
except Exception as e:
    print('Error:', str(e))
