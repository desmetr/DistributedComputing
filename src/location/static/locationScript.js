function initMap()
{
	var map, yourMarker;
	var defaultLocation = {lat: 51.219, lng: 4.402}; // Default location is Antwerp

	map = new google.maps.Map(document.getElementById('geolocation'), {
		center: defaultLocation,
		zoom: 15,
		gestureHandling: 'cooperative'});

	yourMarker = new google.maps.Marker({
 		position: defaultLocation,
 		map: map,
 		label: 'hello world'});

	// Try HTML5 geolocation
	if (navigator.geolocation)
	{
	    navigator.geolocation.getCurrentPosition(function(position)
	    {
	        var pos = 
	        {
	            lat: position.coords.latitude,
	            lng: position.coords.longitude
	        };

	        map.setCenter(pos);
	        yourMarker.setPosition(pos);
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
			var marker0 = new google.maps.Marker({
				position: {lat: 51.2200995, lng: 4.6891696},
				map: map,
				icon: '/static/carrot.ico',
				label: 'Alice'});

			marker0.addListener('click', function() {
				callbackToServer(marker0.label);
			})

			
			var marker1 = new google.maps.Marker({
				position: {lat: 51.22742419999999, lng: 4.699526200000001},
				map: map,
				icon: '/static/potato.ico',
				label: 'Bob'});

			marker1.addListener('click', function() {
				callbackToServer(marker1.label);
			})

			
			var marker2 = new google.maps.Marker({
				position: {lat: 51.2154663, lng: 4.6969522},
				map: map,
				icon: '/static/eggplant.ico',
				label: 'Charlie'});

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