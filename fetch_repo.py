import requests
import base64
import json

url = 'https://api.github.com/repos/billcccheng/ptt-search/contents/'
results = requests.get(url).json()
paths = [result["path"] for result in results if "path" in result]
print(paths)
# print(json.dumps(res, indent=2, sort_keys=False))


