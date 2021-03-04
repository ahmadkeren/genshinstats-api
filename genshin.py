import os

import genshinstats as gs
from flask_caching import Cache

gs.set_cookie(account_id=os.environ["GS_ACCOUNT_ID"], cookie_token=os.environ["GS_COOKIE_TOKEN"])

cache = Cache()

@cache.memoize()
def get_user_info(uid: int):
    return gs.get_user_info(uid)

@cache.memoize()
def get_spiral_abyss(uid: int, previous: bool=False):
    return gs.get_spiral_abyss(uid,previous)

@cache.memoize()
def get_characters(uid: int):
    return gs.get_all_characters(uid)

@cache.memoize(60*60*12)
def get_gacha_details():
    with open('gacha_banners.txt') as file:
        banners = file.read().splitlines()
    return [gs.get_gacha_details(i) for i in banners]
