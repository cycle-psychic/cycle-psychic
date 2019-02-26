//variable for the Google Map
var map;  

// function that initialises the map
function initMap() {   
    // create the map
    map = new google.maps.Map(document.getElementById('map'), {
    // map will be centred on these co-ordinates when it loads
    center: {lat: 53.3453, lng: -6.2722},
    // initial level of zoom when map loads - 15 is street level
    zoom: 14,
    mapTypeControl: false
    });

    var testmarker = new google.maps.Marker({
        position: {lat: 53.3453, lng: -6.2722}, //marker position
        map: map, //map that the marker will be placed on
        });
}