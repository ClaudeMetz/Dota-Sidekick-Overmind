from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<head><title>Dota Sidekick</title></head><body><h2>Welcome to Dota Sidekick!</h2></body>'


@app.route('/api/v1/')
def api_v1():
    return '<head><title>Dota Sidekick</title></head><body><h2>API Stuff!</h2></body>'

if __name__ == '__main__':
    app.run()
