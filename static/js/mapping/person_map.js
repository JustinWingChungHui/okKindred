
var markers = new Array();

$(document).ready(function() {

    if($("#person_map").length == 0) {
        return;
    }

    $('.loading').show();
    var center_latitude = parseFloat($("#person_map").data("latitude"));
    var center_longitude = parseFloat($("#person_map").data("longitude"));
    var zoom = parseFloat($("#person_map").data("zoom"));

    var map = L.map('person_map', {
        center: [center_latitude, center_longitude],
        zoom: zoom,
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

    get_map_data(map);

    map.on('zoomend', function(e) {
        get_map_data(e.target);
    });
});


function get_map_data(map) {
    var bounds = map.getBounds()
    var min = bounds.getSouthWest().wrap();
    var max = bounds.getNorthEast().wrap();

    var max_num_points = Math.floor(Math.min($(document).height(),$(document).width()) / 100.0); //100 pixels per spot
    var min_lat_lng = Math.min(max.lng - min.lng, max.lat - min.lat);
    var division_size = min_lat_lng / max_num_points;


    var url = ['/map_points/'];
    url.push(division_size);
    url.push('/');

    $.get(
        url.join(''),
        function(data){

            for(i = 0; i < markers.length; i++) {
                map.removeLayer(markers[i]);
            }
            markers.length = 0;

            var template = $('#map_person_template').html();

            for (var key in data) {
                var loc = data[key];

                var myIcon = L.divIcon({
                    className:  'circle',
                    iconSize:   [40, 40], // size of the icon
                    iconAnchor: [20, 20], // point of the icon which will correspond to marker's location
                    popupAnchor:[0, -5], // point from which the popup should open relative to the iconAnchor
                    html:       loc.length
                });

                var marker = L.marker([loc[0].latitude,loc[0].longitude], {icon: myIcon}).addTo(map);
                markers.push(marker);

                var html = [];

                if (loc.length == 1) {
                    var popupWidth = 90;
                } else if (loc.length < 5){
                    var popupWidth = 180;
                } else {
                    var popupWidth = 270;
                }

                html.push('<div style="overflow: hidden; width:');
                html.push(popupWidth);
                html.push('px;">');

                for (var i = 0; i < loc.length; i++)
                {
                    var row = loc[i];

                    var image_url;
                    if (row.small_thumbnail) {
                        image_url = '/media/' + row.small_thumbnail;
                    } else {
                        image_url = '/static/img/portrait_80.png';
                    }

                    var person = {
                        id : row.id,
                        name : row.name,
                        image_url : image_url
                    }

                    var output = Mustache.render(template, person);
                    html.push(output);
                }

                html.push('</div>');

                marker.bindPopup(html.join(''));
            }

            $('.loading').hide();
        }
    );
}

