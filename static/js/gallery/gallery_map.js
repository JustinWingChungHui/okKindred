require(["jquery", "mustache", "leaflet","photoswipe", "photoswipe_ui", "leaflet_markercluster"],
    function ($, Mustache, L, PhotoSwipe, PhotoSwipeUI_Default) {

    photoswipe_items = [];

    $(document).ready(function() {

        if ($('#gallery_map').length == 0) {
            return;
        }

        create_gallery_map();

        // When an image is clicked, show photoswipe gallery
        $(document).on("click",".image_in_gallery",function(e){
            var photoswipe_index = $(this).data('photoswipe_index');
            show_photoswipe_window(photoswipe_index);
        });
    });


    // Creates the gallery map.  Run Once page is loaded
    function create_gallery_map() {

        if($("#gallery_map").length == 0) {
            return;
        }

        $('.loading').show();

        var latitude = parseFloat($('#gallery_map').data('latitude'));
        var longitude = parseFloat($('#gallery_map').data('longitude'));
        var zoom = parseFloat($('#gallery_map').data('zoom'));
        var token = $("#gallery_map").data("token");

        var tiles = L.tileLayer('https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.jpg70?access_token={token}', {
    		token: token
    	})

        var map = L.map('gallery_map', {
            center: [latitude, longitude],
            zoom: 5,
            zoomControl: false,
            minZoom: 2,
            scrollWheelZoom: true,
            detectRetina: true,
            maxBounds: [[-90, -200],[90, 200]],
            layers: [tiles]
        });

        map.addControl( L.control.zoom({position: 'bottomleft'}));

        get_gallery_map_data(map, true);
    }


    // Ajax request to get gallery data
    function get_gallery_map_data(map, loading) {

        var gallery_id = parseFloat($('#gallery_map').data('gallery_id'));

        var url = ['/gallery='];
        url.push(gallery_id);
        url.push('/map_data/');

        var request = $.ajax({
            dataType: "json",
            context: this,
            type: "get",
            url : url.join('')
        }).done(function(data, textStatus, jqXHR){
            show_map_items(data, map, loading)
        });
    }

    // Draws the map items
    function show_map_items(data, map, loading) {
        var details_translation = $('#translate').data('details')
        var image_markers = L.markerClusterGroup();

        photoswipe_items.length = 0;

        var template = $('#map_image_template').html();

        for (var i = 0; i < data.length; i++) {
            var loc = data[i];

            var html = build_pop_up(loc, template);

			var marker = L.marker(new L.LatLng(loc.fields.latitude, loc.fields.longitude), { title: loc.fields.title });
			marker.bindPopup(html);
			image_markers.addLayer(marker);
        }

        map.addLayer(image_markers);

        // Centre map on first image
        if (loading) {
            map.panTo(image_markers.getLayers()[0]._latlng, true);
        }

        $('.loading').hide();
    }

    // Builds the html for a map pop up
    function build_pop_up(loc, template) {
        var html = [];

        html.push('<div style="overflow: hidden; width:90px;">');

        var image = loc.fields;
        image.photoswipe_index = photoswipe_items.length;

        var output = Mustache.render(template, image);
        html.push(output);

        var photoswipe_item = {
            src : image.large_thumbnail,
            w : image.large_thumbnail_width,
            h : image.large_thumbnail_height,
            identifier : image.id,
            title : image.title
        };

        photoswipe_items.push(photoswipe_item);

        html.push('</div>');

        return html.join('');
    }

    // Shows the photo swipe window when an image is clicked
    function  show_photoswipe_window(index) {

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

        this.photoswipe = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, photoswipe_items, options);
        this.photoswipe.init();
    }
});