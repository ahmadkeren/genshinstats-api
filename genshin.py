import os

import genshinstats as gs
from cachetools import TTLCache, cached

gs.set_cookie(ltuid=os.environ["GS_LTUID"], ltoken=os.environ["GS_LTOKEN"])

@cached(TTLCache(1024, 3600))
def get_user_stats(uid: int):
    return gs.get_user_stats(uid)


@cached(TTLCache(1024, 3600))
def get_spiral_abyss(uid: int, previous: bool = False):
    return gs.get_spiral_abyss(uid, previous)


@cached(TTLCache(1024, 3600))
def get_characters(uid: int, lang: str = 'en-us'):
    ids = [i['id'] for i in get_user_stats(uid)['characters']]
    return gs.get_characters(uid, ids, lang)


_banner_cache = {}
@cached(_banner_cache)
def get_banner_details():
    with open('gacha_banners.txt') as file:
        banners = file.read().splitlines()
    return [gs.get_banner_details(i) for i in banners]

@cached(TTLCache(1024, 3600))
def get_gacha_items():
    return gs.get_gacha_items()
