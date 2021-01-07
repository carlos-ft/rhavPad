from flask import Flask, request, render_template, jsonify
import redis
import settings

UTF_8 = 'utf-8'

app = Flask(__name__)

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@app.route('/')
def init():
    return render_template('index.html')


@app.route('/<path:url>', methods=['GET', 'PUT', 'POST'])
def update(url):
    note = request.data.decode(UTF_8)

    if request.method == 'PUT':
        redis_instance.set(url, note.encode(UTF_8))
    else:
        note = redis_instance.get(url)
        if note is not None:
            note = note.decode(UTF_8)
        else:
            note = ''

    if request.method == 'PUT' or request.method == 'POST':
        return jsonify({'note': note})
    if request.method == 'GET':
        return render_template('notepad.html', note=note)