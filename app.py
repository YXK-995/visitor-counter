import time
import redis
from flask import Flask

app = Flask(__name__)
# 关键点：这里的 host 填写的是 docker-compose 里定义的服务名 'db'
cache = redis.Redis(host='db', port=6379)

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
    count = get_hit_count()
    return f'你好！我是跑在 Docker 里的 Python。这是第 {count} 次访问。\n'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)