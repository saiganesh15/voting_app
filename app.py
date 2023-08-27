from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import logging

option_a = os.getenv('OPTION_A', "India")
option_b = os.getenv('OPTION_B', "Pakistan")
option_c = os.getenv('OPTION_C', "Nepal")
option_d = os.getenv('OPTION_D', "Srilanka")
option_e = os.getenv('OPTION_E', "Afghanistan")
option_f = os.getenv('OPTION_F', "Bangladesh")

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

app = Flask(__name__)



gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", port=6379, db=0, socket_timeout=5)
        app.logger.info("Migration Synced")
    return g.redis

@app.route("/vote", methods=['POST'])
def record_vote():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = request.form['vote']

    redis = get_redis()
    app.logger.info('Received vote for %s', vote)
    data = json.dumps({'voter_id': voter_id, 'vote': vote})
    redis.rpush('votes', data)

    return "Vote recorded"

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        option_e=option_e,
        option_f=option_f,
        hostname=hostname,
        ip_address=ip_address,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.logger.info("Starting the app in production mode.")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

