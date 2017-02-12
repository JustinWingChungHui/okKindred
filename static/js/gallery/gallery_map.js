require(["jquery", "mustache", "leaflet","photoswipe", "photoswipe_ui"],
    function ($, Mustache, L, PhotoSwipe, PhotoSwipeUI_Default) {

    var OKKINDRED_GALLERY_MAP = {
        image_markers : [],
        photoswipe_items : [],
        set_gallery_map : function() {
            $('.loading').show();

            var latitude = parseFloat($('#gallery_map').data('latitude'));
            var longitude = parseFloat($('#gallery_map').data('longitude'));
            var zoom = parseFloat($('#gallery_map').data('zoom'));

            var map = L.map('gallery_map', {
                center: [latitude, longitude],
                zoom: 5,
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

            OKKINDRED_GALLERY_MAP.get_gallery_map_data(map, true);

            map.on('zoomend', function(e) {
                OKKINDRED_GALLERY_MAP.get_gallery_map_data(e.target, false);
            });
        },

        get_gallery_map_data : function(map, loading) {
            var bounds = map.getBounds()
            var min = bounds.getSouthWest().wrap();
            var max = bounds.getNorthEast().wrap();

            var max_num_points = Math.floor(Math.min($(document).height(),$(document).width()) / 100.0); //100 pixels per spot
            var min_lat_lng = Math.min(max.lng - min.lng, max.lat - min.lat);
            var division_size = min_lat_lng / max_num_points;

            var gallery_id = parseFloat($('#gallery_map').data('gallery_id'));

            var url = ['/gallery='];
            url.push(gallery_id);
            url.push('/map_data/');
            url.push(division_size);
            url.push('/');

            var request = $.ajax({
                context: this,
                type: "GET",
                url : url.join(''),

            }).done(function(data, textStatus, jqXHR){
                OKKINDRED_GALLERY_MAP.show_map_items(data, map, loading)
            });

        },

        show_map_items(data, map, loading) {
            var details_translation = $('#translate').data('details')
            var photoswipe_index = 0;

            for(i = 0; i < this.image_markers.length; i++) {
                map.removeLayer(this.image_markers[i]);
            }

            this.image_markers.length = 0;
            this.photoswipe_items.length = 0;

            var template = $('#map_image_template').html();

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
                this.image_markers.push(marker);

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

                for (var i = 0; i < loc.length; i++) {
                    var image = loc[i];
                    image.photoswipe_index = photoswipe_index;

                    var output = Mustache.render(template, image);
                    html.push(output);

                    var photoswipe_item = {
                        src : image.large_thumbnail,
                        w : image.large_thumbnail_width,
                        h : image.large_thumbnail_height,
                        identifier : image.id,
                        title : image.title
                    };

                    this.photoswipe_items.push(photoswipe_item);
                    photoswipe_index++;
                }

                html.push('</div>');

                marker.bindPopup(html.join(''));
            }

            if (loading) {
                map.panTo(this.image_markers[0]._latlng, true);
            }

            $('.loading').hide();
        },

        show_photoswipe_window : function (index) {

            var template = $('#galley_image_caption_template').html();

            var options = {
                index: index,
            	addCaptionHTMLFn: function(item, captionEl, isFake) {
            		captionEl.children[0].innerHTML =  Mustache.render(template, item);
            		return true;
                },
            };

            // Clears previous images
            $('.pswp__item').empty();
            window.location.hash = '';

            // Initializes and opens PhotoSwipe
            var pswpElement = $('.pswp')[0];

            this.photoswipe = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, OKKINDRED_GALLERY_MAP.photoswipe_items, options);
            this.photoswipe.init();
        },
    };

    $(document).ready(function() {

        if ($('#gallery_map').length == 0) {
            return;
        }

        OKKINDRED_GALLERY_MAP.set_gallery_map();

        $(document).on("click",".image_in_gallery",function(e){
            var photoswipe_index = $(this).data('photoswipe_index');
            OKKINDRED_GALLERY_MAP.show_photoswipe_window(photoswipe_index);
        });
    });

});