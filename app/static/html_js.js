// Location of flask app
ROOT = window.location.origin;
// constructed url to get station location
const getLocation = ROOT + '/getlocation/';
// constructed url to get JSON
const dropDownUrl = ROOT + '/dropdown';
// constructed URL for current weather info
const weatherInfo = ROOT + '/weather';
// constructed URL for avgChart
const avgChart = ROOT + '/avgchart/'
// URL for bikes for last week at this hour by day
const bikes1week = ROOT + '/bikes1week/'
// URL for last 2 weeks this hour
const bikes2weeks = ROOT + '/bikes2weeks/'
// get element id
var dropdown = $('#station');

// This function opens and closes the navigation bar
function navBar() {
  var getWidth = document.getElementById("mySidebar");
    if (getWidth.style.width === "320px") {
        document.getElementById("mySidebar").style.width = "50px";
        document.getElementById("main").style.marginLeft = "50px";
        //document.getElementById("openbtn").style.marginLeft = "0px"; // makes button move with sidebar
        document.getElementById("main").style.marginLeft = "0px";
        $("#nonWeatherElements").fadeOut("fast");

        // also update CSS for the info button & add listeners
        infoFilterUI.style.backgroundColor = '#fff';
        infoFilterUI.style.border = '2px solid #fff';
        infoFilterUI.style.backgroundImage = 'url(' + infoSymbol + ')';

        addListeners("info");


    } else {
        document.getElementById("mySidebar").style.width = "320px";
        //document.getElementById("openbtn").style.marginLeft = "75%";
        $("#nonWeatherElements").fadeIn("slow");

        // also update CSS for the info button & remove listeners
        infoFilterUI.style.backgroundColor = '#464646';
        infoFilterUI.style.border = '2px solid #464646';
        infoFilterUI.style.backgroundImage = 'url(' + infoSymbolInverted + ')';

        removeListeners("info");
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
        var latLng = new google.maps.LatLng(data.lat + 0.0008, data.lng);
        map.setCenter(latLng);
        map.setZoom(16.2);

        // check if the card filter is on, and turn it off if so
        if (cardFilterOn) {
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

        // show the pop-up
        showPop(ID);
    });

    document.getElementById("avg").checked = true;

}

// get current weather information and display it in the DIV element in the sidebar.
$.getJSON(weatherInfo, function (data) {
    $("#weatherElement").html("<img style=\"margin-left: -3px; padding:1%;\" src="+data.iconURL+">");
    $("#weatherElement").append("<p id=\"summary\" style=\"margin-top: -14px; margin-left:6px; position: absolute;\" >" + data.Temperature + " &#176;C" + "</p");
});

// Set default station for chart requests
var currentSelectedText = "";
// initialise two arrays that will hold our time and avg bikes at that time
var chartTime = [];
var chartAvg = [];

// add a listener to call the function every time our dropdown selection changes
$(document).on("change", "#station", function() {
    currentSelectedText = $(this).find("option:selected").text();
    currentSelectedText = currentSelectedText.replace(" ","_");
    buildChart();
});

// function to rebuild the chart with updated average information (i.e. new station selected)
function buildChart() {
    var avg = [];
    var time = [];
    $.getJSON(avgChart+currentSelectedText, function(data) {
        for (var i=0; i < Object.keys(data).length; i++) {
            var zero = "0"; // needed when checking time format 00->09AM to check key since javascript won't preserve a leading 0
            if (i <= 9) {
                var key = zero + i;
                time.push(key);
                avg.push(data[key]);
            } else {
                time.push(i+"");
                avg.push(data[i+""]);
            }
        }
        chartTime = avg;
        chartAvg = time;
        chart(chartTime,chartAvg);
    })
}

// function to build chart from data providing a snapshot of what availability looked like on each day for the last week
function prevWeek() {
    var bikesAvailable = [];
    var day = [];
    
    $.getJSON(bikes1week+currentSelectedText, function(data) {
        for (var i in data) {
            if (i == "Mon") {
                day[0] = i;
                bikesAvailable[0] = data[i]; 
            } else if (i == "Tue") {
                day[1] = i;
                bikesAvailable[1] = data[i];
            } else if (i == "Wed") {
                day[2] = i;
                bikesAvailable[2] = data[i];
            } else if (i == "Thu") {
                day[3] = i;
                bikesAvailable[3] = data[i];
            } else if (i == "Fri") {
                day[4] = i;
                bikesAvailable[4] = data[i];
            } else if (i == "Sat") {
                day[5] = i;
                bikesAvailable[5] = data[i];
            } else if (i == "Sun") {
                day[6] = i;
                bikesAvailable[6] = data[i];
            }
        }
        chart(bikesAvailable,day);
    })
}

// function to get and display on a chart the usage / availability data for the past 2 weeks based on the current hour
function prevTwoWeeks() {
    var bikesAvailable = [];
    var date = [];
    
    $.getJSON(bikes2weeks+currentSelectedText, function(data) {
        for (var i in data) {
            date.push(i);
            bikesAvailable.push(data[i]);
        }
        chart(bikesAvailable,date);
    })
}

// chart function which builds / rebuilds our charts with new data.
function chart(time,data) {
    $('#graph').fadeOut(85);
    $('#radioButtons').fadeOut(85);
    $('#graph').promise().done(function(){
        $("#myChart").remove();
        $("#graph").append('<canvas id="myChart" width="280" height="200"></canvas>');
        var ctx = $('#myChart');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data,
                datasets: [{
                    label: 'Available bikes',
                    data: time,
                    pointBackgroundColor: 'black',
                    fill:false,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                    ],
                    borderColor: [
                        '#8bb08a',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                legend: {
                    labels: {
                        fontColor: 'black',
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            fontColor: 'black'
                        },
                        gridLines: {
                            display: false
                        }
                    }],
                    xAxes: [{
                        gridLines: {
                            display: false,
                          },
                        ticks: {
                            fontColor: 'black'
                        }
                    }]
                },
            }
        });
        $('#graph').fadeIn(1300);
        $('#radioButtons').fadeIn(1300);
    });
}