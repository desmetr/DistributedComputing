function checkRadius(centerLat, centerLng, newLat, newLng, zoomLevel)
{
	var km = 5;

	var kX = Math.cos(Math.PI * centerLat / 180.0) * kY;
	var kY = 40000 / 360;

	var dX = Math.abs(centerLng - newLng) * kX;
	var dY = Math.abs(centerLat - newLat) * kY;

	return Math.sqrt(dX * dX + dY * dY) <= km;
}

function initMap()
{
	var map, yourMarker;
	var zoomLevel = 15;
	var defaultLocation = {lat: 51.219, lng: 4.402}; // Default location is Antwerp
	var currentPos = defaultLocation;

	map = new google.maps.Map(document.getElementById('geolocation'), {
		center: defaultLocation,
		zoom: zoomLevel,
		gestureHandling: 'cooperative'});

	yourMarker = new google.maps.Marker({
 		position: defaultLocation,
 		map: map,
 		label: 'Your position'});

	// Try HTML5 geolocation
	if (navigator.geolocation)
	{
	    navigator.geolocation.getCurrentPosition(function(position)
	    {
	        currentPos = 
	        {
	            lat: position.coords.latitude,
	            lng: position.coords.longitude
	        };

	        map.setCenter(currentPos);
	        yourMarker.setPosition(currentPos);
	    },

    function()
    {
        handleLocationError(true, infoWindow, map.getCenter());
    });

	function callbackToServer(name) 
	{
		$.ajax({
			type: "POST",
			contentType: "application/json;charset=utf-8",
			url: "http://localhost:5000/callback/" + encodeURIComponent(name),
			traditional: "true",
			data: JSON.stringify(name),
			dataType: "json"
		})
	}
			var marker1 = new google.maps.Marker({
				position: {lat: 51.216948, lng: 4.696734999999999},
			
				map: map,
				
				label: 'a'});

			marker1.addListener('click', function() {
				callbackToServer(marker1.label);
			})

			
			var marker2 = new google.maps.Marker({
				position: {lat: 51.1845547, lng: 4.4212374},
			
				map: map,
				
				label: 'b'});

			marker2.addListener('click', function() {
				callbackToServer(marker2.label);
			})

				}
	else
	{
		// Browser doesn't support Geolocation
		handleLocationError(false, infoWindow, map.getCenter());
	}
}

function handleLocationError(browserHasGeoLocation, infoWindow, pos)
{
	infoWindow.setPosition(pos);
	infoWindow.setContent(browserHasGeoLocation ? 'Error: The Geolocation service failed.' : 'Error: Your browser does not support geolocation.');
	infoWindow.open(map);
}