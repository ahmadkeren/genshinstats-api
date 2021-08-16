import genshinstats as gs
from flask import Flask, jsonify, request
from flask import render_template
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

gs.set_cookie(ltuid=119480035, ltoken="cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT")
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
		return jsonify({"error":str(e)})

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
		return jsonify({"error":str(e)})

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
		return jsonify({"error":str(e)})
 
if __name__ == "__main__":
    app.run()