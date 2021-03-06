//load all required images for markers
var markerClosed = "/static/icons/Marker-closed.png";
var markerEmptyEuro = "/static/icons/Marker-empty-euro1.png";
var markerGreenEuro = "/static/icons/Marker-Green-euro.png";
var markerOrangeEuro = "/static/icons/Marker-Orange-euro.png";
var markerRedEuro = "/static/icons/Marker-Red-euro.png";
var markerEmptyStandsEuro = "/static/icons/Marker-empty-stands-euro.png";
var markerGreenStandsEuro = "/static/icons/Marker-Green-stands-euro.png";
var markerOrangeStandsEuro = "/static/icons/Marker-Orange-stands-euro.png";
var markerRedStandsEuro = "/static/icons/Marker-Red-stands-euro.png";
var markerEmpty = "/static/icons/Marker-empty.png";
var markerGreen = "/static/icons/Marker-Green.png";
var markerOrange = "/static/icons/Marker-Orange.png";
var markerRed = "/static/icons/Marker-Red.png";
var markerEmptyStands = "/static/icons/Marker-empty-stands.png";
var markerGreenStands = "/static/icons/Marker-Green-stands.png";
var markerOrangeStands = "/static/icons/Marker-Orange-stands.png";
var markerRedStands = "/static/icons/Marker-Red-stands.png";
// predictive markers
var markerPredictEuro = "/static/icons/Marker-Predictive-euro.png";
var markerPredictHalfEuro = "/static/icons/Marker-Predictive-half-euro.png";
var markerPredictEmptyEuro = "/static/icons/Marker-Predictive-empty-euro.png";
var markerPredictStandsEuro= "/static/icons/Marker-Predictive-stands-euro1.png";
var markerPredictHalfStandsEuro = "/static/icons/Marker-Predictive-half-stands-euro.png";
var markerPredictEmptyStandsEuro = "/static/icons/Marker-Predictive-empty-stands-euro.png";
var markerPredict = "/static/icons/Marker-Predictive.png";
var markerPredictHalf = "/static/icons/Marker-Predictive-half.png";
var markerPredictEmpty = "/static/icons/Marker-Predictive-empty.png";
var markerPredictStands = "/static/icons/Marker-Predictive-stands.png";
var markerPredictHalfStands = "/static/icons/Marker-Predictive-half-stands.png";
var markerPredictEmptyStands = "/static/icons/Marker-Predictive-empty-stands.png";

//load all required images for buttons
var bicycle = "/static/icons/bicycle.png";
var stands = "/static/icons/stands.png";
var euroSymbol = "/static/icons/euro_symbol.png";
var bicycleLight = "/static/icons/bicycle-light.png";
var standsLight = "/static/icons/stands-light.png";
var euroSymbolLight = "/static/icons/euro_symbol-light.png";
var bicycleBlack = "/static/icons/bicycle-black.png";
var standsBlack = "/static/icons/stands-black.png";
var euroSymbolBlack = "/static/icons/euro_symbol-black.png";
var crystalBall = "/static/icons/crystal-ball.png";
var crystalBallBlack = "/static/icons/crystal-ball-black.png";
var crystalBallInverted = "/static/icons/crystal-ball-light.png";
var infoSymbol = "/static/icons/info_symbol_invert.png";
var infoSymbolBlack = "/static/icons/info_symbol_black.png";
var infoSymbolInverted = "/static/icons/info_symbol.png";

// variable for the Google Map
var map;  

// url for the Dublin Bikes API
var urlBikesAPI = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=fd4562884252e255617667387120a3a9ea10a259";

// global variable to track open pop-ups
// set to false initially until a pop-up is opened
var prevPopup = false;

// create dictionaries to hold pop-ups for different markers - one for bikes and one for stands
// these will be used to open pop-ups when a station is selected from the dropdown
var bikeMarkerRef = {};
var standMarkerRef = {};
// create dictionaries for prediction mode as well
var bikeMarkerPredictRef = {};
var standMarkerPredictRef = {};

// set up arrays to store markers
// these will be used later to add/remove markers from the map
var bikeMarkers = [];
var bikeMarkersCard = [];
var standMarkers = [];
var standMarkersCard = [];
var bikeMarkersCardPredictive = [];
var standMarkersCardPredictive = [];
var bikeMarkersPredictive = [];
var standMarkersPredictive = [];

// declare variables for the buttons (so that they have global scope)
var bikeFilterDiv;
var bikeFilter;
var bikeFilterUI;
var standFilterDiv;
var standFilter;
var standFilterUI;
var cardFilterDiv;
var cardFilter;
var cardFilterUI;
var predictionFilterDiv;
var predictionFilter;
var predictionFilterUI;
var predictionFormDiv;
var predictionForm;
var predictionFormUI;
var infoFilterDiv;
var infoFilter;
var infoFilterUI;

// declare variables to track which filter is on
// bike filter is on by default, stand and card filters are off by default
var bikeFilterOn = true;
var standFilterOn = false;
var cardFilterOn = false;
// prediction mode is off by default
var predictionMode = false;

// variable to store current prediction date
var predictionDate;

// variable to store predictive style for map
// reference: https://snazzymaps.com/style/98/purple-rain
var predictiveStyle = [
    {
        "featureType": "road",
        "stylers": [
            {
                "hue": "#5e00ff"
            },
            {
                "saturation": -79
            }
        ]
    },
    {
        "featureType": "poi",
        "stylers": [
            {
                "saturation": -78
            },
            {
                "hue": "#6600ff"
            },
            {
                "lightness": -47
            },
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road.local",
        "stylers": [
            {
                "lightness": 22
            }
        ]
    },
    {
        "featureType": "landscape",
        "stylers": [
            {
                "hue": "#6600ff"
            },
            {
                "saturation": -11
            }
        ]
    },
    {},
    {},
    {
        "featureType": "water",
        "stylers": [
            {
                "saturation": -65
            },
            {
                "hue": "#1900ff"
            },
            {
                "lightness": 8
            }
        ]
    },
    {
        "featureType": "road.local",
        "stylers": [
            {
                "weight": 1.3
            },
            {
                "lightness": 30
            }
        ]
    },
    {
        "featureType": "transit",
        "stylers": [
            {
                "visibility": "simplified"
            },
            {
                "hue": "#5e00ff"
            },
            {
                "saturation": -16
            }
        ]
    },
    {
        "featureType": "transit.line",
        "stylers": [
            {
                "saturation": -72
            }
        ]
    },
    {}
];

// function that initialises the map
function initMap() {   
    // create the map
    map = new google.maps.Map(document.getElementById('map'), {
    // map will be centred on these co-ordinates when it loads
    center: {lat: 53.3465, lng: -6.268},
    // initial level of zoom when map loads - 15 is street level
    zoom: 13.8,
    // turn off some default controls
    mapTypeControl: false,
    fullscreenControl: false
    });

    //call the addButtons function to add buttons to the map
    addButtons();

    // call the popDateForm function to populate the dropdown in the prediction form
    popDateForm();

    // call the Dublin Bikes API directly using JQuery
    $.getJSON(urlBikesAPI, null, function(data) {
        // call the addMarkers function
        addMarkers(data);
        // call the showMarkers function with "bike" as input
        // because bikes should be shown by default
        showMarkers("bike");
    })
    // if the call to the Dublin Bikes API fails, then display an error message to the user
    .fail(function() {
        bikeError();
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

        // get the station id - for pop-up when dropdown selected
        var stationId = data[i].number;

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
            paymentText = "Card Not Accepted"
        }

        // check which icon should be use based on percentage available & payment types
        // first check if the station is closed
        if (stationStatus == 'CLOSED') {
            // use the grey marker for bike and stand markers
            var urlBikes = markerClosed;  
            var urlStands = markerClosed; 
        }
        else {
            // if the station is not closed, check if it accepts card payments
            // then check how many bikes are available and assign marker
            if (cardPayments) {  
                // if card payments are accepted, set images for bike markers
                if (availableBikes == 0) {
                    var urlBikes = markerEmptyEuro; // use the empty marker with euro symbol
                }
                else if (percentAvailable >= 67) {
                    var urlBikes = markerGreenEuro;  // use the green marker with euro symbol
                }
                else if (percentAvailable >= 33) {
                    var urlBikes = markerOrangeEuro;  // use the orange marker with euro symbol
                }
                else {
                    var urlBikes = markerRedEuro;  // use the red marker with euro symbol
                }
                // then set images for stand markers
                if (availableStands == 0) {
                    var urlStands = markerEmptyStandsEuro; // use the empty marker with euro symbol
                }
                else if (percentFree >= 67) {
                    var urlStands = markerGreenStandsEuro;  // use the green marker with euro symbol
                }
                else if (percentFree >= 33) {
                    var urlStands = markerOrangeStandsEuro;  // use the orange marker with euro symbol
                }
                else {
                    var urlStands = markerRedStandsEuro;  // use the red marker with euro symbol
                }
            }
            // if the station doesn't accept card, check how many bikes/stands are available and assign markers
            else { 
                // set images for bike markers
                if (availableBikes == 0) {
                    var urlBikes = markerEmpty; // use the empty marker without euro symbol
                }
                else if (percentAvailable >= 67) {
                    var urlBikes = markerGreen;  // use the green marker without euro symbol
                }
                else if (percentAvailable >= 33) {
                    var urlBikes = markerOrange;  // use the orange marker without euro symbol
                }
                else {
                    var urlBikes = markerRed;  // use the red marker without euro symbol
                }
                // set images for stand markers
                if (availableStands == 0) {
                    var urlStands = markerEmptyStands; // use the empty marker without euro symbol
                }
                else if (percentFree >= 67) {
                    var urlStands = markerGreenStands;  // use the green marker without euro symbol
                }
                else if (percentFree >= 33) {
                    var urlStands = markerOrangeStands;  // use the orange marker without euro symbol
                }
                else {
                    var urlStands = markerRedStands;  // use the red marker without euro symbol
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
        var content = '<div style="color:#464646; width: 190px;">' +
            '<h1 style="font-size:120%; text-align:center; padding: 5px 8px 3px;">' + stationName + '</h1>' +
            '<div style="font-weight: bold; padding-bottom: 10px;">' + 
            '<table><tr>' +
            '<td style="width:40px;">' + 
            '<img src=' + bicycle + ' style="width:35px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
            '<td>' + availableBikes + ' Available</td></tr>' +
            '<td style="width:40px;">' +
            '<img src=' + stands + ' style="width:30px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
            '<td>' + availableStands + ' Free</td></tr>' +
            '<td style="width:40px;">' +
            '<img src=' + euroSymbol + ' style="width:25px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
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

        // add the bike marker to the relevant dict
        bikeMarkerRef[stationId] = [bikeMarker, popup, content]

        // generate a marker object for the station for stands
        var standMarker = new google.maps.Marker({
            position: latLng,  
            //map: map,
            icon: standIcon,  
            title: stationName //this will show the station name when user hovers over marker
        });

        // add the stand marker to the relevant dict
        standMarkerRef[stationId] = [standMarker, popup, content]

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
        if (cardPayments) {  //if card payments are accepted
            bikeMarkersCard.push(bikeMarker);
            standMarkersCard.push(standMarker);
        }
        else {
            bikeMarkers.push(bikeMarker);
            standMarkers.push(standMarker);
        }
    };
};

// function that creates buttons to add to the map
function addButtons() {
    // create a div to hold the button for the bike filter
    bikeFilterDiv = document.createElement('div');
    // call the BikeFilter function to create the button
    bikeFilter = new BikeFilter();

    // create a div to hold the button for the stand filter
    standFilterDiv = document.createElement('div');
    // call the BikeFilter function to create the button
    standFilter = new StandFilter();

    // create a div to hold the button for the card filter
    cardFilterDiv = document.createElement('div');
    // call the CardFilter function to create the button
    cardFilter = new CardFilter();

    // create a div to hold the button for the prediction button
    predictionFilterDiv = document.createElement('div');
    // call the PredictionButton function to create the button
    predictionFilter = new PredictionButton();

    // create a div to hold the button for the info button
    infoFilterDiv = document.createElement('div');
    // call the InfoFilter function to create the button
    infoFilter = new InfoFilter();

    // set positions for the buttons
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(predictionFilterDiv);
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(bikeFilterDiv);  
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(standFilterDiv);
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(cardFilterDiv);
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(infoFilterDiv);
}

// function for creating the bike filter button
function BikeFilter() {
    // Set CSS for the button
    bikeFilterUI = document.createElement('div');
    bikeFilterUI.style.backgroundColor = '#464646';
    bikeFilterUI.style.backgroundImage = 'url(' + bicycleLight + ')';
    bikeFilterUI.style.backgroundSize = '48px';
    bikeFilterUI.style.backgroundPosition = 'center';
    bikeFilterUI.style.backgroundRepeat = 'no-repeat';
    bikeFilterUI.style.border = '2px solid #464646';
    bikeFilterUI.style.borderRadius = '2px';
    bikeFilterUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.15)';
    bikeFilterUI.style.cursor = 'pointer';
    bikeFilterUI.style.textAlign = 'center';
    bikeFilterUI.style.width = '36px';
    bikeFilterUI.style.height = '36px';
    bikeFilterUI.style.marginRight = '10px';
    bikeFilterUI.style.marginBottom = '6px';
    bikeFilterUI.style.display = 'flex';
    bikeFilterUI.style.alignContent = 'center';
    bikeFilterUI.style.justifyContent = 'center';
    bikeFilterUI.style.cursor = 'auto';
    bikeFilterDiv.appendChild(bikeFilterUI);

    // On click, display markers showing bike availability
    bikeFilterUI.addEventListener('click', bikeClick);
}

// function for creating the stand filter button
function StandFilter() {
    // Set CSS for the button
    standFilterUI = document.createElement('div');
    standFilterUI.style.backgroundColor = '#fff';
    standFilterUI.style.backgroundImage = 'url(' + stands + ')';
    standFilterUI.style.backgroundSize = '38px';
    standFilterUI.style.backgroundPosition = 'center';
    standFilterUI.style.backgroundRepeat = 'no-repeat';
    standFilterUI.style.border = '2px solid #fff';
    standFilterUI.style.borderRadius = '2px';
    standFilterUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.15)';
    standFilterUI.style.cursor = 'pointer';
    standFilterUI.style.textAlign = 'center';
    standFilterUI.style.width = '36px';
    standFilterUI.style.height = '36px';
    standFilterUI.style.marginRight = '10px';
    standFilterUI.style.marginBottom = '6px';
    standFilterUI.style.display = 'flex';
    standFilterUI.style.alignContent = 'center';
    standFilterUI.style.justifyContent = 'center';
    standFilterUI.title = 'Show Stand Info';
    standFilterDiv.appendChild(standFilterUI);

    // add listeners for the stand filter button
    // this will cause the icon to turn black on hover
    addListeners("stand");

    // On click, display markers showing stand availability
    standFilterUI.addEventListener('click', standClick);
}

// function for creating the card filter button
function CardFilter() {
    // Set CSS for the button
    cardFilterUI = document.createElement('div');
    cardFilterUI.style.backgroundColor = '#fff';
    cardFilterUI.style.backgroundImage = 'url(' + euroSymbol + ')';
    cardFilterUI.style.backgroundSize = '35px';
    cardFilterUI.style.backgroundPosition = 'center';
    cardFilterUI.style.backgroundRepeat = 'no-repeat';
    cardFilterUI.style.border = '2px solid #fff';
    cardFilterUI.style.borderRadius = '2px';
    cardFilterUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.15)';
    cardFilterUI.style.cursor = 'pointer';
    cardFilterUI.style.textAlign = 'center';
    cardFilterUI.style.width = '36px';
    cardFilterUI.style.height = '36px';
    cardFilterUI.style.marginRight = '10px';
    cardFilterUI.style.marginBottom = '6px';
    cardFilterUI.style.display = 'flex';
    cardFilterUI.style.alignContent = 'center';
    cardFilterUI.style.justifyContent = 'center';
    cardFilterUI.title = 'Credit Card Filter';
    cardFilterDiv.appendChild(cardFilterUI);

    // add listeners for the card filter button
    // this will cause the icon to turn black on hover
    addListeners("card");

    // On click, filter to show only stations that accept card
    cardFilterUI.addEventListener('click', cardClick);
}

// function for creating the info button
function InfoFilter() {
    // Set CSS for the button
    infoFilterUI = document.createElement('div');
    infoFilterUI.style.backgroundColor = '#fff';
    infoFilterUI.style.backgroundImage = 'url(' + infoSymbol + ')';
    infoFilterUI.style.backgroundSize = '35px';
    infoFilterUI.style.backgroundPosition = 'center';
    infoFilterUI.style.backgroundRepeat = 'no-repeat';
    infoFilterUI.style.border = '2px solid #fff';
    infoFilterUI.style.borderRadius = '2px';
    infoFilterUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.15)';
    infoFilterUI.style.cursor = 'pointer';
    infoFilterUI.style.textAlign = 'center';
    infoFilterUI.style.width = '36px';
    infoFilterUI.style.height = '36px';
    infoFilterUI.style.marginRight = '10px';
    infoFilterUI.style.marginBottom = '6px';
    infoFilterUI.style.display = 'flex';
    infoFilterUI.style.alignContent = 'center';
    infoFilterUI.style.justifyContent = 'center';
    infoFilterUI.title = 'Information';
    infoFilterDiv.appendChild(infoFilterUI);

    // add listeners for the info button
    // this will cause the icon to turn black on hover
    addListeners("info");

    // On click, call the function to open/close the navbar
    infoFilterUI.addEventListener('click', navBar);
}

// function for creating the prediction button
function PredictionButton() {
    // create div for the button image and add CSS
    predictionFilterUI = document.createElement('div');
    predictionFilterUI.style.backgroundColor = '#fff';
    predictionFilterUI.style.backgroundImage = 'url(' + crystalBall + ')';
    predictionFilterUI.style.backgroundSize = '32px';
    predictionFilterUI.style.backgroundPosition = 'center';
    predictionFilterUI.style.backgroundRepeat = 'no-repeat';
    predictionFilterUI.style.border = '2px solid #fff';
    predictionFilterUI.style.borderRadius = '2px';
    predictionFilterUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.15)';
    predictionFilterUI.style.cursor = 'pointer';
    predictionFilterUI.style.textAlign = 'center';
    predictionFilterUI.style.width = '36px';
    predictionFilterUI.style.height = '36px';
    predictionFilterUI.style.marginTop = '16px';
    predictionFilterUI.style.marginRight = '10px';
    predictionFilterUI.style.marginBottom = '6px';
    predictionFilterUI.style.display = 'flex';
    predictionFilterUI.style.alignContent = 'center';
    predictionFilterUI.style.justifyContent = 'center';
    predictionFilterUI.title = 'Get Prediction';
    predictionFilterDiv.appendChild(predictionFilterUI);  // append image div to the main button div

    // add listeners for the predictive filter button
    // this will cause the icon to turn black on hover
    addListeners("predictive");

    // On click, pop up form for prediction input
    predictionFilterUI.addEventListener('click', predictionClick);
}

// function for hiding markers on the map
function hideMarkers(type) {
    // if a pop-up is open, close it
    if (prevPopup) {
        prevPopup.close();
    }
    // set PrevPopup to false as all pop-ups should be closed when filter button is clicked
    prevPopup = false;

    if (!predictionMode) {  // if the map is not in prediction mode
        if (type=="bike") {
            // loop through each marker in the markers arrays and set the map to null
            for (var i = 0; i < bikeMarkers.length; i++) {
                bikeMarkers[i].setMap(null);
            }
            for (var i = 0; i < bikeMarkersCard.length; i++) {
                bikeMarkersCard[i].setMap(null);
            }
        }
        else if (type=="stand") {
            // loop through each marker in the markers arrays and set the map to null
            for (var i = 0; i < standMarkers.length; i++) {
                standMarkers[i].setMap(null);
            }
            for (var i = 0; i < standMarkersCard.length; i++) {
                standMarkersCard[i].setMap(null);
            }
        }
        else if (type=="card") {
            // if type is card, hide all stations that don't accept card
            for (var i = 0; i < bikeMarkers.length; i++) {
                bikeMarkers[i].setMap(null);
            }
            for (var i = 0; i < standMarkers.length; i++) {
                standMarkers[i].setMap(null);
            }
        }
    }
    else { // if the map is in prediction mode
        if (type=="bike") {
            // loop through each marker in the markers arrays and set the map to null
            for (var i = 0; i < bikeMarkersPredictive.length; i++) {
                bikeMarkersPredictive[i].setMap(null);
            }
            for (var i = 0; i < bikeMarkersCardPredictive.length; i++) {
                bikeMarkersCardPredictive[i].setMap(null);
            }
        }
        else if (type=="stand") {
            // loop through each marker in the markers arrays and set the map to null
            for (var i = 0; i < standMarkersPredictive.length; i++) {
                standMarkersPredictive[i].setMap(null);
            }
            for (var i = 0; i < standMarkersCardPredictive.length; i++) {
                standMarkersCardPredictive[i].setMap(null);
            }
        }
        else if (type=="card") {
            // if type is card, hide all stations that don't accept card
            for (var i = 0; i < bikeMarkersPredictive.length; i++) {
                bikeMarkersPredictive[i].setMap(null);
            }
            for (var i = 0; i < standMarkersPredictive.length; i++) {
                standMarkersPredictive[i].setMap(null);
            }
        }
    }
}

// function to show the relevant markers on the map
function showMarkers(type) {
    if (!predictionMode) {  // if the map is not in prediction mode
        if (type=="bike") {
            // if type is bike always show stations that accept card
            for (var i = 0; i < bikeMarkersCard.length; i++) {
                bikeMarkersCard[i].setMap(map);
            }
            if (!cardFilterOn) { // if the card filter is off, also show stations that don't accept card
                for (var i = 0; i < bikeMarkers.length; i++) {
                    bikeMarkers[i].setMap(map);
                }
            }
        }
        else if (type=="stand") {
            // if type is bike always show stations that accept card
            for (var i = 0; i < standMarkersCard.length; i++) {
                standMarkersCard[i].setMap(map);
            }
            if (!cardFilterOn) { // if the card filter is off, also show stations that don't accept card
                for (var i = 0; i < standMarkers.length; i++) {
                    standMarkers[i].setMap(map);
                }
            }
        }
        else if (type=="card") {
            // first close any open pop-ups 
            if (prevPopup) {
                prevPopup.close();
            }
            // set PrevPopup to false as all pop-ups should be closed when filter button is clicked
            prevPopup = false;
            // if type is card, check which filter is currently selected (bike vs. stands)
            // and show the appropriate stations
            if (bikeFilterOn) {
                for (var i = 0; i < bikeMarkers.length; i++) {
                    bikeMarkers[i].setMap(map);
                }
            }
            else if (cardFilterOn) {
                for (var i = 0; i < standMarkers.length; i++) {
                    standMarkers[i].setMap(map);
                }
            }
        }
    }
    else {
        if (type=="bike") {
            // if type is bike always show stations that accept card
            for (var i = 0; i < bikeMarkersCardPredictive.length; i++) {
                bikeMarkersCardPredictive[i].setMap(map);
            }
            if (!cardFilterOn) { // if the card filter is off, also show stations that don't accept card
                for (var i = 0; i < bikeMarkersPredictive.length; i++) {
                    bikeMarkersPredictive[i].setMap(map);
                }
            }
        }
        else if (type=="stand") {
            // if type is bike always show stations that accept card
            for (var i = 0; i < standMarkersCardPredictive.length; i++) {
                standMarkersCardPredictive[i].setMap(map);
            }
            if (!cardFilterOn) { // if the card filter is off, also show stations that don't accept card
                for (var i = 0; i < standMarkersPredictive.length; i++) {
                    standMarkersPredictive[i].setMap(map);
                }
            }
        }
        else if (type=="card") {
            // first close any open pop-ups 
            if (prevPopup) {
                prevPopup.close();
            }
            // set PrevPopup to false as all pop-ups should be closed when filter button is clicked
            prevPopup = false;
            // if type is card, check which filter is currently selected (bike vs. stands)
            // and show the appropriate stations
            if (bikeFilterOn) {
                for (var i = 0; i < bikeMarkersPredictive.length; i++) {
                    bikeMarkersPredictive[i].setMap(map);
                }
            }
            else if (cardFilterOn) {
                for (var i = 0; i < standMarkersPredictive.length; i++) {
                    standMarkersPredictive[i].setMap(map);
                }
            }
        }
    }
}

// function that controls what happens when the bike button is clicked
function bikeClick() {
    // if the stand filter is already on, perform the following updates
    if (standFilterOn) {
        // update CSS for bike button
        bikeFilterUI.style.backgroundColor = '#464646';
        bikeFilterUI.style.border = '2px solid #464646';
        bikeFilterUI.style.backgroundImage = 'url(' + bicycleLight + ')';
        bikeFilterUI.title = '';
        bikeFilterUI.style.cursor = 'auto';

        // update CSS for the stand button
        standFilterUI.style.backgroundColor = '#fff';
        standFilterUI.style.border = '2px solid #fff';
        standFilterUI.style.backgroundImage = 'url(' + stands + ')';
        standFilterUI.title = 'Show Stand Info';
        standFilterUI.style.cursor = 'pointer';

        // add listeners for the bike filter button
        // this will cause the icon to turn black on hover
        addListeners("stand");

        // remove listeners for the bike filter button
        // this will stop the icon changing colour on hover
        removeListeners("bike");

        // hide stand markers
        hideMarkers("stand");
        // show bike markers
        showMarkers("bike");

        // update the variables that track the filter
        bikeFilterOn = true;
        standFilterOn = false;
    }
}

// function that controls what happens when the stand button is clicked
function standClick() {
    // if the bike filter is already on, perform the following updates
    if (bikeFilterOn) {
        // update CSS for stand button
        standFilterUI.style.backgroundColor = '#464646';
        standFilterUI.style.border = '2px solid #464646';
        standFilterUI.style.backgroundImage = 'url(' + standsLight + ')';
        standFilterUI.title = '';
        standFilterUI.style.cursor = 'auto';

        // update CSS for the bike button
        bikeFilterUI.style.backgroundColor = '#fff';
        bikeFilterUI.style.border = '2px solid #fff';
        bikeFilterUI.style.backgroundImage = 'url(' + bicycle + ')';
        bikeFilterUI.title = 'Show Bike Info';
        bikeFilterUI.style.cursor = 'pointer';

        // add listeners for the bike filter button
        // this will cause the icon to turn black on hover
        addListeners("bike");

        // remove listeners for the stand filter button
        // this will stop the icon changing colour on hover
        removeListeners("stand");

        // hide stand markers
        hideMarkers("bike");
        // show bike markers
        showMarkers("stand");

        // update the variables that track the filter
        bikeFilterOn = false;
        standFilterOn = true;
    }
}

// function that controls what happens when the card button is clicked
function cardClick() {
    // if the card filter is not already on, perform the following updates
    if (!cardFilterOn) {
        // update CSS for card button
        cardFilterUI.style.backgroundColor = '#464646';
        cardFilterUI.style.border = '2px solid #464646';
        cardFilterUI.style.backgroundImage = 'url(' + euroSymbolLight + ')';

        // remove listeners for the card filter button
        // this will stop the icon changing colour on hover
        removeListeners("card");

        // hide stations that don't accept card
        hideMarkers("card");

        // update the variable that tracks the filter
        cardFilterOn = true;
    }
    else if (cardFilterOn) {
        // update CSS for card button
        cardFilterUI.style.backgroundColor = '#fff';
        cardFilterUI.style.border = '2px solid #fff';
        cardFilterUI.style.backgroundImage = 'url(' + euroSymbol + ')';

        // add listeners for the card filter button
        // this will cause the icon to turn black on hover
        addListeners("card");

        // show stations that don't accept card (bike or stand markers depending on which filter is selected)
        showMarkers("card");

        // update the variable that tracks the filter
        cardFilterOn = false;
    }
}

// function that controls what happens when the prediction button is clicked
function predictionClick() {
    // show the predictive form
    var form = document.getElementById("predictionForm");
    // if prediction mode is not on, hide or show the form
    if (!predictionMode) {
        if (form.style.display == "block") {
            form.style.display = "none";
        } 
        else {
            form.style.display = "block";
        }
    }
    // if prediction mode is on...
    else if (predictionMode) {
        realTime();
    }
}

// function for adding listeners to the buttons
function addListeners(type) {
    // check which type of listener should be added: bike or stand
    if (type == "bike") {
        // on hover, change icon colour to black
        bikeFilterDiv.addEventListener('mouseenter', bikeListenerEnter);
        bikeFilterDiv.addEventListener('mouseleave', bikeListenerLeave);
    }
    else if (type == "stand") {
        // on hover, change icon colour to black
        standFilterDiv.addEventListener('mouseenter', standListenerEnter);
        standFilterDiv.addEventListener('mouseleave', standListenerLeave);
    }
    else if (type == "card") {
        // on hover, change icon colour to black
        cardFilterDiv.addEventListener('mouseenter', cardListenerEnter);
        cardFilterDiv.addEventListener('mouseleave', cardListenerLeave);
    }
    else if (type == "predictive") {
        // on hover, change icon colour to black
        predictionFilterDiv.addEventListener('mouseenter', predictiveListenerEnter);
        predictionFilterDiv.addEventListener('mouseleave', predictiveListenerLeave);
    }
    else if (type == "info") {
        // on hover, change icon colour to black
        infoFilterDiv.addEventListener('mouseenter', infoListenerEnter);
        infoFilterDiv.addEventListener('mouseleave', infoListenerLeave);
    }
}

// function for removing listeners from the buttons
function removeListeners(type) {
    // check which type of listener should be removed: bike or stand
    if (type == "bike") {
        // removing listeners will stop icon colour changing on hover
        bikeFilterDiv.removeEventListener('mouseenter', bikeListenerEnter);
        bikeFilterDiv.removeEventListener('mouseleave', bikeListenerLeave);
    }
    else if (type == "stand") {
        // removing listeners will stop icon colour changing on hover
        standFilterDiv.removeEventListener('mouseenter', standListenerEnter);
        standFilterDiv.removeEventListener('mouseleave', standListenerLeave);
    }
    else if (type == "card") {
        // removing listeners will stop icon colour changing on hover
        cardFilterDiv.removeEventListener('mouseenter', cardListenerEnter);
        cardFilterDiv.removeEventListener('mouseleave', cardListenerLeave);
    }
    else if (type == "predictive") {
        // removing listeners will stop icon colour changing on hover
        predictionFilterDiv.removeEventListener('mouseenter', predictiveListenerEnter);
        predictionFilterDiv.removeEventListener('mouseleave', predictiveListenerLeave);
    }
    else if (type == "info") {
        // removing listeners will stop icon colour changing on hover
        infoFilterDiv.removeEventListener('mouseenter', infoListenerEnter);
        infoFilterDiv.removeEventListener('mouseleave', infoListenerLeave);
    }
}

// function that defines what happens when a bike button listener is added
function bikeListenerEnter() {
    bikeFilterUI.style.backgroundImage = 'url(' + bicycleBlack + ')';
}

// function that defines what happens when a bike button listener is added
function bikeListenerLeave() {
    bikeFilterUI.style.backgroundImage = 'url(' + bicycle + ')';
}

// function that defines what happens when a stand button listener is added
function standListenerEnter() {
    standFilterUI.style.backgroundImage = 'url(' + standsBlack +')';
}

// function that defines what happens when a stand button listener is added
function standListenerLeave() {
    standFilterUI.style.backgroundImage = 'url('+ stands + ')';
}

// function that defines what happens when a card button listener is added
function cardListenerEnter() {
    cardFilterUI.style.backgroundImage = 'url(' + euroSymbolBlack + ')';
}

// function that defines what happens when a card button listener is added
function cardListenerLeave() {
    cardFilterUI.style.backgroundImage = 'url(' + euroSymbol + ')';
}

// function that defines what happens when an info button listener is added
function infoListenerEnter() {
    infoFilterUI.style.backgroundImage = 'url(' + infoSymbolBlack + ')';
}

// function that defines what happens when an info button listener is added
function infoListenerLeave() {
    infoFilterUI.style.backgroundImage = 'url(' + infoSymbol + ')';
}

// function that defines what happens when a predictive button listener is added
function predictiveListenerEnter() {
    predictionFilterUI.style.backgroundImage = 'url(' + crystalBallBlack + ')';
}

// function that defines what happens when a predictive button listener is added
function predictiveListenerLeave() {
    predictionFilterUI.style.backgroundImage = 'url(' + crystalBall + ')';
}

// function that deals with prediction requests - called when the submit button on the prediction form is pressed
function makePrediction() {
    //get values from form fields to pass to subsequent functions
    var predict = document.getElementById("predictionFormFields");
    var time = predict[0].value;
    var date = predict[1].value;

    // split time out into hours and minutes	
    var hour = time.slice(0,2);	
    var min = time.slice(3,5);

    // split the date out into day and month
    var day = parseInt(date.split(" ")[0]);	
    var inputMonth = date.split(" ")[1];

    // create array with month names as they should be displayed
    var months = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ];
    // use the array to get the numeric value of the inputted month
    var month = months.indexOf(inputMonth);

    // get the current date
    var d = new Date(); 
    // get the year from the current date
    if (d.getMonth() == 11 && d.getDate() >= 28) { // if it is 28-31 Dec, we need to be careful about giving the right year 
        // check what day was received in the form, if it is 4 or less, then add 1 to year
        // because it means the current date is December but the request is for Jan the next year
        var year = d.getFullYear() + 1;
    }
    else {  // otherwise, just get the current year
        var year = d.getFullYear();
    }

    // create datetime object 
    var dateTime = new Date(year, month, day, hour, min);

    // convert object to ISO 8601 standard for the Flask function
    var dateConverted = new Date(dateTime.getTime() - (dateTime.getTimezoneOffset() * 60000)).toISOString();

    // create an array with day of the week names as they should be displayed
    var daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    // create a string with details of the prediction date (this is used to display the date in pop-up windows)
    predictionDate = hour + ':' + min + ' ' + daysOfWeek[dateTime.getDay()] + ' ' + day + ' ' + inputMonth;

    // hide the existing markers
    hideMarkers("bike");
    hideMarkers("stand");

    // update the map style
    map.setOptions({styles: predictiveStyle});

    // if prediction mode isn't already on, then call function to invert colours on the button
    if (!predictionMode) {
        invertPredictiveButton();
    }

    // call Flask function with the relevant date and time
    var predictionURL = ROOT + '/predictall/' + dateConverted;

    $.getJSON(predictionURL, function (data) {

        // reset the predictive marker arrays to empty
        // this is done so that the number of markers doesn't keep increasing each time a new prediction is requested
        bikeMarkersCardPredictive = [];
        standMarkersCardPredictive = [];
        bikeMarkersPredictive = [];
        standMarkersPredictive = [];

        // add predictive markers
        addPredictiveMarkers(data);

        // update predictionMode variable to true
        predictionMode = true;

        // show the predictive markers
        // check which filters are currently on
        if (bikeFilterOn) {
            showMarkers("bike");
        }
        else {
            showMarkers("stand");
        }
    })
    // if the API call fails, show the error message for predictions
    .fail(function() {
        on();
    });
}

// function for adding predictive markers for the map
function addPredictiveMarkers(data) {
    // add markers to the map - loop through each station in the JSON object
    $.each(data, function (key, entry) {
        // get the latitude and longitude for the station
        var latitude = entry.lat;
        var longitude = entry.lng;
        var latLng = new google.maps.LatLng(latitude, longitude);

        // get the station address - for the pop-up
        var stationName = entry.address;

        // get the station id - for pop-up when dropdown selected
        var stationId = entry.id;

        // get the occupancy info for each station
        var totalStands = entry.bike_stands;
        var availableBikes = entry.available_bikes;
        // if availableBikes is less than zero, change it to zero
        if (availableBikes < 0) {
            availableBikes = 0;
        }
        var availableStands = entry.available_bike_stands;
        // if availableStands is less than zero, change it to zero
        if (availableStands < 0) {
            availableStands = 0;
        }

        // calculate the percentage of available bikes & stands
        var percentAvailable = (availableBikes/totalStands)*100;
        var percentFree = (availableStands/totalStands)*100;

        // get payment info for each station
        var cardPayments = entry.banking;
        // set text to display on pop-up
        if (cardPayments == "true") {  //if card payments are accepted
            paymentText = "Credit Card Accepted"
        }
        else {
            paymentText = "Card Not Accepted"
        }

        // check which icon should be use based on percentage available & payment types
        // check if the station accepts card payments
        // if so, check how many bikes are available and assign marker
        if (cardPayments == "true") {  
            // if card payments are accepted, set images for bike markers
            if (availableBikes == 0) {
                var urlBikes = markerEmptyEuro; // use the empty marker with euro symbol
            }
            else if (percentAvailable >= 67) {
                var urlBikes = markerPredictEuro;  // use the full marker with euro symbol
            }
            else if (percentAvailable >= 33) {
                var urlBikes = markerPredictHalfEuro;  // use the half marker with euro symbol
            }
            else {
                var urlBikes = markerPredictEmptyEuro;  // use the nearly empty marker with euro symbol
            }
            // then set images for stand markers
            if (availableStands == 0) {
                var urlStands = markerEmptyStandsEuro; // use the empty marker with euro symbol
            }
            else if (percentFree >= 67) {
                var urlStands = markerPredictStandsEuro;  // use the full marker with euro symbol
            }
            else if (percentFree >= 33) {
                var urlStands = markerPredictHalfStandsEuro;  // use the half marker with euro symbol
            }
            else {
                var urlStands = markerPredictEmptyStandsEuro;  // use the nearly empty marker with euro symbol
            }
        }
        // if the station doesn't accept card, check how many bikes/stands are available and assign markers
        else { 
            // set images for bike markers
            if (availableBikes == 0) {
                var urlBikes = markerEmpty; // use the empty marker without euro symbol
            }
            else if (percentAvailable >= 67) {
                var urlBikes = markerPredict;  // use the full marker without euro symbol
            }
            else if (percentAvailable >= 33) {
                var urlBikes = markerPredictHalf;  // use the half marker without euro symbol
            }
            else {
                var urlBikes = markerPredictEmpty;  // use the nearly empty marker without euro symbol
            }
            // set images for stand markers
            if (availableStands == 0) {
                var urlStands = markerEmptyStands; // use the empty marker without euro symbol
            }
            else if (percentFree >= 67) {
                var urlStands = markerPredictStands;  // use the full marker without euro symbol
            }
            else if (percentFree >= 33) {
                var urlStands = markerPredictHalfStands;  // use the half marker without euro symbol
            }
            else {
                var urlStands = markerPredictEmptyStands;  // use the nearly empty marker without euro symbol
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
        var content = '<div style="color:#464646; width: 190px;">' +
            '<h1 style="font-size:120%; text-align:center; padding: 5px 8px 3px;">' + stationName + '</h1>' +
            '<div style="font-weight: bold; padding-bottom: 10px;">' + 
            '<table><tr>' +
            '<td style="width:40px;">' + 
            '<img src=' + crystalBall + ' style="width:22px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
            '<td>' + predictionDate + '</td></tr>' +
            '<td style="width:40px;">' + 
            '<img src=' + bicycle + ' style="width:35px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
            '<td>' + availableBikes + ' Available</td></tr>' +
            '<td style="width:40px;">' +
            '<img src=' + stands + ' style="width:30px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
            '<td>' + availableStands + ' Free</td></tr>' +
            '<td style="width:40px;">' +
            '<img src=' + euroSymbol + ' style="width:25px; vertical-align:middle; display:block; margin-left:auto; margin-right:auto;"></td>' + 
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

        // add the bike marker to the relevant dict
        bikeMarkerPredictRef[stationId] = [bikeMarker, popup, content]

        // generate a marker object for the station for stands
        var standMarker = new google.maps.Marker({
            position: latLng,  
            //map: map,
            icon: standIcon,  
            title: stationName //this will show the station name when user hovers over marker
        });

        // add the stand marker to the relevant dict
        standMarkerPredictRef[stationId] = [standMarker, popup, content]

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
        if (cardPayments == "true") {  //if card payments are accepted
            bikeMarkersCardPredictive.push(bikeMarker);
            standMarkersCardPredictive.push(standMarker);
        }
        else {
            bikeMarkersPredictive.push(bikeMarker);
            standMarkersPredictive.push(standMarker);
        }
    });
}  

// function to invert colours on the predictive button when form is submitted
function invertPredictiveButton() {
    // update CSS for the predictive button
    predictionFilterUI.style.backgroundColor = '#464646';
    predictionFilterUI.style.border = '2px solid #464646';
    predictionFilterUI.style.backgroundImage = 'url(' + crystalBallInverted + ')';
    predictionFilterUI.title = 'Show Real Time Info';

    // update CSS for the prediction form
    predictionForm = document.getElementById("predictionForm");
    predictionForm.style.backgroundColor = '#464646';
    predictionForm.style.border = '2px solid #464646';

    // update CSS for button on prediction form
    predictionFormButton = document.getElementById("predictionFormButton");
    predictionFormButton.style.backgroundColor = '#f2f2f2';
    predictionFormButton.style.border = '1px solid #ccc';
    predictionFormButton.style.color = '#464646';

    // remove listeners for the predictive button
    removeListeners("predictive");
}

// function to populate the dropdown in the prediction form
function popDateForm() {
    // get the current date
    var d = new Date(); 
    // get the day, month and year from the date
    var month = d.getMonth();
    var day = d.getDate();
    var year = d.getFullYear();
    // create array with month names as they should be displayed
    var months = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ];
    // create array to store values to be put into the dropdown
    var values = [];

    // declare variable to store number of days in a month
    var monthDays = 0;
    // check for months with 31 days
    if (month == 0 || month == 2 || month == 4 || month == 6 || month == 7 || month == 9 || month == 11) {
        monthDays = 31;
    }
    // check for months with 30 days
    else if (month == 3 || month == 5 || month == 8 || month == 10) {
        monthDays = 30;
    }
    // check if month is feb
    else if (month == 1) {  
        // check if it is a leap year
        if (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0)) {
            monthDays = 29;
        }
        else {
            monthDays = 28;
        }
    }

    // run the loop five times as we want five days in the dropdown list (including today)
    for (var i=0; i < 5; i++) {
        // if the current day is monthDays or less, add it to the values array, then increment the day
        if (day <= monthDays) {
            values.push(day + " " + months[month]);
            day++;
        }
        // if the current day is more than monthDays, add its modulus to the values array, then increment the day
        else {
            values.push(day % monthDays + " " + months[(month + 1) % 12]); // mod 12 is needed in case the month is Dec
            day++;
        }
    }

    // declare variable for dropdown html
    var dropdown = "";

    // add all the values in the array to the dropdown
    for (var i=0; i < values.length; i++) {
        dropdown += "<option value=\"" + values[i] + "\">" +  values[i] + "</option>";
    }

    // push the html into the form
    document.getElementById("dateDropdown").innerHTML = dropdown;
}

// function to display error message when Dublin Bikes API call fails
function bikeError() {
    document.getElementById("bikeErrorOverlay").style.display = "block";
}

// function to switch back to real time mode
function realTime() {
    // update button CSS
    predictionFilterUI.style.backgroundColor = '#fff';
    predictionFilterUI.style.border = '2px solid #fff';
    predictionFilterUI.style.backgroundImage = 'url(' + crystalBall + ')';
    predictionFilterUI.title = 'Get Prediction';

    // add listeners to the button
    addListeners("predictive");

    // hide form
    var form = document.getElementById("predictionForm");
    form.style.display = "none";

    // update CSS for the prediction form
    predictionForm = document.getElementById("predictionForm");
    predictionForm.style.backgroundColor = '#fff';
    predictionForm.style.border = '2px solid #fff';

    // update CSS for button on prediction form
    predictionFormButton = document.getElementById("predictionFormButton");
    predictionFormButton.style.backgroundColor = '#464646';
    predictionFormButton.style.border = '1px solid #606060';
    predictionFormButton.style.color = '#fff';

    // clear form fields
    var predict = document.getElementById("predictionFormFields");
    predict.reset();

    // set prediction mode to false
    predictionMode = false;

    // remove predictive markers
    for (var i = 0; i < bikeMarkersCardPredictive.length; i++) {
        bikeMarkersCardPredictive[i].setMap(null);
    }
    for (var i = 0; i < standMarkersCardPredictive.length; i++) {
        standMarkersCardPredictive[i].setMap(null);
    }
    for (var i = 0; i < bikeMarkersPredictive.length; i++) {
        bikeMarkersPredictive[i].setMap(null);
    }
    for (var i = 0; i < standMarkersPredictive.length; i++) {
        standMarkersPredictive[i].setMap(null);
    }

    // clear the arrays for the non-predictive markers
    // this is done because the API will be called again to get the most up to date info for the markers
    // existing markers must be cleared or there will be duplicates in the array
    bikeMarkers = [];
    bikeMarkersCard = [];
    standMarkers = [];
    standMarkersCard = [];

    // change map style back to the default
    map.setOptions({styles: []});

    // call Dublin Bikes API to get latest data and add relevant markers
    $.getJSON(urlBikesAPI, null, function(data) {
        // call the addMarkers function
        addMarkers(data);
        // check which filters are on and show relevant markers
        if (bikeFilterOn) {
            showMarkers("bike");
        }
        else {
            showMarkers("stand");
        }
    })
    // if the call to the Dublin Bikes API fails, then display an error message to the user
    .fail(function() {
        bikeError();
    });
}

// function to show pop-up when station selected from dropdown
function showPop(stationId) {
    // declare local variables for marker, pop-up and content
    var marker;
    var popup;
    var content;

    // check if prediction mode is off
    if (!predictionMode) {
        // check if the bike filter is on
        if (bikeFilterOn) {
            // get the relevant marker and pop-up from the dictionary
            marker = bikeMarkerRef[stationId][0];
            popup = bikeMarkerRef[stationId][1];
            content = bikeMarkerRef[stationId][2];
        }
        // check if the stand filter is on
        else if (standFilterOn) {
            // get the relevant marker and pop-up from the dictionary
            marker = standMarkerRef[stationId][0];
            popup = standMarkerRef[stationId][1];
            content = standMarkerRef[stationId][2];
        }
    }
    // if prediction mode is on
    else {
        // check if the bike filter is on
        if (bikeFilterOn) {
            // get the relevant marker and pop-up from the dictionary
            marker = bikeMarkerPredictRef[stationId][0];
            popup = bikeMarkerPredictRef[stationId][1];
            content = bikeMarkerPredictRef[stationId][2];
        }
        // check if the stand filter is on
        else if (standFilterOn) {
            // get the relevant marker and pop-up from the dictionary
            marker = standMarkerPredictRef[stationId][0];
            popup = standMarkerPredictRef[stationId][1];
            content = standMarkerPredictRef[stationId][2];
        }
    }

    // if there's a previous pop-up open, then close it
    if (prevPopup) {
        prevPopup.close();
    }

    // assign the current pop-up to the PrevPopup variable
    prevPopup = popup;

    // set the content and open the popup
    popup.setContent(content);
    popup.open(map,marker);
}