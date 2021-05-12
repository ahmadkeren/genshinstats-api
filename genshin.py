import os
from typing import Iterable

import genshinstats as gs
from flask_caching import Cache
from functools import partial

gs.set_cookie(ltuid=os.environ["GS_LTUID"], ltoken=os.environ["GS_LTOKEN"])
cache = Cache()


@cache.memoize()
def get_user_info(uid: int):
    return gs.get_user_info(uid)


@cache.memoize()
def get_spiral_abyss(uid: int, previous: bool = False):
    return gs.get_spiral_abyss(uid, previous)


@cache.memoize()
def get_characters(uid: int):
    characters = get_user_info(uid)['characters']
    ids = [i['id'] for i in characters]
    return gs.get_characters(uid, ids)


def get_gacha_log(authkey: str, size: int = None, gacha_type: str = None, end_id: int = 0):
    size = size or float('inf')
    # first we load the log
    data = []
    while size > 0:
        i = cache.get(('gacha_log', authkey, end_id))
        if i is None:
            break
        end_id = i['id']
        size -= 1
        data.append(i)
    else:
        return data

    # then we do the actual log request
    func = gs.get_entire_gacha_log if gacha_type is None else partial(gs.get_gacha_log, gacha_type)
    g = func(size, authkey, end_id)

    # and finally we save the log
    prev_id: int = end_id if len(data) == 0 else data[-1]['id']
    for i in g:
        cache.set(('gacha_log', authkey, prev_id), i)
        prev_id = i['id']
        data.append(i)

    return data


@cache.memoize(60*60*24)
def get_gacha_details():
    with open('gacha_banners.txt') as file:
        banners = file.read().splitlines()
    return [gs.get_gacha_details(i) for i in banners]


@cache.memoize(60*60*24)
def get_gacha_items():
    return gs.get_gacha_items()
