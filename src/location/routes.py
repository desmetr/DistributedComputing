from flask import Flask, render_template, jsonify
import requests
import imghdr
from location.key import key
from location import locationApp

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"
photos_url = "https://maps.googleapis.com/maps/api/place/photo"

@locationApp.route("/location", methods=["GET"])
def layout():
	return render_template("layout.html")

@locationApp.route("/sendRequestMap/<string:query>")
def resultsMap(query):
	template_embed_url = "https://www.google.com/maps/embed/v1/place?key=" + key + "&q="
	current_embed_url = template_embed_url + query
	return '<iframe width="600" height="450" frameborder="0" style="border:0" src="' + current_embed_url + '"allowfullscreen></iframe>'

@locationApp.route("/sendRequestPhoto/<string:query>")
def resultsPhoto(query):
	search_payload = {"key" : key, "query" : query}
	search_request = requests.get(search_url, params=search_payload)
	search_json = search_request.json()

	photo_id = search_json["results"][0]["photos"][0]["photo_reference"]

	photo_payload = {"key" : key, "maxwidth" : 500, "maxheight" : 500, "photoreference" : photo_id}
	photo_request = requests.get(photos_url, params=photo_payload)
	
	photo_type = imghdr.what("", photo_request.content)
	photo_name = "static/" + query + "." + photo_type

	with open(photo_name, "wb") as photo:
		photo.write(photo_request.content)

	return "<img src=" + photo_name + ">"

@locationApp.route("/sendRequestCurrentLocation/")
def currentLocation():
	return render_template("currentLocation.html")