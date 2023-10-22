function dosomething() {
    var myDiv = document.getElementById('divtest');
    myDiv.innerHTML = "This is a <hr><strong>Test</strong>"
}

function openMap() {
    var q = searchInput.value;
    
    
    // console.log(q);
    var API_KEY = window.API_KEY;
    // console.log(API_KEY);
    var url = `https://api.weatherapi.com/v1/current.json?key=${API_KEY}&q=${q}&aqi=no`

    
    fetch(url)
        .then(function(response) {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
            return response.json();
        })
        .then(function(data) {
            var name = data.location.name;
            var temperature = data.current.temp_c;
            var weatherCondition = data.current.condition.text;
            var lat = data.location.lat;
            var lon = data.location.lon;
            var map = L.map('weather-map').setView([lat, lon], 10);
        
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
        
            var popupContent = `<b>Current Weather</b><br>
                                Name: ${name}<br>
                                Temperature: ${temperature}°C<br>
                                Condition: ${weatherCondition}<br>
                                <form action="/today" id="locationForm" method="post">
                                    <input name="city" type="hidden" value="${name}">
                                    <div class="col-auto">
                                        <button class="btn btn-link" type="submit" style="font-size: 12px; padding: 0; margin: 0; border: none;">More Info</button>
                                    </div>
                                </form>
                                `;
        
            L.marker([lat, lon]).addTo(map)
                .bindPopup(popupContent)
                .openPopup();

            var popup = L.popup();

            function onMapClick(e) {
                var lat = e.latlng.lat; // Latitude
                var lng = e.latlng.lng; // Longitude
                var newurl = `https://api.weatherapi.com/v1/current.json?key=${API_KEY}&q=${lat},${lng}&aqi=no`
                
                fetch(newurl)
                    .then(function(response) {
                        if (!response.ok) {
                        throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(function(data) {
                        // Here, 'data' contains the weather information based on the provided coordinates
                        var newname = data.location.name;
                        var newtemp = data.current.temp_c;
                        var newwc = data.current.condition.text;

                        var newpopupContent = `<b>Current Weather</b><br>
                                                Name: ${newname}<br>
                                                Temperature: ${newtemp}°C<br>
                                                Condition: ${newwc}<br>
                                                <form action="/today" id="locationForm" method="post">
                                                    <input name="city" type="hidden" value="${newname}">
                                                    <div class="col-auto">
                                                        <button class="btn btn-link" type="submit" style="font-size: 12px; padding: 0; margin: 0; border: none;">More Info</button>
                                                    </div>
                                                </form>
                                                `;
                        popup
                        .setLatLng(e.latlng)
                        .setContent(newpopupContent)
                        .openOn(map);
                    })
                    .catch(function(error) {
                        console.error('There was a problem with the fetch operation:', error);
                    });
            }
            
            map.on('click', onMapClick);

        })
        .catch(function(error) {
        console.error('There was a problem with the fetch operation:', error);
    });

}