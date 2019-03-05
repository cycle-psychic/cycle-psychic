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
    // turn off some default controls
    mapTypeControl: false,
    fullscreenControl: false
    });

    // call the Dublin Bikes API directly using JQuery
    $.getJSON(urlBikes, null, function(data) {
        // call the addMarkers function
        addMarkers(data);
    });
}

//function for adding markers to the map
function addMarkers(data) {
    // add markers to the map - loop through each station in the JSON object
    for (var i = 0; i < data.length; i++) {
        
        // get the latitude and longitude for the station
        var latitude = data[i].position.lat;
        var longitude = data[i].position.lng;
        var latLng = new google.maps.LatLng(latitude, longitude);

        // get the occupancy info for each station
        var totalStands = data[i].bike_stands;
        var availableBikes = data[i].available_bikes;
        // calculate the percentage of available bikes
        var percentAvailable = (availableBikes/totalStands)*100;

        //get payment info for each station
        var cardPayments = data[i].banking;

        // check which icon the marker should use based on percentage & payment types
        if (cardPayments == true) {
            if (percentAvailable >= 67) {
                var urlIcon = "../icons/Marker-Green-euro.png";  // use the red marker with euro symbol
            }
            else if (percentAvailable >= 33) {
                var urlIcon = "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png";  // use the orange marker with euro symbol
            }
            else {
                var urlIcon = "http://maps.google.com/mapfiles/ms/icons/red-dot.png";  // use the green marker with euro symbol
            }
        }
        else {
            if (percentAvailable >= 67) {
                var urlIcon = "http://maps.google.com/mapfiles/ms/icons/green.png";  // use the red marker without euro symbol
            }
            else if (percentAvailable >= 33) {
                var urlIcon = "http://maps.google.com/mapfiles/ms/icons/yellow.png";  // use the orange marker without euro symbol
            }
            else {
                var urlIcon = "http://maps.google.com/mapfiles/ms/icons/red.png";  // use the green marker without euro symbol
            }
        }

        // generate the marker for the station and place on the map
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            icon: {
                url: urlIcon
            }
        });
    };
};