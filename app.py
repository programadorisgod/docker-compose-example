import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    import requests

    response = requests.get('http://nginx-network-1')

    data = response.text
    
    count = get_hit_count()
    return f'Hello from Docker wow! I have been seen {data} time.\n {count}'