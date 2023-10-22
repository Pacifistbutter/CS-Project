google.charts.load('current', { packages: ['corechart', 'line'] });
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {
  var data = new google.visualization.DataTable();
  data.addColumn('timeofday', 'Time'); // Using timeofday type for x-axis
  data.addColumn('number', 'Temp C');

  const xhr = new XMLHttpRequest();
  // console.log('searchInput:', testID);
  var q = testID.value;
  // console.log(q);
  var API_KEY = window.API_KEY;
  // console.log(API_KEY);
  var url = `https://api.weatherapi.com/v1/forecast.json?key=${API_KEY}&q=${q}&days=3&aqi=yes&alerts=no`
  // Open the object
  xhr.open('GET', url , true);
  let array = [];

  // What to do when response is ready
  xhr.onload = function () {
    if (this.status === 200) {
      let obj = JSON.parse(this.responseText);
      //console.log("done");
      let minTemp = Infinity;
      let maxTemp = -Infinity;
      for (var i = 0; i < 24; i += 3) {

        var hour = parseInt(obj.forecast.forecastday[0].hour[i].time.slice(11, 13));
        var temp = parseInt(obj.forecast.forecastday[0].hour[i].temp_c);

        //console.log(hour + " " + temp);
        array.push([[hour, 0, 0], temp]); // Include minutes and seconds as 0

        if (temp < minTemp) {
          minTemp = temp;
        }
        if (temp > maxTemp) {
          maxTemp = temp;
        }
      }

      data.addRows(array); // Use addRows instead of addRow

      var options = {
        legend: 'none',
        hAxis: {
          title: 'Time',
          baselineColor: "transparent",
          gridlines: {
            color: 'transparent',
          },
          baselineColor: 'transparent',
          format: 'h a', // Format the time display with hour and AM/PM
          ticks: [
            [0, 0, 0], // 12 AM
            [3, 0, 0],
            [6, 0, 0], // 6 AM
            [9, 0, 0], // 12 PM
            [12, 0, 0], // 6 PM
            [15, 0, 0], // 11 PM
            [18, 0, 0],
            [21, 0 ,0]
          ],
        },
        vAxis: {
          textPosition: 'none',
          gridlines: {
            color: 'transparent',
          },
          viewWindow: {
            min: minTemp - 5, // Add some padding to the minimum temperature
            max: maxTemp + 5, // Add some padding to the maximum temperature
          },
        },
        backgroundColor: 'transparent',
      };

      var chart = new google.visualization.LineChart(document.getElementById('line_chart'));
      chart.draw(data, options);
    }
    else {
      console.log("Some error occurred")
    }
  }

  xhr.send();
}
