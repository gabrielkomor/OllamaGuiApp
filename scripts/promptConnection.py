import threading
import time
import requests
import subprocess
from scripts.ollamaServer import start_server


def start_server_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(2)


def start_prompts():
    while True:
        prompt = input('\n Ask me a question: \n')

        if prompt == 'bye':
            break

        url = 'http://127.0.0.1:8000/generate'
        params = {'prompt': prompt}
        response = requests.get(url, params=params, stream=True)

        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                print(chunk.decode('utf-8'), end='', flush=True)

    subprocess.run("taskkill /f /im ollama.exe", shell=True)
