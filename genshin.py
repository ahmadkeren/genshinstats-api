import os

import genshinstats as gs
from flask_caching import Cache

gs.session.cookies.update(dict(account_id=os.environ["GS_ACCOUNT_ID"], cookie_token=os.environ["GS_COOKIE_TOKEN"]))

cache = Cache()

@cache.memoize()
def get_user_info(uid: int):
    return gs.get_user_info(uid)

@cache.memoize()
def get_spiral_abyss(uid: int, previous: bool=False):
    return gs.get_spiral_abyss(uid,previous)

@cache.memoize()
def get_characters(uid: int):
    characters = get_user_info(uid)['characters']
    ids = [i['id'] for i in characters]
    return gs.get_characters(uid,ids)

@cache.memoize()
def get_gacha_log(authkey: str, size: int=60, gacha_type: str=None):
    if gacha_type is None:
        g = gs.get_entire_gacha_log(size,authkey=authkey)
    else:
        g = gs.get_gacha_log(gacha_type,size,authkey=authkey)
    return list(g)

@cache.memoize(60*60*12)
def get_gacha_details():
    with open('gacha_banners.txt') as file:
        banners = file.read().splitlines()
    return [gs.get_gacha_details(i) for i in banners]

@cache.memoize(60*60*12)
def get_gacha_items():
    return gs.get_gacha_items()
