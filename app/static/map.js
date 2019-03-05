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

        //get the station status i.e. open or closed
        var stationStatus = data[i].status;

        // get the occupancy info for each station
        var totalStands = data[i].bike_stands;
        var availableBikes = data[i].available_bikes;
        // calculate the percentage of available bikes
        var percentAvailable = (availableBikes/totalStands)*100;

        //get payment info for each station
        var cardPayments = data[i].banking;

        // check which icon the marker should use based on percentage & payment types
        // first check station if the station is closed
        if (stationStatus == 'CLOSED') {
            var urlIcon = "/static/icons/Marker-closed.png";  // use the grey marker
        }
        else {
            // if the station is not closed, check if it accepts card payments
            // then check how many bikes are availble and assign marker
            if (cardPayments == true) {
                if (percentAvailable >= 67) {
                    var urlIcon = "/static/icons/Marker-Green-euro.png";  // use the green marker with euro symbol
                }
                else if (percentAvailable >= 33) {
                    var urlIcon = "/static/icons/Marker-Orange-euro.png";  // use the orange marker with euro symbol
                }
                else {
                    var urlIcon = "/static/icons/Marker-Red-euro.png";  // use the red marker with euro symbol
                }
            }
            // if the station doesn't accept card, check how many bikes are available and assing marker
            else {
                if (percentAvailable >= 67) {
                    var urlIcon = "/static/icons/Marker-Green.png";  // use the green marker without euro symbol
                }
                else if (percentAvailable >= 33) {
                    var urlIcon = "/static/icons/Marker-Orange.png";  // use the orange marker without euro symbol
                }
                else {
                    var urlIcon = "/static/icons/Marker-Red.png";  // use the red marker without euro symbol
                }
            }
        }

        // create an object for the image icon
        var imageicon = {
            url: urlIcon, // url for the image
            scaledSize: new google.maps.Size(50, 50), // size of the image
            origin: new google.maps.Point(0, 0), // origin
            anchor: new google.maps.Point(25, 50) // anchor
        };

        // generate the marker object for the station and place on the map
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            icon: imageicon
        });
    };
};