from hashlib import sha256
from typing import List, Literal

import genshinstats as gs
from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse

import genshin

API_TOKEN = "8374258755b6f7c9743c993d15e835a240d8cda9171327e8fb476bd8046663cc"

app = FastAPI(
    title="genshinstats API",
    description="Api for genshin stats",
    contact={"name": "sadru", "url": "https://github.com/thesadru"},
)

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(app.docs_url)


@app.get("/user/{uid}", tags=["stats"], summary="User Stats")
def user(uid: int = Path(..., description="user's game uid", example=710785423)):
    """User's stats, characters, exploration percentage and teapot info"""
    return genshin.get_user_stats(uid)


@app.get("/abyss/{uid}", tags=["stats"], summary="Spiral Abyss")
def abyss(
    uid: int = Path(..., description="user's game uid", example=710785423),
    previous: bool = Query(False, description="Return the previous season's spiral abyss"),
):
    """User's Spiral Abyss runs during an entire season"""
    return genshin.get_spiral_abyss(uid, previous)


@app.get("/characters/{uid}", tags=["stats"], summary="Characters")
def characters(
    uid: int = Path(..., description="user's game uid", example=710785423),
    name: str = Query(None, description="Character's name"),
    lang: str = Query("en-us", description="Language of the response"),
):
    """List of user's characters"""
    if lang not in gs.get_langs():
        raise HTTPException(422, "Lang must be one of: " + ", ".join(gs.get_langs()))

    characters = genshin.get_characters(uid, lang)
    if name is None:
        return characters

    for char in characters:
        if char["name"].title() == name.title():
            return char
    else:
        raise HTTPException(status_code=418, detail=f"User doesn't have a character named {name!r}")


@app.get("/gacha", tags=["gacha"], summary="Current banners")
def gacha():
    """List of the information of all current gacha banners."""
    return genshin.get_banner_details()


@app.post("/gacha", tags=["gacha"], include_in_schema=False)
def update_gacha(ids: List[str], request: Request):
    """Update the banner ids, requires the user to be authorized"""
    token = request.cookies.get("api_token")
    if token is None or sha256(token.encode()).hexdigest() != API_TOKEN:
        raise HTTPException(403, "You are not authorized")

    genshin._banner_cache.clear()
    with open("gacha_banners.txt", "w") as file:
        file.write("\n".join(ids))


@app.get("/gacha/items", tags=["gacha"], summary="Gacha Items")
def gacha_items():
    """A list of all items that you can pull from the gacha excluding limited items."""
    return genshin.get_gacha_items()


@app.exception_handler(gs.GenshinStatsException)
def handle_genshinstats(request: Request, exc: gs.GenshinStatsException):
    return JSONResponse(
        {"error": type(exc).__name__, "retcode": exc.retcode, "message": exc.msg, "orig_msg": exc.orig_msg},
        status_code=400,
    )
