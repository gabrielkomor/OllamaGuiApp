import requests

url = 'http://127.0.0.1:8000/generate'
params = {'prompt': 'tell me only how many kilograms sun weight'}
response = requests.get(url, params=params, stream=True)

for chunk in response.iter_content(chunk_size=None):
    if chunk:
        print(chunk.decode('utf-8'), end='', flush=True)
