/**
  For displaying the location of an image on the image detail view
 **/

$(document).ready(function() {

    if ($('#image_location_map').length == 0) {
        return;
    }

    set_image_map();
});


function set_image_map() {

    var latitude = parseFloat($('#image_location_map').data('latitude'));
    var longitude = parseFloat($('#image_location_map').data('longitude'));

    var map = L.map('image_location_map', {
        center: [latitude, longitude],
        zoom: 14,
        zoomControl: false,
        minZoom: 2,
        scrollWheelZoom: true,
        detectRetina: true,
        maxBounds: [[-90, -200],[90, 200]]
    });



    L.tileLayer('https://{s}.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={token}', {
    	subdomains: ['a','b','c','d'],
    	id: 'okkindred.ldfc645h',
    	token: 'pk.eyJ1Ijoib2traW5kcmVkIiwiYSI6Ild2MnY5dDQifQ.EHr6blIYPYeg4bWmSStT-g'
    }).addTo(map);

    map.addControl( L.control.zoom({position: 'bottomleft'}));

    var myIcon = L.divIcon({
        className:  'circle',
        iconSize:   [20, 20], // size of the icon
        iconAnchor: [10, 10], // point of the icon which will correspond to marker's location
        popupAnchor:[0, -5], // point from which the popup should open relative to the iconAnchor
        html: ''
    });

    var marker = L.marker([latitude, longitude], {icon: myIcon}).addTo(map);
}