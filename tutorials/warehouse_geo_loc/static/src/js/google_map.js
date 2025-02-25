function initMap() {
    var latitude = parseFloat(document.querySelector("input[name='lat']").value) || 0;
    var longitude = parseFloat(document.querySelector("input[name='long']").value) || 0;
    var mapOptions = {
        zoom: 15,
        center: { lat: latitude, lng: longitude }
    };
    var map = new google.maps.Map(document.getElementById("google_map"), mapOptions);
    new google.maps.Marker({ position: { lat: latitude, lng: longitude }, map: map });
}

document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("google_map")) {
        var script = document.createElement("script");
        script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBWDcfFV2tau7FNaxO0eIGqniJEGv3GO9c&callback=initMap";
        document.head.appendChild(script);
    }
});