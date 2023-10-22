var card = document.getElementById('favMainCard');

document.addEventListener("DOMContentLoaded", function() {
    var citiesList = JSON.parse(document.getElementById("favArray").value);
    str = "";

    for (let i = 0; i < citiesList.length; i++) {
        var q = citiesList[i];
        var API_KEY = window.API_KEY;
        const url = `http://api.weatherapi.com/v1/current.json?key=${API_KEY}&q=${q}&aqi=no`

        fetch(url)
        .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // This parses the JSON response
        })
        .then(data => {
        // 'data' contains the parsed JSON
        str += `<a href="#" id="favCard" onclick="submitter('${data.location.name}')" class="list-group-item list-group-item-action" aria-current="true">
                    <div class="row container">
                        <div class="col-auto" style="text-align: start;">
                            <h4 style="font-weight: normal;">${data.location.name}, ${data.location.country}</h4>
                            <div class="d-flex">
                                <p class="lead" style="height: 35px; padding-top: 18px;">${data.current.condition.text}</p>
                                <img src="${data.current.condition.icon}" alt="weather" id="weather-icon" class="img-fluid">
                            </div>
                        </div>
                        <div id="favCardMid" class="col-7" style="text-align: center;">
                            <div class="row">
                                <div class="col">
                                    <p>Wind: ${data.current.wind_kph} kph</p>
                                    <p>Precipitation: ${data.current.precip_mm} mm</p>
                                </div>
                                <div class="col">
                                    <p>Humidity: ${data.current.humidity}%</p>
                                    <p>visibility: ${data.current.vis_km}km</p>
                                </div>
                            </div>
                            <div class="row">
                                <p>UV: ${data.current.uv}</p>
                            </div>
                        </div>
                        <div class="col" style="text-align: left;">
                                <h1 class="display-4">${data.current.temp_c}&deg;C</h1>
                                <p>Feels Like ${data.current.feelslike_c}&deg;C</p>
                        </div>
                    </div>
    
                <div class="delete-button">
                    <form action="/favourite" method="post">
                        <input name="remove" type="hidden" value="${data.location.name}">
                        <button class="btn btn-primary" type="submit">Remove</button>
                    </form>
                </div>
            </a>`;
            if (i == citiesList.length - 1) {
                card.innerHTML = str;
            }
        })
        .catch(error => {
        console.error('Fetch error:', error);
        });
    }
});