
// require the require function
require(["require", "jquery", "masonry","photoswipe", "photoswipe_ui", "mustache", "mobile"],
    function (require, $, Masonry, PhotoSwipe, PhotoSwipeUI_Default, Mustache) {

// require jquery-bridget, it's included in masonry.pkgd.js
require(["jquery-bridget/jquery-bridget"],
function() {

    $.bridget('masonry', Masonry);

    var OKKINDRED_GALLERY = {
        gallery_page : 0,
        gallery_loading : false,
        photoswipe_items : [],
        default_image_id : 0,
        default_image_index: 0,
        photoswipe: null,
        missing_default_image : function() {

            if (this.default_image_id !== 0) {
                for (var i in this.photoswipe_items) {
                    var item = this.photoswipe_items[i];

                    if (item.identifier === this.default_image_id) {
                        this.default_image_index = i;
                        return false;
                    }
                }

                return true;
            }
            return false;
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

            this.photoswipe = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, OKKINDRED_GALLERY.photoswipe_items, options);
            this.photoswipe.init();
        },
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

        var $default_image = $('#default_image');
        if ($default_image.length !== 0) {
            OKKINDRED_GALLERY.default_image_id = $default_image.data('image_id');
        }

        $(document).on("click",".image_in_gallery",function(e){
            var photoswipe_index = $(this).data('photoswipe_index');
            OKKINDRED_GALLERY.show_photoswipe_window(photoswipe_index);
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
                          photoswipe_index : OKKINDRED_GALLERY.photoswipe_items.length,
                          id :   data_row.pk,
                          title : data_row.fields.title,
                          thumbnail : data_row.fields.thumbnail,
                          large_thumbnail : data_row.fields.large_thumbnail,
                          width : Math.floor(data_row.fields.thumbnail_width / scale),
                          height : Math.floor(data_row.fields.thumbnail_height / scale)
                        };

                        var photoswipe_item = {
                            src :  image_data.large_thumbnail,
                            w : data_row.fields.large_thumbnail_width,
                            h : data_row.fields.large_thumbnail_height,
                            identifier :   data_row.pk,
                            title : data_row.fields.title
                        };

                        OKKINDRED_GALLERY.photoswipe_items.push(photoswipe_item);

                        var output = Mustache.render(template, image_data);
                        html.push(output);

                        if (data_row.fields.latitude != 0) {
                            show_map = true;
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
                    if ($('#image_container').height() < $(window).height()
                        || (OKKINDRED_GALLERY.missing_default_image() === true)) {
                        gallery_load_more()

                        if (OKKINDRED_GALLERY.missing_default_image() === false
                            && OKKINDRED_GALLERY.default_image_id !== 0
                            && OKKINDRED_GALLERY.photoswipe == null) {
                             OKKINDRED_GALLERY.show_photoswipe_window(OKKINDRED_GALLERY.default_image_index);
                        }
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
});
});