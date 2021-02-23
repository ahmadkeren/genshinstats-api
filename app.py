import os

import genshinstats as gs
from flask import Flask, jsonify, redirect
from flask_caching import Cache
from flask_cors import CORS
from requests.structures import CaseInsensitiveDict

# init
gs.set_cookie(account_id=os.environ["GS_ACCOUNT_ID"], cookie_token=os.environ["GS_COOKIE_TOKEN"])
app = Flask(__name__)
app.config.update({
    # "DEBUG": True,
    'JSON_SORT_KEYS': False, # bad idea?
    
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 3600 # 1 hour
})
app.url_map.strict_slashes = False
cache = Cache(app)
CORS(app)

@cache.memoize()
def get_user_info(uid: int):
    return gs.prettify_user_info(gs.get_user_info(uid))

@cache.memoize()
def get_spiral_abyss(uid: int, previous: bool=False):
    return gs.prettify_spiral_abyss(gs.get_spiral_abyss(uid,previous))

@cache.memoize()
def get_characters(uid: int):
    return gs.prettify_characters(gs.get_all_characters(uid))

def find_one(data, **kwargs):
    """Takes in a list of dicts and a keyword, returns a dict."""
    key,value = next(iter(kwargs.items()))
    data = CaseInsensitiveDict({i[key]:i for i in data})
    if value in data:
        return data[value]
    raise type('InvalidEnum',Exception)(f'"{value}" is not a valid Enum for "{key}", must be one of [{", ".join(data)}]')


@app.route('/')
def index():
    return redirect('endpoints')

@app.route('/endpoints')
def endpoints():
    return {'endpoints':[f"'{rule.rule}' -> {rule.endpoint}" for rule in app.url_map.iter_rules()]}

@app.route('/user')
@app.route('/user/<int:uid>')
def user_all(uid: int=None):
    if uid is None:
        raise gs.InvalidUID('No UID was provided')
    return get_user_info(uid)

@app.route('/user/<int:uid>/stats')
def user_stats(uid: int):
    return get_user_info(uid)['stats']

@app.route('/user/<int:uid>/characters')
@app.route('/user/<int:uid>/characters/<character_name>')
def user_characters(uid: int, character_name: str=None):
    characters = get_user_info(uid)['characters']
    if character_name is None:
        return {'characters':characters}
    return find_one(characters,name=character_name)

@app.route('/user/<int:uid>/exploration')
@app.route('/user/<int:uid>/exploration/<region>')
def user_exploration(uid: int, region: str=None):
    exploration = get_user_info(uid)['exploration']
    if region is None:
        return jsonify(exploration)
    return find_one(exploration,name=region)

@app.route('/spiral_abyss/<int:uid>')
@app.route('/spiral_abyss/<int:uid>/<any(current, previous):schedule>')
def spiral_abyss(uid: int, schedule: str=None):
    if schedule is None:
        return {
            'current':get_spiral_abyss(uid,False),
            'previous':get_spiral_abyss(uid,True)
        }
    elif schedule == 'current':
        return get_spiral_abyss(uid,False)
    elif schedule == 'previous':
        return get_spiral_abyss(uid,True)

@app.route('/characters/<int:uid>')
@app.route('/characters/<int:uid>/<character_name>')
@app.route('/characters/<int:uid>/<character_name>/<any(weapon, artifacts):field>')
def characters(uid: int, character_name: str=None, field: str=None):
    chars = get_characters(uid)
    if character_name is None:
        return jsonify(chars)
    char = find_one(chars,name=character_name)
    if field is None:
        return char
    return char[field]

if __name__ == '__main__':
    app.run(port=5000, threaded=True)
