from genshinstats import genshinstats as gs
from flask import Flask, jsonify, request
from flask import render_template
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def setCookie():
	gs.set_cookies(
		{"ltuid": 119480035, "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"},
		{"ltuid": 28604126, "ltoken": "HxIDjzIZBwbqgneTSGK8L2zz9AhL3V2nNIbh6wYy"}, #Dohan
		{"ltuid": 150712156, "ltoken": "9osNFLqaiEtD6HWkh9cB32Gd0QVpdYcP8zZcLDBq"}, #Adolf
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

setCookie()

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

@app.route("/spav2")
def api_spav2():
	query_parameters = request.args
	uid = query_parameters.get("uid")
	ltoken = query_parameters.get("ltoken")
	ltuid = query_parameters.get("ltuid")
	if uid == None:
		return jsonify({"error":"UID belum dimasukkan!"})
	if ltoken == None:
		return jsonify({"error":"ltoken belum dimasukkan!"})
	if ltuid == None:
		return jsonify({"error":"ltuid belum dimasukkan!"})
	try:
		gs.set_cookie(ltuid= ltuid, ltoken= ltoken)
		data = gs.get_spiral_abyss(uid)
		setCookie();
		return jsonify(data)
	except Exception as e:
		return jsonify({"error":str(e)}), 404

@app.route("/travelerv2")
def api_travelerv2():
	query_parameters = request.args
	uid = query_parameters.get("uid")
	ltoken = query_parameters.get("ltoken")
	ltuid = query_parameters.get("ltuid")
	if uid == None:
		return jsonify({"error":"UID belum dimasukkan!"})
	if ltoken == None:
		return jsonify({"error":"ltoken belum dimasukkan!"})
	if ltuid == None:
		return jsonify({"error":"ltuid belum dimasukkan!"})
	try:
		gs.set_cookie(ltuid= ltuid, ltoken= ltoken)
		data = gs.get_all_user_data(uid)
		setCookie();
		return jsonify(data)
	except Exception as e:
		return jsonify({"error":str(e)}), 404

@app.route("/note")
def api_note():
	query_parameters = request.args
	uid = query_parameters.get("uid")
	ltoken = query_parameters.get("ltoken")
	ltuid = query_parameters.get("ltuid")
	if uid == None:
		return jsonify({"error":"UID belum dimasukkan!"})
	if ltoken == None:
		return jsonify({"error":"ltoken belum dimasukkan!"})
	if ltuid == None:
		return jsonify({"error":"ltuid belum dimasukkan!"})
	try:
		gs.set_cookie(ltuid= ltuid, ltoken= ltoken)
		data = gs.get_notes(uid)
		setCookie();
		return jsonify(data)
	except Exception as e:
		return jsonify({"error":str(e)}), 404

@app.route("/set_visibility")
def api_visibility():
	query_parameters = request.args
	toggle = query_parameters.get("toggle")
	ltoken = query_parameters.get("ltoken")
	ltuid = query_parameters.get("ltuid")
	if toggle == None:
		return jsonify({"error":"Toggle on/of belum dimasukkan!"})
	if ltoken == None:
		return jsonify({"error":"ltoken belum dimasukkan!"})
	if ltuid == None:
		return jsonify({"error":"ltuid belum dimasukkan!"})
	if toggle == "on":
		toggle = True
	else:
		toggle = False
	try:
		gs.set_cookie(ltuid= ltuid, ltoken= ltoken)
		data = gs.set_visibility(toggle)
		setCookie();
		return jsonify({"success":True})
	except Exception as e:
		return jsonify({"error":str(e)}), 404

@app.route("/karakter")
def api_karakter():
	query_parameters = request.args
	uid = query_parameters.get("uid")
	if uid == None:
		return jsonify({"error":"UID belum dimasukkan!"})
	try:
		data = gs.get_characters(uid)
		return jsonify(data)
	except Exception as e:
		return jsonify({"error":str(e)}), 404

@app.route("/transaction")
def transaction():
	query_parameters = request.args
	auth_key = query_parameters.get("auth_key")
	if auth_key == None:
		return jsonify({"error":"Parameter auth_key belum dimasukkan!"})
	try:
		gs.set_authkey(auth_key)
		primogems = []
		for i in gs.get_primogem_log():
			primogems.append(i)
		resin = []
		for i in gs.get_resin_log():
			resin.append(i)
		crystals = []
		for i in gs.get_crystal_log():
			crystal.append(i)
		artifact = []
		for i in gs.get_artifact_log():
			artifact.append(i)
		weapons = []
		for i in gs.get_weapon_log():
			weapons.append(i)
		return jsonify({
			"primogems":primogems,
			"resin":resin,
			"crystals":crystals,
			"artifact":artifact,
			"weapons":weapons,
			})
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