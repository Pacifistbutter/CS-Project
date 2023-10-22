function getLocation() {
    if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showLocation, showerror);
    } else {
        alert("Geolocation is not supported by your browser!");
    }
}

function showLocation(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;

    // Update form input with latitude and longitude
    document.getElementById("latitudeInput").value = latitude;
    document.getElementById("longitudeInput").value = longitude;
    // console.log(latitude);
    // console.log(longitude);
    // Submits the form
    document.getElementById("locationForm").submit()
}

function showerror(){
    switch (error.code){
        case error.PERMISSION_DENIED:
            alert("User denied the Geolocation Request!");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("User location information unavailable!");
            break;
        case error.TIMEOUT:
            alert("Request to get user loction time out!");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred!")
            break;
    }
}