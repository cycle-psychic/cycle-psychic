// variable for the Google Map
var map;  

// url for the Dublin Bikes API
var urlBikes = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=fd4562884252e255617667387120a3a9ea10a259";

// global variable to track open pop-ups
// set to false initially until a pop-up is opened
var prevPopup = false;

// set up arrays to store markers
// these will be used later to add/remove markers from the map
var bikeMarkers = [];
var standMarkers = [];

// declare variables for the buttons (so that they have global scope)
var bikeFilterDiv;
var bikeFilter;
var standFilterDiv;
var standFilter;

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

    //call the addButtons function to add buttons to the map
    addButtons();

    // call the Dublin Bikes API directly using JQuery
    $.getJSON(urlBikes, null, function(data) {
        // call the addMarkers function
        addMarkers(data);
        // call the showMarkers function with "bike" as input
        // because bikes should be shown by default
        showMarkers("bike");
    });
}

// function for adding markers to the map
function addMarkers(data) {
    // add markers to the map - loop through each station in the JSON object
    for (var i = 0; i < data.length; i++) {
        
        // get the latitude and longitude for the station
        var latitude = data[i].position.lat;
        var longitude = data[i].position.lng;
        var latLng = new google.maps.LatLng(latitude, longitude);

        // get the station status i.e. open or closed
        var stationStatus = data[i].status;

        // get the station name - for the pop-up
        // using 'address' from the JSON file as the station address is 
        // always the same as the station name but has correct capitalisation
        var stationName = data[i].address;

        // get the occupancy info for each station
        var totalStands = data[i].bike_stands;
        var availableBikes = data[i].available_bikes;
        var availableStands = data[i].available_bike_stands;

        // calculate the percentage of available bikes & stands
        var percentAvailable = (availableBikes/totalStands)*100;
        var percentFree = (availableStands/totalStands)*100;

        // get payment info for each station
        var cardPayments = data[i].banking;
        // set text to display on pop-up
        if (cardPayments) {  //if card payments are accepted
            paymentText = "Credit Card Accepted"
        }
        else {
            paymentText = "Credit Card Not Accepted"
        }

        // check which icon should be use based on percentage available & payment types
        // first check if the station is closed
        if (stationStatus == 'CLOSED') {
            // use the grey marker for bike and stand markers
            var urlBikes = "/static/icons/Marker-closed.png";  
            var urlStands = "/static/icons/Marker-closed.png"; 
        }
        else {
            // if the station is not closed, check if it accepts card payments
            // then check how many bikes are available and assign marker
            if (cardPayments) {  
                // if card payments are accepted, set images for bike markers
                if (availableBikes == 0) {
                    var urlBikes = "/static/icons/Marker-empty-euro1.png"; // use the empty marker with euro symbol
                }
                else if (percentAvailable >= 67) {
                    var urlBikes = "/static/icons/Marker-Green-euro.png";  // use the green marker with euro symbol
                }
                else if (percentAvailable >= 33) {
                    var urlBikes = "/static/icons/Marker-Orange-euro.png";  // use the orange marker with euro symbol
                }
                else {
                    var urlBikes = "/static/icons/Marker-Red-euro.png";  // use the red marker with euro symbol
                }
                // then set images for stand markers
                if (availableStands == 0) {
                    var urlStands = "/static/icons/Marker-empty-stands-euro.png"; // use the empty marker with euro symbol
                }
                else if (percentFree >= 67) {
                    var urlStands = "/static/icons/Marker-Green-stands-euro.png";  // use the green marker with euro symbol
                }
                else if (percentFree >= 33) {
                    var urlStands = "/static/icons/Marker-Orange-stands-euro.png";  // use the orange marker with euro symbol
                }
                else {
                    var urlStands = "/static/icons/Marker-Red-stands-euro.png";  // use the red marker with euro symbol
                }
            }
            // if the station doesn't accept card, check how many bikes/stands are available and assign markers
            else { 
                // set images for bike markers
                if (availableBikes == 0) {
                    var urlBikes = "/static/icons/Marker-empty.png"; // use the empty marker without euro symbol
                }
                else if (percentAvailable >= 67) {
                    var urlBikes = "/static/icons/Marker-Green.png";  // use the green marker without euro symbol
                }
                else if (percentAvailable >= 33) {
                    var urlBikes = "/static/icons/Marker-Orange.png";  // use the orange marker without euro symbol
                }
                else {
                    var urlBikes = "/static/icons/Marker-Red.png";  // use the red marker without euro symbol
                }
                // set images for stand markers
                if (availableStands == 0) {
                    var urlStands = "/static/icons/Marker-empty-stands.png"; // use the empty marker without euro symbol
                }
                else if (percentFree >= 67) {
                    var urlStands = "/static/icons/Marker-Green-stands.png";  // use the green marker without euro symbol
                }
                else if (percentFree >= 33) {
                    var urlStands = "/static/icons/Marker-Orange-stands.png";  // use the orange marker without euro symbol
                }
                else {
                    var urlStands = "/static/icons/Marker-Red-stands.png";  // use the red marker without euro symbol
                }
            }
        }

        // create an object for the bike icon
        var bikeIcon = {
            url: urlBikes, // url for the image
            scaledSize: new google.maps.Size(60, 60), // size of the image
            origin: new google.maps.Point(0, 0), // origin
            anchor: new google.maps.Point(30, 60) // anchor
        };

        // create an object for the stand icon
        var standIcon = {
            url: urlStands, // url for the image
            scaledSize: new google.maps.Size(60, 60), // size of the image
            origin: new google.maps.Point(0, 0), // origin
            anchor: new google.maps.Point(30, 60) // anchor
        };

        // create a variable to hold the content for the pop-up window
        // this will be the same for both types of markers
        var content = '<div style="color:rgb(89, 89, 89); width: 220px;">' +
            '<h1 style="font-size:120%; text-align:center; padding: 5px 8px 3px;">' + stationName + '</h1>' +
            '<div style="font-weight: bold; padding-bottom: 10px;">' + 
            '<table><tr>' +
            '<td style="width:40px;">' + 
            '<img src="/static/icons/bicycle.png" style="width:35px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
            '<td>' + availableBikes + ' Available</td></tr>' +
            '<td style="width:40px;">' +
            '<img src="/static/icons/stands.png" style="width:30px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
            '<td>' + availableStands + ' Free</td></tr>' +
            '<td style="width:40px;">' +
            '<img src="/static/icons/euro_symbol.png" style="width:25px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
            '<td>' + paymentText + '</td></tr></table></div>';

        // create an object for the pop-up
        var popup = new google.maps.InfoWindow();

        // generate a marker object for the station for bikes
        var bikeMarker = new google.maps.Marker({
            position: latLng,  
            //map: map,
            icon: bikeIcon,  
            title: stationName //this will show the station name when user hovers over marker
        });

        // generate a marker object for the station for stands
        var standMarker = new google.maps.Marker({
            position: latLng,  
            //map: map,
            icon: standIcon,  
            title: stationName //this will show the station name when user hovers over marker
        });

        // add a listener to each type of marker that displays the pop-up on click
        google.maps.event.addListener(bikeMarker,'click', (function(bikeMarker, content, popup){ 
            return function() {
                // if a pop-up has already been opened, close it
                if (prevPopup) {
                    prevPopup.close();
                }

                // assign the current pop-up to the PrevPopup variable
                prevPopup = popup;

                // set the content and open the popup
                popup.setContent(content);
                popup.open(map,bikeMarker);
            };
        })(bikeMarker,content,popup));

        google.maps.event.addListener(standMarker,'click', (function(standMarker, content, popup){ 
            return function() {
                // if a pop-up has already been opened, close it
                if (prevPopup) {
                    prevPopup.close();
                }

                // assign the current pop-up to the PrevPopup variable
                prevPopup = popup;

                // set the content and open the popup
                popup.setContent(content);
                popup.open(map,standMarker);
            };
        })(standMarker,content,popup));     

        // add each marker to the relevant markers array
        // this will be used later to add/remove markers from the map
        bikeMarkers.push(bikeMarker);
        standMarkers.push(standMarker);
    };
};

// function that creates buttons to add to the map
function addButtons() {
    // create a div to hold the button for the bike filter
    bikeFilterDiv = document.createElement('div');
    // call the BikeFilter function to create the button
    bikeFilter = new BikeFilter(bikeFilterDiv, map);

    // create a div to hold the button for the stand filter
    standFilterDiv = document.createElement('div');
    // call the BikeFilter function to create the button
    standFilter = new StandFilter(standFilterDiv, map);

    // set positions for the buttons
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(bikeFilterDiv);
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(standFilterDiv);
}

// function for creating the bike filter button
function BikeFilter(controlDiv, map) {
    // Set CSS for the button
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.backgroundImage = 'url("/static/icons/bicycle.png")';
    controlUI.style.backgroundSize = '48px';
    controlUI.style.backgroundPosition = 'center';
    controlUI.style.backgroundRepeat = 'no-repeat';
    controlUI.style.border = '2px solid #fff';
    controlUI.style.borderRadius = '2px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.15)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.textAlign = 'center';
    controlUI.style.width = '33px';
    controlUI.style.height = '33px';
    controlUI.style.marginRight = '8px';
    controlUI.style.marginTop = '16px';
    controlUI.style.marginBottom = '6px';
    controlUI.style.display = 'flex';
    controlUI.style.alignContent = 'center';
    controlUI.style.justifyContent = 'center';
    //controlUI.title = '...';
    controlDiv.appendChild(controlUI);

    // on hover, change icon colour to black
    controlDiv.addEventListener('mouseenter', function() {
        controlUI.style.backgroundImage = 'url("/static/icons/bicycle-black.png")';
    });
    controlDiv.addEventListener('mouseleave', function() {
        controlUI.style.backgroundImage = 'url("/static/icons/bicycle.png")';
    });

    // On click, display markers showing bike availability
    controlUI.addEventListener('click', function() {
        // hide stand markers
        hideMarkers("stand");
        // show bike markers
        showMarkers("bike");
    });
}

// function for creating the stand filter button
function StandFilter(controlDiv, map) {
    // Set CSS for the button
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.backgroundImage = 'url("/static/icons/stands.png")';
    controlUI.style.backgroundSize = '38px';
    controlUI.style.backgroundPosition = 'center';
    controlUI.style.backgroundRepeat = 'no-repeat';
    controlUI.style.border = '2px solid #fff';
    controlUI.style.borderRadius = '2px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.15)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.textAlign = 'center';
    controlUI.style.width = '33px';
    controlUI.style.height = '33px';
    controlUI.style.marginRight = '8px';
    //controlUI.style.marginTop = '16px';
    controlUI.style.marginBottom = '6px';
    controlUI.style.display = 'flex';
    controlUI.style.alignContent = 'center';
    controlUI.style.justifyContent = 'center';
    //controlUI.title = '...';
    controlDiv.appendChild(controlUI);

    // on hover, change icon colour to black
    controlDiv.addEventListener('mouseenter', function() {
        controlUI.style.backgroundImage = 'url("/static/icons/stands-black.png")';
    });
    controlDiv.addEventListener('mouseleave', function() {
        controlUI.style.backgroundImage = 'url("/static/icons/stands.png")';
    });

    // On click, display markers showing stand availability
    controlUI.addEventListener('click', function() {
        // hide bike markers
        hideMarkers("bike");
        // show stand markers
        showMarkers("stand");
    });
}

// function for hiding markers on the map
function hideMarkers(type) {
    // if a pop-up is open, close it
    if (prevPopup) {
        prevPopup.close();
    }
    // set PrevPopup to false as all pop-ups should be closed when filter button is clicked
    prevPopup = false;

    if (type=="bike") {
        // loop through each marker in the markers array and set the map to null
        for (var i = 0; i < bikeMarkers.length; i++) {
            bikeMarkers[i].setMap(null);
        }
    }
    else if (type=="stand") {
        for (var i = 0; i < standMarkers.length; i++) {
            standMarkers[i].setMap(null);
        }
    }
}

// function to show the relevant markers on the map
function showMarkers(type) {
    if (type=="bike") {
        for (var i = 0; i < bikeMarkers.length; i++) {
            bikeMarkers[i].setMap(map);
        }
    }
    else if (type=="stand") {
        for (var i = 0; i < standMarkers.length; i++) {
            standMarkers[i].setMap(map);
        }
    }
}