// Location of flask app
ROOT = window.location.origin;
// constructed url to get station location
const getLocation = ROOT + '/getlocation/';
// constructed url to get JSON
const dropDownUrl = ROOT + '/dropdown';
// constructed URL for current weather info
const weatherInfo = ROOT + '/weather';
// get element id
var dropdown = $('#station');

// This function opens and closes the navigation bar
function navBar() {
  var getWidth = document.getElementById("mySidebar");
    if (getWidth.style.width === "250px") {
        document.getElementById("mySidebar").style.width = "50px";
        document.getElementById("main").style.marginLeft = "50px";
        document.getElementById("openbtn").style.marginLeft = "0px";
        document.getElementById("main").style.marginLeft = "0px";
        $("#nonWeatherElements").fadeOut("fast");

    } else {
        document.getElementById("mySidebar").style.width = "250px";
        document.getElementById("openbtn").style.marginLeft = "75%";
        $("#nonWeatherElements").fadeIn("slow");
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


$.getJSON(weatherInfo, function (data) {
    console.log(data);
    $("#weatherElement").html("<img style=\"margin-left: -3px; padding:10%;\" src="+data.iconURL+">");
    $("#weatherElement").append("<p id=\"summary\" style=\"margin-top: -20px; margin-left:5px; position: absolute;\" >" + data.Temperature + " &#8451 " + "</p");
});

var ctx = $('#myChart');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Red'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            fill:false,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});