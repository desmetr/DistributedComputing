$(document).ready(function() 
{

  $("#searchMap").click(function()
  {
    console.info("yes 1");
    var searchReq = $.get("/sendRequestMap/" + $("#query").val());
    searchReq.done(function(data) 
    {
      $("#googleResults").html(data);
    });
  });

  $("#searchPhoto").click(function()
  {
    console.info("yes 2");
    var searchReq = $.get("/sendRequestPhoto/" + $("#query").val());
    searchReq.done(function(data) 
    {
      $("#googleResults").html(data);
    });
  });

  // $("#currentLocation").click(function() 
  // {
  //   console.log("yes 3");
  //   var searchReq = $.get("/sendRequestOthers/");
    // searchReq.done(function(data) 
    // {
    //   console.info("yes 4");
    //   // $("#locationScript").html(data);
    // });
  // });
});

/*
var map, marker, infoWindow;
            function initMap()
            {
              var defaultLocation = {lat: 51.219, lng: 4.402}; // Default location is Antwerp

                map = new google.maps.Map(document.getElementById('geolocation'), {
                    center: defaultLocation, 
                    zoom: 15, 
                    gestureHandling: 'cooperative'}); 

                // marker = new google.maps.Marker({
                //    position: defaultLocation, 
                //    map: map,
                //    style: "blue",
                //    label: "hello world"});

                infoWindow = new google.maps.InfoWindow;

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
                        // marker.setPosition(pos);
                        infoWindow.setPosition(pos);
                        infoWindow.setContent("Hello World");
                        infoWindow.open(map);
                    },
                    function()
                    {
                        handleLocationError(true, infoWindow, map.getCenter());
                    });
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
                infoWindow.setContent(browserHasGeoLocation ? "Error: The Geolocation service failed." : "Error: Your browser doesn't support geolocation.");
                infoWindow.open(map);
            }
            */