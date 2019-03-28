from flask import Flask, render_template, jsonify
import requests
from key import key
from location import locationApp

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@locationApp.route("/location", methods=["GET"])
def layout():
	return render_template("layout.html")

@locationApp.route("/sendRequest/<string:query>")
def results(query):
	search_payload = {"key" : key, "query" : query}
	search_request = requests.get(search_url, params=search_payload)
	search_json = search_request.json()

	place_id = search_json["results"][0]["place_id"]

	details_payload = {"key" : key, "placeid" : place_id}
	details_response = requests.get(details_url, params=details_payload)
	details_json = details_response.json()

	url = details_json["result"]["url"]
	return jsonify({'result' : url})