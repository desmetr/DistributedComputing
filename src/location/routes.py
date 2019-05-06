from flask import Flask, render_template, jsonify, redirect
from location.key import key
from location import locationApp
from location.forms import LocationForm
import requests
import imghdr
import urlsConfig

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"
photos_url = "https://maps.googleapis.com/maps/api/place/photo"
template_embed_url = "https://www.google.com/maps/embed/v1/place?key=" + key + "&q="
# geo_location_url = "https://maps.googleapis.com/maps/api/js?key=" + key + "&callback=initMap"         

IN_RADIUS = False
ICON = False

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

@locationApp.route("/sendRequestOthers", methods=["GET", "POST"])
def showOthersOnMap():
	# Structure of an address:
	#	[id, username, lat, lng]
	# can be extended to
	#	[id, username, lat, lng, icon]

	addresses = getAllAddressesFromUsers()

	locationScriptStart = open("static/locationScriptStart.js", "r")
	locationScript = locationScriptStart.read()
	locationScriptStart.close()

	# currentVegetables = ['potato', 'tomato']
	# currentFruits = ['apple', 'strawberry']
	currentHerbs = ['basilicum']

	for _, address in enumerate(addresses):
		lat = address[2]
		lng = address[3]

		currentVegetables = requests.get(urlsConfig.URLS['garden_url'] + "/" + str(address[0]) + "/getVegetables")
		currentFruits = requests.get(urlsConfig.URLS['garden_url'] + "/" + str(address[0]) + "/getFruits")
		currentHerbs = requests.get(urlsConfig.URLS['garden_url'] + "/" + str(address[0]) + "/getHerbs")

		if ICON:
			locationScript += """
				icon: '""" + address[4] + """',
				"""

		contentString = getContentString(address, currentVegetables.json(), currentFruits.json(), currentHerbs.json())
				
		# label: '""" + address[1] + """'});
		locationScript += """
			var contentString = """ + contentString + """;
			var infoWindow""" + str(address[0]) + """ = new google.maps.InfoWindow({
				position: {lat: """ + str(lat) + """, lng: """ + str(lng) + """},
				content: contentString,"""

		if not IN_RADIUS:
			locationScript += """
				map: map,
				"""

		locationScript += """
			})

			"""

		contentString = ""
	
		if IN_RADIUS:
			locationScript += """
				if (checkRadius(currentPso.lat, currentPos.lng, """ + str(lat) + """, """ + str(lng) + """, zoomLevel))
					marker""" + str(address[0]) + """.setMap(null);
				else
					marker""" + str(address[0]) + """.setMap(map);
			"""

	locationScriptEnd = open("static/locationScriptEnd.js", "r")
	locationScript += locationScriptEnd.read()
	locationScriptEnd.close()

	f = open("static/locationScript.js", "w+")
	f.write(locationScript)
	f.close()
	
	return render_template("location.html")

@locationApp.route("/callback/<id>", methods=["GET", "POST", "OPTIONS"])
def callback(id):
	print("You clicked on user with id ", id)
	response = requests.get(urlsConfig.URLS['single_user_url'], params={'user_id': str(id)})

	responseData = response.json()["data"]
	return redirect(urlsConfig.URLS['garden_url'])

def getAllAddressesFromUsers():
	addresses = []

	# {
	# 	"id": self.id,
	#	"username": self.username,
	#	"email": self.email,
	#	"location": self.location,
	#	"lat": self.lat,
	#	"lng": self.lng,
	# }

	response = requests.get(urlsConfig.URLS['users_url'])

	for user in response.json():
		addresses.append([user["id"], user["username"], user["lat"], user["lng"]])

	return addresses

def getContentString(address, currentVegetables, currentFruits, currentHerbs):
	contentString = """
		'<div id="content">' +
		'User: <b>""" + address[1] + """</b>' +
		'<br>Vegetables:' +
		'<ul>' +
		"""

	for vegetable in currentVegetables:
		contentString += """'<li><b>""" + str(vegetable[0]) + """</b> (""" + str(vegetable[2]) + """)</li>'+"""

	contentString += """
		'</ul>'+
		'Fruits:'+
		'<ul>'+
	"""

	for fruit in currentFruits:			
		contentString += """'<li><b>""" + str(fruit[0]) + """</b> (""" + str(fruit[2]) + """)</li>'+"""

	contentString += """
		'</ul>'+
		'Herbs:'+
		'<ul>'+
	"""

	for herb in currentHerbs:
		contentString += """'<li><b>""" + str(herb[0]) + """</b> (""" + str(herb[2]) + """)</li>'+"""

	contentString += """'</ul>'+"""

	# TODO correct urls
	contentString += """'\t<a href=\"""" + urlsConfig.URLS['garden_url'] + """">Go To Garden</a>'+"""
	# contentString += """'\t<a href=\"""" + urlsConfig.URLS['garden_url'] + str(address[0]) + """">Go To User's Garden</a>'+"""
	contentString += """'<a href=\"""" + urlsConfig.URLS['chat_url'] + """">Chat With User</a>'+"""
	# contentString += '<a href="' + urlsConfig.URLS['chat_url'] + '/' + str(address[0]) + '">Chat With User</a>'
	
	contentString += """'<a href=\"""" + urlsConfig.URLS['friendship_url'] + str(address[0]) + """>Become Friends</a>'+"""
	
	contentString += "'</div>'"

	return contentString