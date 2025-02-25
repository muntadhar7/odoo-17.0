document.addEventListener("DOMContentLoaded", function () {
    const x = document.getElementById("demo");

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition);
        } else {
            x.innerHTML = "Geolocation is not supported by this browser.";
        }
    }

    function showPosition(position) {
        x.innerHTML = "Latitude: " + position.coords.latitude +
            "<br>Longitude: " + position.coords.longitude;
    }

    // Optional: Add a button event listener if you want it to trigger on click
    const locationButton = document.getElementById("getLocationBtn");
    if (locationButton) {
        locationButton.addEventListener("click", getLocation);
    }
});
