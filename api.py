import genshinstats.errors as gs
from flask import Blueprint, jsonify, redirect, request
from requests.structures import CaseInsensitiveDict

from genshin import *

api = Blueprint('api',__name__,url_prefix='/api')

class InvalidEnum(Exception): ...
def find_one(data, **kwargs):
    """Takes in a list of dicts and a keyword, returns a dict."""
    key,value = next(iter(kwargs.items()))
    if value is None:
        raise InvalidEnum(f"No Enum argument was provided, must be one of [{', '.join(data)}]",list(data))
    data = CaseInsensitiveDict({i[key]:i for i in data})
    if value in data:
        return data[value]
    raise InvalidEnum(f"'{value}' is not a valid Enum for '{key}', must be one of [{', '.join(data)}]",list(data))


@api.route('/docs')
def docs():
    return redirect('https://app.swaggerhub.com/apis-docs/thesadru/genshinstats-api/1.0.0')

@api.route('/user/<int:uid>')
def user(uid: int):
    return get_user_info(uid)

@api.route('/spiral_abyss/<int:uid>')
def spiral_abyss(uid: int):
    previous = request.args.get('previous')=='true'
    return get_spiral_abyss(uid, previous)

@api.route('/characters/<int:uid>')
@api.route('/characters/<int:uid>/<character_name>')
def characters(uid: int, character_name: str=None):
    chars = get_characters(uid)
    if character_name is None:
        return jsonify(chars)
    return find_one(chars,name=character_name)

@api.route('/characters/<int:uid>/items')
def character_items(uid: int):
    chars = get_characters(uid)
    return {
        'weapons': [{**c['weapon'],'equipped_by':c['id']} for c in chars],
        'artifacts': [{**i,'equipped_by':c['id']} for c in chars for i in c['artifacts']]
    }

@api.route('/gachalog')
def gachalog():
    authkey = request.args.get('authkey')
    size = request.args.get('size',60,type=int)
    gacha_type = request.args.get('gacha_type')
    if authkey is None:
        raise gs.MissingAuthKey('An authkey must be given as a parameter.')
    return jsonify(get_gacha_log(authkey,size,gacha_type))

@api.route('/gacha')
def gacha():
    return jsonify(get_gacha_details())

@api.route('/gacha/items')
def gacha_items():
    return jsonify(get_gacha_items())


@api.errorhandler(Exception)
def server_error_handler(e):
    if isinstance(e,gs.DataNotPublic):
        status = 403
    elif isinstance(e,gs.GenshinStatsException):
        status = 400
    else:
        status = 500
    return {'error':e.__class__.__name__,'message':e.args[0]}, status

@api.errorhandler(InvalidEnum)
def invalidenum_handler(e):
    return {'error':e.__class__.__name__,'message':e.args[0],'choices':e.args[1]}, 400
