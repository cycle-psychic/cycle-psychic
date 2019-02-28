// variable for the Google Map
var map;  

// url for the Dublin Bikes API
var urlBikes = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=fd4562884252e255617667387120a3a9ea10a259";

// function that initialises the map
function initMap() {   
    // create the map
    map = new google.maps.Map(document.getElementById('map'), {
    // map will be centred on these co-ordinates when it loads
    center: {lat: 53.347, lng: -6.268},
    // initial level of zoom when map loads - 15 is street level
    zoom: 13.5,
    mapTypeControl: false
    });

    // call the Dublin Bikes API directly using JQuery
    $.getJSON(urlBikes, null, function(data) {

        // add markers to the map - loop through each station in the JSON object
        for (var i = 0; i < data.length; i++) {
            
            // get the latitude and longitude for the station
            var latitude = data[i].position.lat;
            var longitude = data[i].position.lng;
            var latLng = new google.maps.LatLng(latitude, longitude);

            // generate the marker for the station and place on the map
            var marker = new google.maps.Marker({
                position: latLng,
                map: map
                });
            };
        });
}