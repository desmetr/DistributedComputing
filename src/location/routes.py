from flask import Flask, render_template, jsonify
import requests
import imghdr
from location.key import key
from location import locationApp
from location.forms import LocationForm

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"
photos_url = "https://maps.googleapis.com/maps/api/place/photo"
template_embed_url = "https://www.google.com/maps/embed/v1/place?key=" + key + "&q="
# geo_location_url = "https://maps.googleapis.com/maps/api/js?key=" + key + "&callback=initMap"         

@locationApp.route("/location", methods=["GET"])
def layout():
	form = LocationForm()
	return render_template("layout.html", form=form)

@locationApp.route("/sendRequestMap/<string:query>")
def resultsMap(query):
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

@locationApp.route("/sendRequestOthers/", methods=["GET", "POST"])
def showOthersOnMap():
	tempAddresses = [['Alice', 'goormansstraat 20, zandhoven', '/static/carrot.ico'], 
					 ['Bob', 'molenheide 104, pulderbos', '/static/potato.ico'], 
					 ['Charlie', 'viesenboslaan 32, pulderbos', '/static/eggplant.ico']]

	locationScriptStart = open("static/locationScriptStart.js", "r")
	locationScript = locationScriptStart.read()
	locationScriptStart.close()

	for counter, address in enumerate(tempAddresses):
		search_payload = {"key" : key, "query" : address[1]}
		search_request = requests.get(search_url, params=search_payload)
		search_json = search_request.json()

		location = search_json["results"][0]["geometry"]["location"]
		lat = location["lat"]
		lng = location["lng"]

		locationScript += """
			var marker""" + str(counter) + """ = new google.maps.Marker({
				position: {lat: """ + str(lat) + """, lng: """ + str(lng) + """},
				map: map,
				icon: '""" + address[2] + """',
				label: '""" + address[0] + """'});

			marker""" + str(counter) + """.addListener('click', function() {
				callbackToServer(marker""" + str(counter) + """.label);
			})

			"""
	
	locationScriptEnd = open("static/locationScriptEnd.js", "r")
	locationScript += locationScriptEnd.read()
	locationScriptEnd.close()

	f = open("static/locationScript.js", "w+")
	f.write(locationScript)
	f.close()
	
	return render_template("location.html")

@locationApp.route("/callback/<string:query>", methods=["GET", "POST", "OPTIONS"])
def callback(query):
	print("You clicked on ", query)
	return "200 OK"