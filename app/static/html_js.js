// Location of flask app
ROOT = window.location.origin;
// constructed url to get station location
const getLocation = ROOT + '/getlocation/';
// constructed url to get JSON
const dropDownUrl = ROOT + '/dropdown';
// get element id
var dropdown = $('#station');

// This function opens and closes the navigation bar and makes the button move correctly alongside it.
function navBar() {
  var getWidth = document.getElementById("mySidebar");
    if (getWidth.style.width === "250px") {
        document.getElementById("mySidebar").style.width = "50px";
        document.getElementById("main").style.marginLeft = "50px";
        $("#nonWeatherElements").fadeOut();

    } else {
        document.getElementById("mySidebar").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
        document.getElementById("openbtn").style.marginLeft = "0px";
        $("#nonWeatherElements").fadeIn();
    }
}

// This function populates the dropdown with list of stations
$.getJSON(dropDownUrl, function (data) {
    $.each(data, function (key, entry) {
        dropdown.append($('<option></option>').attr('value', entry.ID).text(entry.Address));
    })
});

// This function gets the selected station ID and centers the map on its location.
function goToStation() {
    var ID = document.getElementById('station').value;

    $.getJSON(getLocation+ID, function(data) {
        var latLng = new google.maps.LatLng(data.lat, data.lng);
        console.log(latLng);
        map.setCenter(latLng);
        map.setZoom(17.5);
    });

}
