odoo.define('website_custom.geo_checkout', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.GeoCheckout = publicWidget.Widget.extend({
        selector: '#wrapwrap',

        start: function () {
            if ($('#map').length && typeof L !== 'undefined') {
                this.initMap();
            }
            return this._super.apply(this, arguments);
        },

        initMap: function () {
            var map = L.map('map').setView([33.3152, 44.3661], 12);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            var marker;

            if ($('#partner_latitude').val() && $('#partner_longitude').val()) {
                var lat = parseFloat($('#partner_latitude').val());
                var lng = parseFloat($('#partner_longitude').val());
                marker = L.marker([lat, lng]).addTo(map);
                map.setView([lat, lng], 15);
            }

            map.on('click', function (e) {
                if (marker) map.removeLayer(marker);
                marker = L.marker(e.latlng).addTo(map);
                $('#partner_latitude').val(e.latlng.lat);
                $('#partner_longitude').val(e.latlng.lng);
            });
        }
    });
});