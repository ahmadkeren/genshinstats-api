import genshinstats as gs
from flask import Flask, jsonify, request
from flask import render_template
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

data = open('cookie.json',"r")
data_cookie = json.load(data)
cookie_used = 0 #index
gs.set_cookie(ltuid=data_cookie[0]["ltuid"], ltoken=data_cookie[0]["ltoken"])
#uid = 710785423
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
		return smart_handle_limit(e)

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
		return smart_handle_limit(e)

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
		return smart_handle_limit(e)
 
def smart_handle_limit(e):
	global cookie_used, data_cookie
	if(str(e) == "Cannnot get data for more than 30 accounts per day."):
		if(cookie_used < len(data_cookie)-1):
			gs.set_cookie(ltuid=data_cookie[cookie_used+1]["ltuid"], ltoken=data_cookie[cookie_used+1]["ltoken"])
			cookie_used+=1
			return jsonify({"success":str("COOKIE berhasil direfresh, silahkan coba lagi!")})
		else:
			gs.set_cookie(ltuid=data_cookie[0]["ltuid"], ltoken=data_cookie[0]["ltoken"])
			cookie_used = 0;
	else:
		return jsonify({"error":str(e)})

if __name__ == "__main__":
    app.run()