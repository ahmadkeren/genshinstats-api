from flask import Flask, url_for
from flask_cors import CORS
import os

from api import api
from genshin import cache

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.update({
    "JSON_SORT_KEYS": False, # bad idea?
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 3600 # 1 hour
})
app.register_blueprint(api)

cache.init_app(app)
CORS(app)


@app.route('/')
def index():
    return {
        'api': api.url_prefix,
        'docs': url_for('api.docs'),
        'github': "https://github.com/thesadru/genshinstats-api",
        'endpoints': [rule.rule for rule in app.url_map.iter_rules()],
    }


if __name__ == '__main__':
    if os.name == 'nt':
        import colorama
        colorama.init()
    app.run(port=5000, threaded=True, debug=False)
