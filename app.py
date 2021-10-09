import genshinstats as gs
from flask import Flask, jsonify, request
from flask import render_template
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
gs.set_cookies(
	{"ltuid": 119480035, "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"},
	{"ltuid": 149113841, "ltoken": "7Qbp2v4WSuQZ76zqetbJv0usM95imp9NvE6lDfW6"}, #GUI
	{"ltuid": 25492983, "ltoken": "Dx5ibXqMljpv8rOOM1Y8MWPVlPhM1FB7khqndUWZ"}, #Ayna
	{"ltuid": 170305200, "ltoken": "GZLBAmp58ZPkbBeKw3PTPTGLIjkK3yHdyxHhONKO"},
	{"ltuid": 170299611, "ltoken": "kGhft0dTMnc7RAsjHLKTVrrGmXhblcF5lfCZJO81"},
	{"ltuid": 170302702, "ltoken": "tEHeC8NLmf3QtXb1R7lknfo9GxiAiKMdNeKA3rMC"},
	{"ltuid": 170306282, "ltoken": "tjiZwlRyAJTosNT3w0XE79ZlfUaVE5LtjQ9FvZaE"},
	{"ltuid": 170306586, "ltoken": "W2f8iRR6DbXWAIvSciGBqqHizqee2iF0pi7O6NAA"},
	{"ltuid": 96745167, "ltoken": "BRrxtAVyitJnntnbB4pnXx4NskvpUC9IWY7DIEmL"}, #Reza
	{"ltuid": 40559632, "ltoken": "uPEFJZ0GlRnRJBhX1lRI8oLTzFZDZvXpcWYMezh5"}, #Bimbe
	{"ltuid": 67128700, "ltoken": "PqExNu7ZIRorgTkZEZQpvmnfjhlykfRARvAnx5As"}, #Natsu
	{"ltuid": 170306105, "ltoken": "a80Lt8Tq5czWlgbP4BvwRT0ZfhaqIpfRphZgHWAl"}
)
app = Flask(__name__)
 
@app.route("/")
def hello():
    return jsonify({"note":"Ada keperluan? silahkan hubungi Actinium..."})

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({"error":"End point tidak ditemukan..."}), 404

@app.route("/user")
def api_user():
	query_parameters = request.args
	uid = query_parameters.get("uid")
	if uid == None:
		return jsonify({"error":"UID belum dimasukkan!"})
	try:
		data = gs.get_user_stats(uid)
		return jsonify(data)
	except Exception as e:
		return jsonify({"error":str(e)}), 404

@app.route("/spa")
def api_spa():
	query_parameters = request.args
	uid = query_parameters.get("uid")
	if uid == None:
		return jsonify({"error":"UID belum dimasukkan!"})
	try:
		data = gs.get_spiral_abyss(uid)
		return jsonify(data)
	except Exception as e:
		return jsonify({"error":str(e)}), 404

@app.route("/traveler")
def api_traveler():
	query_parameters = request.args
	uid = query_parameters.get("uid")
	if uid == None:
		return jsonify({"error":"UID belum dimasukkan!"})
	try:
		data = gs.get_all_user_data(uid)
		return jsonify(data)
	except Exception as e:
		return jsonify({"error":str(e)}), 404


@app.route("/wish")
def wish():
    query_parameters = request.args
    auth_key = query_parameters.get("auth_key")
    if auth_key == None:
        return jsonify({"error":"Parameter auth_key belum dimasukkan!"})
    try:
        gs.set_authkey(auth_key)
        # {100: 'Novice Wishes',
        #  200: 'Permanent Wish',
        #  301: 'Character Event Wish',
        #  302: 'Weapon Event Wish'}
        novice_banner = []
        for i in gs.get_wish_history(100):
            novice_banner.append(i)
        char_banner = []
        for i in gs.get_wish_history(301):
            char_banner.append(i)
        weapon_banner = []
        for i in gs.get_wish_history(302):
            weapon_banner.append(i)
        permanent_banner = []
        for i in gs.get_wish_history(200):
            permanent_banner.append(i)
        return jsonify({"novice_banner":novice_banner,"char_banner":char_banner,"weapon_banner":weapon_banner,"permanent_banner":permanent_banner})
    except Exception as e:
        return jsonify({"error":str(e)}), 404

if __name__ == "__main__":
    app.run()