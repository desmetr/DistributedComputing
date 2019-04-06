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

locationScriptStart =  "function initMap()\n"
locationScriptStart += "{\n"
locationScriptStart += "	var map, yourMarker;\n"
locationScriptStart += "	var defaultLocation = {lat: 51.219, lng: 4.402}; // Default location is Antwerp\n"
locationScriptStart += "\n"
locationScriptStart += "	map = new google.maps.Map(document.getElementById('geolocation'), {\n"
locationScriptStart += "		center: defaultLocation,\n" 
locationScriptStart += "		zoom: 15,\n" 
locationScriptStart += "		gestureHandling: 'cooperative'});\n"	
locationScriptStart += "\n"
locationScriptStart += "	yourMarker = new google.maps.Marker({\n"
locationScriptStart += " 		position: defaultLocation,\n" 
locationScriptStart += " 		map: map,\n"
locationScriptStart += " 		label: 'hello world'});\n"
locationScriptStart += "\n"
locationScriptStart += "	// Try HTML5 geolocation\n"
locationScriptStart += "	if (navigator.geolocation)\n"
locationScriptStart += "{\n"
locationScriptStart += "    navigator.geolocation.getCurrentPosition(function(position)\n"
locationScriptStart += "    {\n"
locationScriptStart += "        var pos = \n"
locationScriptStart += "        {\n"
locationScriptStart += "            lat: position.coords.latitude,\n"
locationScriptStart += "            lng: position.coords.longitude\n"
locationScriptStart += "        };\n"
locationScriptStart += "\n"
locationScriptStart += "        map.setCenter(pos);\n"
locationScriptStart += "        yourMarker.setPosition(pos);\n"
locationScriptStart += "    },\n"
locationScriptStart += "\n"
locationScriptStart += "    function()\n"
locationScriptStart += "    {\n"
locationScriptStart += "        handleLocationError(true, infoWindow, map.getCenter());\n"
locationScriptStart += "    });\n"

locationScriptEnd = "	}\n"
locationScriptEnd += "	else\n"
locationScriptEnd += "	{\n"
locationScriptEnd += "		// Browser doesn't support Geolocation\n"
locationScriptEnd += "		handleLocationError(false, infoWindow, map.getCenter());\n"
locationScriptEnd += "	}\n"
locationScriptEnd += "}\n"
locationScriptEnd += "\n"
locationScriptEnd += "function handleLocationError(browserHasGeoLocation, infoWindow, pos)\n"
locationScriptEnd += "{\n"
locationScriptEnd += "	infoWindow.setPosition(pos);\n"
locationScriptEnd += "	infoWindow.setContent(browserHasGeoLocation ? 'Error: The Geolocation service failed.' : 'Error: Your browser does not support geolocation.');\n"
locationScriptEnd += "	infoWindow.open(map);\n"
locationScriptEnd += "}\n"
         

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
	tempAddresses = [['Alice', 'goormansstraat 20, zandhoven'], ['Bob', 'molenheide 104, pulderbos'], ['Charlie', 'viesenboslaan 32, pulderbos']]
	locationScript = locationScriptStart

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
				label: '""" + address[0] + """'});

			"""
	
	locationScript += locationScriptEnd

	f = open("static/locationScript.js", "w+")
	f.write(locationScript)
	f.close()
	
	return render_template("location.html")