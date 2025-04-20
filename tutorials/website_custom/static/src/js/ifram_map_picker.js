// static/src/js/iframe_map_picker.js
odoo.define('website_custom.iframe_map_picker', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');

    var IframeMapPicker = AbstractField.extend({
        template: 'IframeMapPicker',

        start: function() {
            this._super.apply(this, arguments);
            this.$el.find('iframe').on('load', this._setupIframe.bind(this));
        },

        _setupIframe: function() {
            var iframe = this.$el.find('iframe')[0];
            var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;

            // Create a simple HTML page inside the iframe
            iframeDoc.open();
            iframeDoc.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { margin: 0; padding: 0; }
                        #map { height: 100%; width: 100%; }
                        .coordinates { position: absolute; bottom: 10px; left: 10px; background: white; padding: 5px; }
                    </style>
                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
                    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
                </head>
                <body>
                    <div id="map"></div>
                    <div class="coordinates">Click on the map to select a location</div>
                    <script>
                        var map = L.map('map').setView([0, 0], 2);
                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

                        var marker;
                        map.on('click', function(e) {
                            if (marker) map.removeLayer(marker);
                            marker = L.marker(e.latlng).addTo(map);
                            window.parent.postMessage({
                                type: 'map_click',
                                coordinates: e.latlng
                            }, '*');
                        });
                    </script>
                </body>
                </html>
            `);
            iframeDoc.close();

            // Listen for messages from the iframe
            window.addEventListener('message', this._onMessage.bind(this));
        },

        _onMessage: function(event) {
            if (event.data.type === 'map_click') {
                this._setValue(JSON.stringify({
                    lat: event.data.coordinates.lat,
                    lng: event.data.coordinates.lng
                }));
            }
        }
    });

    registry.add('iframe_map_picker', IframeMapPicker);
    return IframeMapPicker;
});