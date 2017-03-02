require(['jquery', 'leaflet', 'mustache', 'leaflet_markercluster'], function($, L, Mustache){

    $(document).ready(function() {

        if($("#person_map").length == 0) {
            return;
        }

        $('.loading').show();
        var center_latitude = parseFloat($("#person_map").data("latitude"));
        var center_longitude = parseFloat($("#person_map").data("longitude"));
        var zoom = parseFloat($("#person_map").data("zoom"));
        var token = $("#person_map").data("token");

        var tiles = L.tileLayer('https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.jpg70?access_token={token}', {
    		token: token
    	});

        var map = L.map('person_map', {
            center: [center_latitude, center_longitude],
            zoom: zoom,
            zoomControl: false,
            minZoom: 2,
            scrollWheelZoom: true,
            detectRetina: true,
            maxBounds: [[-90, -200],[90, 200]],
            layers: [tiles]
        });

        map.addControl( L.control.zoom({position: 'bottomleft'}));

        get_map_data(map);
    });

    // Gets the map data using ajax
    function get_map_data(map) {

        $.ajax({
            url : '/map_points/',
            dataType: "json",
            type: "get"
        }).done(function(data, textStatus, jqXHR) {
            display_map_points(data, map)
        });
    }

    // Displays the map points from the result of the ajax query
    function display_map_points(data, map) {

        var template = $('#map_person_template').html();
        var markers = L.markerClusterGroup();

		for (var i = 0; i < data.length; i++) {
			var loc = data[i];
			var html = build_pop_up(loc, template);

			var marker = L.marker(new L.LatLng(loc.fields.latitude, loc.fields.longitude), { title: html });
			marker.bindPopup(html);
			markers.addLayer(marker);
		}

		map.addLayer(markers);

        $('.loading').hide();
    }

    // Builds the html for a map pop up
    function build_pop_up(loc, template) {
        var html = [];

        html.push('<div style="overflow: hidden; width:90px;">');

        var image_url;
        if (loc.fields.small_thumbnail) {
            image_url = loc.fields.small_thumbnail;
        } else {
            image_url = '/static/img/portrait_80.png';
        }

        var person = {
            id : loc.pk,
            name : loc.fields.name,
            image_url : image_url
        }

        var output = Mustache.render(template, person);
        html.push(output);

        html.push('</div>');

        return html.join('');
    }

});


