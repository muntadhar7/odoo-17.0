// static/src/js/map_picker.js
odoo.define('website_custom.map_picker', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');
    var rpc = require('web.rpc');

    var MapPickerWidget = AbstractField.extend({
        template: 'MapPickerWidget',
        jsLibs: [
            'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js'
        ],
        cssLibs: [
            'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css'
        ],

        start: function() {
            this._super.apply(this, arguments);

            // Initialize map
            this.map = L.map(this.$el.find('.map-container')[0]).setView([0, 0], 2);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(this.map);

            // Add click handler
            this.map.on('click', this._onMapClick.bind(this));

            // If we have existing value, show marker
            if (this.value) {
                var coords = JSON.parse(this.value);
                this._addMarker(coords.lat, coords.lng);
            }
        },

        _onMapClick: function(e) {
            this._addMarker(e.latlng.lat, e.latlng.lng);
            this._setValue(JSON.stringify({lat: e.latlng.lat, lng: e.latlng.lng}));
        },

        _addMarker: function(lat, lng) {
            if (this.marker) {
                this.map.removeLayer(this.marker);
            }
            this.marker = L.marker([lat, lng]).addTo(this.map);
            this.map.setView([lat, lng], 13);
        }
    });

    registry.add('map_picker', MapPickerWidget);
    return MapPickerWidget;
});