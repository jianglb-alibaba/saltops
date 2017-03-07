import requests

url = 'http://192.168.80.133:5000/upload'
path = '/Users/kira/oschina/saltops/README.md'
files = {'file': open(path, 'rb')}
r = requests.post(url, files=files)