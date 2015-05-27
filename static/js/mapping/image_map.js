/**
  For displaying the location of an image on the image detail view
 **/

var this_map;
var this_marker;

$(document).ready(function() {

    if ($('#image_location_map').length == 0) {
        return;
    }

    this_map = set_image_map();

    $("#address_search_button").click(function(e) {
       do_address_search();
    });

    $('#address_search_form').on('submit', function(e) {
        e.preventDefault();  //prevent form from submitting
        do_address_search();
    });

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

    this_marker = L.marker([latitude, longitude], {icon: myIcon}).addTo(map);

    return map
}

function do_address_search()
{
    var $form = $("#address_search_form");

    // Serialize the data in the form
    var serializedData = $form.serialize();
    var image_id = $('#image_map').data('id');

    // Fire off the request
    request = $.ajax({
        url: "/image=" + image_id + "/address/",
        dataType: "json",
        type: "post",
        data: serializedData
    });

    // Callback handler that will be called on success
    request.done(function (data){

        $('#latitude').html(data['latitude']);
        $('#longitude').html(data['longitude']);
        $('#image_location_map').data('latitude', data['latitude']);
        $('#image_location_map').data('longitude', data['longitude']);

        this_map.removeLayer(this_marker);

        var latitude = parseFloat(data['latitude']);
        var longitude = parseFloat(data['longitude']);

        this_map.panTo(new L.LatLng(latitude, longitude));

        var myIcon = L.divIcon({
            className:  'circle',
            iconSize:   [20, 20], // size of the icon
            iconAnchor: [10, 10], // point of the icon which will correspond to marker's location
            popupAnchor:[0, -5], // point from which the popup should open relative to the iconAnchor
            html: ''
        });

        this_marker = L.marker([latitude, longitude], {icon: myIcon}).addTo(this_map);
    });
}