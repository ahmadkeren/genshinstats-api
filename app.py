import os
from typing import TypeVar

import genshinstats as gs
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

gs.set_cookie(account_id=os.environ["GS_ACCOUNT_ID"], cookie_token=os.environ["GS_COOKIE_TOKEN"])
app = Flask(__name__)
app.config.update({
    # "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 3600 # 1 hour
})
cache = Cache(app)
CORS(app)

T = TypeVar('T')
def no_raise(func: T) -> T:
    def inner(*args, **kwargs):
        try:
            data = func(*args,**kwargs)
        except gs.GenshinStatsException as e:
            return {'error':e.__class__.__name__,'message':e.args[0]}, 400
        except Exception as e:
            return {'error':e.__class__.__name__,'message':e.args[0]}, 500
        else:
            return {'data':data}, 200
    return inner

response_filter = lambda r: r[1]==200

@app.route('/', methods=['GET'])
def index():
    return {'endpoints':['/user_info/<int:uid>']}

@app.route('/user_info/<int:uid>', methods=['GET'])
@cache.memoize(response_filter=response_filter)
def get_user_info(uid: int):
    return no_raise(gs.get_user_info)(uid)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
