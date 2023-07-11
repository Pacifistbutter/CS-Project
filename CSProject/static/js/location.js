function getLocation() {
    if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showLocation, showerror);
        alert("herer");
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
    console.log(latitude);
    console.log(longitude);
    // Submits the form
    document.getElementById("locationForm").submit()
}