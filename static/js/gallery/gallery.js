var OKKINDRED_GALLERY = {
    gallery_page : 0,
    gallery_loading : false,
    photoswipe_items : []
};

//Request the galleries on page load
$( document ).ready(function() {
    //Initiate  masonry
    var $container = $('#image_container');

    if ($container.length == 0) {
        return;
    }

    $container.masonry({
        itemSelector: '.image_in_gallery',
        columnWidth: 1,
        isFitWidth: true
    });

    //Display the default image if there is one
    if ($('#default_image').length > 0) {
        $('#default_image').trigger('click');
    }

    $(document).on("click",".image_in_gallery",function(e){
        var photoswipe_index = $(this).data('photoswipe_index');
        show_photoswipe_window(photoswipe_index);
    });

    gallery_load_more();
});


//Request more galleries when we scroll to the bottom
$(window).scroll(function()
{
    if ($('#image_container').length == 0) {
        return;
    }

    if($(window).scrollTop() > $(document).height() - $(window).height() - 100)
    {
        gallery_load_more();
    }
});

function show_photoswipe_window(index) {

    var template = $('#galley_image_caption_template').html();

    // define options (if needed)
    var options = {
        // optionName: 'option value'
        // for example:
        index: index,
    	addCaptionHTMLFn: function(item, captionEl, isFake) {
    		captionEl.children[0].innerHTML =  Mustache.render(template, item);
    		return true;
        },
    };

    // Initializes and opens PhotoSwipe
    var pswpElement = document.querySelectorAll('.pswp')[0];
    var gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, OKKINDRED_GALLERY.photoswipe_items, options);
    gallery.init();
};

//Ajax request to get more galleries
function gallery_load_more()
{
    if (OKKINDRED_GALLERY.gallery_loading == true) { return; }

    OKKINDRED_GALLERY.gallery_loading = true;

    OKKINDRED_GALLERY.gallery_page = OKKINDRED_GALLERY.gallery_page + 1;

    var gallery_url = $('#image_container').data('gallery_url');

    $('div#loadmoreajaxloader').show();
    $.ajax({
        url: gallery_url + OKKINDRED_GALLERY.gallery_page.toString(),
        success: function(data) {
            if(data && data.length > 0) {

                var isMobile = jQuery.browser.mobile;
                var scale = 1;
                if (isMobile) {
                    scale = 2;
                }

                var template = $('#galley_image_template').html();

                var html =[];
                var show_map = false;
                for (var i in data) {
                    var data_row = data[i];

                    var image_data = {
                      photoswipe_index : i,
                      id :   data_row.pk,
                      title : data_row.fields.title,
                      thumbnail : data_row.fields.thumbnail,
                      large_thumbnail : data_row.fields.large_thumbnail,
                      width : Math.floor(data_row.fields.thumbnail_width / scale),
                      height : Math.floor(data_row.fields.thumbnail_height / scale)
                    };

                    var photoswipe_item = {
                        src :  '/media/' + image_data.large_thumbnail,
                        w : data_row.fields.large_thumbnail_width,
                        h : data_row.fields.large_thumbnail_height,
                        identifier :   data_row.pk,
                        title : data_row.fields.title
                    };

                    OKKINDRED_GALLERY.photoswipe_items.push(photoswipe_item);

                    var output = Mustache.render(template, image_data);
                    html.push(output);

                    if (data_row.fields.latitude != 0) {
                        show_map = true;;
                    }

                }

                if (show_map == true) {
                    $('#map_button').show();
                }
                $('div#loadmoreajaxloader').hide();

                var $data = $(html.join(''));
                var $container = $('#image_container');
                $container.append($data);
                $container.masonry( 'appended', $data.filter(".image_in_gallery"), true );

                OKKINDRED_GALLERY.gallery_loading = false;

                //Keep loading images until we see a scroll bar
                if ($container.height() < $(window).height()) {
                    gallery_load_more()
                }
            }
            else {
                $('#NoMoreImages').show();
                $('div#loadmoreajaxloader').hide();
            }
        },

        error: function(jqXHR, textStatus, errorThrown ) {
            $('#ErrorLoadingImages').show();
            $('div#loadmoreajaxloader').hide();
            OKKINDRED_GALLERY.gallery_loading = false;
        }
    });
}