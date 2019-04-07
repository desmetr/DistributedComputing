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