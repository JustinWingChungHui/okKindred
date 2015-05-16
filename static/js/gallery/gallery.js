
var gallery_page = 0;
var gallery_loading = false;

//Request the galleries on page load
$( document ).ready(function() {
    //Initiate  masonry
    var $container = $('#image_container');

    if ($container.length == 0) {
        return;
    }

    $container.imagesLoaded(function(){
        $container.masonry({
            itemSelector: '.image_in_gallery',
            columnWidth: 1,
            isFitWidth: true
        });
    });

    //Display the default image if there is one
    if ($('#default_image').length > 0) {
        $('#default_image').trigger('click');
    }

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
    if (gallery_loading == true) { return; }

    gallery_loading = true;

    gallery_page = gallery_page + 1;

    var gallery_url = $('#image_container').data('gallery_url');

    $('div#loadmoreajaxloader').show();
    $.ajax({
        url: gallery_url + gallery_page.toString(),
        success: function(data) {
            if(data && data.length > 0) {

                var details_translation = $("#translate").data("details");

                var html =[];

                for (var i in data) {
                    html.push('<a class="image_in_gallery" href="/media/');
                    html.push(data[i].fields.large_thumbnail);
                    html.push('" data-lightbox="gallery"');
                    html.push(' data-title="');
                    html.push('&lt;a href=\'/image=');
                    html.push(data[i].pk);
                    html.push('/details/\' class=\'btn btn-info\' &gt; ');
                    html.push(details_translation);
                    html.push(' &lt;/a&gt ');
                    html.push(data[i].fields.title);
                    html.push('">');

                    html.push('<img class="masonry_thumbnail" src="/media/' + data[i].fields.thumbnail + '" ');
                    html.push('alt="' + data[i].fields.title +'/"')
                    html.push('/>');

                    html.push('</a>');

                    if (data[i].fields.latitude != 0) {
                        $('#map_button').show();
                    }

                }

                 $('div#loadmoreajaxloader').hide();

                var $data = $(html.join(''));
                var $container = $('#image_container');
                $container.append($data).imagesLoaded(function(){
                    $container.masonry( 'appended', $data.filter(".image_in_gallery"), true );

                    gallery_loading = false;

                    //Keep loading images until we see a scroll bar
                    if ($container.height() < $(window).height()) {
                        gallery_load_more()
                    }
                });
            }
            else {
                $('#NoMoreImages').show();
                $('div#loadmoreajaxloader').hide();
            }
        },

        error: function(jqXHR, textStatus, errorThrown ) {
            $('#ErrorLoadingImages').show();
            $('div#loadmoreajaxloader').hide();
            gallery_loading = false;
        }
    });
}